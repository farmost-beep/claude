#!/usr/bin/env python3
"""灵感收集 — 从QQ邮箱提取灵感邮件，归档到灵感合集。

使用方式：
  1. 手机QQ邮箱发邮件：主题「灵感：<标题>」，正文写想法
  2. 发送到 7302282@qq.com
  3. 运行本脚本自动提取归档

用法:
  python3 scripts/collect_inspiration.py        # 提取所有未归档灵感
  python3 scripts/collect_inspiration.py --watch # 持续运行（每30分钟检查一次）
"""

import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from lib.email_push import check_replies

INSPIRATION_FILE = os.path.expanduser("~/claude/deliverables/inspiration/灵感合集.md")
PROCESSED_LOG = "/tmp/inspiration_processed_ids.json"


def load_processed():
    if os.path.exists(PROCESSED_LOG):
        with open(PROCESSED_LOG) as f:
            return set(json.load(f))
    return set()


def save_processed(ids):
    with open(PROCESSED_LOG, "w") as f:
        json.dump(list(ids), f)


def extract_inspirations(replies, processed):
    inspirations = []
    for r in replies:
        subj = r.get("subject", "")
        content = r.get("content", "")
        msg_id = r.get("id", "")

        # 跳过已处理的
        if msg_id in processed:
            continue

        # 检测灵感邮件：主题含"灵感"或"idea"
        if "灵感" in subj or "idea" in subj.lower():
            # 从主题提取标题
            title = re.sub(r"^.*灵感[：:]\s*", "", subj).strip()
            if not title:
                title = subj.strip()
            inspirations.append({
                "id": msg_id,
                "title": title,
                "content": content.strip(),
                "date": r.get("date", ""),
            })
        # 也可以支持"多想了一个"等关键词
        elif any(kw in subj for kw in ["想了一个", "有个想法", "突然想到", "记一下"]):
            inspirations.append({
                "id": msg_id,
                "title": subj.strip() or "未命名灵感",
                "content": content.strip(),
                "date": r.get("date", ""),
            })

    return inspirations


def append_to_file(inspirations):
    if not inspirations:
        print("📭 无新灵感")
        return 0

    with open(INSPIRATION_FILE, "a", encoding="utf-8") as f:
        for insp in reversed(inspirations):
            f.write(f"### {insp['date']} | {insp['title']}\n\n")
            if insp["content"]:
                f.write(f"{insp['content']}\n\n")
            f.write(f"---\n\n")

    print(f"✅ 收录 {len(inspirations)} 条新灵感 → {INSPIRATION_FILE}")
    return len(inspirations)


def main():
    processed = load_processed()
    replies = check_replies(hours_back=72)
    inspirations = extract_inspirations(replies, processed)

    count = append_to_file(inspirations)
    if count > 0:
        new_ids = {i["id"] for i in inspirations}
        save_processed(processed | new_ids)

    if "--watch" in sys.argv:
        import time
        print("👀 监听模式，每30分钟检查一次...")
        while True:
            time.sleep(1800)
            replies = check_replies(hours_back=72)
            inspirations = extract_inspirations(replies, load_processed())
            if inspirations:
                append_to_file(inspirations)
                new_ids = {i["id"] for i in inspirations}
                save_processed(load_processed() | new_ids)


if __name__ == "__main__":
    main()
