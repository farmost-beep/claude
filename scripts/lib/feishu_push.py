#!/usr/bin/env python3
"""飞书消息推送 — 通过飞书开放API发送通知到群。

配置环境变量（已保存在 ~/.zshrc）：
  export FEISHU_APP_ID="cli_aaae95d4a2f8dcf5"
  export FEISHU_APP_SECRET="4oWaPNCsfSF9cbadJNzexgdxIuEUeLSE"

用法:
  python3 -c "from lib.feishu_push import push; push('标题', '内容')"
  python3 scripts/lib/feishu_push.py "标题" "内容"
"""

import os, json, urllib.request

CHAT_ID = "oc_f1a6804e3b539ea30888fb067e82ac42"


def push(title: str, content: str) -> tuple[bool, str]:
    app_id = os.environ.get("FEISHU_APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET")

    if not app_id or not app_secret:
        return False, "飞书未配置（设置 FEISHU_APP_ID + FEISHU_APP_SECRET）"

    try:
        # 1. 获取 token
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        token = json.loads(urllib.request.urlopen(req).read())["tenant_access_token"]

        # 2. 发送消息到群
        full_text = f"{title}\n\n{content}"
        url2 = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
        data2 = json.dumps({
            "receive_id": CHAT_ID,
            "msg_type": "text",
            "content": json.dumps({"text": full_text})
        }).encode()
        req2 = urllib.request.Request(url2, data=data2, headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })
        resp = json.loads(urllib.request.urlopen(req2).read())
        if resp.get("code") == 0:
            return True, "✅ 飞书推送成功"
        return False, f"推送失败: {resp.get('msg','')}"
    except Exception as e:
        return False, f"飞书推送异常: {e}"


if __name__ == "__main__":
    import sys
    title = sys.argv[1] if len(sys.argv) > 1 else "测试通知"
    content = sys.argv[2] if len(sys.argv) > 2 else "Hello from Claude Code"
    ok, msg = push(title, content)
    print(msg)
