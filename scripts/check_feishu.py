#!/usr/bin/env python3
"""检查飞书群消息 → 提取用户输入 → 写入 .bridge/feishu_inbox.md"""

import os, json, urllib.request, sys

APP_ID = os.environ.get("FEISHU_APP_ID", "cli_aaae95d4a2f8dcf5")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "4oWaPNCsfSF9cbadJNzexgdxIuEUeLSE")
CHAT_ID = "oc_f1a6804e3b539ea30888fb067e82ac42"
OUTPUT = os.path.expanduser("~/.bridge/feishu_inbox.md")
PROCESSED_LOG = "/tmp/feishu_processed_ids.json"


def get_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req).read())["tenant_access_token"]


def get_messages(token):
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?container_id_type=chat&container_id={CHAT_ID}&page_size=10&sort_type=ByCreateTimeDesc"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        resp = json.loads(urllib.request.urlopen(req).read())
        if resp.get("code") == 99992402:
            return None
        return resp.get("data", {}).get("items", [])
    except:
        return []


def load_processed():
    if os.path.exists(PROCESSED_LOG):
        with open(PROCESSED_LOG) as f:
            return set(json.load(f))
    return set()


def save_processed(ids):
    with open(PROCESSED_LOG, "w") as f:
        json.dump(list(ids), f)


def main():
    token = get_token()
    messages = get_messages(token)

    if messages is None:
        print("⚠ 飞书应用缺少消息读取权限，请在开放平台开通 im:message 权限并发布")
        return

    processed = load_processed()
    new_entries = []

    for msg in messages:
        msg_id = msg.get("message_id", "")
        if msg_id in processed:
            continue
        sender = msg.get("sender", {}).get("id", "")
        if sender == APP_ID:
            processed.add(msg_id)
            continue
        body = msg.get("body", {}).get("content", "{}")
        try:
            content = json.loads(body).get("text", "")
        except:
            content = body
        if content.strip():
            new_entries.append({"id": msg_id, "content": content.strip(), "time": msg.get("create_time", "")})
        processed.add(msg_id)

    if new_entries:
        os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
        with open(OUTPUT, "a", encoding="utf-8") as f:
            for e in reversed(new_entries):
                f.write(f"\n## [{e['time']}] 飞书消息\n**内容**: {e['content']}\n\n")
        save_processed(processed)
        print(f"✅ 发现 {len(new_entries)} 条新飞书消息")
        for e in new_entries:
            print(f"  📩 {e['content'][:60]}")
    else:
        print("📭 无新飞书消息")


if __name__ == "__main__":
    main()
