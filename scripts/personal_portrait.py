#!/usr/bin/env python3
"""
personal_portrait.py — 周度个人画像生成器

每周汇聚六维度数据，生成一份2分钟可扫完的快照画像。
含：六维红绿灯、关键信号、本周行动、下周预警。

用法:
  python3 personal_portrait.py           # 扫描+微信推送
  python3 personal_portrait.py --dry-run # 只打印画像
"""

import subprocess
import sys
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

DELIVERABLES = Path("/Users/cyingfang/claude/deliverables")
SCRIPTS_DIR = Path("/Users/cyingfang/claude/scripts")
HEALTH_DATA = DELIVERABLES / "health" / "健康数据" / "health_data.json"
VAULT = Path("/Users/cyingfang/Documents/Obsidian Vault 6goals")
CARDS_DIR = VAULT / "06-知识库" / "知识卡片"
MOC_DIR = VAULT / "00-MOC"
MEMORY_DIR = Path("/Users/cyingfang/.claude/projects/-Users-cyingfang-claude/memory")

SIX_DIMS = ["投资成功", "事业进阶", "家庭支持", "百岁健康", "AI能力", "知识库"]


# ============================================================
# 数据加载
# ============================================================

def load_health_data() -> dict:
    if HEALTH_DATA.exists():
        try:
            return json.loads(HEALTH_DATA.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, KeyError):
            pass
    return {}


def recent_days_from(path: Path) -> Optional[int]:
    """文件最后修改距今多少天，文件不存在返回None"""
    if not path.exists():
        return None
    return (datetime.now() - datetime.fromtimestamp(path.stat().st_mtime)).days


def count_files_mtime_within(dir_path: Path, pattern: str, days: int) -> int:
    """目录下匹配模式且最近N天内修改的文件数"""
    if not dir_path.exists():
        return 0
    cutoff = datetime.now() - timedelta(days=days)
    count = 0
    for f in dir_path.glob(pattern):
        if datetime.fromtimestamp(f.stat().st_mtime) >= cutoff:
            count += 1
    return count


def count_files_total(dir_path: Path, pattern: str) -> int:
    if not dir_path.exists():
        return 0
    return len(list(dir_path.glob(pattern)))


# ============================================================
# 维度评估
# ============================================================

def assess_investment() -> dict:
    """投资成功：组合健康度+行为纪律+还本进度"""
    signals, gaps = [], []

    # 检查持仓分析文件
    持仓文件 = DELIVERABLES / "持仓分析与操作建议_20260528.md"
    age = recent_days_from(持仓文件)

    if age is not None and age <= 7:
        signals.append(f"持仓分析文件{age}天前更新")
    elif age is not None:
        gaps.append(f"持仓分析已{age}天未更新——需刷新")
    else:
        gaps.append("无持仓分析文件")

    # 投资决策日志
    日志文件 = DELIVERABLES / "投资决策日志.md"
    log_age = recent_days_from(日志文件)
    if log_age is not None and log_age <= 7:
        signals.append(f"投资日志{log_age}天内有更新")
    else:
        gaps.append("投资决策日志超7天无新记录")

    # 检查投资飞轮最近运行
    飞轮 = recent_days_from(Path("/Users/cyingfang/claude/scripts/investment_flywheel.py"))
    if 飞轮 is None or 飞轮 > 7:
        gaps.append("投资飞轮超7天未运行")

    # 异常日志
    异常日志 = DELIVERABLES / "ai" / "执行与简报" / "AI异常日志.md"
    if 异常日志.exists():
        signals.append("AI异常日志已建立，Agent E交叉验证就绪")

    # 量化脚本
    策略目录 = Path("/Users/cyingfang/claude/策略研究")
    scripts_count = count_files_total(策略目录, "*.py")
    if scripts_count >= 3:
        signals.append(f"量化工具{scripts_count}个脚本可用")

    level = "🟢 正常"
    if len(gaps) >= 3:
        level = "🔴 需关注"
    elif len(gaps) >= 1:
        level = "🟡 待完善"

    return {"level": level, "signals": signals, "gaps": gaps}


