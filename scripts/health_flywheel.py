#!/usr/bin/env python3
"""
health_flywheel.py — 百岁健康自进化飞轮

扫描健康三层因果链：输入（运动/睡眠/饮水）→ 过程（腰围/血压）→ P0行动。
对应健康追踪规范 v2.0。

用法:
  python3 health_flywheel.py           # 扫描+微信推送
  python3 health_flywheel.py --dry-run # 只打印报告
"""

from lib.wechat import push_to_wechat
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

DELIVERABLES = Path("/Users/cyingfang/claude/deliverables")
HEALTH_DIR = DELIVERABLES / "health"
SCRIPTS_DIR = Path("/Users/cyingfang/claude/scripts")
HEALTH_DATA = HEALTH_DIR / "健康数据" / "health_data.json"

# 基于百岁健康计划的P0行动清单
P0_ACTIONS = [
    ("购买血压计", "上臂式电子血压计（欧姆龙），不买腕式", "P0"),
    ("内分泌科就诊", "TPO-Ab 178.5↑，右侧甲状腺多发结节，瑞金/华山/中山", "P0"),
    ("泌尿外科就诊", "双肾多发结石+F-PSA/T-PSA 0.20，仁济/华山/长海", "P0"),
    ("肠镜+胃镜", "49岁未筛查已逾期+CA72-4 9.48↑，无痛一次完成", "P0"),
    ("启动降脂饮食", "LDL-C 3.68↑+主动脉钙化，3个月后复查血脂", "P0"),
    ("眼科验光配镜", "右0.5 左0.4，五官科医院或第一人民医院", "P1"),
    ("血管外科评估", "双下肢静脉曲张，中山/仁济血管外科", "P1"),
    ("牙科检查", "如>1年未洗牙，安排牙科预约", "P1"),
]


def load_health_data() -> dict:
    if HEALTH_DATA.exists():
        try:
            return json.loads(HEALTH_DATA.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, KeyError):
            pass
    return {}


def assess_输入层() -> dict:
    evidence = {"level": "数据不足", "signals": [], "gaps": []}
    data = load_health_data()

    # 从 daily_records 读取
    records = data.get("daily_records", [])
    recent = records[-7:] if len(records) > 0 else []

    # 运动 — 步行步数
    if recent:
        avg_steps = sum(r.get("steps", 0) for r in recent) / len(recent)
        days_over_8k = sum(1 for r in recent if r.get("steps", 0) >= 8000)
        evidence["signals"].append(f"近{len(recent)}天日均步数：{avg_steps:.0f}步 | ≥8000步 {days_over_8k}/{len(recent)}天")
        if avg_steps < 8000:
            evidence["gaps"].append(f"日均步数不足（{avg_steps:.0f} < 8000）")
    else:
        evidence["gaps"].append("无步数数据——需开始记录")

    # 睡眠
    if recent:
        avg_sleep = sum(r.get("sleep_hours", 0) for r in recent) / len(recent)
        evidence["signals"].append(f"近{len(recent)}天日均睡眠：{avg_sleep:.1f}h")
        if avg_sleep < 7:
            evidence["gaps"].append(f"睡眠不足（{avg_sleep:.1f}h < 7h）")
        elif avg_sleep >= 7:
            evidence["signals"].append("  ✅ 睡眠达标（≥7h）")
    else:
        evidence["gaps"].append("无睡眠数据——需开始记录")

    # 饮水
    if recent:
        avg_water = sum(r.get("water_liters", 0) for r in recent) / len(recent)
        evidence["signals"].append(f"近{len(recent)}天日均饮水：{avg_water:.1f}L")
        if avg_water < 2.0:
            evidence["gaps"].append(f"饮水不足（{avg_water:.1f}L < 2.0L底线，目标2.5L）")
        elif avg_water < 2.5:
            evidence["signals"].append(f"  ⚠️ 饮水接近底线，距目标2.5L差{2.5 - avg_water:.1f}L")
        else:
            evidence["signals"].append("  ✅ 饮水达标（≥2.5L）")
    else:
        evidence["gaps"].append("无饮水数据——需开始记录")

    # 整体判断
    gap_count = len(evidence["gaps"])
    if gap_count == 0:
        evidence["level"] = "达标"
    elif gap_count <= 1:
        evidence["level"] = "接近达标"

    return evidence


