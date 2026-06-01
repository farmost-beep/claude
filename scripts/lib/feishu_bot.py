#!/usr/bin/env python3
"""飞书Bot双通道——推送消息 + 轮询回传。

配置（环境变量）：
  export FEISHU_APP_ID="cli_xxxxxxxxxxxx"
  export FEISHU_APP_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

飞书应用创建（5分钟）：
  1. 访问 https://open.feishu.cn/app  → 创建企业自建应用
  2. 应用功能 → 机器人 → 开启
  3. 权限管理 → 添加：
     - im:message:send_as_bot（发送消息）
     - im:message:read（读取消息）
     - im:resource（获取消息中的资源）
  4. 版本管理与发布 → 创建版本 → 提交审核（个人用可申请线上发布）
  5. 获得 App ID (cli_开头) + App Secret
"""

import os
import json
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timedelta

# 常量
BASE_URL = "https://open.feishu.cn/open-apis"
CACHE_DIR = Path(__file__).resolve().parent.parent.parent / ".bridge" / "feishu_cache"
INBOX_FILE = Path(__file__).resolve().parent.parent.parent / ".bridge" / "feishu_inbox.md"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def get_config():
    app_id = os.environ.get("FEISHU_APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET")
    return (app_id, app_secret) if app_id and app_secret else (None, None)


def _get_tenant_token() -> str:
    """获取 tenant_access_token（缓存到文件，2小时有效）"""
    token_file = CACHE_DIR / "tenant_token.json"
    if token_file.exists():
        cached = json.loads(token_file.read_text())
        if cached.get("expire", 0) > time.time():
            return cached["token"]

    app_id, app_secret = get_config()
    if not app_id:
        return ""

    url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req, timeout=10)
    result = json.loads(resp.read())
    token = result.get("tenant_access_token", "")
    expire_at = time.time() + result.get("expire", 7200) - 300  # 提前5分钟刷新
    token_file.write_text(json.dumps({"token": token, "expire": expire_at}))
    return token


def _api_call(method: str, path: str, data: dict = None) -> dict:
    """调用飞书API"""
    token = _get_tenant_token()
    if not token:
        return {"error": "未配置FEISHU_APP_ID/FEISHU_APP_SECRET"}

    url = f"{BASE_URL}{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode()}"}
    except Exception as e:
        return {"error": str(e)}


def send_message(title: str, content: str) -> tuple[bool, str]:
    """向Bot的对话发送消息。首次需获取chat_id。"""
    # 先获取对话列表找到与Bot的对话
    chat_result = _api_call("GET", "/im/v1/chats?page_size=10")
    if "error" in chat_result:
        return False, chat_result["error"]

    # 找用户的chat（个人与Bot的对话）
    chat_id = None
    for chat in chat_result.get("data", {}).get("items", []):
        if chat.get("chat_type") == "p2p":  # 一对一
            chat_id = chat.get("chat_id")
            break

    if not chat_id:
        return False, "未找到与Bot的对话，请先在飞书搜索Bot名称并发送一条消息"

    # 拼接标题和内容
    full_content = f"**{title}**\n\n{content}"
    msg_data = {
        "receive_id": chat_id,
        "msg_type": "markdown",
        "content": json.dumps({"text": full_content}),
    }
    result = _api_call("POST", "/im/v1/messages?receive_id_type=chat_id", msg_data)
    if "error" in result:
        return False, f"发送失败: {result.get('error', result)}"
    return True, "消息已发送到飞书"


def check_replies(hours_back: int = 24) -> list[dict]:
    """检查Bot收到的消息，提取回传内容"""
    # 先找chat_id
    chat_result = _api_call("GET", "/im/v1/chats?page_size=10")
    if "error" in chat_result:
        return []

    chat_id = None
    for chat in chat_result.get("data", {}).get("items", []):
        if chat.get("chat_type") == "p2p":
            chat_id = chat.get("chat_id")
            break

    if not chat_id:
        return []

    # 获取最近消息
    since = (datetime.now() - timedelta(hours=hours_back)).strftime("%s")
    msg_result = _api_call("GET", f"/im/v1/messages?container_id_type=chat&container_id={chat_id}&page_size=20&sort_type=ByCreateTimeDesc&start_time={since}000")
    if "error" in msg_result:
        return []

    replies = []
    reader = _get_tenant_token()  # 重新获取一次作为读取凭证

    for msg in msg_result.get("data", {}).get("items", []):
        msg_type = msg.get("msg_type", "")
        if msg_type != "text":
            continue
        try:
            body = json.loads(msg.get("body", {}).get("content", "{}"))
            text = body.get("text", "")
            replies.append({
                "from": "用户",
                "body": text,
                "date": msg.get("create_time", ""),
                "msg_id": msg.get("message_id", ""),
            })
        except (json.JSONDecodeError, KeyError):
            continue

    return replies


def save_replies_to_inbox(replies: list[dict]):
    """将回复写入 .bridge/feishu_inbox.md"""
    if not replies:
        return

    INBOX_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing = ""
    if INBOX_FILE.exists():
        existing = INBOX_FILE.read_text(encoding="utf-8")

    new_entries = []
    for r in replies:
        key = f"{r['msg_id']}"
        if key not in existing:
            new_entries.append(f"## [{r['date']}] 来自飞书\n\n{r['body']}\n\n---\n")

    if new_entries:
        with open(INBOX_FILE, "w", encoding="utf-8") as f:
            f.write("# 📥 飞书回传箱\n\n> Claude定期检查此文件。你在飞书回复的内容会自动出现在这里。\n\n---\n\n")
            f.write("".join(new_entries))
            f.write(existing)
        print(f"📬 {len(new_entries)} 条新飞书消息已写入 {INBOX_FILE}")
    else:
        print("📭 无新消息")


def main():
    import sys
    if len(sys.argv) < 2:
        print("用法: python3 feishu_bot.py [push|check] [内容]")
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "push":
        title = sys.argv[2] if len(sys.argv) > 2 else "来自Claude"
        content = sys.argv[3] if len(sys.argv) > 3 else ""
        ok, msg = send_message(title, content)
        print(f"{'✅' if ok else '❌'} {msg}")
    elif mode == "check":
        replies = check_replies()
        save_replies_to_inbox(replies)
        for r in replies:
            print(f"  📩 {r['date'][:19]}  {r['body'][:80]}...")
        if not replies:
            print("  📭 无新消息")


if __name__ == "__main__":
    main()