def assess_career() -> dict:
    """事业进阶：文章产出+考试进度+网络活跃度"""
    signals, gaps = [], []

    # 公众号文章
    发表目录 = DELIVERABLES / "career" / "发表文章"
    total_articles = count_files_total(发表目录, "公众号文章_*.md")
    recent_articles = count_files_mtime_within(发表目录, "公众号文章_*.md", 7)
    if total_articles > 0:
        signals.append(f"公众号文章{total_articles}篇已就绪（近7天产出{recent_articles}篇）")
    else:
        gaps.append("尚无公众号文章")

    # AI方法论系列
    ai_method_articles = count_files_total(发表目录, "*AI方法论*.md") + count_files_total(发表目录, "*AI能力*.md") + count_files_total(发表目录, "*Agent*.md") + count_files_total(发表目录, "*Claude*.md") + count_files_total(发表目录, "*AGI*.md") + count_files_total(发表目录, "*协作*.md") + count_files_total(发表目录, "*组织*.md") + count_files_total(发表目录, "*知识库*.md") + count_files_total(发表目录, "*注意力*.md") + count_files_total(发表目录, "*管理模式*.md") + count_files_total(发表目录, "*投资管理*.md") + count_files_total(发表目录, "*操作系统*.md") + count_files_total(发表目录, "*演绎*.md") + count_files_total(发表目录, "*逆向*.md") + count_files_total(发表目录, "*国内*.md") + count_files_total(发表目录, "*产品*.md") + count_files_total(发表目录, "*未来*.md") + count_files_total(发表目录, "*一年后*.md")

    # More accurate: count AI方法论 related articles
    ai_articles = total_articles - 3  # minus the 3 科技金融 articles
    if ai_articles >= 7:
        signals.append(f"AI方法论系列已产出≥{ai_articles}篇")
    elif ai_articles > 0:
        signals.append(f"AI方法论系列{ai_articles}篇")

    # 科技金融系列
    techfin_articles = count_files_total(发表目录, "*科技金融*.md") + count_files_total(发表目录, "*含科量*.md") + count_files_total(发表目录, "*万亿*.md")
    if techfin_articles >= 3:
        signals.append("科技金融三部曲已就绪")
    elif techfin_articles > 0:
        signals.append(f"科技金融系列{techfin_articles}篇")
    else:
        gaps.append("科技金融系列尚未产出")

    # 中级经济师备考
    备考计划 = DELIVERABLES / "career" / "民建与职称" / "中级经济师备考计划_20260528.md"
    if 备考计划.exists():
        plan_age = recent_days_from(备考计划)
        signals.append(f"备考计划已制定（{plan_age}天前更新）")
    else:
        gaps.append("中级经济师备考计划缺失")

    # 民建建言
    建言文件 = DELIVERABLES / "career" / "民建与职称" / "民建社情民意-并购贷款与科创金融生态_提交版.md"
    if 建言文件.exists():
        signals.append("民建建言提交版已就绪")

    # 网络经营（三重网络）
    网络产出 = count_files_mtime_within(DELIVERABLES / "career", "*.md", 14)
    if 网络产出 >= 3:
        signals.append(f"事业产出近2周{网络产出}份文件")

    level = "🟢 正常"
    if len(gaps) >= 3:
        level = "🔴 需关注"
    elif len(gaps) >= 1:
        level = "🟡 待完善"

    return {"level": level, "signals": signals, "gaps": gaps}


def assess_family() -> dict:
    """家庭支持：考研准备+赡养提醒+子女成长"""
    signals, gaps = [], []

    # 考研准备
    考研文件 = [
        DELIVERABLES / "family" / "考研支持" / "考研AI辅助系统_进度周报.md",
        DELIVERABLES / "family" / "考研支持" / "考研AI辅助系统_错题库.md",
        DELIVERABLES / "family" / "考研支持" / "考研暑假执行计划.md",
        DELIVERABLES / "family" / "考研支持" / "上海大学考研完全手册_20260527.md",
    ]
    考研就绪 = sum(1 for f in 考研文件 if f.exists())
    if 考研就绪 >= 4:
        signals.append(f"考研AI辅助系统4件套已就绪")
    elif 考研就绪 > 0:
        signals.append(f"考研准备{考研就绪}/4件就绪")
    else:
        gaps.append("考研准备文件缺失")

    # 暑假计划确认
    暑假计划 = DELIVERABLES / "family" / "考研支持" / "考研暑假执行计划.md"
    if 暑假计划.exists():
        plan_age = recent_days_from(暑假计划)
        if plan_age is not None and plan_age <= 14:
            signals.append(f"暑假执行计划{plan_age}天前更新")
        elif plan_age is not None:
            gaps.append(f"暑假执行计划{plan_age}天未更新——需确认暑假起始日")

    # 赡养提醒
    赡养文件 = DELIVERABLES / "family" / "赡养" / "赡养提醒系统_20260528.md"
    if 赡养文件.exists():
        signals.append("赡养提醒系统已建立")

    # 子女成长
    子女文件 = DELIVERABLES / "family" / "子女成长" / "子女成长支持计划.md"
    if 子女文件.exists():
        signals.append("子女成长支持计划已建立")

    # 家庭执行计划
    家庭执行 = DELIVERABLES / "family" / "家庭6月执行脚本_20260528.md"
    if 家庭执行.exists():
        signals.append("家庭6月执行脚本已制定")

    level = "🟢 正常"
    if len(gaps) >= 2:
        level = "🟡 待推动"
    elif len(gaps) >= 1:
        level = "🟢 基本正常"

    return {"level": level, "signals": signals, "gaps": gaps}


