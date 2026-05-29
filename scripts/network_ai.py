#!/usr/bin/env python3
"""
network_ai.py — 四重网络经营AI助手

扫描四重网络的互动活跃度，标记断联风险，生成本周联系建议。

用法:
  python3 network_ai.py           # 扫描+微信推送
  python3 network_ai.py --dry-run # 只打印报告
"""

import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

DELIVERABLES = Path("/Users/cyingfang/claude/deliverables")
OBSIDIAN_CAREER = Path("/Users/cyingfang/Documents/Obsidian Vault 6goals/02-事业进阶")
SCRIPTS_DIR = Path("/Users/cyingfang/claude/scripts")

# 四重网络定义
NETWORKS = {
    "民建": {
        "keywords": ["民建", "建言", "社情民意", "参政", "民主党派", "政协", "统战",
                     "提案", "调研报告", "民主监督"],
        "contact_hint": "民建市委/区委联系人、同组委员、课题组成员",
        "action_suggestion": "检查建言提交反馈、关注民建课题征集、准备下季度选题",
    },
    "中科大": {
        "keywords": ["中科大", "USTC", "校友", "合肥", "科大"],
        "contact_hint": "校友会骨干、同行业校友（金融/科技）、导师",
        "action_suggestion": "联系校友会了解近期活动、对接科技金融领域校友",
    },
    "浙江": {
        "keywords": ["浙江", "杭州", "宁波", "温州", "绍兴", "籍贯", "金华",
                     "台州", "嘉兴", "湖州", "衢州", "丽水", "舟山"],
        "contact_hint": "浙江商会/同乡会、浙江籍企业家、浙江政商界人士",
        "action_suggestion": "关注浙江籍企业家在上海的动态、对接产业资源",
    },
    "邮储": {
        "keywords": ["邮储", "PSBC", "行内", "总行", "分行", "支行",
                     "银行", "信贷", "授信", "风控"],
        "contact_hint": "总行条线领导、分行管理层、支行行长、业务骨干",
        "action_suggestion": "跨部门项目对接、内部培训分享、业务协同机会",
    },
}


def scan_network_activity(network_name: str, keywords: list[str]) -> dict:
    """扫描某个网络在所有deliverable中的近期活跃度。"""
    result = {
        "name": network_name,
        "recent_7d": 0,
        "recent_14d": 0,
        "recent_30d": 0,
        "files": [],
        "cold": False,
    }

    today = datetime.now()
    for f in DELIVERABLES.rglob("*.md"):
        try:
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            days = (today - mtime).days
            if days > 30:
                continue
            content = f.read_text(encoding="utf-8")[:5000]
            if any(kw in content for kw in keywords):
                if days <= 7:
                    result["recent_7d"] += 1
                if days <= 14:
                    result["recent_14d"] += 1
                if days <= 30:
                    result["recent_30d"] += 1
                if days <= 14:
                    result["files"].append(f.stem)
        except (OSError, UnicodeDecodeError):
            pass

    result["cold"] = result["recent_14d"] == 0
    return result


def scan_opportunity_signals() -> list[str]:
    """从近期产出中检测可能的网络机会信号。"""
    signals = []
    today = datetime.now()

    # 检查是否有新的建言/文章可以分享给网络
    for f in DELIVERABLES.rglob("*.md"):
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        if (today - mtime).days > 7:
            continue
        try:
            content = f.read_text(encoding="utf-8")[:3000]
        except:
            continue

        fname = f.stem.lower()

        if "民建" in fname or "建言" in fname:
            signals.append(f"📣 民建建言产出「{f.stem}」→ 可同步给课题组成员")
        if "客户" in fname or "拜访" in fname:
            signals.append(f"🏦 客户方案产出「{f.stem}」→ 可对接行内相关部门")
        if "公众号" in fname or "文章" in fname:
            signals.append(f"📝 内容产出「{f.stem}」→ 可转发到校友/同行群")
        if "方法" in fname or "框架" in fname:
            signals.append(f"🔧 方法论产出「{f.stem}」→ 可作为内部培训分享素材")

    return signals[:5]


