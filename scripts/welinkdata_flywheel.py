#!/usr/bin/env python3
"""
welinkdata_flywheel.py — WeLinkData（文沥）AI启动飞轮

每周扫描4个维度：战略清晰度 → 执行进度 → 竞争适配 → 方法示范
对齐陈颖芳AI方法论4层框架，展示方法论在供应链金融科技公司的应用。

用法:
  python3 welinkdata_flywheel.py           # 扫描+微信推送
  python3 welinkdata_flywheel.py --dry-run # 只打印报告
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

DELIVERABLES = Path("/Users/cyingfang/claude/deliverables")
CASE_DIR = DELIVERABLES / "ai/AI方法论/案例/welinkdata"
SCRIPTS_DIR = Path("/Users/cyingfang/claude/scripts")


# ============================================================
# 维度1：战略清晰度 — L1 人与AI关系
# ============================================================

def assess_战略清晰度() -> dict:
    evidence = {"level": "模糊", "signals": [], "gaps": []}

    strategy = CASE_DIR / "welinkdata_ai_strategy.md"
    if not strategy.exists():
        evidence["gaps"].append("战略文档缺失——welinkdata_ai_strategy.md不存在")
        return evidence

    content = strategy.read_text(encoding="utf-8")

    departments = ["风控", "数据服务", "产品/技术", "销售/客户成功",
                   "运营", "合规/法务", "管理层",
                   "三阶段实施路线", "终极变化"]
    found = [d for d in departments if d in content]
    coverage = len(found) / len(departments)
    evidence["signals"].append(f"10部门覆盖：{len(found)}/{len(departments)} ({coverage:.0%})")

    for phase in ["Phase 1", "Phase 2", "Phase 3"]:
        if phase in content:
            evidence["signals"].append(f"✅ {phase} 已定义")
        else:
            evidence["gaps"].append(f"{phase} 未定义")

    if "→" in content:
        evidence["signals"].append("✅ 部门AI场景使用了输入→输出描述")
    else:
        evidence["gaps"].append("AI场景缺少输入→输出描述，停留在功能列表层面")

    if coverage >= 0.9 and len([g for g in evidence["gaps"]]) == 0:
        evidence["level"] = "清晰"
    elif coverage >= 0.7:
        evidence["level"] = "部分清晰"
    else:
        evidence["level"] = "模糊"

    return evidence


# ============================================================
# 维度2：执行进度 — L2 指令层
# ============================================================

def assess_执行进度() -> dict:
    evidence = {"level": "滞后", "signals": [], "gaps": []}

    progress = CASE_DIR / "welinkdata_ai_progress.md"
    if not progress.exists():
        evidence["gaps"].append("进度追踪文件不存在——welinkdata_ai_progress.md缺失")
        return evidence

    mtime = datetime.fromtimestamp(progress.stat().st_mtime)
    days = (datetime.now() - mtime).days
    content = progress.read_text(encoding="utf-8")

    total_not_started = content.count("[ ]")
    total_planning = content.count("[~]")
    total_completed = content.count("[x]")
    total_blocked = content.count("[!]")
    if "状态标记" in content and "[!] 受阻" in content:
        total_blocked -= 1
    total = total_not_started + total_planning + total_completed + max(0, total_blocked)

    if total == 0:
        evidence["gaps"].append("进度矩阵为空——无checkbox可统计")
        return evidence

    pct_completed = total_completed / total if total > 0 else 0
    pct_in_progress = (total_planning + total_completed) / total if total > 0 else 0

    evidence["signals"].append(
        f"进度矩阵：{total}项 — [x]完成{total_completed} | [~]规划中{total_planning} | [ ]未开始{total_not_started}"
    )
    if total_blocked > 0:
        evidence["gaps"].append(f"[!]受阻项：{total_blocked}项需要关注")

    for phase_name in ["Phase 1", "Phase 2", "Phase 3"]:
        if phase_name in content:
            evidence["signals"].append(f"✅ {phase_name} 已定义在进度矩阵中")

    gates = CASE_DIR / "welinkdata_phase_gates.md"
    if gates.exists():
        evidence["signals"].append("✅ Phase Gate定义文件存在")
    else:
        evidence["gaps"].append("Phase Gate定义文件缺失")

    if pct_completed >= 0.8:
        evidence["level"] = "超前"
    elif pct_in_progress >= 0.3:
        evidence["level"] = "按计划"
    elif total_planning > 0:
        evidence["level"] = "按计划"
    else:
        evidence["level"] = "滞后"

    if days > 14:
        evidence["gaps"].append(f"进度文件{days}天未更新——可能已停滞")

    return evidence


# ============================================================
# 维度3：竞争适配 — L3 质量层
# ============================================================

def assess_竞争适配() -> dict:
    evidence = {"level": "数据不足", "signals": [], "gaps": []}

    comp_scan = CASE_DIR / "welinkdata_competitive_scan.md"
    if not comp_scan.exists():
        evidence["gaps"].append("竞争情报文件缺失")
        return evidence

    mtime = datetime.fromtimestamp(comp_scan.stat().st_mtime)
    days = (datetime.now() - mtime).days
    content = comp_scan.read_text(encoding="utf-8")

    competitors = ["联易融", "中企云链", "蚂蚁链", "京东供应链金融",
                   "平安壹账通", "雪松控股", "普洛斯金融"]
    covered = [c for c in competitors if c in content]
    evidence["signals"].append(f"竞争对手覆盖：{len(covered)}/7")

    if "最近更新" in content:
        evidence["signals"].append("✅ 竞争情报表结构已建立")
    else:
        evidence["gaps"].append("竞争情报表缺少'最近更新'列")

    has_intel = False
    for comp in competitors:
        if comp in content and "待补充" not in content.split(comp)[1][:100]:
            has_intel = True
            break

    if has_intel:
        evidence["signals"].append("✅ 至少1条竞争情报已填充")
        if days <= 30:
            evidence["level"] = "领先" if len(covered) >= 5 else "持平"
        else:
            evidence["level"] = "持平"
            evidence["gaps"].append(f"最近情报{days}天前——需刷新")
    else:
        evidence["gaps"].append("所有竞争对手情报均为'待补充'——竞争扫描未启动")
        evidence["level"] = "数据不足"

    if "行业趋势信号" in content:
        trend_section = content.split("行业趋势信号")[1].split("---")[0] if "---" in content.split("行业趋势信号")[1] else ""
        if "待补充" in trend_section and len(trend_section.strip().split("\n")) <= 3:
            evidence["gaps"].append("行业趋势信号为空——未追踪供应链金融科技行业AI动态")
    else:
        evidence["gaps"].append("行业趋势信号表缺失")

    return evidence


# ============================================================
# 维度4：方法示范 — L4 进化层
# ============================================================

def assess_方法示范() -> dict:
    evidence = {"level": "弱", "signals": [], "gaps": []}

    mapping = CASE_DIR / "welinkdata_methodology_mapping.md"
    if not mapping.exists():
        evidence["gaps"].append("方法论映射文件缺失")
        return evidence

    content = mapping.read_text(encoding="utf-8")

    total_principles = 18
    strong_count = content.count("★★★ 强")
    mid_count = content.count("★★☆ 中")
    weak_count = content.count("★☆☆ 弱")
    mapped = strong_count + mid_count + weak_count

    evidence["signals"].append(f"18条原则映射：{mapped}/{total_principles}")
    evidence["signals"].append(f"映射质量：强{strong_count} | 中{mid_count} | 弱{weak_count}")

    if weak_count >= 3:
        evidence["gaps"].append(f"{weak_count}条原则为弱映射——需加强")

    if "五维度能力模型" in content or "规范力" in content:
        evidence["signals"].append("✅ 五维度能力模型已在案例中体现")
    else:
        evidence["gaps"].append("五维度能力模型未在案例中体现")

    unmapped = total_principles - mapped
    if unmapped > 0:
        evidence["gaps"].append(f"{unmapped}条原则未映射——方法示范不完整")

    if mapped == 18 and weak_count <= 1:
        evidence["level"] = "强"
    elif mapped >= 15:
        evidence["level"] = "中"
    else:
        evidence["level"] = "弱"

    return evidence


# ============================================================
# 飞轮联动判断
# ============================================================

def 联动判断(战略: dict, 进度: dict, 竞争: dict, 示范: dict) -> tuple:
    total_gaps = (len(战略.get("gaps", [])) + len(进度.get("gaps", [])) +
                  len(竞争.get("gaps", [])) + len(示范.get("gaps", [])))

    real_gaps = [g for g in
                 (战略.get("gaps", []) + 进度.get("gaps", []) +
                  竞争.get("gaps", []) + 示范.get("gaps", []))
                 if not g.startswith("📋")]

    战略_lvl = 战略.get("level", "")
    进度_lvl = 进度.get("level", "")
    竞争_lvl = 竞争.get("level", "")
    示范_lvl = 示范.get("level", "")

    if "模糊" in 战略_lvl:
        return ("🔴 方向需校准", "战略文档不够清晰", [
            "优先完善 welinkdata_ai_strategy.md — 确保10部门全部有输入→输出描述",
            "定义每个Phase的ROI量化目标（风控AUC提升/不良率下降/OCR准确率等）",
            "确认三阶段路线的优先级逻辑是否与供应链金融业务现状一致",
        ])

    if "滞后" in 进度_lvl:
        return ("⚠️ 执行滞后", "推进速度不匹配战略清晰度", [
            "将Phase 1的4个核心项（交易征信/实时风控/贸易文档/数据清洗）从'规划中'推进到'已启动'",
            "为Phase 1的每个方向指定owner和第一个里程碑日期",
            "检查是否有阻塞因素（数据/技术/合规/资源）未在进度文件中标注",
        ])

    if "数据不足" in 竞争_lvl or "落后" in 竞争_lvl:
        return ("⚠️ 竞争预警", "竞争情报缺失，战略方向可能脱节", [
            "本周至少补充3家竞争对手的AI动态（联易融/蚂蚁链/平安壹账通）",
            "搜索'supply chain finance AI 2026'和'供应链金融 AI 风控 2026'判断行业趋势",
            "对比WeLinkData的Phase 1方向（交易征信+实时风控）与竞对AI方向是否一致",
        ])

    if "弱" in 示范_lvl:
        return ("📝 案例待强化", "方法论展示不充分", [
            "补全未映射的原则到方法论映射文件中",
            "将弱映射原则（原则18 AI自进化）升级到至少'中映射'——添加具体WeLinkData场景",
            "在案例README中说明'这个案例展示了方法论的哪些部分'",
        ])

    if len(real_gaps) == 0:
        return ("✅ 飞轮正常运转", "四维无实质性缺口，WeLinkData AI飞轮健康", [
            "维护当前节奏：每周进度更新 + 月度竞争扫描",
            "关注Phase Gate条件——确认交易征信AUC/OCR准确率等指标是否达标",
            "考虑将WeLinkData案例展示给相关方（方法论在供应链金融科技领域可复制性验证）",
        ])

    if len(real_gaps) <= 3:
        return ("🟡 有小缺口", f"{len(real_gaps)}项实质性缺口", [
            f"优先补：{real_gaps[0][:80]}",
            "不影响案例整体价值，但补齐后可作为完整的方法论示范",
        ])

    return ("🔴 飞轮卡住", f"{len(real_gaps)}项缺口，飞轮未正常运转", [
        f"本周从战略文档开始逐项排查：{real_gaps[0][:80]}",
        f"下周：{real_gaps[1][:80] if len(real_gaps) > 1 else '继续排查下一项'}",
    ])


# ============================================================
# 汇总报告
# ============================================================

def build_report(assessments: dict, flywheel: tuple) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    状态, 诊断, 行动 = flywheel

    lines = [
        f"# WeLinkData AI启动飞轮 | {now}",
        f"> 四维联动：{状态} — {诊断}\n",
    ]

    lines.append("## 飞轮判断")
    lines.append(f"**{状态}**：{诊断}")
    lines.append("")
    for a in 行动:
        lines.append(f"- [ ] {a}")
    lines.append("")

    layers = [
        ("战略清晰度", "🎯", "L1 人与AI关系", "战略文档完整度+部门覆盖+阶段定义"),
        ("执行进度", "📊", "L2 指令层", "Phase推进状态+Gate满足度"),
        ("竞争适配", "🔍", "L3 质量层", "竞对AI动态+战略方向校准"),
        ("方法示范", "📐", "L4 进化层", "18条原则映射+5维度模型体现"),
    ]

    for layer_name, icon, method_layer, desc in layers:
        data = assessments.get(layer_name, {})
        lines.append(f"## {icon} {layer_name} — {desc}")
        lines.append(f"**等级：{data.get('level', '未知')}** | 方法论层：{method_layer}")
        for s in data.get("signals", []):
            lines.append(f"- {s}")
        for g in data.get("gaps", []):
            lines.append(f"- ❌ {g}")
        lines.append("")

    lines.append("## 📋 方法论一致性自检")
    lines.append("- [ ] 四维是否对齐4层框架？（战略→L1 / 进度→L2 / 竞争→L3 / 示范→L4）")
    lines.append("- [ ] 联动判断的6种状态是否覆盖了飞轮的主要情况？")
    lines.append("- [ ] 行动建议是否具体可执行？（不出现'加强''优化'等空洞词）")
    lines.append("- [ ] 本周是否至少补了1条竞争情报或更新了1项进度？")

    lines.append(f"\n---\nWeLinkData飞轮自动运行 | {now}")
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

    print("🔍 扫描WeLinkData AI飞轮四维...")
    assessments = {
        "战略清晰度": assess_战略清晰度(),
        "执行进度": assess_执行进度(),
        "竞争适配": assess_竞争适配(),
        "方法示范": assess_方法示范(),
    }

    flywheel = 联动判断(
        assessments["战略清晰度"],
        assessments["执行进度"],
        assessments["竞争适配"],
        assessments["方法示范"],
    )
    report = build_report(assessments, flywheel)

    if is_dry_run:
        print(report)
        return

    状态, _, _ = flywheel
    if "正常" in 状态:
        emoji = "✅"
    elif "小缺口" in 状态 or "待强化" in 状态 or "预警" in 状态 or "滞后" in 状态:
        emoji = "⚠️"
    else:
        emoji = "🔴"
    title = f"WeLinkData AI飞轮 {emoji} {状态}"
    success = push_to_wechat(title, report)
    if success:
        print(f"推送成功 | {状态}")
    else:
        print("推送失败")
        print(report)


if __name__ == "__main__":
    main()
