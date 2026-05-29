#!/usr/bin/env python3
"""
ai_capability_flywheel.py — AI能力自进化飞轮

每周评估五维度能力等级变化，检测升级证据，更新提升方案。

用法:
  python3 ai_capability_flywheel.py           # 扫描+推送微信
  python3 ai_capability_flywheel.py --dry-run # 只打印证据报告
"""

import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

DELIVERABLES = Path("/Users/cyingfang/claude/deliverables")
SPECS_DIR = DELIVERABLES / "记忆规范"
SCRIPTS_DIR = Path("/Users/cyingfang/claude/scripts")
AI_DIR = DELIVERABLES / "ai"


def push_to_wechat(title: str, content: str) -> bool:
    script = SCRIPTS_DIR / "wechat_push.py"
    result = subprocess.run(
        ["python3", str(script), title, content],
        capture_output=True, text=True, timeout=15,
    )
    return result.returncode == 0


# ============================================================
# 证据收集：每个维度独立扫描
# ============================================================

def assess_规范力() -> dict:
    """规范力：检查规范更新频率、实战驱动更新占比、新规范创建。"""
    evidence = {"level": "L1.5", "signals": [], "gaps": []}

    specs = list(SPECS_DIR.glob("*.md"))
    recent_days = 7

    # 近7天更新的规范
    recent_updates = []
    for s in specs:
        mtime = datetime.fromtimestamp(s.stat().st_mtime)
        days = (datetime.now() - mtime).days
        if days <= recent_days:
            recent_updates.append(s.stem)

    evidence["signals"].append(f"近7天更新：{len(recent_updates)}份规范")
    for name in recent_updates:
        evidence["signals"].append(f"  ✅ {name}")

    # v2.0 规范数量
    v2_specs = []
    for s in specs:
        content = s.read_text(encoding="utf-8")
        if "version: v2.0" in content or "version: v2" in content:
            v2_specs.append(s.stem)
    evidence["signals"].append(f"v2.0规范：{len(v2_specs)}份（{', '.join(v2_specs)}）")

    # 实战驱动更新的证据
    plan = SPECS_DIR / "AI能力五维提升方案_20260528.md"
    if plan.exists():
        content = plan.read_text(encoding="utf-8")
        if "Agent A/B/C 已完成" in content or "3家公司的Agent A/B/C产出已完成" in content:
            evidence["signals"].append("✅ 投资分析Agent组用3家真实公司财报跑通Agent A/B/C")

    # gaps
    if len(v2_specs) < 4:
        evidence["gaps"].append("v2.0规范覆盖率不足50%")
    thirty_days_ago = datetime.now() - timedelta(days=30)
    stale = [s.stem for s in specs if datetime.fromtimestamp(s.stat().st_mtime) < thirty_days_ago]
    if stale:
        evidence["gaps"].append(f"{len(stale)}份规范超30天未更新：{stale}")

    return evidence


def assess_编排力() -> dict:
    """编排力：检查Agent组使用频率、并行任务记录、新Agent组创建。"""
    evidence = {"level": "L1.0", "signals": [], "gaps": []}

    # Agent组配置文件
    agent_config = SPECS_DIR / "投资分析Agent组配置.md"
    if agent_config.exists():
        mtime = datetime.fromtimestamp(agent_config.stat().st_mtime)
        days = (datetime.now() - mtime).days
        evidence["signals"].append(f"✅ Agent组配置存在（{days}天前更新）")

        content = agent_config.read_text(encoding="utf-8")
        if "Agent A：指标提取" in content and "Agent E：汇总与异常排序" in content:
            evidence["signals"].append("✅ 5-Agent完整配置已就绪")

    # 实战使用证据
    analysis_files = list(AI_DIR.glob("**/*.md")) + list(DELIVERABLES.glob("**/投资分析*.md"))
    recent_analyses = [f for f in analysis_files
                       if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days <= 7]
    if recent_analyses:
        evidence["signals"].append(f"✅ 近7天有投资分析产出")

    # 多场景Agent组
    evidence["gaps"].append("仅投资分析1个场景有Agent组，缺事业/健康场景")

    return evidence


def assess_验证力() -> dict:
    """验证力：检查交叉验证规则、AI异常日志、产出质量检查记录。"""
    evidence = {"level": "L0.5", "signals": [], "gaps": []}

    # Agent E 交叉验证
    agent_config = SPECS_DIR / "投资分析Agent组配置.md"
    if agent_config.exists():
        content = agent_config.read_text(encoding="utf-8")
        if "数据一致性检查" in content:
            evidence["signals"].append("✅ Agent E 包含数据一致性检查设计")

    # 异常日志
    auto_fixes_dir = AI_DIR / "执行与简报" / "auto_fixes"
    if auto_fixes_dir.exists():
        fix_files = list(auto_fixes_dir.glob("*.md"))
        if fix_files:
            evidence["signals"].append(f"✅ auto_fix系统就绪，{len(fix_files)}份修复草案")

    # AI产出验证规则
    evidence["gaps"].append("无独立的'AI产出验证规则'文件")
    evidence["gaps"].append("Agent E交叉验证尚未实际运行并产出矛盾发现")
    evidence["gaps"].append("无AI异常行为记录日志")

    return evidence


