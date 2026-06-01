#!/usr/bin/env python3
"""
knowledge_flywheel.py — 知识库自进化飞轮

每周自动运行，执行：
  1. 幽灵链接检测——MOC链接了但Vault中不存在的文件
  2. 孤儿卡片检测——存在于Vault但未被任何MOC链接的文件
  3. Layer 2→1 升级候选——近期被频繁引用的卡片，建议升级到规范
  4. Layer 1 腐烂检测——规范中的规则未被触发的记录

用法:
  python3 knowledge_flywheel.py           # 扫描+推送微信
  python3 knowledge_flywheel.py --dry-run # 只打印报告
"""

from lib.wechat import push_to_wechat
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

VAULT_ROOT = Path("/Users/cyingfang/Documents/Obsidian Vault 6goals")
MOC_DIR = VAULT_ROOT / "00-MOC"
DELIVERABLES = Path("/Users/cyingfang/claude/deliverables")
SPECS_DIR = DELIVERABLES / "记忆规范"
SCRIPTS_DIR = Path("/Users/cyingfang/claude/scripts")

# 不被视为"孤儿"的目录（系统/模板目录）
IGNORE_DIRS = {"assets", "templates", ".obsidian", ".trash"}

# 已知存在于deliverables/中但MOC引用了的规范文件名（在Obsidian中创建对应的stub即可）
KNOWN_EXTERNAL_REFS = {
    "投资行为规范", "投资分析规范", "投资分析Agent组配置",
    "事业决策规范", "家庭管理规范", "健康追踪规范",
    "AI能力发展规范", "AI能力五维提升方案_20260528", "AI能力雷达周报模板",
    "知识库建设规范",
}

# 除了MOC，也扫描这些索引文件来找引用
INDEX_FILES = {
    VAULT_ROOT / "06-知识库" / "知识卡片" / "知识卡片索引.md",
    VAULT_ROOT / "06-知识库" / "Layer2到Layer1升级映射.md",
    VAULT_ROOT / "01-投资成功" / "大师研究" / "大师研究.md",
    VAULT_ROOT / "00-MOC" / "幸福人生描述.md",
}


# ============================================================
# 1. 幽灵链接检测
# ============================================================

def find_ghost_links() -> list[dict]:
    """扫描所有MOC文件，找出链接了但不存在的目标。"""
    ghosts = []
    all_md_files = {f.stem for f in VAULT_ROOT.rglob("*.md")
                    if not any(d in f.parts for d in IGNORE_DIRS)}

    moc_files = list(MOC_DIR.glob("*.md"))
    for moc in moc_files:
        content = moc.read_text(encoding="utf-8")
        links = re.findall(r'\[\[([^\]|#]+)', content)
        for link in links:
            target = link.strip()
            # 跳过空链接、外部规范引用、和标注了(待建)的
            if not target:
                continue
            if target in KNOWN_EXTERNAL_REFS:
                continue
            if target in all_md_files:
                continue
            # 检查链接附近是否有"(待建)"标记
            idx = content.find(f"[[{target}]]")
            if idx == -1:
                idx = content.find(f"[[{target}|")
            context = content[max(0, idx-30):idx+len(target)+40] if idx >= 0 else ""
            if "待建" in context:
                continue
            ghosts.append({
                "moc": moc.name,
                "link": target,
                "moc_path": str(moc.relative_to(VAULT_ROOT)),
            })

    return ghosts


# ============================================================
# 2. 孤儿卡片检测
# ============================================================

