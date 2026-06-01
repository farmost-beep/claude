#!/usr/bin/env python3
"""检查飞书Bot回复 → 写入 .bridge/feishu_inbox.md → Claude下次读取。

用法:
  python3 scripts/check_feishu.py           # 检查过去24小时的消息
  python3 scripts/check_feishu.py --hours 2 # 检查过去2小时
"""

import sys
sys.path.insert(0, __file__.rsplit("/", 2)[0])
from lib.feishu_bot import check_replies, save_replies_to_inbox


def main():
    hours = 24
    if "--hours" in sys.argv:
        idx = sys.argv.index("--hours")
        if idx + 1 < len(sys.argv):
            hours = int(sys.argv[idx + 1])

    replies = check_replies(hours_back=hours)
    save_replies_to_inbox(replies)

    if replies:
        print(f"✅ 发现 {len(replies)} 条新飞书消息，已写入 .bridge/feishu_inbox.md")
    else:
        print("📭 无新消息")


if __name__ == "__main__":
    main()