def assess_health() -> dict:
    """百岁健康：输入层+过程层+P0行动"""
    signals, gaps = [], []
    data = load_health_data()

    records = data.get("daily_records", [])
    recent = records[-7:] if records else []

    # 步数
    if recent:
        avg_steps = sum(r.get("steps", 0) for r in recent) / len(recent)
        days_over_8k = sum(1 for r in recent if r.get("steps", 0) >= 8000)
        signals.append(f"近{len(recent)}天日均{avg_steps:.0f}步 | ≥8000步 {days_over_8k}/{len(recent)}天")
        if avg_steps < 8000:
            gaps.append(f"日均步数不足（{avg_steps:.0f} < 8000）")
    else:
        gaps.append("无步数数据")

    # 睡眠
    if recent:
        avg_sleep = sum(r.get("sleep_hours", 0) for r in recent) / len(recent)
        signals.append(f"日均睡眠{avg_sleep:.1f}h")
        if avg_sleep < 7:
            gaps.append(f"睡眠不足（{avg_sleep:.1f}h < 7h）")

    # 饮水
    if recent:
        avg_water = sum(r.get("water_liters", 0) for r in recent) / len(recent)
        signals.append(f"日均饮水{avg_water:.1f}L")
        if avg_water < 2.0:
            gaps.append(f"饮水不足（{avg_water:.1f}L < 2.0L）")

    # P0医疗行动
    p0_actions = data.get("p0_actions", {})
    P0_ITEMS = [
        "购买血压计", "内分泌科就诊", "泌尿外科就诊",
        "肠镜+胃镜", "启动降脂饮食", "眼科验光配镜",
        "血管外科评估", "牙科检查",
    ]
    p0_done = sum(1 for a in P0_ITEMS if p0_actions.get(a) == "✅")
    p0_total = len(P0_ITEMS)
    if p0_done >= p0_total:
        signals.append(f"P0医疗行动全部完成（{p0_done}/{p0_total}）")
    elif p0_done >= 5:
        signals.append(f"P0行动{p0_done}/{p0_total}已完成，剩余P1项")
    else:
        gaps.append(f"P0医疗行动仅{p0_done}/{p0_total}完成")

    # 记录天数
    if len(records) >= 7:
        signals.append(f"健康数据记录{len(records)}天，持续追踪中")
    elif len(records) > 0:
        gaps.append(f"健康数据仅{len(records)}天记录——需持续记录")

    level = "🟢 达标"
    if len(gaps) >= 3:
        level = "🔴 需关注"
    elif len(gaps) >= 1:
        level = "🟡 待改善"

    return {"level": level, "signals": signals, "gaps": gaps}


def assess_ai_capability() -> dict:
    """AI能力：五维度等级+雷达报告+学习执行"""
    signals, gaps = [], []

    # 雷达周报
    雷达文件 = DELIVERABLES / "ai" / "AI能力雷达周报_2026W22.md"
    radar_age = recent_days_from(雷达文件)
    if radar_age is not None and radar_age <= 7:
        signals.append(f"AI能力雷达周报{radar_age}天前更新")
    elif radar_age is not None:
        gaps.append(f"雷达周报已{radar_age}天未更新")
    else:
        gaps.append("尚无AI能力雷达周报")

    # AI执行包
    执行包 = DELIVERABLES / "ai" / "AI能力6月执行包.md"
    if 执行包.exists():
        signals.append("AI能力6月执行包已制定")

    # Claude Code手册
    手册数 = count_files_total(DELIVERABLES / "ai" / "Claude_Code", "*.md")
    if 手册数 >= 3:
        signals.append(f"Claude Code手册{手册数}份")

    # AI产物计数
    ai_output_count = count_files_mtime_within(DELIVERABLES / "ai", "*.md", 7)
    signals.append(f"近7天AI相关产出{ai_output_count}份")

    # 规范更新
    规范文件 = DELIVERABLES / "记忆规范" / "AI能力雷达周报模板.md"
    if 规范文件.exists():
        signals.append("AI能力雷达模板已建立")

    level = "🟢 正常"
    if len(gaps) >= 2:
        level = "🟡 待提升"
    elif len(gaps) >= 1:
        level = "🟢 基本正常"

    return {"level": level, "signals": signals, "gaps": gaps}


