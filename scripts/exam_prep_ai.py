#!/usr/bin/env python3
"""
exam_prep_ai.py — 中级经济师备考AI助手

追踪320小时备考计划进度，检测落后风险，生成针对性练习建议。

用法:
  python3 exam_prep_ai.py           # 进度扫描+微信推送
  python3 exam_prep_ai.py --dry-run # 只打印报告
  python3 exam_prep_ai.py --quiz    # 从笔记中生成练习题
"""

import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

OBSIDIAN_CAREER = Path("/Users/cyingfang/Documents/Obsidian Vault 6goals/02-事业进阶")
DELIVERABLES = Path("/Users/cyingfang/claude/deliverables")
CAREER_DIR = DELIVERABLES / "career"
SCRIPTS_DIR = Path("/Users/cyingfang/claude/scripts")

EXAM_DATE = datetime(2026, 11, 7)  # 预计11月第一个周末
PLAN_START = datetime(2026, 6, 1)

# 三阶段计划定义
PHASES = {
    "阶段一：通读奠基": {
        "start": "2026-06-01", "end": "2026-07-12",
        "weekly_hours": 8, "target_questions": 300,
        "milestones": [
            ("第1周(6/1-6/7)", "购买教材，经济基础模块1第1-5章", 50),
            ("第2周(6/8-6/14)", "经济基础模块1第6-10章完成", 50),
            ("第3周(6/15-6/21)", "经济基础模块2（财政）完成", 50),
            ("第4周(6/22-6/28)", "经济基础模块3（货币金融）完成", 50),
            ("第5周(6/29-7/5)", "金融实务第1-5章完成", 50),
            ("第6周(7/6-7/12)", "金融实务第6-10章完成", 50),
        ],
    },
    "阶段二：系统强化": {
        "start": "2026-07-13", "end": "2026-09-13",
        "weekly_hours": 10, "target_questions": 1050,
        "milestones": [
            ("第7-8周(7/13-7/31)", "统计+报名+章节练习", 250),
            ("第9-10周(8/1-8/14)", "会计+金融实务6-10章章节练习", 250),
            ("第11-12周(8/15-8/31)", "法律+案例分析专项", 250),
            ("第13-14周(9/1-9/14)", "薄弱模块回顾+首套真题自测≥65%", 300),
        ],
    },
    "阶段三：刷题冲刺": {
        "start": "2026-09-14", "end": "2026-11-07",
        "weekly_hours": 15, "target_questions": 1600,
        "milestones": [
            ("第15-16周(9/15-9/30)", "近5年真题第一轮(10套)", 500),
            ("第17-18周(10/1-10/15)", "近5年真题第二轮+掐时间模拟", 500),
            ("第19-20周(10/16-10/31)", "每周2套完整模拟卷，目标≥85分", 400),
            ("考前1周(11/1-11/7)", "错题回归+记忆强化，不做新题", 200),
        ],
    },
}

# 薄弱模块定义
WEAK_MODULES = [
    ("经济学基础", "供需曲线+弹性理论+市场结构+GDP核算", "画图理解+公式推导+真题反复练"),
    ("财政", "税收分类+财政政策工具", "记忆表格+口诀+碎片时间背诵"),
    ("证券/保险/信托", "三块全新知识", "教材+视频课辅助，从头系统学"),
    ("国际金融", "汇率理论+国际收支", "系统学+公式记忆"),
]

# 强项模块
STRONG_MODULES = [
    ("货币与金融", "CISA/CIA+20年从业，快速回顾即可"),
    ("会计", "CIA审计背景，财务分析是舒适区"),
    ("商业银行经营与管理", "日常工作高度相关，重点把实践经验转化为考试语言"),
    ("金融风险与金融监管", "审计部负责人+CIA，快速回顾"),
]


def get_current_phase() -> dict:
    """判断当前处于哪个备考阶段。"""
    today = datetime.now()
    for phase_name, phase_info in PHASES.items():
        start = datetime.strptime(phase_info["start"], "%Y-%m-%d")
        end = datetime.strptime(phase_info["end"], "%Y-%m-%d")
        if start <= today <= end:
            return {"name": phase_name, **phase_info}
    if today < PLAN_START:
        return {"name": "尚未开始", "weekly_hours": 0, "target_questions": 0, "milestones": []}
    if today > EXAM_DATE:
        return {"name": "考试已结束", "weekly_hours": 0, "target_questions": 0, "milestones": []}
    return {"name": "阶段过渡期", "weekly_hours": 0, "target_questions": 0, "milestones": []}


def find_study_notes() -> list[Path]:
    """扫描所有备考笔记。"""
    notes = []
    for d in [OBSIDIAN_CAREER, CAREER_DIR / "民建与职称"]:
        if d.exists():
            for f in d.glob("*.md"):
                if "经济师" in f.stem or "经济基础" in f.stem or "金融实务" in f.stem:
                    notes.append(f)
    return notes


