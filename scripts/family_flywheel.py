#!/usr/bin/env python3
"""
family_flywheel.py — 家庭支持自进化飞轮

扫描家庭四维度：关系清晰度 → 执行进度 → 风险预警 → 系统进化
覆盖：子女考研支持 + 两位母亲赡养 + 配偶关系 + 家庭财务

用法:
  python3 family_flywheel.py           # 扫描+微信推送
  python3 family_flywheel.py --dry-run # 只打印报告
"""

import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

DELIVERABLES = Path("/Users/cyingfang/claude/deliverables")
FAMILY_DIR = DELIVERABLES / "family"
SCRIPTS_DIR = Path("/Users/cyingfang/claude/scripts")


# ============================================================
# 维度1：关系清晰度 — L1 人与AI/家庭角色关系
# ============================================================

def assess_关系清晰度() -> dict:
    evidence = {"level": "模糊", "signals": [], "gaps": []}

    # 检查核心文档是否存在
    plan = FAMILY_DIR / "子女成长/子女成长支持计划.md"
    ops = FAMILY_DIR / "子女成长/子女成长支持操作手册.md"
    elder = FAMILY_DIR / "赡养/赡养提醒系统_20260528.md"
    june = FAMILY_DIR / "考研支持/家庭6月执行脚本_20260528.md"
    summer = FAMILY_DIR / "考研支持/考研暑假执行计划.md"

    checks = [
        (plan, "子女成长支持计划"),
        (ops, "子女成长支持操作手册"),
        (elder, "赡养提醒系统"),
        (june, "家庭6月执行脚本"),
        (summer, "考研暑假执行计划"),
    ]

    found = 0
    for path, name in checks:
        if path.exists():
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
            days = (datetime.now() - mtime).days
            if days <= 14:
                evidence["signals"].append(f"✅ {name} — {days}天前更新")
            else:
                evidence["signals"].append(f"⚠️ {name} — {days}天未更新")
            found += 1
        else:
            evidence["gaps"].append(f"{name} 缺失")

    # 检查四大维度覆盖
    plan_content = plan.read_text(encoding="utf-8") if plan.exists() else ""
    dimensions = ["子女", "考研", "赡养", "配偶", "家庭财务"]
    covered = [d for d in dimensions if d in plan_content]
    evidence["signals"].append(f"四大维度覆盖：{len(covered)}/5 ({', '.join(covered)})")

    if len(covered) < 4:
        evidence["gaps"].append(f"家庭计划缺少维度：{set(dimensions) - set(covered)}")

    # 综合判断
    if found >= 4 and len(covered) >= 4:
        evidence["level"] = "清晰"
    elif found >= 2:
        evidence["level"] = "部分清晰"
    else:
        evidence["level"] = "模糊"

    return evidence


# ============================================================
# 维度2：执行进度 — L2 指令层
# ============================================================

def assess_执行进度() -> dict:
    evidence = {"level": "滞后", "signals": [], "gaps": [], "actions": []}

    june_script = FAMILY_DIR / "考研支持/家庭6月执行脚本_20260528.md"
    if not june_script.exists():
        evidence["gaps"].append("6月执行脚本缺失——无执行基准")
        return evidence

    content = june_script.read_text(encoding="utf-8")

    total_checks = content.count("[ ]")
    completed = content.count("[x]")
    total = total_checks + completed
    pct = completed / total * 100 if total > 0 else 0

    evidence["signals"].append(f"6月执行项：{completed}/{total} 完成 ({pct:.0f}%)")

    # 检查当前在6月中的位置
    now = datetime.now()
    if now.month == 6:
        if now.day <= 7:
            week_label = "Week 1"
        elif now.day <= 14:
            week_label = "Week 2"
        elif now.day <= 21:
            week_label = "Week 3"
        else:
            week_label = "Week 4+"
        evidence["signals"].append(f"当前：6月{now.day}日（{week_label}）")
    else:
        week_label = "6月未开始"
        evidence["signals"].append(f"当前：{now.month}月{now.day}日（6月执行脚本尚未进入执行窗口）")

    # 检测紧急未完成项
    urgent_keywords = ["联系", "确认", "报班", "暑假起始", "端午"]
    urgent_unchecked = []
    for kw in urgent_keywords:
        for line in content.split("\n"):
            if kw in line and "[ ]" in line:
                urgent_unchecked.append(line.strip())
                break

    if urgent_unchecked:
        evidence["gaps"].append(f"{len(urgent_unchecked)}项紧急行动未完成")
        evidence["actions"] = urgent_unchecked[:3]

    # 检查赡养提醒系统
    elder_file = FAMILY_DIR / "赡养/赡养提醒系统_20260528.md"
    if elder_file.exists():
        elder_content = elder_file.read_text(encoding="utf-8")
        elder_checks = elder_content.count("[ ]")
        elder_done = elder_content.count("[x]")
        evidence["signals"].append(f"赡养提醒项：{elder_done}/{elder_checks + elder_done} 已配置")

    # 检查暑假执行计划新鲜度
    summer_plan = FAMILY_DIR / "考研支持/考研暑假执行计划.md"
    if summer_plan.exists():
        summer_mtime = datetime.fromtimestamp(summer_plan.stat().st_mtime)
        summer_days = (datetime.now() - summer_mtime).days
        if summer_days > 30:
            evidence["gaps"].append(f"暑假执行计划{summer_days}天未更新——临近暑假需检查")
        else:
            evidence["signals"].append(f"✅ 暑假执行计划 {summer_days}天前更新")

    # 进度判断
    if now.month < 6:
        evidence["level"] = "就绪"  # 6月尚未开始，已有执行脚本=就绪状态
    elif pct >= 0.8:
        evidence["level"] = "超前"
    elif pct >= 0.3:
        evidence["level"] = "按计划"
    elif total > 0 and completed > 0:
        evidence["level"] = "按计划"
    else:
        evidence["level"] = "滞后"

    return evidence


