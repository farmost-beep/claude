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
    """早间推送：发P0行动清单"""
    today_str = date.today().strftime("%Y年%m月%d日")
    title = f"今日P0行动 | {today_str}"
    parts = [f"## {today_str} 今日P0行动清单\n"]
    # 从综合行动卡提取P0
    action_path = DELIVERABLES / f"6月1日综合行动卡_20260601.md"
    if action_path.exists():
        content = action_path.read_text(encoding="utf-8")
        in_p0 = False
        for line in content.split("\n"):
            if "P0-" in line and "🔴" in line:
                name = line.split("P0-")[-1].split("：")[0] if "：" in line else line[:30]
                parts.append(f"🔴 {name}")
                in_p0 = True
            elif "P1-" in line and "🟡" in line:
                name = line.split("P1-")[-1].split("：")[0] if "：" in line else line[:30]
                parts.append(f"🟡 {name}")
    if len(parts) == 1:
        parts.append("- 查看综合行动卡获取今日P0")
    parts.append("")
    parts.append("---\n完整行动卡: deliverables/6月1日综合行动卡_20260601.md")
    return title, "\n".join(parts)


def build_evening_checkin() -> tuple[str, str]:
    """晚间推送：只发异常提醒（去掉固定模板）"""
    today_str = date.today().strftime("%Y年%m月%d日")
    title = f"晚间提醒 | {today_str}"
    alerts = []
    # 检查有没有未完成的关键P0
    action_path = DELIVERABLES / f"6月1日综合行动卡_20260601.md"
    if action_path.exists():
        content = action_path.read_text(encoding="utf-8")
        if "⬜" in content:
            unchecked = content.count("⬜")
            if unchecked > 3:
                alerts.append(f"⚠️ 今日还有 {unchecked} 项未完成，建议优先处理投资+健康P0")
    if not alerts:
        alerts.append("✅ 系统健康，无异常需关注")
    parts = [f"## {today_str}\n"]
    parts.extend(f"{a}\n" for a in alerts)
    parts.append("---")
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