def assess_过程层() -> dict:
    evidence = {"level": "数据不足", "signals": [], "gaps": []}
    data = load_health_data()

    # 腰围
    腰围数据 = data.get("waist", {})
    if 腰围数据:
        latest = 腰围数据.get("latest_cm", 0)
        weeks_ago = 腰围数据.get("weeks_ago", 0)
        baseline = 腰围数据.get("baseline_cm", 87)
        变化 = latest - baseline
        trend = "↓" if 变化 < 0 else "↑" if 变化 > 0 else "→"
        evidence["signals"].append(f"腰围：{latest}cm（基线{baseline}cm，{trend}{abs(变化)}cm）")
        if latest >= 85:
            evidence["signals"].append(f"  目标<85cm，还差{latest - 85}cm")
        if weeks_ago and weeks_ago > 1:
            evidence["gaps"].append(f"腰围数据{weeks_ago}周未更新")
    else:
        evidence["gaps"].append("无腰围数据——基线87cm（2025.09体检），需每周自测")

    # 晨起血压
    血压数据 = data.get("blood_pressure", {})
    p0_status = data.get("p0_actions", {})
    血压计 = p0_status.get("购买血压计", "⬜") == "✅"
    if 血压数据:
        systolic = 血压数据.get("avg_systolic_last_week", 0)
        diastolic = 血压数据.get("avg_diastolic_last_week", 0)
        weeks = 血压数据.get("weeks_recorded", 0)
        evidence["signals"].append(f"晨起血压：{systolic}/{diastolic} mmHg（{weeks}周数据）")

        if systolic >= 150 or diastolic >= 95:
            evidence["gaps"].append(f"🔴 血压{systolic}/{diastolic}，≥150/95需当天就医")
        elif systolic >= 140 or diastolic >= 90:
            evidence["gaps"].append(f"⚠️ 血压{systolic}/{diastolic}，连续2周>140/90需关注")
    elif 血压计:
        evidence["gaps"].append("血压计已购——即日开始每日晨起测量（空腹、排尿后）")
    else:
        evidence["gaps"].append("无血压数据——138/90基线（2025.09体检），需每日晨起测量")
        evidence["gaps"].append("需先购买血压计（P0行动#3）")

    gap_count = len(evidence["gaps"])
    if gap_count == 0 and evidence["signals"]:
        evidence["level"] = "达标"
    elif gap_count <= 1:
        evidence["level"] = "接近达标"

    return evidence


def assess_P0行动() -> dict:
    evidence = {"level": "未启动", "signals": [], "gaps": [], "completed": 0, "total": len(P0_ACTIONS)}

    data = load_health_data()
    p0_status = data.get("p0_actions", {})

    for action, reason, priority in P0_ACTIONS:
        status = p0_status.get(action, "⬜")
        if status in ("✅", "done", "completed"):
            evidence["completed"] += 1
            evidence["signals"].append(f"✅ {action} — 已完成")
        else:
            tag = "🔴" if priority == "P0" else "🟡"
            evidence["gaps"].append(f"{tag} {action}：{reason}")

    if evidence["completed"] == evidence["total"]:
        evidence["level"] = "全部完成"
    elif evidence["completed"] >= len([a for a, _, p in P0_ACTIONS if p == "P0"]):
        evidence["level"] = "P0已启动"
    elif evidence["completed"] > 0:
        evidence["level"] = "已启动"

    return evidence


def 联动判断(输入: dict, 过程: dict, P0: dict) -> tuple:
    data = load_health_data()
    p0_status = data.get("p0_actions", {})
    P0_critical = 0
    P1_pending = 0
    for action, reason, priority in P0_ACTIONS:
        if priority == "P0" and p0_status.get(action, "⬜") != "✅":
            P0_critical += 1
        elif priority == "P1" and p0_status.get(action, "⬜") != "✅":
            P1_pending += 1

    P0_pending = P0["total"] - P0["completed"]

    if P0_critical >= 3:
        return ("🔴 P0延迟", f"还有{P0_critical}项P0医疗行动未完成——这比运动饮食更紧急", [
            f"本周必须预约：泌尿外科/肠镜胃镜/降脂饮食",
            "P0行动不是'有空再做'——是'本月内必须完成'",
            "健康飞轮的前提是基础医疗检查到位",
        ])
    elif P0_critical > 0:
        return ("🟠 P0收尾", f"只剩{P0_critical}项P0，快收尾了", [
            f"本周完成最后{P0_critical}项P0",
            "P0完成后就能专注日常追踪",
        ])
    elif P1_pending > 0 and 输入["level"] in ("达标", "接近达标"):
        return ("🟢 P1推进中", f"P0全部完成！{P1_pending}项P1待做，输入层达标", [
            f"P1按优先级逐一安排：眼科验光→血管外科→牙科",
            "输入层达标很好，继续记录，积累4周趋势",
            "血压计已购→开始每日晨起测量",
        ])
    elif 输入["level"] == "数据不足":
        return ("⚪ 数据不足", "大部分指标无数据，无法判断飞轮状态", [
            "本周：开始记录3项输入（运动/睡眠/饮水）",
            "已购血压计→开始每日晨起测量",
            "至少4周数据后才能做趋势判断",
        ])
    elif 输入["level"] == "达标" and 过程["level"] in ("达标", "接近达标"):
        return ("✅ 飞轮正常", "输入达标+过程在改善，健康飞轮在转", [
            "保持当前节奏",
            "继续推进P1行动",
        ])
    else:
        return ("⚠️ 输入待改善", "先盯输入层——运动/睡眠/饮水——过程指标会跟着改善", [
            "本周：确保运动≥3次+力量≥1次",
            "本周：确保睡眠日均≥7h",
            "饮水目标2.5L，当前有差距",
        ])


