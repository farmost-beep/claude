#!/usr/bin/env python3
"""微信推送 — 通过 wechat-claude-code 桥接API发送消息到微信。

替代旧版多渠道推送（WxPusher/PushPlus/Server酱等），解决超时问题。

使用方式：
  python3 scripts/wechat_push.py "标题" "内容"

配置：
  自动读取 ~/.wechat-claude-code/accounts/ 下的微信桥接账号
  需先安装 wechat-claude-code skill 并扫码绑定微信

回退：
  如果桥接不可用，自动尝试旧推送渠道（环境变量配置的 WxPusher/PushPlus/Server酱）
"""

import json
import os
import sys
import time
import urllib.request
import uuid
from pathlib import Path

# 账号配置路径
ACCOUNTS_DIR = Path.home() / ".wechat-claude-code" / "accounts"


def load_account():
    """读取微信桥接账号配置"""
    if not ACCOUNTS_DIR.exists():
        return None
    json_files = list(ACCOUNTS_DIR.glob("*.json"))
    if not json_files:
        return None
    with open(json_files[0]) as f:
        return json.load(f)


def push_via_bridge(title: str, content: str, to_wxid: str = ""):
    """通过 wechat-claude-code 桥接API发送消息

    Args:
        title: 消息标题
        content: 消息内容
        to_wxid: 目标微信用户ID。为空则发给自己（通知模式）
    """
    account = load_account()
    if not account:
        return False, "未找到微信桥接账号"

    bot_token = account.get("botToken", "")
    account_id = account.get("accountId", "")
    user_id = to_wxid or account.get("userId", "")
    base_url = account.get("baseUrl", "https://ilinkai.weixin.qq.com")

    if not bot_token or not account_id or not user_id:
        return False, "微信账号配置不完整"

    # 合并标题和内容
    full_text = f"{title}\n\n{content}"
    client_id = f"wcc-push-{int(time.time() * 1000)}-{uuid.uuid4().hex[:6]}"

    payload = {
        "msg": {
            "from_user_id": account_id,
            "to_user_id": user_id,
            "client_id": client_id,
            "message_type": 2,   # BOT
            "message_state": 2,  # FINISH
            "context_token": "",
            "item_list": [
                {
                    "type": 1,  # TEXT
                    "text_item": {"text": full_text},
                }
            ],
        }
    }

    url = f"{base_url}/ilink/bot/sendmessage"

    # 退避重试（应对 ret:-2 限流）
    max_retries = 3
    delay = 2
    uin = os.urandom(4).hex()

    for attempt in range(max_retries + 1):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {bot_token}")
        req.add_header("AuthorizationType", "ilink_bot_token")
        req.add_header("X-WECHAT-UIN", uin)

        try:
            resp = urllib.request.urlopen(req, timeout=10)
            result = json.loads(resp.read().decode())
            ret = result.get("ret")
            if ret is None or ret == 0 or result.get("errcode") == 0:
                return True, "微信桥接推送成功"
            if ret == -2:
                if attempt < max_retries:
                    time.sleep(delay)
                    delay = min(delay * 2, 12)
                    continue
                return False, "桥接API限流已达最大重试次数"
            return False, f"桥接API返回: {result}"
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:200]
            return False, f"桥接HTTP {e.code}: {body}"
        except urllib.error.URLError as e:
            return False, f"桥接网络错误: {e.reason}"
        except Exception as e:
            return False, f"桥接异常: {e}"

    return False, "桥接发送失败（未知错误）"


def push_fallback(title: str, content: str):
    """回退到旧推送渠道（环境变量配置）"""
    wxpusher_token = os.environ.get("WECHAT_WXPUSHER_TOKEN")
    wxpusher_uid = os.environ.get("WECHAT_WXPUSHER_UID")
    pushplus_token = os.environ.get("WECHAT_PUSH_TOKEN")
    sendkey = os.environ.get("WECHAT_SENDKEY")
    webhook = os.environ.get("WECHAT_WEBHOOK")

    if wxpusher_token and wxpusher_uid:
        return _push_wxpusher(wxpusher_token, wxpusher_uid, title, content)
    elif webhook:
        return _push_wecom_webhook(webhook, title, content)
    elif pushplus_token:
        return _push_pushplus(pushplus_token, title, content)
    elif sendkey:
        return _push_serverchan(sendkey, title, content)
    return False, "无可用推送渠道"


def _push_wxpusher(token: str, uid: str, title: str, content: str):
    url = "http://wxpusher.zjiecode.com/api/send/message"
    data = json.dumps({"appToken": token, "content": f"# {title}\n\n{content}", "contentType": 3, "uids": [uid]}).encode()
    try:
        resp = json.loads(urllib.request.urlopen(urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}), timeout=10).read())
        return (True, "WxPusher推送成功") if resp.get("code") == 1000 else (False, f"WxPusher失败: {resp}")
    except Exception as e:
        return False, f"WxPusher异常: {e}"


def _push_wecom_webhook(webhook: str, title: str, content: str):
    data = json.dumps({"msgtype": "markdown", "markdown": {"content": f"## {title}\n\n{content[:3500]}"}}).encode()
    try:
        resp = json.loads(urllib.request.urlopen(urllib.request.Request(webhook, data=data, headers={"Content-Type": "application/json"}), timeout=10).read())
        return (True, "企业微信推送成功") if resp.get("errcode") == 0 else (False, f"企业微信失败: {resp}")
    except Exception as e:
        return False, f"企业微信异常: {e}"


def _push_pushplus(token: str, title: str, content: str):
    data = json.dumps({"token": token, "title": title, "content": content}).encode()
    try:
        resp = json.loads(urllib.request.urlopen(urllib.request.Request("http://www.pushplus.plus/send", data=data, headers={"Content-Type": "application/json"}), timeout=10).read())
        return (True, "PushPlus推送成功") if resp.get("code") == 200 else (False, f"PushPlus失败: {resp}")
    except Exception as e:
        return False, f"PushPlus异常: {e}"


def _push_serverchan(sendkey: str, title: str, content: str):
    import urllib.parse
    data = urllib.parse.urlencode({"title": title, "desp": content[:50000]}).encode()
    try:
        resp = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://sctapi.ftqq.com/{sendkey}.send", data=data), timeout=10).read())
        return (True, "Server酱推送成功") if resp.get("code") == 0 else (False, f"Server酱失败: {resp}")
    except Exception as e:
        return False, f"Server酱异常: {e}"


def main():
    if len(sys.argv) < 2:
        print("用法: python3 scripts/wechat_push.py [--to-wxid USER_ID] 标题 [内容]", file=sys.stderr)
        sys.exit(1)

    # 解析 --to-wxid 参数
    to_wxid = ""
    args = sys.argv[1:]
    title_idx = 0
    if len(args) >= 2 and args[0] == "--to-wxid":
        to_wxid = args[1]
        title_idx = 2

    if title_idx >= len(args):
        print("错误：缺少标题参数", file=sys.stderr)
        sys.exit(1)

    title = args[title_idx]
    content = args[title_idx + 1] if len(args) > title_idx + 1 else ""

    if not content.strip():
        print("错误：内容不能为空", file=sys.stderr)
        sys.exit(1)

    # 优先使用微信桥接
    ok, msg = push_via_bridge(title, content, to_wxid=to_wxid)
    if ok:
        print(msg)
        return

    print(f"桥接推送失败: {msg}", file=sys.stderr)
    print("尝试回退渠道...", file=sys.stderr)

    ok, msg = push_fallback(title, content)
    if ok:
        print(msg)
    else:
        print(f"所有推送渠道均失败: {msg}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