# ============================================================
# 维度3：风险预警 — L3 质量层
# ============================================================

def assess_风险预警() -> dict:
    evidence = {"level": "正常", "signals": [], "gaps": [], "risks": []}

    now = datetime.now()
    risks_detected = []

    # 风险1：暑假窗口逼近 — 6月是启动前最后准备月
    june_script = FAMILY_DIR / "考研支持/家庭6月执行脚本_20260528.md"
    if june_script.exists():
        content = june_script.read_text(encoding="utf-8")
        # 检查"确认期末考试结束日期"是否完成
        if "[ ]" in content and "期末考试" in content:
            risks_detected.append(("⚠️ 考研启动窗口", "尚未确认陈于东期末考试结束日期——暑假时间表v2.0无法生成", "本周内微信联系陈于东"))

    # 风险2：端午节点 — 6月端午节（约6/19前后）
    if now.month == 6 and now.day < 20:
        elder_file = FAMILY_DIR / "赡养/赡养提醒系统_20260528.md"
        if elder_file.exists():
            elder_content = elder_file.read_text(encoding="utf-8")
            if "端午" in elder_content and "[ ]" in elder_content:
                risks_detected.append(("⚠️ 端午赡养", "端午节点临近——保健品/礼品待采购，回乡计划待确认", "本周内下单保健品+确认回乡安排"))

    # 风险3：文件新鲜度
    for path, label in [
        (FAMILY_DIR / "子女成长/子女成长支持计划.md", "子女成长支持计划"),
        (FAMILY_DIR / "赡养/赡养提醒系统_20260528.md", "赡养提醒系统"),
    ]:
        if path.exists():
            days = (now - datetime.fromtimestamp(path.stat().st_mtime)).days
            if days > 30:
                risks_detected.append(("📋 文档陈旧", f"{label} {days}天未更新——信息可能已过时", "安排一次更新检查"))

    # 风险4：配偶关系 — 无显式追踪
    plan = FAMILY_DIR / "子女成长/子女成长支持计划.md"
    if plan.exists():
        plan_text = plan.read_text(encoding="utf-8")
        if "配偶" not in plan_text or plan_text.count("配偶") < 3:
            risks_detected.append(("📋 配偶关系", "家庭计划中配偶维度内容不足——可能被忽略", "在家庭计划中增加配偶关系维护的具体行动"))

    if risks_detected:
        for item in risks_detected:
            evidence["risks"].append({"label": item[0], "detail": item[1], "action": item[2]})
        evidence["signals"].append(f"检测到 {len(risks_detected)} 项风险")
        critical = [r for r in risks_detected if r[0].startswith("⚠️")]
        if critical:
            evidence["level"] = "需关注"
            evidence["gaps"].append(f"{len(critical)}项紧急风险需本周处理")
        else:
            evidence["level"] = "轻度关注"
    else:
        evidence["signals"].append("✅ 未检测到家庭风险信号")
        evidence["level"] = "正常"

    return evidence


# ============================================================
# 维度4：系统进化 — L4 进化层
# ============================================================

