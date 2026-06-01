#!/usr/bin/env python3
"""检查QQ邮箱回复 → 写入 .bridge/inbox.md → Claude下次读取。

用法:
  python3 scripts/check_inbox.py           # 检查过去24小时的回复
  python3 scripts/check_inbox.py --hours 2 # 检查过去2小时的回复

配置: 同 email_push.py (QQ_EMAIL + QQ_EMAIL_AUTH)
"""

import sys
sys.path.insert(0, __file__.rsplit("/", 2)[0])  # 添加project root
from lib.email_push import check_replies, save_replies_to_inbox


def main():
    hours = 24
    if "--hours" in sys.argv:
        idx = sys.argv.index("--hours")
        if idx + 1 < len(sys.argv):
            hours = int(sys.argv[idx + 1])

    replies = check_replies(hours_back=hours)
    save_replies_to_inbox(replies)

    if replies:
        print(f"✅ 发现 {len(replies)} 条回复，已写入 .bridge/inbox.md")
        for r in replies:
            print(f"  📩 {r['date']} | {r['subject']}")
    else:
        print("📭 无新回复")


if __name__ == "__main__":
    main()
