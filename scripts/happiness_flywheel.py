#!/usr/bin/env python3
"""
happiness_flywheel.py — 幸福人生元飞轮

每周扫描六维度满意区间，识别瓶颈目标，判断跨目标联动效应。
在所有6个领域飞轮之后运行（周六10:11），是飞轮体系的顶层聚合。

用法:
  python3 happiness_flywheel.py           # 扫描+微信推送
  python3 happiness_flywheel.py --dry-run # 只打印报告
"""

from lib.wechat import push_to_wechat
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

DELIVERABLES = Path("/Users/cyingfang/claude/deliverables")
SCRIPTS_DIR = Path("/Users/cyingfang/claude/scripts")
VAULT_ROOT = Path("/Users/cyingfang/Documents/Obsidian Vault 6goals")
HEALTH_DATA = DELIVERABLES / "health/健康数据/health_data.json"
SPECS_DIR = DELIVERABLES / "记忆规范"
REPORT_DIR = DELIVERABLES / "ai/执行与简报"

# 六维度满意区间（来自 personal_portrait.md）
DIMS = [
    ("投资成功", "💰", "被动收入覆盖生活支出"),
    ("事业成功", "💼", "科技金融框架+社会资源网"),
    ("家庭支持", "🏠", "子女独立幸福有温度"),
    ("百岁健康", "🏃", "活力充沛百岁可期"),
    ("AI能力", "🤖", "持续学习AI赋能"),
    ("知识库", "📚", "系统化可检索可传承"),
]
DIM_SHORT = {
    "投资": "投资成功", "事业": "事业成功", "家庭": "家庭支持",
    "健康": "百岁健康", "AI能力": "AI能力", "知识库": "知识库",
}
ZONE_TARGET = {name: target for name, _, target in DIMS}


# ============================================================
# 维度1：投资成功
# ============================================================

def assess_投资() -> dict:
    evidence = {"zone": "待判断", "signals": [], "gaps": []}

    # 检查投资分析产出活跃度
    invest_dir = DELIVERABLES / "投资分析"
    if invest_dir.exists():
        recent = [f for f in invest_dir.rglob("*.md")
                  if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days <= 30]
        evidence["signals"].append(f"近30天投资分析产出：{len(recent)}份")
        if not recent:
            evidence["gaps"].append("近30天无投资分析产出——分析管道可能停滞")
    else:
        evidence["gaps"].append("投资分析目录不存在")

    # 检查持仓数据
    portfolio_file = DELIVERABLES / "投资分析/持仓分析" / "持仓明细.md"
    if portfolio_file.exists():
        mtime = datetime.fromtimestamp(portfolio_file.stat().st_mtime)
        days = (datetime.now() - mtime).days
        evidence["signals"].append(f"持仓数据{days}天前更新")
        if days > 30:
            evidence["gaps"].append("持仓数据超30天未更新")
    else:
        evidence["gaps"].append("持仓明细文件缺失")

    # 投资飞轮脚本存在（基础设施）
    flywheel_script = SCRIPTS_DIR / "investment_flywheel.py"
    if flywheel_script.exists():
        evidence["signals"].append("✅ 投资飞轮脚本就绪")

    # 投资分析Agent组
    agent_config = SPECS_DIR / "投资分析Agent组配置.md"
    if agent_config.exists():
        evidence["signals"].append("✅ 投资分析Agent组已配置")

    # 执行信号：最近交易/清仓进度
    trade_files = list(DELIVERABLES.rglob("*清仓*")) + list(DELIVERABLES.rglob("*交易记录*"))
    if trade_files:
        latest_trade = max(trade_files, key=lambda f: f.stat().st_mtime)
        days_since = (datetime.now() - datetime.fromtimestamp(latest_trade.stat().st_mtime)).days
        evidence["signals"].append(f"最近交易记录：{latest_trade.name}（{days_since}天前）")
        if days_since > 30:
            evidence["gaps"].append(f"交易记录{days_since}天未更新——执行可能停滞")
    else:
        evidence["gaps"].append("无交易记录或清仓进度文件——无法验证执行状态")

    # 仓位集中度
    position_files = list(DELIVERABLES.rglob("*持仓*"))
    if position_files:
        evidence["signals"].append(f"持仓相关文件：{len(position_files)}份")
    else:
        evidence["gaps"].append("无持仓分析文件——集中度风险不可见")

    # 判断zone
    gap_count = len(evidence["gaps"])
    if gap_count == 0:
        evidence["zone"] = "满意区"
    elif gap_count <= 2:
        evidence["zone"] = "满意区（有小事）"
    else:
        evidence["zone"] = "焦虑区" if "停滞" in str(evidence["gaps"]) else "焦虑区"

    return evidence