def build_weekly_contact_suggestions(networks_data: dict) -> list[str]:
    """生成本周联系建议。"""
    suggestions = []

    for net_name, data in networks_data.items():
        net = NETWORKS[net_name]
        if data["cold"]:
            suggestions.append(
                f"🔴 **{net_name}网络** 近14天无互动 → {net['action_suggestion']}。"
                f"联系：{net['contact_hint']}。"
            )
        elif data["recent_7d"] == 0 and data["recent_14d"] > 0:
            suggestions.append(
                f"🟡 **{net_name}网络** 7-14天前有过互动但近7天无 → 本周发一条消息保持热度。"
            )
        else:
            suggestions.append(
                f"🟢 **{net_name}网络** 活跃中（近7天 {data['recent_7d']} 次提及）"
            )

    return suggestions


def build_report(networks_data: dict, suggestions: list[str],
                 opportunities: list[str]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# 网络经营AI助手 | {now}",
        f"> 四重网络活跃度扫描 + 本周联系建议\n",
    ]

    # 总览
    cold_count = sum(1 for d in networks_data.values() if d["cold"])
    active_count = sum(1 for d in networks_data.values() if not d["cold"])
    emoji = "✅" if cold_count == 0 else "⚠️" if cold_count <= 1 else "🔴"
    lines.append(f"## {emoji} 活跃度总览：{active_count}活跃 / {cold_count}静默")

    for net_name, data in networks_data.items():
        lines.append(
            f"- **{net_name}**：7d={data['recent_7d']} | "
            f"14d={data['recent_14d']} | 30d={data['recent_30d']}"
        )
    lines.append("")

    # 本周联系建议
    lines.append("## 📞 本周联系建议")
    for s in suggestions:
        lines.append(f"- {s}")
    lines.append("")

    # 机会信号
    if opportunities:
        lines.append("## 🎯 检测到的网络机会")
        for o in opportunities:
            lines.append(f"- {o}")
        lines.append("")

    # 深度经营检查
    lines.append("## 🔍 每网络深度检查")
    for net_name, data in networks_data.items():
        net = NETWORKS[net_name]
        lines.append(f"### {net_name}")
        lines.append(f"- 联系人：{net['contact_hint']}")
        if data["files"]:
            lines.append(f"- 近14天相关文件：{', '.join(data['files'][:3])}")
        if data["cold"]:
            lines.append(f"- ⚠️ 断联>14天，建议行动：{net['action_suggestion']}")
        lines.append("")

    # 自检
    lines.append("## 📋 每周自检")
    lines.append("- [ ] 上周主动联系了几个关键联系人？（不是等他们找你）")
    lines.append("- [ ] 最近一次因为你而认识了另一个人？")
    lines.append("- [ ] 有没有新的产出可以转发给网络？")
    lines.append("- [ ] 有没有哪个网络的人最近需要你帮忙？（先给价值）")

    lines.append(f"\n---\nAI助手自动运行 | {now}")
    return "\n".join(lines)


def push_to_wechat(title: str, content: str) -> bool:
    script = SCRIPTS_DIR / "wechat_push.py"
    result = subprocess.run(
        ["python3", str(script), title, content],
        capture_output=True, text=True, timeout=15,
    )
    return result.returncode == 0


def main():
    is_dry_run = "--dry-run" in sys.argv

    print("🔍 扫描四重网络...")
    networks_data = {}
    for net_name, net_info in NETWORKS.items():
        networks_data[net_name] = scan_network_activity(
            net_name, net_info["keywords"]
        )

    suggestions = build_weekly_contact_suggestions(networks_data)
    opportunities = scan_opportunity_signals()
    report = build_report(networks_data, suggestions, opportunities)

    if is_dry_run:
        print(report)
        return

    cold_count = sum(1 for d in networks_data.values() if d["cold"])
    emoji = "✅" if cold_count == 0 else "⚠️" if cold_count <= 1 else "🔴"
    title = f"网络经营 {emoji} {4-cold_count}/4网络活跃"
    success = push_to_wechat(title, report)
    if success:
        print(f"推送成功 | {4-cold_count}/4网络活跃")
    else:
        print("推送失败")
        print(report)


if __name__ == "__main__":
    main()