def build_report(assessments: dict, flywheel: tuple) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    状态, 诊断, 行动 = flywheel

    lines = [
        f"# 健康飞轮 | {now}",
        f"> 三层因果链：{状态} — {诊断}\n",
    ]

    lines.append("## 🎯 飞轮判断")
    lines.append(f"**{状态}**：{诊断}")
    lines.append("")
    for a in 行动:
        lines.append(f"- [ ] {a}")
    lines.append("")

    # 输入层
    lines.append("## 第一层：输入（你直接控制的）")
    输入 = assessments["输入层"]
    for s in 输入.get("signals", []):
        lines.append(f"- {s}")
    for g in 输入.get("gaps", []):
        lines.append(f"- ❌ {g}")
    lines.append("")

    # 过程层
    lines.append("## 第二层：过程（每周可见的）")
    过程 = assessments["过程层"]
    for s in 过程.get("signals", []):
        lines.append(f"- {s}")
    for g in 过程.get("gaps", []):
        lines.append(f"- ❌ {g}")
    lines.append("")

    # P0行动
    lines.append("## 🏥 P0医疗行动追踪")
    P0 = assessments["P0行动"]
    lines.append(f"**完成：{P0['completed']}/{P0['total']}**")
    for s in P0.get("signals", []):
        lines.append(f"- {s}")
    for g in P0.get("gaps", []):
        lines.append(f"- {g}")
    lines.append("")

    # 风险信号
    lines.append("## 🔍 风险信号")
    风险 = []
    for g in 过程.get("gaps", []):
        if "🔴" in g or "150" in g or "160" in g:
            风险.append(g)
    if not 风险:
        lines.append("- ✅ 当前无触发风险信号")
    else:
        for r in 风险:
            lines.append(f"- {r}")
    lines.append("")

    # 每周自检
    lines.append("## 📋 每周10分钟自检")
    lines.append("- [ ] 运动：[ ]次有氧 + [ ]次力量，完成率 [ ]%")
    lines.append("- [ ] 睡眠：平均 [ ]h，有连续<6h吗？[是/否]")
    lines.append("- [ ] 饮水：日均 [ ]L")
    lines.append("- [ ] 腰围：[ ]cm（较上周 ±[ ]cm）")
    lines.append("- [ ] 血压：晨起 [ ]/[ ] mmHg（本周趋势：降/平/升）")
    lines.append("- [ ] P0行动有进展吗？[具体哪项]")
    lines.append("")

    lines.append("## L3 质量自检")
    lines.append("- [ ] 测量值和参考范围正确")
    lines.append("- [ ] 趋势判断明确（当前值 vs 基线 vs 目标方向）")
    lines.append("- [ ] 标注'此为数据追踪，非医学建议'")
    lines.append("")

    lines.append("## L4 飞轮反思")
    lines.append("- 本周最显著的输入→过程关联：")
    lines.append("- 数据记录的连续性如何：")
    lines.append("- 下次扫描可以改进的地方：")

    lines.append(f"\n---\n飞轮自动运行 | {now}")
    return "\n".join(lines)


def main():
    is_dry_run = "--dry-run" in sys.argv

    print("🔍 扫描健康三层因果链...")
    assessments = {
        "输入层": assess_输入层(),
        "过程层": assess_过程层(),
        "P0行动": assess_P0行动(),
    }

    flywheel = 联动判断(
        assessments["输入层"],
        assessments["过程层"],
        assessments["P0行动"],
    )
    report = build_report(assessments, flywheel)

    if is_dry_run:
        print(report)
        return

    状态, _, _ = flywheel
    emoji = "✅" if "正常" in 状态 else "⚪" if "数据不足" in 状态 else "🟡" if "P0推进" in 状态 else "🔴"
    title = f"健康飞轮 {emoji} {状态}"
    success = push_to_wechat(title, report)
    if success:
        print(f"推送成功 | {状态}")
    else:
        print("推送失败")
        print(report)


if __name__ == "__main__":
    main()