def assess_系统进化() -> dict:
    evidence = {"level": "起步", "signals": [], "gaps": []}

    # 检查支持系统完备度
    systems = {
        "考研AI辅助系统": FAMILY_DIR / "考研支持/考研AI辅助系统_启动包.md",
        "错题库": FAMILY_DIR / "考研支持/考研AI辅助系统_错题库.md",
        "进度周报模板": FAMILY_DIR / "考研支持/考研AI辅助系统_进度周报.md",
        "赡养提醒系统": FAMILY_DIR / "赡养/赡养提醒系统_20260528.md",
        "家庭AI工具推荐": FAMILY_DIR / "家庭AI/AI工具推荐_家庭场景_20260527.md",
        "家庭AI支持方案": FAMILY_DIR / "家庭AI/家庭AI支持方案_20260527.md",
        "大学生朋友圈手册": FAMILY_DIR / "考研支持/大学生朋友圈手册_20260528.md",
        "大学生人脉资源手册": FAMILY_DIR / "考研支持/大学生人脉资源手册_20260528.md",
    }

    built = 0
    stale = 0
    for name, path in systems.items():
        if path.exists():
            days = (datetime.now() - datetime.fromtimestamp(path.stat().st_mtime)).days
            if days <= 30:
                built += 1
            else:
                stale += 1
                evidence["gaps"].append(f"{name} {days}天未更新")

    evidence["signals"].append(f"支持系统：{built}/{len(systems)} 活跃")
    if stale > 0:
        evidence["signals"].append(f"⚠️ {stale}个系统超过30天未更新")

    # 检查飞轮本身是否在cron中
    tasks_json = Path("/Users/cyingfang/claude/.claude/scheduled_tasks.json")
    if tasks_json.exists():
        import json
        tasks = json.loads(tasks_json.read_text(encoding="utf-8"))
        flywheel_ids = [t["id"] for t in tasks.get("tasks", [])]
        if "family-flywheel-001" in flywheel_ids:
            evidence["signals"].append("✅ 家庭飞轮已配置定时任务")
        else:
            evidence["gaps"].append("家庭飞轮尚未配置定时任务")

    # 综合判断
    if built >= 6 and stale == 0:
        evidence["level"] = "成熟"
    elif built >= 4:
        evidence["level"] = "建设中"
    else:
        evidence["level"] = "起步"

    return evidence


# ============================================================
# 飞轮联动判断
# ============================================================

def 联动判断(关系: dict, 进度: dict, 风险: dict, 系统: dict) -> tuple:
    real_gaps = []
    for d in [关系, 进度, 风险, 系统]:
        real_gaps.extend(d.get("gaps", []))

    now = datetime.now()
    关系_lvl = 关系.get("level", "")
    进度_lvl = 进度.get("level", "")
    风险_lvl = 风险.get("level", "")
    系统_lvl = 系统.get("level", "")

    # 6种状态决策
    if "模糊" in 关系_lvl:
        return ("🔴 方向需校准", "家庭四大维度定义不够清晰", [
            "优先完善子女成长支持计划——确认陈于东考研目标院校和专业方向",
            "补充配偶关系维护的具体行动（目前文档中配偶内容偏少）",
            "补全两位母亲的健康档案（缺少精确出生年份/住址/基础病史）",
        ])

    if "滞后" in 进度_lvl:
        actions = 进度.get("actions", [])
        if now.month < 6:
            return ("✅ 6月就绪", "执行脚本已到位，等待6月启动窗口", [
                "在6月1日前完成：确认陈于东期末考试日期 + 两位母亲端午问候准备",
                "6月Week 1重点：暑假起始日确认 + 目标沟通 + 时间表v2.0",
                "赡养系统：检查两位母亲通讯方式+紧急联系人是否已配置",
            ])
        return ("⚠️ 执行滞后", "6月执行项推进不够，暑假窗口在逼近", [
            f"本周P0：{actions[0][:80] if actions else '联系陈于东确认期末考试日期'}",
            "6月是暑假启动前最后一公里——确认暑假起始日+报班窗口+英语启动包",
            "端午节点逼近（6/19前后）——保健品采购+回乡确认",
        ])

    if "需关注" in 风险_lvl:
        risk_items = 风险.get("risks", [])
        risk_desc = "、".join([r["label"] for r in risk_items[:2]]) if risk_items else "未知风险"
        actions = [r["action"] for r in risk_items[:3]] if risk_items else ["排查风险来源"]
        return ("⚠️ 风险预警", f"检测到家庭风险：{risk_desc}", actions)

    if "起步" in 系统_lvl:
        return ("📝 系统待建", "家庭支持系统还在起步阶段", [
            "补齐考研AI辅助系统的实际使用数据（陈于东是否已在用DeepSeek+墨墨背单词？）",
            "启用赡养提醒系统的定时推送（每周视频提醒+每月转账提醒）",
            "建立配偶关系维护的定期行动项（非节日也有的日常维护）",
        ])

    if len(real_gaps) == 0:
        return ("✅ 飞轮正常运转", "家庭四维无实质性缺口", [
            "维护当前节奏：每周进度更新+月度健康关注+节日节点提醒",
            "关注6月→7月过渡——暑假启动后切换为'考研暑假支持模式'",
            "端午节点（6/19前后）：保健品+回乡+视频问候两位母亲",
        ])

    if len(real_gaps) <= 3:
        return ("🟡 有小缺口", f"{len(real_gaps)}项缺口", [
            f"优先补：{real_gaps[0][:80]}",
            "不影响整体家庭支持质量，但补齐后系统更完备",
        ])

    return ("🔴 飞轮卡住", f"{len(real_gaps)}项缺口，家庭飞轮未正常运转", [
        f"本周从关系清晰度开始排查：{real_gaps[0][:80]}",
        f"下周继续：{real_gaps[1][:80] if len(real_gaps) > 1 else '排查下一项'}",
    ])


