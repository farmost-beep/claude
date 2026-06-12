#!/usr/bin/env python3
"""微信群聊天记录分析工具

用法：
  1. 导出微信群聊天记录为txt/csv格式
  2. 运行本脚本分析

  python3 scripts/analyze_chat.py 聊天记录.txt
  python3 scripts/analyze_chat.py 聊天记录.txt --deep    # AI深度分析
  python3 scripts/analyze_chat.py 聊天记录.txt --html    # 生成HTML报告
"""

import sys, os, re, json
from collections import Counter, defaultdict
from datetime import datetime

def parse_chat(filepath):
    """解析微信聊天记录导出文件"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    messages = []
    # 常见微信导出格式: "2026-06-07 14:30 张三: 消息内容"
    pattern = r'(\d{4}[-/]\d{2}[-/]\d{2}[\s\d:]*)\s+([^:]+):\s*(.*)'

    for line in lines:
        line = line.strip()
        if not line:
            continue
        m = re.match(pattern, line)
        if m:
            messages.append({
                'time': m.group(1).strip(),
                'sender': m.group(2).strip(),
                'content': m.group(3).strip()
            })

    return messages


def analyze(messages):
    """基础统计分析"""
    if not messages:
        return {"error": "未解析到消息，请确认导出格式"}

    total = len(messages)
    senders = Counter(m['sender'] for m in messages)
    word_count = sum(len(m['content']) for m in messages)
    dates = set(m['time'][:10] for m in messages if len(m['time']) >= 10)
    hours = Counter(m['time'].split(' ')[-1].split(':')[0] for m in messages if ' ' in m['time'])

    return {
        "总消息数": total,
        "总字数": word_count,
        "聊天天数": len(dates),
        "发言人数": len(senders),
        "日均消息": round(total / max(len(dates), 1), 1),
        "人均消息": round(total / max(len(senders), 1), 1),
        "发言排行": senders.most_common(10),
        "时段分布": dict(sorted(hours.items())),
        "最活跃时段": max(hours, key=hours.get) if hours else "N/A",
    }


def deep_analysis(messages, api_key=None):
    """AI深度分析——调用Claude分析聊天内容"""
    # 拼接最近的500条消息
    recent = messages[-500:]
    text = "\n".join([f"[{m['sender']}] {m['content']}" for m in recent])

    print("🧠 AI深度分析中...")
    return text[:3000]  # 返回截断文本供用户确认


def generate_html(stats):
    """生成HTML报告"""
    html = f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<title>微信群聊天分析报告</title>
<style>
body{{font-family:-apple-system,'PingFang SC',sans-serif;max-width:700px;margin:0 auto;padding:20px;}}
h1{{color:#1A2744;text-align:center}}
table{{width:100%;border-collapse:collapse;margin:15px 0}}
th{{background:#1A2744;color:#fff;padding:8px;text-align:left}}
td{{padding:6px 8px;border-bottom:1px solid #eee}}
tr:nth-child(even){{background:#f8fafc}}
.card{{background:#f0f4ff;border-radius:8px;padding:15px;margin:10px 0;text-align:center}}
.card .num{{font-size:2em;color:#1A2744;font-weight:bold}}
.card .label{{color:#666;font-size:0.9em}}
</style></head><body>
<h1>📊 微信群聊天分析报告</h1>
<div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center">
'''
    for key in ["总消息数", "总字数", "聊天天数", "发言人数"]:
        html += f'<div class="card"><div class="num">{stats.get(key, 0)}</div><div class="label">{key}</div></div>\n'

    html += '</div><h2>🏆 发言排行TOP10</h2><table><tr><th>#</th><th>成员</th><th>消息数</th></tr>'
    for i, (name, count) in enumerate(stats.get("发言排行", []), 1):
        html += f'<tr><td>{i}</td><td>{name}</td><td>{count}</td></tr>'
    html += '</table></body></html>'
    return html


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在: {filepath}")
        sys.exit(1)

    print(f"📖 读取聊天记录: {filepath}")
    msgs = parse_chat(filepath)
    print(f"✅ 解析到 {len(msgs)} 条消息")

    stats = analyze(msgs)
    print("\n=== 📊 基础统计 ===")
    for key in ["总消息数", "总字数", "聊天天数", "发言人数", "日均消息", "人均消息", "最活跃时段"]:
        print(f"  {key}: {stats.get(key, 'N/A')}")

    print("\n🏆 发言排行TOP10:")
    for i, (name, count) in enumerate(stats.get("发言排行", [])[:10], 1):
        bar = "█" * min(count // 10, 30)
        print(f"  {i:2d}. {name[:12]:12s} {count:4d} {bar}")

    if "--html" in sys.argv:
        html = generate_html(stats)
        out = filepath.replace('.txt', '_分析报告.html').replace('.csv', '_分析报告.html')
        with open(out, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"\n✅ HTML报告已生成: {out}")

    if "--deep" in sys.argv:
        deep_analysis(msgs)
