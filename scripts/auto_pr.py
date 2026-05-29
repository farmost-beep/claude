#!/usr/bin/env python3
"""
auto_pr.py — 第二大脑自动运转系统 v2.0

Cherny 150 PR/天模式完整复刻：
  L1.5 检查+通知：发现问题 → 推送微信
  L2.0+ 自动修复 ：发现问题 → AI生成修复草案 → 推送微信 → 人批准后执行

四个"代码库"各有一套检查+修复规则：
  1. 投资组合 — 风险信号扫描 + 仓位合规检查
  2. 记忆规范 — 腐烂检测（>30天未更新）→ 起草更新建议
  3. AI能力雷达 — 周报中断检测 → 自动生成雷达初稿提示
  4. 目标进度 — 偏离检测 → 生成追赶计划

用法:
  python3 auto_pr.py                  # 检查+推送微信（L1.5）
  python3 auto_pr.py --auto-fix       # 检查+生成修复草案+推送微信（L2.0+）
  python3 auto_pr.py --dry-run        # 只打印报告，不推送
  python3 auto_pr.py --scope invest   # 只检查投资组合
  python3 auto_pr.py --list-fixes     # 列出所有待处理的修复草案
"""

import subprocess
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
DELIVERABLES = PROJECT_ROOT / "deliverables"
SPECS_DIR = DELIVERABLES / "记忆规范"
AI_DIR = DELIVERABLES / "ai"
FIXES_DIR = DELIVERABLES / "ai" / "执行与简报" / "auto_fixes"
FIXES_DIR.mkdir(parents=True, exist_ok=True)

SPEC_FRESHNESS_DAYS = 30
RADAR_MAX_GAP_DAYS = 10
HEALTH_CHECK_DAYS = 7
CAREER_CHECK_DAYS = 14


# ============================================================
# 推送层
# ============================================================

def push_to_wechat(title: str, content: str) -> bool:
    script = SCRIPTS_DIR / "wechat_push.py"
    result = subprocess.run(
        ["python3", str(script), title, content],
        capture_output=True, text=True, timeout=15,
    )
    return result.returncode == 0


# ============================================================
# 修复草案生成器（L2.0+核心）
# ============================================================

def save_fix_draft(codebase: str, issue_slug: str, fix_title: str,
                   what_is_broken: str, target_state: str, ai_prompt: str,
                   auto_apply: bool = False) -> Path:
    """保存一份修复草案——相当于Cherny的PR。"""
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}_{codebase}_{issue_slug}.md"
    filepath = FIXES_DIR / filename

    content = f"""---
codebase: {codebase}
status: pending
auto_apply: {str(auto_apply).lower()}
created: {today}
---

# {fix_title}

## 发现了什么
{what_is_broken}

## 修复后应该是什么样
{target_state}

## AI修复指令（给Claude的Prompt）
{ai_prompt}

---
> 状态：pending | 批准后运行 `python3 scripts/auto_pr.py --apply {filename}` 或在Claude中说"执行auto-fix {filename}"
"""
    filepath.write_text(content, encoding="utf-8")
    return filepath