# ============================================================
# 汇总报告
# ============================================================

def build_report(assessments: dict, flywheel: tuple) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    状态, 诊断, 行动 = flywheel

    lines = [
        f"# 🏠 家庭支持飞轮 | {now}",
        f"> 四维联动：{状态} — {诊断}\n",
    ]

    lines.append("## 飞轮判断")
    lines.append(f"**{状态}**：{诊断}")
    lines.append("")
    for a in 行动:
        lines.append(f"- [ ] {a}")
    lines.append("")

    layers = [
        ("关系清晰度", "🎯", "L1 角色与目标", "四大维度定义+文档完整度"),
        ("执行进度", "📊", "L2 行动推进", "6月执行项+赡养提醒+暑假准备"),
        ("风险预警", "⚠️", "L3 风险检测", "考研窗口/端午节点/文档新鲜度"),
        ("系统进化", "🔄", "L4 支持系统", "AI辅助系统+提醒系统+工具覆盖"),
    ]

    for layer_name, icon, method_layer, desc in layers:
        data = assessments.get(layer_name, {})
        lines.append(f"## {icon} {layer_name} — {desc}")
        lines.append(f"**等级：{data.get('level', '未知')}** | 方法论层：{method_layer}")
        for s in data.get("signals", []):
            lines.append(f"- {s}")
        for g in data.get("gaps", []):
            lines.append(f"- ❌ {g}")
        if data.get("risks"):
            for r in data["risks"]:
                lines.append(f"- {r['label']}：{r['detail']} → {r['action']}")
        lines.append("")

    # 下周预测
    lines.append("## 📅 下周关键节点")
    now_dt = datetime.now()
    next_week = now_dt + timedelta(days=7)
    if now_dt.month == 5 and now_dt.day >= 25:
        lines.append("- 🎓 **期末窗口**：联系陈于东确认期末考试日期——暑假起始日")
    if (now_dt.month == 6 and now_dt.day < 20) or (now_dt.month == 5 and now_dt.day >= 25):
        lines.append("- 🎋 **端午节点准备**（约6/19）：保健品采购+回乡确认+两位母亲视频")
    if now_dt.month == 6 and now_dt.day >= 15:
        lines.append("- 📚 **暑假启动**：切换为考研暑假支持模式——启动英语+数学第1周计划")
    elif now_dt.month == 5:
        lines.append("- 📚 **暑假准备**：英语启动包+专业课路线图提前就位")
    lines.append("- 💬 **每周视频**：两位母亲各一次，听日常、关注健康")

    lines.append(f"\n---\n家庭飞轮自动运行 | {now}")
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

    print("🏠 扫描家庭支持飞轮四维...")
    assessments = {
        "关系清晰度": assess_关系清晰度(),
        "执行进度": assess_执行进度(),
        "风险预警": assess_风险预警(),
        "系统进化": assess_系统进化(),
    }

    flywheel = 联动判断(
        assessments["关系清晰度"],
        assessments["执行进度"],
        assessments["风险预警"],
        assessments["系统进化"],
    )
    report = build_report(assessments, flywheel)

    if is_dry_run:
        print(report)
        return

    状态, _, _ = flywheel
    if "正常" in 状态:
        emoji = "✅"
    elif "小缺口" in 状态 or "待建" in 状态:
        emoji = "🟡"
    elif "预警" in 状态 or "滞后" in 状态:
        emoji = "⚠️"
    else:
        emoji = "🔴"
    title = f"🏠 家庭飞轮 {emoji} {状态}"
    success = push_to_wechat(title, report)
    if success:
        print(f"推送成功 | {状态}")
    else:
        print("推送失败")
        print(report)


if __name__ == "__main__":
    main()