def assess_knowledge() -> dict:
    """知识库：卡片数+MOC状态+跨域连接"""
    signals, gaps = [], []

    # 知识卡片
    card_count = count_files_total(CARDS_DIR, "*.md")
    if card_count >= 80:
        signals.append(f"知识卡片{card_count}张（≥80目标✅）")
    elif card_count >= 22:
        signals.append(f"知识卡片{card_count}张")
    else:
        gaps.append(f"知识卡片仅{card_count}张")

    # 近期新卡片（用deliverables目录，非Obsidian Vault）
    卡片交付目录 = DELIVERABLES / "knowledge-base" / "知识卡片"
    new_cards = count_files_mtime_within(卡片交付目录, "*.md", 7)
    if new_cards > 0:
        signals.append(f"近7天新增{new_cards}张卡片")

    # MOC（只统计以MOC.md结尾的文件）
    moc_count = count_files_total(MOC_DIR, "*MOC.md")
    if moc_count >= 6:
        signals.append(f"MOC {moc_count}个完整")
    elif moc_count > 0:
        signals.append(f"MOC {moc_count}个")

    # 跨域连接
    升级映射 = VAULT / "06-知识库" / "Layer2到Layer1升级映射.md"
    if 升级映射.exists():
        signals.append("Layer2→Layer1升级映射已建立")

    # Vault同步（递归统计）
    vault_files = sum(1 for _ in VAULT.rglob("*.md"))
    signals.append(f"Obsidian Vault {vault_files}个文件")

    level = "🟢 正常"
    if len(gaps) >= 2:
        level = "🟡 待完善"
    elif len(gaps) >= 1:
        level = "🟢 基本正常"

    return {"level": level, "signals": signals, "gaps": gaps}


# ============================================================
# 整体判断
# ============================================================

def overall_diagnosis(assessments: dict) -> tuple:
    """综合六维度给出整体画像判断"""
    red_dims = []
    yellow_dims = []
    green_dims = []

    for dim, result in assessments.items():
        level = result["level"]
        if "🔴" in level:
            red_dims.append(dim)
        elif "🟡" in level:
            yellow_dims.append(dim)
        else:
            green_dims.append(dim)

    total_gaps = sum(len(a["gaps"]) for a in assessments.values())
    total_signals = sum(len(a["signals"]) for a in assessments.values())

    if len(red_dims) >= 2:
        diagnosis = f"{len(red_dims)}维度红色预警——本周需聚焦解决"
        overall = "🔴 需干预"
    elif len(red_dims) == 1:
        diagnosis = f"{red_dims[0]}亮红灯，其余{len(green_dims)}维度正常"
        overall = "🟡 局部预警"
    elif len(yellow_dims) >= 3:
        diagnosis = f"{len(yellow_dims)}维度待完善，节奏尚可"
        overall = "🟡 持续优化"
    elif len(green_dims) >= 5:
        diagnosis = f"{len(green_dims)}/6维度绿灯，系统运转良好"
        overall = "🟢 健康运转"
    else:
        diagnosis = "系统运转中，部分维度待完善"
        overall = "🟢 基本正常"

    return overall, diagnosis, {
        "red": red_dims, "yellow": yellow_dims, "green": green_dims,
        "total_gaps": total_gaps, "total_signals": total_signals,
    }


# ============================================================
# 画像报告构建
# ============================================================