# ============================================================
# 维度2：事业成功
# ============================================================

def assess_事业() -> dict:
    evidence = {"zone": "待判断", "signals": [], "gaps": []}

    career_dir = DELIVERABLES / "career"
    if career_dir.exists():
        all_md = list(career_dir.rglob("*.md"))
        recent = [f for f in all_md
                  if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days <= 30]
        evidence["signals"].append(f"事业产出：{len(all_md)}份md（近30天{len(recent)}份活跃）")

        # 检查公开发表
        pub_dir = career_dir / "发表文章"
        if pub_dir.exists():
            pub_files = list(pub_dir.glob("*.md"))
            evidence["signals"].append(f"待发表文章：{len(pub_files)}篇")
            if not pub_files:
                evidence["gaps"].append("0篇投稿文章——内部积累未外部验证")
        else:
            evidence["gaps"].append("无发表目录")

    # 事业飞轮脚本
    flywheel_script = SCRIPTS_DIR / "career_flywheel.py"
    if flywheel_script.exists():
        evidence["signals"].append("✅ 事业飞轮脚本就绪")

    # 方法论手册
    methodology = DELIVERABLES / "ai/AI方法论/AI方法论完整手册_20260529.md"
    if methodology.exists():
        evidence["signals"].append("✅ AI方法论V1.0已完成")

    # 判断zone
    gap_count = len(evidence["gaps"])
    if gap_count == 0:
        evidence["zone"] = "满意区"
    elif gap_count <= 1:
        evidence["zone"] = "满意区（有小事）"
    else:
        evidence["zone"] = "焦虑区"

    return evidence


# ============================================================
# 维度3：家庭支持
# ============================================================

def assess_家庭() -> dict:
    evidence = {"zone": "待判断", "signals": [], "gaps": []}

    family_dir = DELIVERABLES / "family"
    if family_dir.exists():
        all_md = list(family_dir.rglob("*.md"))
        evidence["signals"].append(f"家庭相关产出：{len(all_md)}份")

    # 检查考研相关
    kaoyan_files = list(DELIVERABLES.rglob("*考研*"))
    if kaoyan_files:
        evidence["signals"].append(f"✅ 考研支持文件：{len(kaoyan_files)}份")

    # 检查赡养提醒
    elder_care = list(DELIVERABLES.rglob("*赡养*")) + list(DELIVERABLES.rglob("*父母*"))
    if elder_care:
        evidence["signals"].append(f"✅ 赡养提醒文件：{len(elder_care)}份")
    else:
        evidence["gaps"].append("赡养提醒系统未建立——两位母亲需要定期关怀")

    # 家庭飞轮脚本
    flywheel_script = SCRIPTS_DIR / "family_flywheel.py"
    if flywheel_script.exists():
        evidence["signals"].append("✅ 家庭飞轮脚本就绪")

    # 关键日期检查（6月高考/考研窗口）
    now = datetime.now()
    if now.month == 6:
        evidence["signals"].append("📅 6月：考研暑假准备窗口开启")

    gap_count = len(evidence["gaps"])
    if gap_count == 0:
        evidence["zone"] = "满意区"
    elif gap_count <= 1:
        evidence["zone"] = "满意区（有小事）"
    else:
        evidence["zone"] = "焦虑区"

    return evidence


# ============================================================
# 维度4：百岁健康
# ============================================================