def find_orphan_cards() -> list[str]:
    """找出存在于知识卡片目录但未被任何MOC或索引文件链接的文件。"""
    all_md_files = {f for f in VAULT_ROOT.rglob("*.md")
                    if not any(d in f.parts for d in IGNORE_DIRS)}

    # 收集所有引用源（MOC + 索引文件）
    all_reference_content = ""
    try:
        for moc in MOC_DIR.glob("*.md"):
            try:
                all_reference_content += moc.read_text(encoding="utf-8") + "\n"
            except (PermissionError, FileNotFoundError):
                pass
        for idx_file in INDEX_FILES:
            try:
                if idx_file.exists():
                    all_reference_content += idx_file.read_text(encoding="utf-8") + "\n"
            except (PermissionError, FileNotFoundError):
                pass
    except (PermissionError, FileNotFoundError):
        print("⚠️ Obsidian Vault不可访问，跳过MOC扫描")

    orphans = []
    for f in all_md_files:
        if f.parent == MOC_DIR:
            continue
        if f.stem not in all_reference_content:
            orphans.append(str(f.relative_to(VAULT_ROOT)))

    # 只报告知识卡片和大师研究目录下的孤儿
    knowledge_orphans = [o for o in orphans if "知识卡片/" in o or "大师研究/" in o]
    return knowledge_orphans


# ============================================================
# 3. Layer 2→1 升级候选
# ============================================================

def find_upgrade_candidates() -> list[dict]:
    """检测近期被频繁修改/引用的Layer 2文件，建议评估是否升级到Layer 1。"""
    candidates = []
    bridge_file = VAULT_ROOT / "06-知识库" / "Layer2到Layer1升级映射.md"

    # 3.1 从升级映射中提取"待升级"条目
    try:
        if bridge_file.exists():
            content = bridge_file.read_text(encoding="utf-8")
    except (PermissionError, FileNotFoundError):
        content = ""
        in_pending = False
        for line in content.split("\n"):
            if "## 待升级" in line:
                in_pending = True
                continue
            if in_pending and line.startswith("## "):
                break
            if in_pending and line.startswith("|") and "Layer 2 卡片" not in line and "|---" not in line and ":---" not in line:
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 2 and parts[0] and parts[0] != ":---":
                    candidates.append({
                        "card": parts[0],
                        "target": parts[1] if len(parts) > 1 else "",
                        "reason": parts[2] if len(parts) > 2 else "",
                        "status": "待升级（来自映射表）",
                    })

    # 3.2 检测最近7天在deliverable中被引用的知识卡片
    recent_deliverable_content = ""
    seven_days_ago = datetime.now() - timedelta(days=7)
    for f in DELIVERABLES.rglob("*.md"):
        if datetime.fromtimestamp(f.stat().st_mtime) > seven_days_ago:
            recent_deliverable_content += f.read_text(encoding="utf-8")[:2000]

    # 简化：检查哪些卡片名出现在最近产出中
    card_dir = VAULT_ROOT / "06-知识库" / "知识卡片"
    if card_dir.exists():
        for card_file in card_dir.glob("*.md"):
            card_name = card_file.stem
            if card_name in recent_deliverable_content:
                # 检查是否已标记"已升级"
                if bridge_file.exists() and f"| {card_name} |" in bridge_file.read_text(encoding="utf-8"):
                    continue  # 已升级，跳过
                candidates.append({
                    "card": card_name,
                    "target": "待判断",
                    "reason": f"近7天在deliverable中被引用",
                    "status": "新发现（高频引用）",
                })

    return candidates


# ============================================================
# 4. Layer 1 新鲜度摘要
# ============================================================

def check_spec_freshness() -> list[str]:
    """快速检查规范新鲜度（复用auto_pr逻辑的简化版）。"""
    findings = []
    for spec in sorted(SPECS_DIR.glob("*.md")):
        mtime = datetime.fromtimestamp(spec.stat().st_mtime)
        days = (datetime.now() - mtime).days
        if days > 30:
            findings.append(f"🟡 [{spec.stem}] {days}天未更新")
    return findings


# ============================================================
# 汇总报告
# ============================================================

