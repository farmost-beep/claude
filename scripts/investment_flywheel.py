#!/usr/bin/env python3
"""
investment_flywheel.py — 投资系统自进化飞轮

扫描投资系统四层架构：决策质量→行为纪律→资本配置→系统进化。
对应投资系统架构.md的四层模型。

用法:
  python3 investment_flywheel.py           # 扫描+微信推送
  python3 investment_flywheel.py --dry-run # 只打印报告
"""

from lib.wechat import push_to_wechat, push_incremental
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 第5层：执行层
sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from investment_execution import assess_执行, run_daily

DELIVERABLES = Path("/Users/cyingfang/claude/deliverables")
SPECS_DIR = DELIVERABLES / "记忆规范"
AI_DIR = DELIVERABLES / "ai"
SCRIPTS_DIR = Path("/Users/cyingfang/claude/scripts")
OBSIDIAN_INVEST = Path("/Users/cyingfang/Documents/Obsidian Vault 6goals/01-投资成功")


# ============================================================
# 第一层：决策质量 — 分析管道健康
# ============================================================

def assess_决策质量() -> dict:
    evidence = {"level": "正常", "signals": [], "gaps": []}

    # Agent E 交叉验证报告
    agent_e_files = list(AI_DIR.glob("**/AgentE_汇总报告_*.md"))
    if agent_e_files:
        latest_e = max(agent_e_files, key=lambda f: f.stat().st_mtime)
        days = (datetime.now() - datetime.fromtimestamp(latest_e.stat().st_mtime)).days
        evidence["signals"].append(f"✅ Agent E交叉验证报告存在（{days}天前：{latest_e.stem}）")

        content = latest_e.read_text(encoding="utf-8")
        if "数据一致性检查" in content:
            evidence["signals"].append("✅ 数据一致性检查已运行")
        if "发现的矛盾" in content or "需要你注意的信号" in content:
            evidence["signals"].append("⚠️ Agent E发现了需要关注的数据矛盾")
    else:
        evidence["gaps"].append("无Agent E交叉验证报告")

    # Agent组配置
    agent_config = SPECS_DIR / "投资分析Agent组配置.md"
    if agent_config.exists():
        days = (datetime.now() - datetime.fromtimestamp(agent_config.stat().st_mtime)).days
        evidence["signals"].append(f"✅ Agent组配置存在（{days}天前更新）")

    # 投资分析产出
    analysis_dir = AI_DIR / "投资分析"
    if analysis_dir.exists():
        analysis_files = list(analysis_dir.glob("*.md"))
        recent = [f for f in analysis_files
                  if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days <= 7]
        evidence["signals"].append(f"投资分析产出：{len(analysis_files)} 份（近7天 {len(recent)} 份）")

    # 数据质量（来自Agent E自我验证）
    evidence["gaps"].append("数据质量阶梯未完全实施：Agent A缺完整财报PDF，Agent B依赖训练知识而非客观数据")

    return evidence


# ============================================================
# 第二层：行为纪律 — 规范执行
# ============================================================

def assess_行为纪律() -> dict:
    evidence = {"level": "正常", "signals": [], "gaps": []}

    行为规范 = SPECS_DIR / "投资行为规范.md"
    if 行为规范.exists():
        mtime = datetime.fromtimestamp(行为规范.stat().st_mtime)
        days = (datetime.now() - mtime).days
        evidence["signals"].append(f"✅ 投资行为规范 v2.0 存在（{days}天前更新）")

        content = 行为规范.read_text(encoding="utf-8")
        chapters = ["投资哲学", "买入规则", "分析框架", "仓位与风险管理",
                     "卖出规则", "行为禁区", "节奏与回顾"]
        found = [c for c in chapters if c in content]
        evidence["signals"].append(f"8章完整度：{len(found)}/7 章")
    else:
        evidence["gaps"].append("投资行为规范缺失！")

    # 投资日志
    投资日志 = DELIVERABLES.rglob("*投资日志*.md")
    日志_files = list(投资日志)
    if not 日志_files:
        evidence["gaps"].append("无投资决策日志——买入逻辑/卖出理由未书面记录")
    else:
        evidence["signals"].append(f"✅ 投资决策日志：{len(日志_files)} 份")

    # 月度自审
    evidence["gaps"].append("📋 月度自我审计是否完成需手动确认（§7.2四问）")

    return evidence


# ============================================================
# 第三层：资本配置 — 组合管理
# ============================================================