def generate_fixes(findings: dict[str, list[str]], auto_fix: bool = False) -> list[Path]:
    """根据检查发现问题，生成修复草案。只在 auto_fix 模式下生成。"""
    if not auto_fix:
        return []

    fix_files = []

    # --- 投资组合修复 ---
    portfolio = findings.get("portfolio", [])
    for item in portfolio:
        if "规范已" in item and "未更新" in item:
            fp = save_fix_draft(
                "invest", "stale_spec",
                "投资行为规范过期 — 建议更新",
                item,
                "规范在过去30天内有一次实战驱动的更新（新增/修改至少1条规则）",
                "读取 /deliverables/记忆规范/投资行为规范.md，检查最近30天是否有实际投资决策可以提炼为新规则。"
                "如果有：更新规范，新增'修改日志'条目。如果没有：在规范末尾增加一条'Auto-PR标记：[日期] 检查通过，无新增规则'。",
            )
            fix_files.append(fp)

        if "Agent组配置" in item and "未更新" in item:
            fp = save_fix_draft(
                "invest", "agent_stale",
                "Agent组未使用 — 建议跑一次实战",
                item,
                "Agent组配置在近14天内被用于至少1次真实投资分析",
                "选取1家自选池中的公司最新财报，按 /deliverables/记忆规范/投资分析Agent组配置.md 的启动指令，"
                "运行Agent A+B+C+D+E完整分析流程。产出保存到 deliverables/ai/投资分析/。",
            )
            fix_files.append(fp)

    # --- 记忆规范修复 ---
    memory = findings.get("memory", [])
    for item in memory:
        if item.startswith("🔴") or item.startswith("🟡"):
            # 提取规范文件名
            import re
            match = re.search(r'\[(.+?)\]', item)
            spec_name = match.group(1) if match else "未知规范"

            fp = save_fix_draft(
                "memory", f"stale_{spec_name[:20]}",
                f"{spec_name} 可能腐烂 — 建议回顾更新",
                item,
                f"{spec_name} 经过一次内容回顾，确认所有判断标准仍然适用，或更新不再适用的部分",
                f"读取 /deliverables/记忆规范/{spec_name}.md。逐项检查：\n"
                "1. 判断标准（好/关注/有问题）是否仍然适用？\n"
                "2. 风险信号是否有触发过但规范没覆盖的？\n"
                "3. 最近30天是否有相关的实际经验可以提炼为新规则？\n"
                "更新规范并在修改日志中记录本次回顾。",
            )
            fix_files.append(fp)

    # --- 雷达修复 ---
    radar = findings.get("radar", [])
    for item in radar:
        if "中断" in item or "超过" in item:
            fp = save_fix_draft(
                "radar", "missing_report",
                "AI能力雷达周报中断 — 自动起草补报提示",
                item,
                "补上缺失的雷达周报，恢复每周一次的节奏",
                "按 /deliverables/记忆规范/AI能力雷达周报模板.md 的格式，扫描本周AI领域最新动态（四源：基准/产品/实战/反向），"
                "生成一份补报的雷达周报初稿，保存到 deliverables/ai/AI能力雷达周报_[周次].md。",
                auto_apply=True,
            )
            fix_files.append(fp)

    # --- 目标进度修复 ---
    goals = findings.get("goals", [])
    for item in goals:
        if "健康" in item:
            fp = save_fix_draft(
                "goals", "health_gap",
                "健康追踪中断 — 建议补记录",
                item,
                "近7天至少有一条健康相关记录（运动/体重/睡眠任一项）",
                "提醒用户：健康追踪已中断。建议立即记录：今天的体重、本周运动次数、最近3天的平均睡眠时长。"
                "如果用户提供数据，更新到 deliverables/健康/ 对应文件中。",
                auto_apply=True,
            )
            fix_files.append(fp)

        if "事业" in item:
            fp = save_fix_draft(
                "goals", "career_gap",
                "事业产出中断 — 建议检查进度",
                item,
                "近14天至少有一项事业相关产出（文章/建言/学术/行业评论）",
                "提醒用户：事业产出已中断14天。检查事业决策规范中的季度目标，判断当前进度是否落后于时间表。"
                "如果落后：建议本周内至少启动一项最小可交付的产出。",
            )
            fix_files.append(fp)

    return fix_files


# ============================================================
# 代码库 1：投资组合检查
# ============================================================

def check_portfolio() -> list[str]:
    findings = []

    spec = SPECS_DIR / "投资行为规范.md"
    if spec.exists():
        mtime = datetime.fromtimestamp(spec.stat().st_mtime)
        days = (datetime.now() - mtime).days
        if days > SPEC_FRESHNESS_DAYS:
            findings.append(f"🔴 投资行为规范已 {days} 天未更新，超过{SPEC_FRESHNESS_DAYS}天阈值")

    analysis_files = list(DELIVERABLES.glob("**/投资分析*.md")) + \
                     list(AI_DIR.glob("AI能力雷达周报*.md"))
    recent = [f for f in analysis_files
              if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days <= 14]
    if not recent:
        findings.append("⚠️ 近14天无投资分析相关产出")

    agent_config = SPECS_DIR / "投资分析Agent组配置.md"
    if agent_config.exists():
        mtime = datetime.fromtimestamp(agent_config.stat().st_mtime)
        days = (datetime.now() - mtime).days
        if days > 14:
            findings.append(f"⚠️ Agent组配置 {days} 天未更新，可能未在实战中使用")

    debt_tracker = SCRIPTS_DIR / "debt_repayment_tracker.py"
    if debt_tracker.exists():
        findings.append("📊 还本追踪器：运行 `python3 scripts/debt_repayment_tracker.py` 查看清仓进度")

    return findings


