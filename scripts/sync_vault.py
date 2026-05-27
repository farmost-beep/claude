#!/usr/bin/env python3
"""补齐 Obsidian Vault 6goals 中缺失的 deliverable 链接文件

只创建 VAULT 中完全不存在的文件，不修改已有文件。
用法: python3 scripts/sync_vault.py [--dry-run]
"""

import os, re, sys

VAULT = os.path.expanduser("~/Documents/Obsidian Vault 6goals")
DELIVERABLES = os.path.expanduser("~/claude/deliverables")

GOAL_MAP = {
    "investment": "01-投资成功",
    "career": "02-事业进阶",
    "family": "03-家庭支持",
    "health": "04-百岁健康",
    "ai": "05-AI能力",
    "knowledge-base": "06-知识库",
}

def get_one_liner(md_path):
    with open(md_path) as f:
        lines = f.readlines()
    for line in lines:
        s = line.strip()
        if s.startswith(">"):
            return s.lstrip("> ").strip()
        if s.startswith("# ") and len(s) > 2:
            return s[2:].strip()
    return ""

def build_link(md_path):
    """创建指向 deliverables 的 Obsidian 链接文件内容"""
    rel = os.path.relpath(md_path, os.path.dirname(DELIVERABLES))
    one = get_one_liner(md_path)
    lines = [f"---", f'link: "../deliverables/{rel}"', "---", "", f"> {one}", ""]
    return "\n".join(lines)

def vault_path(goal_folder, name):
    return os.path.join(VAULT, goal_folder, f"{name}.md")

def guess_vault_name(name):
    """将 deliverable 文件名映射为 vault 可能使用的文件名"""
    # e.g., "巴菲特_护城河与能力圈_20260528" → may exist as "大师-巴菲特"
    # Strip date suffixes
    base = re.sub(r'_\d{8}$', '', name)
    base = re.sub(r'^.*?_', '', base)  # strip prefix
    return base

def exists_in_vault(goal_folder, name, md_path):
    """检查 vault 中是否存在该文件（包括名称变体）"""
    exact = vault_path(goal_folder, name)
    if os.path.exists(exact):
        return True
    # Check basename matching
    base = guess_vault_name(name)
    vdir = os.path.join(VAULT, goal_folder)
    if not os.path.isdir(vdir):
        return False
    for f in os.listdir(vdir):
        if f.endswith(".md") and base in f:
            return True
    return False

def sync_folder(goal, goal_folder, dry_run=False):
    """同步一个目标领域的新文件到 vault"""
    src_dir = os.path.join(DELIVERABLES, goal)
    if not os.path.isdir(src_dir):
        return 0

    count = 0
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            if not f.endswith(".md"):
                continue
            name = f[:-3]
            md_path = os.path.join(root, f)
            vf = vault_path(goal_folder, name)

            if os.path.exists(vf):
                continue  # 已有 → 跳过
            if exists_in_vault(goal_folder, name, md_path):
                continue  # 变体名已有 → 跳过

            # 真正缺失
            if dry_run:
                print(f"  [NEW] {goal}/{name} →  {goal_folder}/{name}.md")
            else:
                os.makedirs(os.path.dirname(vf), exist_ok=True)
                with open(vf, "w") as fh:
                    fh.write(build_link(md_path))
                print(f"  [NEW] {goal}/{name}")
            count += 1
    return count

def main():
    dry_run = "--dry-run" in sys.argv
    total = 0

    label = "[DRY RUN] " if dry_run else ""
    print(f"{label}补齐 Obsidian Vault 缺失链接\n")

    for goal, gf in sorted(GOAL_MAP.items()):
        n = sync_folder(goal, gf, dry_run)
        if n:
            print(f"  {goal} → {gf}: {n} new")
        total += n

    # Root-level files → 00-MOC
    moc_dir = os.path.join(VAULT, "00-MOC")
    for f in os.listdir(DELIVERABLES):
        if not f.endswith(".md"):
            continue
        name = f[:-3]
        md_path = os.path.join(DELIVERABLES, f)
        if os.path.isfile(md_path):
            vf = os.path.join(moc_dir, f)
            if not os.path.exists(vf) and not exists_in_vault("00-MOC", name, md_path):
                if dry_run:
                    print(f"  [NEW] 00-MOC/{name}")
                else:
                    os.makedirs(moc_dir, exist_ok=True)
                    with open(vf, "w") as fh:
                        fh.write(build_link(md_path))
                    print(f"  [NEW] 00-MOC/{name}")
                total += 1

    if total == 0:
        print("All vault files are up to date.")
    else:
        print(f"\n{total} files {'would be' if dry_run else ''} added to vault.")


if __name__ == "__main__":
    main()