def assess_健康() -> dict:
    evidence = {"zone": "待判断", "signals": [], "gaps": []}

    # 读取健康数据
    if HEALTH_DATA.exists():
        try:
            data = json.loads(HEALTH_DATA.read_text(encoding="utf-8"))
            records = data.get("daily_records", [])
            recent = records[-7:] if records else []

            if recent:
                avg_steps = sum(r.get("steps", 0) for r in recent) / len(recent)
                evidence["signals"].append(f"近{len(recent)}天日均步数：{avg_steps:.0f}")
                if avg_steps < 8000:
                    evidence["gaps"].append(f"步数不足（{avg_steps:.0f} < 8000）")
                avg_sleep = sum(r.get("sleep_hours", 0) for r in recent) / len(recent)
                evidence["signals"].append(f"日均睡眠：{avg_sleep:.1f}h")
                if avg_sleep < 7:
                    evidence["gaps"].append(f"睡眠不足（{avg_sleep:.1f}h < 7h）")
            else:
                evidence["gaps"].append("无健康日记录数据——基线未采集")

            # 腰围
            waist = data.get("waist", {})
            if waist:
                latest = waist.get("latest_cm", 0)
                baseline = waist.get("baseline_cm", 87)
                if latest:
                    变化 = latest - baseline
                    trend = "↓" if 变化 < 0 else "↑" if 变化 > 0 else "→"
                    evidence["signals"].append(f"腰围：{latest}cm（基线{baseline}，{trend}{abs(变化)}cm）")
                    if latest >= 90:
                        evidence["gaps"].append(f"腰围≥90cm，中心性肥胖风险（{latest}cm）")
                else:
                    evidence["gaps"].append("腰围基线87cm但无最新测量——需每周自测")
            else:
                evidence["gaps"].append("腰围数据缺失——基线87cm（2025.09体检）")

            # 晨起血压
            bp = data.get("blood_pressure", {})
            if bp:
                systolic = bp.get("avg_systolic_last_week", 0)
                diastolic = bp.get("avg_diastolic_last_week", 0)
                if systolic:
                    evidence["signals"].append(f"晨起血压：{systolic}/{diastolic} mmHg")
                    if systolic >= 140 or diastolic >= 90:
                        evidence["gaps"].append(f"血压偏高（{systolic}/{diastolic}，≥140/90需关注）")
                    elif systolic >= 150 or diastolic >= 95:
                        evidence["gaps"].append(f"🔴 血压{systolic}/{diastolic}，≥150/95需当天就医")
                else:
                    evidence["gaps"].append("血压计已购但无测量数据——需要每日晨起测量")
            else:
                evidence["gaps"].append("血压数据缺失——基线138/90（2025.09体检），需每日晨起测量")

            # P0行动
            p0 = data.get("p0_actions", {})
            p0_completed = sum(1 for v in p0.values() if v in ("✅", "done", "completed"))
            p0_total = len(p0) if p0 else 8  # 默认8项P0
            evidence["signals"].append(f"P0医疗行动：{p0_completed}/{p0_total}完成")
            if p0_completed < 5:
                evidence["gaps"].append(f"P0行动进度<50%——这是最紧急的缺口")
        except (json.JSONDecodeError, KeyError):
            evidence["gaps"].append("健康数据文件损坏")
    else:
        evidence["gaps"].append("健康数据文件缺失——所有基线未采集")

    # 健康飞轮脚本
    flywheel_script = SCRIPTS_DIR / "health_flywheel.py"
    if flywheel_script.exists():
        evidence["signals"].append("✅ 健康飞轮脚本就绪")

    # 判断zone
    gap_count = len(evidence["gaps"])
    if gap_count == 0:
        evidence["zone"] = "满意区"
    elif gap_count <= 2:
        evidence["zone"] = "满意区（有小事）"
    else:
        evidence["zone"] = "焦虑区"

    return evidence


# ============================================================
# 维度5：AI能力
# ============================================================