# ============================================================
# 代码库 2：记忆规范腐烂检测
# ============================================================

def check_memory_specs() -> list[str]:
    findings = []
    spec_files = sorted(SPECS_DIR.glob("*.md"))

    for spec in spec_files:
        mtime = datetime.fromtimestamp(spec.stat().st_mtime)
        days = (datetime.now() - mtime).days
        name = spec.stem

        if days > 60:
            findings.append(f"🔴 [{name}] {days} 天未更新 — 严重腐烂风险")
        elif days > SPEC_FRESHNESS_DAYS:
            findings.append(f"🟡 [{name}] {days} 天未更新 — 建议近期回顾")
        else:
            findings.append(f"✅ [{name}] {days} 天前更新 — 新鲜")

    return findings


# ============================================================
# 代码库 3：AI能力雷达连续性
# ============================================================

def check_radar() -> list[str]:
    findings = []
    radar_files = sorted(AI_DIR.glob("AI能力雷达周报_*.md"))

    if not radar_files:
        findings.append("🔴 尚未创建任何雷达周报")
        return findings

    latest = radar_files[-1]
    mtime = datetime.fromtimestamp(latest.stat().st_mtime)
    days = (datetime.now() - mtime).days

    findings.append(f"📡 最近雷达周报：{latest.name}（{days} 天前）")

    if days > RADAR_MAX_GAP_DAYS:
        findings.append(f"🔴 雷达周报中断超过{RADAR_MAX_GAP_DAYS}天 — 感知力可能退化")
    elif days > 7:
        findings.append("🟡 雷达周报超过7天未更新 — 建议本周补上")

    if len(radar_files) >= 2:
        d1 = datetime.fromtimestamp(radar_files[-1].stat().st_mtime)
        d2 = datetime.fromtimestamp(radar_files[-2].stat().st_mtime)
        gap = (d1 - d2).days
        if gap > RADAR_MAX_GAP_DAYS:
            findings.append(f"⚠️ 雷达间隔 {gap} 天，超过每周一次的节律")

    return findings


# ============================================================
# 代码库 4：目标进度对照
# ============================================================

def check_goals() -> list[str]:
    findings = []

    health_logs = list(DELIVERABLES.glob("**/健康*.md")) + \
                  list(DELIVERABLES.glob("**/运动*.md"))
    recent_health = [f for f in health_logs
                     if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days <= HEALTH_CHECK_DAYS]
    if not recent_health:
        findings.append(f"⚠️ 近{HEALTH_CHECK_DAYS}天无健康相关记录 — 健康追踪可能中断")

    career_files = list((DELIVERABLES / "career").glob("**/*.md"))
    recent_career = [f for f in career_files
                     if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days <= CAREER_CHECK_DAYS]
    if not recent_career:
        findings.append(f"⚠️ 近{CAREER_CHECK_DAYS}天无事业相关产出")

    md_count = len(list(DELIVERABLES.glob("**/*.md")))
    pdf_count = len(list(DELIVERABLES.glob("**/*.pdf")))
    findings.append(f"📁 deliverable文件：md={md_count} | pdf={pdf_count}")

    return findings


# ============================================================
# 汇总与推送
# ============================================================