def assess_资本配置() -> dict:
    evidence = {"level": "正常", "signals": [], "gaps": []}

    # 投资组合数据
    portfolio_files = list(DELIVERABLES.rglob("*投资组合*.md")) + \
                      list(DELIVERABLES.rglob("*portfolio*.json"))
    if portfolio_files:
        evidence["signals"].append(f"✅ 投资组合数据存在：{len(portfolio_files)} 份")
        recent = [f for f in portfolio_files
                  if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days <= 7]
        if recent:
            evidence["signals"].append(f"  近7天更新：{len(recent)} 份")
    else:
        evidence["gaps"].append("无投资组合数据文件")

    # 仓位检查（auto_pr.py 投资组合模块）
    auto_pr = SCRIPTS_DIR / "auto_pr.py"
    if auto_pr.exists():
        content = auto_pr.read_text(encoding="utf-8")
        if "check_portfolio" in content:
            evidence["signals"].append("✅ auto_pr.py 仓位自动检查已集成")

    # 现金仓位
    evidence["gaps"].append("📋 现金仓位≥10%需手动确认")
    evidence["gaps"].append("📋 单行业≤40%、AI产业链≤60%需手动确认")
    evidence["gaps"].append("📋 教育金/赡养费/医疗应急金防火墙状态需手动确认")

    return evidence


# ============================================================
# 第四层：系统进化 — 投资飞轮
# ============================================================

def assess_系统进化() -> dict:
    evidence = {"level": "正常", "signals": [], "gaps": []}

    # Auto-PR 修复草案
    auto_fixes = AI_DIR / "执行与简报" / "auto_fixes"
    if auto_fixes.exists():
        fix_files = list(auto_fixes.glob("*.md"))
        if fix_files:
            recent_fixes = [f for f in fix_files
                           if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days <= 7]
            evidence["signals"].append(f"✅ Auto-PR修复草案：{len(fix_files)} 份（近7天 {len(recent_fixes)} 份）")
    else:
        evidence["gaps"].append("auto_fixes目录不存在")

    # Agent E 改进建议
    agent_e_files = list(AI_DIR.glob("**/AgentE_汇总报告_*.md"))
    if agent_e_files:
        latest_e = max(agent_e_files, key=lambda f: f.stat().st_mtime)
        content = latest_e.read_text(encoding="utf-8")
        if "改进建议" in content or "改进建议" in content:
            evidence["signals"].append("✅ Agent E自验证包含系统改进建议")
            # Count improvement suggestions
            import re
            suggestions = re.findall(r'[→➡️]\s*\*?\*?[^*\n]+', content)
            evidence["signals"].append(f"  已记录约 {len(suggestions)} 条改进方向")

    # AI异常日志
    异常日志 = AI_DIR / "执行与简报" / "AI异常日志.md"
    if 异常日志.exists():
        evidence["signals"].append("✅ AI异常日志已创建")
    else:
        evidence["gaps"].append("AI异常日志尚未建立（Agent E首次运行已产生3条待记录异常）")

    # 知识卡片→规范升级（兼容Vault不可访问的情况）
    bridge = Path("/Users/cyingfang/Documents/Obsidian Vault 6goals/06-知识库/Layer2到Layer1升级映射.md")
    try:
        if bridge.exists():
            content = bridge.read_text(encoding="utf-8")
            if "已升级" in content:
                evidence["signals"].append("✅ 知识卡片→规范升级映射表存在")
            if "待升级" in content:
                evidence["signals"].append("⚠️ 有待升级的投资相关卡片（贝叶斯更新/凯利公式/均值回归）")
    except (PermissionError, FileNotFoundError):
        evidence["signals"].append("⚠️ Obsidian Vault不可访问，知识卡片升级映射表跳过")
    
    # 月度复盘    # 月度复盘
    evidence["gaps"].append("📋 本月投资决策复盘是否完成需手动确认")

    return evidence


# ============================================================
# 飞轮联动判断
# ============================================================