def assess_AI能力() -> dict:
    evidence = {"zone": "待判断", "signals": [], "gaps": []}

    # 脚本统计
    py_files = list(SCRIPTS_DIR.glob("*.py"))
    evidence["signals"].append(f"脚本总数：{len(py_files)}个")

    recent_scripts = [f for f in py_files
                      if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days <= 7]
    evidence["signals"].append(f"近7天活跃脚本：{len(recent_scripts)}个")

    # AI相关产出
    ai_dir = DELIVERABLES / "ai"
    if ai_dir.exists():
        ai_md = list(ai_dir.rglob("*.md"))
        evidence["signals"].append(f"AI相关文档：{len(ai_md)}份")

    # AI能力飞轮
    flywheel_script = SCRIPTS_DIR / "ai_capability_flywheel.py"
    if flywheel_script.exists():
        evidence["signals"].append("✅ AI能力飞轮脚本就绪")

    # 规范文件
    specs = list(SPECS_DIR.glob("*.md"))
    v2_specs = 0
    for s in specs:
        try:
            if "v2.0" in s.read_text(encoding="utf-8")[:500]:
                v2_specs += 1
        except Exception:
            pass
    evidence["signals"].append(f"规范文件：{len(specs)}份（v2.0={v2_specs}）")

    if not recent_scripts:
        evidence["gaps"].append("近7天无脚本活动")

    gap_count = len(evidence["gaps"])
    if gap_count == 0:
        evidence["zone"] = "满意区"
    elif gap_count <= 1:
        evidence["zone"] = "满意区（有小事）"
    else:
        evidence["zone"] = "焦虑区"

    return evidence


# ============================================================
# 维度6：知识库与思维框架
# ============================================================

def assess_知识库() -> dict:
    evidence = {"zone": "待判断", "signals": [], "gaps": []}

    # Obsidian Vault统计
    if VAULT_ROOT.exists():
        all_md = list(VAULT_ROOT.rglob("*.md"))
        evidence["signals"].append(f"Obsidian Vault：{len(all_md)}个md文件")

        # 知识卡片
        card_dir = VAULT_ROOT / "06-知识库/知识卡片"
        if card_dir.exists():
            cards = list(card_dir.glob("*.md"))
            evidence["signals"].append(f"知识卡片：{len(cards)}张")

        # MOC
        moc_dir = VAULT_ROOT / "00-MOC"
        if moc_dir.exists():
            mocs = list(moc_dir.glob("*.md"))
            evidence["signals"].append(f"MOC入口：{len(mocs)}个")
            if len(mocs) < 3:
                evidence["gaps"].append("MOC<3个——知识导航不完整")
    else:
        evidence["gaps"].append("Obsidian Vault文件夹不存在")

    # 知识库飞轮
    flywheel_script = SCRIPTS_DIR / "knowledge_flywheel.py"
    if flywheel_script.exists():
        evidence["signals"].append("✅ 知识库飞轮脚本就绪")

    # 升级映射
    bridge = VAULT_ROOT / "06-知识库/Layer2到Layer1升级映射.md"
    if bridge.exists():
        evidence["signals"].append("✅ Layer2→Layer1升级映射表就绪")

    gap_count = len(evidence["gaps"])
    if gap_count == 0:
        evidence["zone"] = "满意区"
    elif gap_count <= 1:
        evidence["zone"] = "满意区（有小事）"
    else:
        evidence["zone"] = "焦虑区"

    return evidence


# ============================================================
# 联动判断
# ============================================================

def _build_chain(bottleneck: str, assessments: dict) -> list[str]:
    """根据实际缺口动态生成跨目标联动链。"""
    chains = []

    if bottleneck == "健康":
        chains.append("健康缺口 → 精力不足 → 投资执行拖延（无法盯盘/分析）")
        if "焦虑" in assessments.get("投资", {}).get("zone", ""):
            chains.append("投资拖延 → 退休目标延迟 → 事业被迫延长")
    elif bottleneck == "投资":
        chains.append("投资滞后 → 财务自由推迟 → 事业被迫延续")
        chains.append("财务压力 → 家庭支持力度下降 → 考研/教育投入受限")
    elif bottleneck == "事业":
        chains.append("事业停滞 → 影响力无法建立 → 社会网络闲置")
        if "焦虑" in assessments.get("投资", {}).get("zone", ""):
            chains.append("事业停滞+投资滞后 → 双向拖累2037退休目标")
    elif bottleneck == "家庭":
        chains.append("家庭疏忽 → 情感账户透支 → 修复成本远大于维护成本")
    elif bottleneck in ("知识库", "AI能力"):
        chains.append("知识/AI过度建设 → 基建时间>执行时间 → '系统很美但人生没变'")

    # 通用检测：AI/知识库维度是否挤占了更高优先级维度
    ai_gaps = len(assessments.get("AI能力", {}).get("gaps", []))
    k_gaps = len(assessments.get("知识库", {}).get("gaps", []))
    invest_gaps = len(assessments.get("投资", {}).get("gaps", []))
    health_gaps = len(assessments.get("健康", {}).get("gaps", []))

    if (ai_gaps == 0 and k_gaps == 0) and (invest_gaps >= 2 or health_gaps >= 2):
        chains.append("⚠️ AI/知识基建完美但投资/健康有缺口——基建时间可能挤压了执行时间")

    if not bottleneck:
        chains.append("六维平衡 → 复利效应加速 → 2037退休目标可达")

    if len(chains) == 0:
        chains.append("当前维度间无显著负向联动——系统健康运转中")

    return chains