def build_portrait(assessments: dict, diagnosis_result: tuple) -> str:
    now = datetime.now()
    week_num = now.isocalendar()[1]
    overall, diagnosis, detail = diagnosis_result

    lines = [
        f"# 🧬 陈颖芳 | 周度个人画像",
        f"> W{week_num} | {now.strftime('%Y-%m-%d %H:%M')}",
        f"> **{overall}** — {diagnosis}",
        "",
    ]

    # ---- 六维红绿灯 ----
    lines.append("## 📊 六维度快照")
    lines.append("")
    lines.append("| 维度 | 状态 | 绿灯信号 | 需关注 |")
    lines.append("|:---|:---:|:---|:---|")
    for dim in SIX_DIMS:
        a = assessments[dim]
        emoji = "🟢" if "🟢" in a["level"] else "🟡" if "🟡" in a["level"] else "🔴"
        top_signal = a["signals"][0] if a["signals"] else "—"
        top_gap = a["gaps"][0] if a["gaps"] else "✅ 无"
        lines.append(f"| {dim} | {emoji} | {top_signal} | {top_gap} |")
    lines.append("")

    # ---- 各维度详情 ----
    dim_labels = {
        "投资成功": "💰 投资成功",
        "事业进阶": "🏛 事业进阶",
        "家庭支持": "🏠 家庭支持",
        "百岁健康": "💪 百岁健康",
        "AI能力": "🤖 AI能力",
        "知识库": "📚 知识库",
    }

    for dim in SIX_DIMS:
        a = assessments[dim]
        label = dim_labels.get(dim, dim)
        lines.append(f"## {label} — {a['level']}")
        for s in a["signals"]:
            lines.append(f"- ✅ {s}")
        for g in a["gaps"]:
            lines.append(f"- ❌ {g}")
        lines.append("")

    # ---- 下周预警 ----
    lines.append("## ⚠️ 下周关键预警")
    预警 = []
    for dim in SIX_DIMS:
        a = assessments[dim]
        for g in a["gaps"]:
            预警.append(f"- [{dim}] {g}")
    if not 预警:
        lines.append("- ✅ 六维度无阻塞性预警")
    else:
        # 只列前5条
        for w in 预警[:5]:
            lines.append(w)
    lines.append("")

    # ---- 本周行动建议 ----
    lines.append("## 🎯 本周行动建议")
    lines.append("")

    if detail["red"]:
        lines.append(f"**优先灭火（{len(detail['red'])}维度红色）**：")
        for dim in detail["red"]:
            a = assessments[dim]
            for g in a["gaps"][:2]:
                lines.append(f"- [ ] {g}")
        lines.append("")

    if detail["yellow"]:
        lines.append(f"**持续优化（{len(detail['yellow'])}维度黄色）**：")
        for dim in detail["yellow"]:
            a = assessments[dim]
            for g in a["gaps"][:1]:
                lines.append(f"- [ ] {g}")
        lines.append("")

    # ---- 本周金句 ----
    金句 = [
        "系统胜过目标。胜者建系统，输家设目标。",
        "复利是宇宙最强大的力量——财富、知识、健康、关系，都是日积月累的复利结果。",
        "够好就是最好。每个维度达到满意区间即可，不追求极致。",
        "能量管理 > 时间管理。49岁以后，保护精力比榨取时间更重要。",
        "杠杆思维——用AI撬动效率，用知识撬动判断力，用投资撬动财富，用健康撬动一切。",
    ]
    week_idx = week_num % len(金句)
    金句本周 = 金句[week_idx]
    lines.append(f'> *"{金句本周}"*')
    lines.append("")

    lines.append(f"---")
    lines.append(f"个人画像自动生成 | {now.strftime('%Y-%m-%d %H:%M')} | 下次更新：下周六")

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

    print("🧬 生成周度个人画像...")

    assessments = {
        "投资成功": assess_investment(),
        "事业进阶": assess_career(),
        "家庭支持": assess_family(),
        "百岁健康": assess_health(),
        "AI能力": assess_ai_capability(),
        "知识库": assess_knowledge(),
    }

    diagnosis_result = overall_diagnosis(assessments)
    portrait = build_portrait(assessments, diagnosis_result)

    # 保存画像到文件
    now = datetime.now()
    week_num = now.isocalendar()[1]
    output_dir = DELIVERABLES / "个人画像"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"个人画像_W{week_num}_{now.strftime('%Y%m%d')}.md"
    output_file.write_text(portrait, encoding="utf-8")
    print(f"画像已保存：{output_file}")

    if is_dry_run:
        print(portrait)
        return

    overall, diagnosis, _ = diagnosis_result
    emoji = "🟢" if "🟢" in overall else "🟡" if "🟡" in overall else "🔴"
    title = f"个人画像 {emoji} W{week_num} | {diagnosis}"
    success = push_to_wechat(title, portrait)
    if success:
        print(f"推送成功 | {overall}")
    else:
        print("推送失败")
        print(portrait)


if __name__ == "__main__":
    main()