def build_report(ghosts: list[dict], orphans: list[str],
                 candidates: list[dict], stale_specs: list[str],
                 is_dry_run: bool = False) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    week = datetime.now().strftime("%Y-W%W")

    lines = [
        f"# 知识库飞轮 {week} | {now}",
        f"> 自进化扫描：幽灵链接 → 孤儿卡片 → 升级候选 → 规范腐烂\n",
    ]

    # 幽灵链接
    lines.append("## 👻 幽灵链接")
    if not ghosts:
        lines.append("✅ 无幽灵链接\n")
    else:
        for g in ghosts:
            lines.append(f"- 🔗 `[[{g['link']}]]` ← {g['moc']}")
        lines.append("")

    # 孤儿卡片
    lines.append("## 🃏 孤儿卡片（未被MOC引用）")
    if not orphans:
        lines.append("✅ 无孤儿知识卡片\n")
    else:
        for o in orphans[:10]:  # 最多显示10个
            lines.append(f"- 📄 {o}")
        if len(orphans) > 10:
            lines.append(f"- ... 还有 {len(orphans) - 10} 个")
        lines.append("")

    # 升级候选
    lines.append("## ⬆️ Layer 2→1 升级候选")
    if not candidates:
        lines.append("✅ 无新的升级候选\n")
    else:
        for c in candidates[:8]:
            lines.append(f"- 📈 **{c['card']}** → {c['target']}")
            lines.append(f"  {c['reason']} | {c['status']}")
        lines.append("")

    # 规范腐烂
    lines.append("## 🦠 规范腐烂预警")
    if not stale_specs:
        lines.append("✅ 全部规范新鲜\n")
    else:
        for s in stale_specs:
            lines.append(f"- {s}")
        lines.append("")

    # 行动建议
    lines.append("## 🎯 本周建议行动")
    actions = []
    if ghosts:
        actions.append(f"修复 {len(ghosts)} 个幽灵链接：创建缺失文件或修正MOC链接")
    if orphans:
        actions.append(f"审查 {len(orphans)} 张孤儿卡片：要么链接到MOC，要么归档删除")
    if candidates:
        pending = [c for c in candidates if "待升级" in c["status"]]
        if pending:
            actions.append(f"评估 {len(pending)} 张待升级卡片：选择1-2张升级到Layer 1规范")
    if stale_specs:
        actions.append(f"回顾 {len(stale_specs)} 份可能腐烂的规范")
    if not actions:
        actions.append("知识库健康，保持当前节奏")
    for a in actions:
        lines.append(f"- [ ] {a}")
    lines.append("")

    lines.append("## L3 质量自检")
    lines.append("- [ ] 幽灵链接检测覆盖所有MOC文件")
    lines.append("- [ ] 孤儿检测包含所有索引文件的引用源")
    lines.append("- [ ] 升级候选判断基于实际引用频率而非猜测")
    lines.append("")

    lines.append("## L4 飞轮反思")
    lines.append("- 本周最需要人工判断的发现：")
    lines.append("- 知识库增长 vs 腐烂的趋势：")
    lines.append("- 下次扫描可以改进的地方：")

    lines.append(f"\n---\n飞轮自动运行 | {now}")
    return "\n".join(lines)


# ============================================================
# 主入口
# ============================================================

def main():
    is_dry_run = "--dry-run" in sys.argv

    print("🔍 扫描中...")
    ghosts = find_ghost_links()
    orphans = find_orphan_cards()
    candidates = find_upgrade_candidates()
    stale_specs = check_spec_freshness()

    report = build_report(ghosts, orphans, candidates, stale_specs, is_dry_run)

    ghost_count = len(ghosts)
    orphan_count = len(orphans)
    candidate_count = len(candidates)
    total_issues = ghost_count + orphan_count + len(stale_specs)

    if is_dry_run:
        print(report)
        print(f"\n--- DRY RUN | {total_issues} 项待处理 ---")
        return

    emoji = "✅" if total_issues == 0 else "⚠️"
    title = f"知识库飞轮 {emoji} {total_issues}项"
    success = push_to_wechat(title, report)
    if success:
        print(f"推送成功 | 👻{ghost_count} 🃏{orphan_count} ⬆️{candidate_count} 🦠{len(stale_specs)}")
    else:
        print("推送失败")
        print(report)


if __name__ == "__main__":
    main()