def 联动判断(assessments: dict) -> tuple:
    """跨六维度联动判断——找出瓶颈和动态生成连锁效应。"""

    # 统计各区数量
    焦虑区 = [k for k, v in assessments.items() if "焦虑" in v.get("zone", "")]
    满意区 = [k for k, v in assessments.items() if "满意" in v.get("zone", "")]
    满意数 = len(满意区)
    总维度 = len(assessments)

    # 瓶颈识别逻辑
    if "健康" in 焦虑区:
        行动 = [
            "P0医疗行动是第一优先级——肠镜胃镜、泌尿外科、甲状腺必须本月推进",
            "健康是所有飞轮的前提（49岁关键窗口），健康不达标则投资/事业/家庭都无意义",
            "启动每日三基础记录（步数/饮水/睡眠），4周后才能有趋势判断",
        ]
        return ("🔴 健康是最大短板", f"健康在焦虑区，{满意数}/{总维度}满意——先治身后治财", 行动,
                _build_chain("健康", assessments))

    if "投资" in 焦虑区:
        行动 = [
            "优先执行清仓计划：减昆仑万维集中度（69.5%→≤40%）",
            "分析管道已有Agent组，需实际跑通一次完整的Agent A-E流程",
            "投资成功是幸福人生引擎——它带动事业/家庭/健康/知识库的资金支持",
        ]
        return ("⚠️ 投资执行滞后", f"投资在焦虑区，{满意数}/{总维度}满意——系统建好了但仓位没动", 行动,
                _build_chain("投资", assessments))

    if "事业" in 焦虑区:
        行动 = [
            "从待发表的公众号文章中选1篇投出去（对外验证方法论水平）",
            "激活三重社会网络中的至少1个（中科大校友/浙江同乡/民建建言）",
            "中级经济师备考启动（7月考试，还有~2个月）",
        ]
        return ("🟡 事业缺乏外部验证", f"事业在焦虑区——内部积累够了，该往外走了", 行动,
                _build_chain("事业", assessments))

    if "家庭" in 焦虑区:
        行动 = [
            "确认考研暑假准备计划（英语启动包+专业课路线图）",
            "检查赡养提醒系统：两位母亲近期有无联系缺口",
        ]
        return ("🟡 家庭关键窗口", "家庭维度有缺口——关注时间敏感事项", 行动,
                _build_chain("家庭", assessments))

    if "知识库" in 焦虑区 or "AI能力" in 焦虑区:
        tool_dim = "知识库" if "知识库" in 焦虑区 else "AI能力"
        行动 = [
            "知识库和AI是杠杆工具，别让'建工具'替代'做实事'",
            "当前基建已足够支撑投资/事业/家庭/健康运转，先执行再优化",
        ]
        return ("💡 工具/知识库基建关注", f"{tool_dim}有缺口，但不应挤占更高优先级目标", 行动,
                _build_chain(tool_dim, assessments))

    if 满意数 == 总维度:
        行动 = [
            "保持当前节奏，不要让任何一个维度滑出满意区",
            "每季度做一次全面的PDCA复盘",
            "警惕'满意区幻觉'——满意不代表完美，持续微调",
        ]
        return ("✅ 六维全满", f"幸福人生飞轮正常运转——{满意数}/{总维度}在满意区间", 行动,
                _build_chain(None, assessments))

    return ("🟢 大体健康", f"{满意数}/{总维度}在满意区，少数小事待处理", [
        f"关注焦虑区：{', '.join(焦虑区) if 焦虑区 else '无'}",
        "当前最重要：不要让小事升级为系统性缺口",
    ], _build_chain(None, assessments))


# ============================================================
# 汇总报告
# ============================================================