def build_report(findings: dict[str, list[str]], fix_files: list[Path],
                 is_dry_run: bool = False, auto_fix: bool = False) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    mode_parts = []
    if is_dry_run:
        mode_parts.append("DRY RUN")
    if auto_fix:
        mode_parts.append("Auto-Fix L2.0+")
    if not mode_parts:
        mode_parts.append("L1.5 检查")
    mode = " | ".join(mode_parts)

    lines = [
        f"# Auto-PR 日报 | {now}",
        f"> {mode} | Cherny模式：人只看异常\n",
    ]

    section_icons = {
        "portfolio": "💰 投资组合",
        "memory": "🧠 记忆规范",
        "radar": "📡 AI雷达",
        "goals": "🎯 目标进度",
    }

    total_warnings = 0
    for key, icon in section_icons.items():
        items = findings.get(key, [])
        lines.append(f"## {icon}")
        if not items:
            lines.append("✅ 无异常\n")
        else:
            for item in items:
                lines.append(f"- {item}")
                if item.startswith("🔴") or item.startswith("⚠️"):
                    total_warnings += 1
            lines.append("")

    # 修复草案摘要（L2.0+）
    if fix_files:
        lines.append("## 🔧 自动修复草案（待批准）")
        lines.append(f"> 共 {len(fix_files)} 份PR等待审核\n")
        for fp in fix_files:
            content = fp.read_text(encoding="utf-8")
            # 提取标题
            for line in content.split("\n"):
                if line.startswith("# ") and not line.startswith("# Auto-PR"):
                    lines.append(f"- 📝 {line[2:]}")
                    break
            lines.append(f"  → 批准：在Claude中说 `执行auto-fix {fp.name}`\n")

    # 汇总
    if total_warnings == 0 and not fix_files:
        lines.append("## 总结：✅ 全部通过，无待处理异常")
    elif auto_fix:
        lines.append(f"## 总结：{total_warnings} 项异常 → 已生成 {len(fix_files)} 份修复草案")
        lines.append("在Claude中说 `执行auto-fix [文件名]` 来逐项批准，或 `执行auto-fix --all` 全部批准")
    else:
        lines.append(f"## 总结：{total_warnings} 项待处理")
        lines.append("运行 `python3 scripts/auto_pr.py --auto-fix` 自动生成修复草案")

    lines.append(f"\n---\n自动生成 | {now}")
    return "\n".join(lines)


def run_checks(scope: Optional[str] = None) -> dict[str, list[str]]:
    findings = {}
    if scope is None or scope == "invest":
        findings["portfolio"] = check_portfolio()
    if scope is None or scope == "memory":
        findings["memory"] = check_memory_specs()
    if scope is None or scope == "radar":
        findings["radar"] = check_radar()
    if scope is None or scope == "goals":
        findings["goals"] = check_goals()
    return findings


def main():
    is_dry_run = "--dry-run" in sys.argv
    auto_fix = "--auto-fix" in sys.argv
    list_fixes = "--list-fixes" in sys.argv
    scope = None

    for i, arg in enumerate(sys.argv[1:]):
        if arg.startswith("--scope="):
            scope = arg.split("=")[1]
        elif arg == "--scope" and i + 1 < len(sys.argv) - 1:
            scope = sys.argv[i + 2]

    # 列出待处理修复草案
    if list_fixes:
        fixes = sorted(FIXES_DIR.glob("*.md"))
        if not fixes:
            print("无待处理的修复草案。")
        else:
            print(f"{'='*60}")
            print(f"待处理修复草案：{len(fixes)} 份")
            print(f"{'='*60}\n")
            for fp in fixes:
                content = fp.read_text(encoding="utf-8")
                for line in content.split("\n"):
                    if line.startswith("# "):
                        print(f"📝 {fp.name}")
                        print(f"   {line[2:]}")
                        # 找状态
                        for l in content.split("\n"):
                            if l.startswith("status:") or l.startswith("auto_apply:"):
                                print(f"   {l.strip()}")
                        break
                print()
        return

    # 运行检查
    findings = run_checks(scope)
    if not findings:
        print("无检查结果。")
        return

    # 生成修复草案（仅 auto-fix 模式）
    fix_files = generate_fixes(findings, auto_fix)

    report = build_report(findings, fix_files, is_dry_run, auto_fix)

    if is_dry_run:
        print(report)
        print("\n--- DRY RUN: 未推送微信 ---")
        return

    warning_count = sum(
        1 for items in findings.values()
        for item in items
        if item.startswith("🔴") or item.startswith("⚠️")
    )

    if auto_fix:
        title = f"Auto-PR 🔧 {warning_count}异常→{len(fix_files)}份修复草案"
    else:
        title = f"Auto-PR {'⚠️' if warning_count > 0 else '✅'} {warning_count}项待处理"

    success = push_to_wechat(title, report)
    if success:
        if auto_fix and fix_files:
            print(f"推送成功 | {warning_count} 异常 → {len(fix_files)} 份修复草案已生成")
        else:
            print(f"推送成功 | {warning_count} 项待处理")
    else:
        print("推送失败，请检查微信推送配置")
        print(report)


if __name__ == "__main__":
    main()