def assess_扩展力() -> dict:
    """扩展力：检查新脚本创建、Python学习进度、工具使用频率。"""
    evidence = {"level": "L0.5", "signals": [], "gaps": []}

    # 近7天新增/更新的脚本
    py_files = list(SCRIPTS_DIR.glob("*.py"))
    recent_scripts = []
    for f in py_files:
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        days = (datetime.now() - mtime).days
        if days <= 7:
            recent_scripts.append(f.name)

    evidence["signals"].append(f"脚本总数：{len(py_files)}个")
    if recent_scripts:
        evidence["signals"].append(f"近7天活跃脚本：{len(recent_scripts)}个")
        for name in recent_scripts[:5]:
            evidence["signals"].append(f"  ✅ {name}")

    # 新脚本
    new_this_week = [f.name for f in py_files
                     if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days <= 1]
    if new_this_week:
        evidence["signals"].append(f"🆕 今天新建脚本：{', '.join(new_this_week)}")

    # Cherny系统脚本
    key_scripts = ["auto_pr.py", "knowledge_flywheel.py", "push_briefing.py", "wechat_push.py"]
    existing = [s for s in key_scripts if (SCRIPTS_DIR / s).exists()]
    evidence["signals"].append(f"Cherny系统脚本：{len(existing)}/{len(key_scripts)} 就绪")

    evidence["gaps"].append("Python Week 1基础训练未启动")
    evidence["gaps"].append("所有脚本均由AI生成，独立编码能力未验证")

    return evidence


def assess_感知力() -> dict:
    """感知力：检查雷达周报连续性、四源扫描完成度、新能力判断记录。"""
    evidence = {"level": "L0.5", "signals": [], "gaps": []}

    radar_files = sorted(AI_DIR.glob("AI能力雷达周报_*.md"))
    if radar_files:
        latest = radar_files[-1]
        days = (datetime.now() - datetime.fromtimestamp(latest.stat().st_mtime)).days
        evidence["signals"].append(f"✅ 雷达周报已创建：{latest.name}（{days}天前）")
        if days <= 7:
            evidence["signals"].append("✅ 在每周节律内")
    else:
        evidence["gaps"].append("无雷达周报")

    # 首次雷达的四源扫描是否完成
    if radar_files:
        content = radar_files[0].read_text(encoding="utf-8")
        sources = ["源1", "源2", "源3", "源4"]
        covered = [s for s in sources if s in content]
        evidence["signals"].append(f"四源覆盖：{len(covered)}/4")

    evidence["gaps"].append("连续运行<2周，尚未形成习惯")
    evidence["gaps"].append("四源扫描耗时远超15分钟")

    return evidence


# ============================================================
# 汇总报告
# ============================================================

def build_flywheel_report(assessments: dict, is_dry_run: bool = False) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    dims = [
        ("规范力", "📋", "L1.5", "L2.5"),
        ("编排力", "🔀", "L1.0", "L2.0"),
        ("验证力", "🔍", "L0.5", "L1.5"),
        ("扩展力", "🔧", "L0.5", "L1.5"),
        ("感知力", "📡", "L0.5", "L1.5"),
    ]

    lines = [
        f"# AI能力飞轮 | {now}",
        "> 五维度自进化扫描：收集证据 → 判断升级 → 更新目标\n",
    ]

    # 每个维度
    for dim_name, icon, current, target in dims:
        data = assessments.get(dim_name, {})
        lines.append(f"## {icon} {dim_name}（{current} → {target}）")

        signals = data.get("signals", [])
        gaps = data.get("gaps", [])

        if signals:
            for s in signals:
                lines.append(f"- {s}")
        if gaps:
            lines.append(f"")
            for g in gaps:
                lines.append(f"- ❌ {g}")
        lines.append("")

    # 升级判断
    lines.append("## 🎯 升级判断")

    # Check if any dimension has evidence of level-up
    # 规范力: v2.0 specs ≥ 3, all specs updated in 7 days, real usage → could be L2.0
    lines.append("- **规范力 L1.5**：3份v2.0规范+3家公司Agent实战+Cherny系统建成。若再经过1轮财报季实战迭代 → L2.0")
    lines.append("- **编排力 L1.0**：5-Agent配置完成+3公司并行跑通。若扩展到5家公司+1个新场景 → L1.5")
    lines.append("- **验证力 L0.5**：Agent E交叉验证已设计未跑通。本周优先 → L1.0")
    lines.append("- **扩展力 L0.5**：auto_pr.py+knowledge_flywheel.py建成，Cherny系统就绪。→ 已接近L1.0")
    lines.append("- **感知力 L0.5**：首次雷达完成+四源扫描。连续4周不中断 → L1.0")
    lines.append("")

    # 本周行动
    lines.append("## ⚡ 本周优先行动")
    lines.append("1. **验证力**（最大短板）：跑通Agent E交叉验证，记录至少1条AI产出矛盾")
    lines.append("2. **扩展力→L1.0**：Python Week 1启动——写第一个独立脚本")
    lines.append("3. **编排力**：将3家公司Agent A-E完整产出合并为一份投资分析报告")

    lines.append(f"\n---\n飞轮自动运行 | {now}")
    return "\n".join(lines)


# ============================================================
# 主入口
# ============================================================

def main():
    is_dry_run = "--dry-run" in sys.argv

    print("🔍 扫描五维度证据...")
    assessments = {
        "规范力": assess_规范力(),
        "编排力": assess_编排力(),
        "验证力": assess_验证力(),
        "扩展力": assess_扩展力(),
        "感知力": assess_感知力(),
    }

    report = build_flywheel_report(assessments, is_dry_run)

    if is_dry_run:
        print(report)
        return

    # 统计信号数
    total_signals = sum(len(a.get("signals", [])) for a in assessments.values())
    total_gaps = sum(len(a.get("gaps", [])) for a in assessments.values())

    emoji = "✅" if total_gaps <= 3 else "⚠️"
    title = f"AI能力飞轮 {emoji} {total_signals}信号 {total_gaps}缺口"
    success = push_to_wechat(title, report)
    if success:
        print(f"推送成功 | {total_signals}信号 {total_gaps}缺口")
    else:
        print("推送失败")
        print(report)


if __name__ == "__main__":
    main()