def assess_progress() -> dict:
    """评估备考进度。"""
    evidence = {"status": "未启动", "signals": [], "gaps": [], "risks": []}

    phase = get_current_phase()

    # 倒计时
    today = datetime.now()
    days_left = (EXAM_DATE - today).days
    evidence["signals"].append(f"📅 距考试还有 {days_left} 天")

    if phase["name"] == "尚未开始":
        days_to_start = (PLAN_START - today).days
        evidence["signals"].append(f"备考计划将于 {days_to_start} 天后启动（6月1日）")
        evidence["gaps"].append("教材尚未购买（计划6月第1周）")
        evidence["gaps"].append("刷题APP尚未下载")
        return evidence

    evidence["signals"].append(f"📖 当前阶段：{phase['name']}（目标 {phase['weekly_hours']}h/周）")

    # 检查笔记是否存在
    notes = find_study_notes()
    if notes:
        evidence["signals"].append(f"✅ 备考笔记：{len(notes)} 份")
        for n in notes:
            mtime = datetime.fromtimestamp(n.stat().st_mtime)
            days = (today - mtime).days
            if days <= 7:
                evidence["signals"].append(f"  ✅ {n.stem}（{days}天前更新）")
    else:
        if today >= PLAN_START:
            evidence["gaps"].append("备考已启动但无笔记文件——需要开始记录学习笔记")

    # 检查教材
    evidence["gaps"].append("📋 教材购买状态需手动确认（计划6月第1周）")
    evidence["gaps"].append("📋 刷题APP下载状态需手动确认")

    # 阶段里程碑检查
    for milestone, _, _ in phase["milestones"]:
        evidence["signals"].append(f"  📍 {milestone}")

    # 风险检测
    if today >= PLAN_START and not notes:
        evidence["risks"].append("⚠️ 备考已启动但无学习笔记产出——进度可能落后")

    # 薄弱模块提醒
    evidence["signals"].append(f"\n🎯 薄弱模块（{len(WEAK_MODULES)}个）：")
    for mod, focus, method in WEAK_MODULES:
        evidence["signals"].append(f"  🔴 {mod}：{focus} → {method}")
    evidence["signals"].append(f"\n✅ 强项模块（{len(STRONG_MODULES)}个）：")
    for mod, reason in STRONG_MODULES:
        evidence["signals"].append(f"  🟢 {mod}：{reason}")

    return evidence


def generate_quiz_from_notes() -> str:
    """从备考笔记中提取知识点，生成练习题。"""
    notes = find_study_notes()
    if not notes:
        return "❌ 暂无备考笔记，无法生成题目。请创建学习笔记后重试。"

    lines = ["# AI生成练习题 | " + datetime.now().strftime("%Y-%m-%d"), ""]

    for note in notes:
        content = note.read_text(encoding="utf-8")
        lines.append(f"## 来源：{note.stem}")
        lines.append("")

        # 从笔记中找加粗的术语作为考点
        import re
        bold_terms = re.findall(r'\*\*(.+?)\*\*', content)
        if bold_terms:
            lines.append("### 概念题")
            for i, term in enumerate(bold_terms[:5]):
                lines.append(f"{i+1}. {term} 的定义是什么？请用自己的话解释。")
                lines.append("")
            lines.append("")

        # 从笔记中找列表项
        list_items = re.findall(r'^- (.+)$', content, re.MULTILINE)
        if list_items:
            lines.append("### 简答题")
            for i, item in enumerate(list_items[:3]):
                lines.append(f"{i+1}. 关于「{item[:30]}...」，请展开说明其要点。")
                lines.append("")
            lines.append("")

        break  # 只处理第一份笔记

    lines.append("---")
    lines.append("> AI生成，仅用于自测练习。建议对照教材验证答案。")
    return "\n".join(lines)


def build_report(evidence: dict) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# 中级经济师备考AI助手 | {now}",
        f"> 状态：{evidence['status']} | 考试日期：2026年11月上旬\n",
    ]

    for s in evidence.get("signals", []):
        lines.append(f"- {s}")

    if evidence.get("gaps", []):
        lines.append("\n## ❌ 待完成")
        for g in evidence["gaps"]:
            lines.append(f"- {g}")

    if evidence.get("risks", []):
        lines.append("\n## ⚠️ 风险信号")
        for r in evidence["risks"]:
            lines.append(f"- {r}")

    if not evidence.get("risks") and not evidence.get("gaps"):
        lines.append("\n✅ 当前进度正常，按计划推进。")

    # 每周自检四问
    phase = get_current_phase()
    lines.append(f"\n## 📋 每周自检（目标 {phase['weekly_hours']}h/周）")
    lines.append("- [ ] 学习时长达标？")
    lines.append("- [ ] 薄弱模块有专门花时间？")
    lines.append("- [ ] 刷题量达标？错题当天搞懂？")
    lines.append("- [ ] 状态正常？无熬夜/长时间中断？")

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
    is_quiz = "--quiz" in sys.argv

    if is_quiz:
        quiz = generate_quiz_from_notes()
        print(quiz)
        return

    print("🔍 扫描备考进度...")
    evidence = assess_progress()

    # 判断状态
    if evidence["risks"]:
        evidence["status"] = "⚠️ 有风险"
    elif evidence["gaps"]:
        evidence["status"] = "🟡 待启动"
    else:
        evidence["status"] = "✅ 正常"

    report = build_report(evidence)

    if is_dry_run:
        print(report)
        return

    emoji = "✅" if "正常" in evidence["status"] else "⚠️"
    title = f"备考助手 {emoji} {evidence['status']}"
    success = push_to_wechat(title, report)
    if success:
        print(f"推送成功 | {evidence['status']}")
    else:
        print("推送失败")
        print(report)


if __name__ == "__main__":
    main()