def 联动判断(决策: dict, 纪律: dict, 配置: dict, 进化: dict, 执行: dict = None) -> tuple:
    total_gaps = (len(决策.get("gaps", [])) + len(纪律.get("gaps", [])) +
                  len(配置.get("gaps", [])) + len(进化.get("gaps", [])))

    # 统计真正需要关注的缺口（排除📋手动确认项）
    all_gaps = (决策.get("gaps", []) + 纪律.get("gaps", []) +
                配置.get("gaps", []) + 进化.get("gaps", []))
    if 执行:
        all_gaps += 执行.get("gaps", [])
    real_gaps = [g for g in all_gaps if not g.startswith("📋")]

    if len(real_gaps) == 0:
        return ("✅ 系统健康", "四层无实质性缺口，飞轮正常运转", [
            "维护当前节奏：Agent E每季运行 + 月度自审 + 每周组合体检",
        ])
    elif len(real_gaps) <= 2:
        return ("⚠️ 有小缺口", f"{len(real_gaps)} 项实质性缺口待补", [
            f"优先补缺口：{real_gaps[0][:60]}...",
            "不影响当前投资决策，但长期会累积为系统风险",
        ])
    else:
        return ("🔴 系统有漏洞", f"{len(real_gaps)} 项实质性缺口，投资系统不完整", [
            f"本周优先：补上 {real_gaps[0][:60]}...",
            f"下周：补上 {real_gaps[1][:60] if len(real_gaps) > 1 else ''}...",
        ])


# ============================================================
# 汇总报告
# ============================================================

def build_report(assessments: dict, flywheel: tuple) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    状态, 诊断, 行动 = flywheel

    lines = [
        f"# 投资飞轮 | {now}",
        f"> 五层联动：{状态} — {诊断}\n",
    ]

    lines.append("## 🎯 飞轮判断")
    lines.append(f"**{状态}**：{诊断}")
    lines.append("")
    for a in 行动:
        lines.append(f"- [ ] {a}")
    lines.append("")

    # 五层
    layers = [
        ("决策质量", "🔬", "分析管道健康"),
        ("行为纪律", "📏", "规范执行"),
        ("资本配置", "💰", "组合管理"),
        ("系统进化", "🔄", "投资飞轮"),
        ("执行", "⚡", "操作执行层"),
    ]

    for layer_name, icon, desc in layers:
        data = assessments.get(layer_name, {})
        lines.append(f"## {icon} 第一层：{layer_name} — {desc}")
        for s in data.get("signals", []):
            lines.append(f"- {s}")
        for g in data.get("gaps", []):
            lines.append(f"- ❌ {g}")
        lines.append("")

    # 季度自检
    lines.append("## 📋 季度健康自检")
    lines.append("- [ ] 管道健康：Agent E是否运行？发现了什么矛盾？")
    lines.append("- [ ] 纪律健康：最近3月有无违反投资行为规范？")
    lines.append("- [ ] 配置健康：仓位有无超标？现金≥10%？")
    lines.append("- [ ] 进化健康：Auto-PR有修复吗？Agent E改进建议落实了没？")
    lines.append("- [ ] 知识健康：投资卡片有无该升级到规范的？")
    lines.append("")

    lines.append("## L3 质量自检")
    lines.append("- [ ] 所有定价数据标注了来源和日期")
    lines.append("- [ ] 关键判断经两个独立来源交叉验证")
    lines.append("- [ ] 不确定的推断标注了[待核实]")
    lines.append("- [ ] 分析结论不含'买入/卖出'操作指令")
    lines.append("")

    lines.append("## L4 飞轮反思")
    lines.append("- 本周扫描最意外的发现：")
    lines.append("- 数据管道哪个环节最脆弱：")
    lines.append("- 下次扫描可以改进的地方：")

    lines.append(f"\n---\n飞轮自动运行 | {now}")
    return "\n".join(lines)


def main():
    is_dry_run = "--dry-run" in sys.argv

    print("🔍 扫描投资系统五层架构...")
    assessments = {
        "决策质量": assess_决策质量(),
        "行为纪律": assess_行为纪律(),
        "资本配置": assess_资本配置(),
        "系统进化": assess_系统进化(),
        "执行": assess_执行(),
    }

    flywheel = 联动判断(
        assessments["决策质量"],
        assessments["行为纪律"],
        assessments["资本配置"],
        assessments["系统进化"],
        assessments["执行"],
    )
    report = build_report(assessments, flywheel)

    # 如果有P0待办，也推送执行层订单
    exec_data = assessments.get("执行", {})
    if exec_data.get("orders"):
        try:
            run_daily(dry_run=is_dry_run)
        except Exception:
            pass

    if is_dry_run:
        print(report)
        return

    状态, _, _ = flywheel
    emoji = "✅" if "健康" in 状态 else "⚠️" if "小缺口" in 状态 else "🔴"
    title = f"投资飞轮 {emoji} {状态}"
    success = push_incremental("投资", title, report, f"{状态}")
    if success:
        print(f"推送成功 | {状态}")
    else:
        print("推送失败")
        print(report)


if __name__ == "__main__":
    main()