def build_report(assessments: dict, flywheel: tuple) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    状态, 诊断, 行动, 联动链 = flywheel

    满意区 = [k for k, v in assessments.items() if "满意" in v.get("zone", "")]
    焦虑区 = [k for k, v in assessments.items() if "焦虑" in v.get("zone", "")]

    lines = [
        f"# 幸福人生飞轮 | {now}",
        f"> 六维度：{len(满意区)}/6 满意区间 — 瓶颈：{焦虑区[0] if 焦虑区 else '无'}",
        f"> 满意区间标准：投资=被动收入覆盖生活支出, 事业=科技金融框架, 家庭=子女独立幸福, 健康=百岁可期, AI=持续赋能, 知识库=可检索传承\n",
    ]

    # 瓶颈判断
    lines.append("## 🎯 瓶颈判断")
    lines.append(f"**{状态}**：{诊断}")
    lines.append("")
    for a in 行动:
        lines.append(f"- [ ] {a}")
    lines.append("")

    # 跨目标联动
    lines.append("## 🔗 跨目标联动链")
    for link in 联动链:
        lines.append(f"- {link}")
    lines.append("")

    # 六维度仪表盘
    lines.append("## 📊 六维度仪表盘")

    for name, icon, target_desc in DIMS:
        short_key = {v: k for k, v in DIM_SHORT.items()}.get(name, "")
        data = assessments.get(short_key, {})
        zone = data.get("zone", "未知")
        emoji = "🟢" if "满意" in zone else "🔴" if "焦虑" in zone else "⚪"
        lines.append(f"### {icon} {name} — {emoji} {zone}")
        lines.append(f"目标：{target_desc}")
        for s in data.get("signals", []):
            lines.append(f"- {s}")
        for g in data.get("gaps", []):
            lines.append(f"- ❌ {g}")
        lines.append("")

    # 优先级排序
    lines.append("## ⚡ 本周优先级排序")
    priority = 焦虑区 + [k for k in assessments if k not in 焦虑区]
    for i, dim in enumerate(priority):
        long_name = DIM_SHORT.get(dim, dim)
        target = ZONE_TARGET.get(long_name, "")
        lines.append(f"{i+1}. **{long_name}**（目标：{target}）")
    lines.append("")

    # L3 质量自检
    lines.append("## L3 质量自检")
    lines.append("- [ ] 六维度信号均来自实际文件读取（非主观判断）")
    lines.append("- [ ] zone判断标准一致（0缺口=满意，1-2=有小事，3+=焦虑）")
    lines.append("- [ ] 跨目标联动链有因果逻辑支撑")
    lines.append("- [ ] 行动建议具体可执行（不出现'加强''优化'等空洞词）")
    lines.append("")

    # L4 飞轮反思
    lines.append("## L4 飞轮反思")
    lines.append("- 本周六维度中最意外的信号：")
    lines.append("- 是否存在'某个维度好但拖累了另一个维度'的零和现象：")
    lines.append("- 下次扫描可以改进的地方：")

    lines.append(f"\n---\n幸福人生飞轮自动运行 | {now}")
    return "\n".join(lines)


# ============================================================
# 主入口
# ============================================================

def main():
    is_dry_run = "--dry-run" in sys.argv

    print("🌟 扫描幸福人生六维度...")
    assessments = {
        "投资": assess_投资(),
        "事业": assess_事业(),
        "家庭": assess_家庭(),
        "健康": assess_健康(),
        "AI能力": assess_AI能力(),
        "知识库": assess_知识库(),
    }

    flywheel = 联动判断(assessments)
    report = build_report(assessments, flywheel)

    if is_dry_run:
        print(report)
        return

    # 保存本地报告
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    report_path = REPORT_DIR / f"幸福人生飞轮_{date_str}.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"报告已保存：{report_path}")

    状态, 诊断, _, _ = flywheel
    满意区 = [k for k, v in assessments.items() if "满意" in v.get("zone", "")]
    emoji = "✅" if len(满意区) >= 5 else "🟡" if len(满意区) >= 3 else "🔴"
    title = f"幸福人生飞轮 {emoji} {len(满意区)}/6满意"
    success = push_to_wechat(title, report)
    if success:
        print(f"推送成功 | {len(满意区)}/6满意 | 瓶颈：{诊断[:20]}")
    else:
        print("推送失败")
        print(report)


if __name__ == "__main__":
    main()
