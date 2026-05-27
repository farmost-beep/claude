#!/usr/bin/env python3
"""每日简报微信推送管道。

调用方式：
  python3 scripts/push_briefing.py morning   # 早间简报
  python3 scripts/push_briefing.py evening   # 晚间检视
  python3 scripts/push_briefing.py test      # 测试推送
"""

import os
import sys
import subprocess
from datetime import date, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = PROJECT_ROOT / "deliverables"
AI_BRIEFING = DELIVERABLES / "ai" / "执行与简报" / f"每日AI简报_{date.today().strftime('%Y%m')}.md"


def push(title: str, content: str) -> bool:
    script = PROJECT_ROOT / "scripts" / "wechat_push.py"
    result = subprocess.run(
        ["python3", str(script), title, content],
        capture_output=True, text=True, timeout=15,
    )
    return result.returncode == 0


def get_today_ai_briefing() -> str:
    if not AI_BRIEFING.exists():
        return ""
    today = date.today().strftime("%Y-%m-%d")
    lines = AI_BRIEFING.read_text(encoding="utf-8").split("\n")
    collected = []
    in_today = False
    for line in lines:
        if today in line and line.startswith("#"):
            in_today = True
            continue
        if in_today:
            if line.startswith("#") and today not in line:
                break
            collected.append(line)
    return "\n".join(collected).strip()


def check_system_health() -> dict:
    issues = []
    md_count = len(list(DELIVERABLES.rglob("*.md")))
    pdf_count = len(list(DELIVERABLES.rglob("*.pdf")))
    if md_count != pdf_count:
        issues.append(f"md/pdf数量不一致: {md_count} vs {pdf_count}")
    return {
        "md_count": md_count,
        "pdf_count": pdf_count,
        "issues": issues,
        "healthy": len(issues) == 0,
    }


def build_morning_briefing() -> tuple[str, str]:
    ai = get_today_ai_briefing()
    health = check_system_health()
    today_str = date.today().strftime("%Y年%m月%d日")
    title = f"早间简报 | {today_str}"

    parts = [f"## {today_str} 早间简报\n"]
    if ai:
        parts.append("### AI 前沿动态\n")
        ai_items = [l for l in ai.split("\n") if l.strip().startswith(("-", "1.", "2.", "3.", "*"))]
        for item in ai_items[:3]:
            text = item.lstrip("-* 0123456789.。")
            if len(text) > 100:
                text = text[:100] + "..."
            parts.append(f"- {text}")
        parts.append("")

    status = "健康" if health["healthy"] else "需关注"
    parts.append(f"### 系统状态：{status}")
    parts.append(f"- md: {health['md_count']} | pdf: {health['pdf_count']}")
    for issue in health["issues"]:
        parts.append(f"- {issue}")
    parts.append("")
    parts.append(f"---\n推送: {datetime.now().strftime('%H:%M')}")
    return title, "\n".join(parts)


def build_evening_checkin() -> tuple[str, str]:
    today_str = date.today().strftime("%Y年%m月%d日")
    title = f"晚间检视 | {today_str}"
    parts = [f"## {today_str} 晚间检视\n"]
    parts.append("- [ ] 运动完成？")
    parts.append("- [ ] 知识卡片 x3")
    parts.append("- [ ] 投资组合复查")
    parts.append("- [ ] 体重记录")
    parts.append("")
    parts.append(f"---\n推送: {datetime.now().strftime('%H:%M')}")
    return title, "\n".join(parts)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 push_briefing.py [morning|evening|test]", file=sys.stderr)
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "test":
        title = f"管道测试 | {date.today().strftime('%Y年%m月%d日')}"
        content = "推送管道配置成功。"
    elif mode == "morning":
        title, content = build_morning_briefing()
    elif mode == "evening":
        title, content = build_evening_checkin()
    else:
        print(f"未知模式: {mode}", file=sys.stderr)
        sys.exit(1)

    print(f"推送: {title}")
    if push(title, content):
        print("推送成功")
    else:
        print("推送失败", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
