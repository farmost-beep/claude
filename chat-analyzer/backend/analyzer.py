"""聊天记录分析引擎"""
import re
from collections import Counter, defaultdict


def parse_chat(text: str) -> list:
    """解析聊天文本"""
    msgs = []
    for line in text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        m = re.match(r'(\d{4}[-/]\d{2}[-/]\d{2}[\s\d:]*)\s+([^:]+):\s*(.*)', line)
        if m:
            msgs.append({
                'time': m.group(1).strip(),
                'sender': m.group(2).strip(),
                'content': m.group(3).strip()
            })
    return msgs


def analyze(msgs: list) -> dict:
    if not msgs:
        return {"error": "未解析到消息"}

    senders = Counter(m['sender'] for m in msgs)
    hours = Counter()
    dates = set()

    for m in msgs:
        if ' ' in m['time']:
            h = m['time'].split(' ')[-1].split(':')[0]
            hours[h] += 1
        dates.add(m['time'][:10])

    max_c = senders.most_common(1)[0][1] if senders else 1
    max_h = max(hours.values()) if hours else 1
    total = len(msgs)

    return {
        "total_msgs": total,
        "total_chars": sum(len(m['content']) for m in msgs),
        "speakers": len(senders),
        "days": len(dates),
        "daily_avg": round(total / max(len(dates), 1), 1),
        "rankings": [
            {"name": name, "count": c}
            for name, c in senders.most_common(10)
        ],
        "hours": [
            {"hour": h, "count": hours[h]}
            for h in sorted(hours.keys())
        ],
        "peak_hour": max(hours, key=hours.get) if hours else "N/A",
        "top_speaker": senders.most_common(1)[0][0] if senders else "N/A",
    }
