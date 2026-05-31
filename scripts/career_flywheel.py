#!/usr/bin/env python3
"""
career_flywheel.py — 事业成功自进化飞轮

每周扫描事业三层结构：引擎层→加速器层→结果层，输出联动判断。

用法:
  python3 career_flywheel.py           # 扫描+推送微信
  python3 career_flywheel.py --dry-run # 只打印报告
"""

from lib.wechat import push_to_wechat
import sys
from datetime import datetime, timedelta
from pathlib import Path

DELIVERABLES = Path("/Users/cyingfang/claude/deliverables")
CAREER_DIR = DELIVERABLES / "career"
OBSIDIAN_CAREER = Path("/Users/cyingfang/Documents/Obsidian Vault 6goals/02-事业进阶")
SPECS_DIR = DELIVERABLES / "记忆规范"
SCRIPTS_DIR = Path("/Users/cyingfang/claude/scripts")

# ============================================================
# 第一层：引擎 — 专业产出力
# ============================================================

def assess_产出力() -> dict:
    evidence = {"level": "正常", "signals": [], "gaps": []}

    articles_dir = CAREER_DIR / "发表文章"
    if articles_dir.exists():
        md_files = list(articles_dir.glob("*.md"))
        recent_7d = [f for f in md_files
                     if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days <= 7]
        evidence["signals"].append(f"发表文章目录：{len(md_files)} 篇Markdown")

        today = [f for f in md_files
                 if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days <= 1]
        if today:
            evidence["signals"].append(f"今日产出：{len(today)} 篇")
            for t in today:
                evidence["signals"].append(f"  ✅ {t.stem}")
        if len(recent_7d) >= 3:
            evidence["level"] = "强"
            evidence["signals"].append(f"近7天产出 {len(recent_7d)} 篇，超基准(≥2篇/月)")
        elif len(recent_7d) >= 1:
            evidence["signals"].append(f"近7天产出 {len(recent_7d)} 篇，符合基准")
        else:
            evidence["gaps"].append("近7天无新增文章")

    # 科技金融方法论
    方法论 = CAREER_DIR / "科技金融方法论"
    if 方法论.exists():
        方法论_files = list(方法论.glob("*.md"))
        evidence["signals"].append(f"科技金融方法论：{len(方法论_files)} 份")

    # 案例库
    案例 = OBSIDIAN_CAREER / "科技金融案例库_20260528.md"
    if 案例.exists():
        evidence["signals"].append("✅ 科技金融案例库已建立（5个深度案例）")

    # 内容日历
    日历 = OBSIDIAN_CAREER / "6-12月内容日历.md"
    if 日历.exists():
        evidence["signals"].append("✅ 6-12月内容日历已建立（16项产出规划）")

    # 工作方法论
    工作方法 = CAREER_DIR / "工作方法论_20260528.md"
    if 工作方法.exists():
        evidence["signals"].append("✅ 工作方法论已建立")

    return evidence


# ============================================================
# 第一层：引擎 — 网络经营力
# ============================================================

def assess_经营力() -> dict:
    evidence = {"level": "正常", "signals": [], "gaps": []}

    # 民建
    民建 = CAREER_DIR / "民建与职称" / "民建社情民意-并购贷款与科创金融生态.md"
    if 民建.exists():
        民建_mtime = datetime.fromtimestamp(民建.stat().st_mtime)
        民建_days = (datetime.now() - 民建_mtime).days
        evidence["signals"].append(f"✅ 民建建言已完成（{民建_days}天前），.doc+.pages+.pdf 多格式就绪")

        提交版 = CAREER_DIR / "民建与职称" / "民建社情民意-并购贷款与科创金融生态_提交版.md"
        if 提交版.exists():
            evidence["signals"].append("✅ 提交版（2500字精缩版）已备好")
        else:
            evidence["gaps"].append("提交版（2500字）尚未准备")

    # 关系经营手册
    关系 = CAREER_DIR / "社会关系经营手册_20260528.md"
    if 关系.exists():
        evidence["signals"].append("✅ 社会关系经营手册已建立")

    人脉 = CAREER_DIR / "人脉资源手册_20260528.md"
    if 人脉.exists():
        evidence["signals"].append("✅ 人脉资源手册已建立")

    # 客户拜访
    客户_dir = CAREER_DIR / "客户方案"
    if 客户_dir.exists():
        客户_files = list(客户_dir.glob("*.md"))
        evidence["signals"].append(f"客户方案：{len(客户_files)} 份")
        recent_客户 = [f for f in 客户_files
                      if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days <= 7]
        if recent_客户:
            evidence["signals"].append(f"  近7天更新：{len(recent_客户)} 份")

    # 四重网络检查
    网络_mapping = {
        "民建": ["民建", "建言", "社情民意"],
        "中科大": ["中科大", "校友", "USTC"],
        "浙江": ["浙江", "籍贯", "同乡"],
        "邮储": ["邮储", "PSBC", "行内", "银行"],
    }

    网络_覆盖 = {}
    for net, keywords in 网络_mapping.items():
        found = False
        for f in DELIVERABLES.rglob("*.md"):
            if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days > 14:
                continue
            try:
                content = f.read_text(encoding="utf-8")[:3000]
                if any(kw in content for kw in keywords):
                    found = True
                    break
            except:
                pass
        网络_覆盖[net] = found

    活跃网络 = [net for net, active in 网络_覆盖.items() if active]
    静默网络 = [net for net, active in 网络_覆盖.items() if not active]
    evidence["signals"].append(f"近14天活跃网络：{len(活跃网络)}/4（{', '.join(活跃网络) if 活跃网络 else '无'}）")
    if 静默网络:
        evidence["gaps"].append(f"静默网络：{', '.join(静默网络)}")

    if len(活跃网络) >= 2:
        evidence["level"] = "强"
    elif len(活跃网络) == 0:
        evidence["level"] = "弱"

    return evidence


# ============================================================
# 第二层：加速器 — AI杠杆率
# ============================================================

def assess_AI杠杆() -> dict:
    evidence = {"level": "正常", "signals": [], "gaps": []}

    # AI辅助产出的证据
    ai_career_files = [
        CAREER_DIR / "事业AI加速方案_20260527.md" if (CAREER_DIR / "事业AI加速方案_20260527.md").exists() else None,
        OBSIDIAN_CAREER / "事业AI加速方案_20260527.md",
    ]

    ai加速方案 = None
    for f in ai_career_files:
        if f and f.exists():
            ai加速方案 = f
            break

    if ai加速方案:
        evidence["signals"].append(f"✅ 事业AI加速方案已建立")

    # 检查公众号文章是否用AI辅助
    articles_dir = CAREER_DIR / "发表文章"
    if articles_dir.exists():
        gen_scripts = list(articles_dir.glob("generate_*.py"))
        if gen_scripts:
            evidence["signals"].append(f"✅ AI生成封面脚本：{len(gen_scripts)} 个（generate_cover_*.py）")
        html_files = list(articles_dir.glob("公众号HTML_*.html"))
        if html_files:
            evidence["signals"].append(f"✅ AI生成HTML：{len(html_files)} 个")

    # 备考AI辅助
    evidence["gaps"].append("中级经济师备考AI辅助未启动（计划中，尚未到执行日期）")
    evidence["gaps"].append("网络经营场景AI辅助为0（无互动提醒/机会评估等自动化）")

    # AI辅助工作方法
    工作方法 = CAREER_DIR / "工作方法论_20260528.md"
    if 工作方法.exists():
        content = 工作方法.read_text(encoding="utf-8")
        if "AI" in content or "Claude" in content:
            evidence["signals"].append("✅ 工作方法论中已集成AI辅助")

    # 计数活跃场景
    active_scenes = len(gen_scripts) > 0 if articles_dir.exists() else 0
    if active_scenes >= 3:
        evidence["level"] = "强"
    elif active_scenes == 0:
        evidence["level"] = "弱"
        evidence["gaps"].append("AI辅助场景仅限文章生成，未覆盖备考/研究/经营")

    return evidence


# ============================================================
# 第三层：结果 — 位置安全 + 资源获取 + 资本转化
# ============================================================

def assess_位置安全() -> dict:
    evidence = {"level": "通过", "signals": [], "gaps": [], "warnings": []}

    # 产出量是位置安全的核心代理指标
    articles_dir = CAREER_DIR / "发表文章"
    if articles_dir.exists():
        recent_articles = [f for f in articles_dir.glob("*.md")
                          if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days <= 7]
        if len(recent_articles) >= 5:
            evidence["signals"].append("✅ 高产状态，不可替代性强")
        elif len(recent_articles) >= 2:
            evidence["signals"].append("✅ 产出稳定")
        else:
            evidence["warnings"].append("⚠️ 近7天产出偏低，检查是否有工作在替代你")

    # 科技金融标签清晰度
    方法论_dir = CAREER_DIR / "科技金融方法论"
    if 方法论_dir.exists() and list(方法论_dir.glob("*.md")):
        evidence["signals"].append("✅ '科技金融专家'标签有方法论+案例库支撑")
    else:
        evidence["warnings"].append("⚠️ 科技金融标签缺少体系化支撑")

    # 竞聘准备
    竞聘 = OBSIDIAN_CAREER / "竞聘准备.md"
    if 竞聘.exists():
        evidence["signals"].append("✅ 竞聘倒计时计划已建立")

    # 入库与职称
    入库 = CAREER_DIR / "民建与职称" / "入库与职称攻坚计划.md"
    if 入库.exists():
        evidence["signals"].append("✅ 入库与职称攻坚计划A+B路径已建立")

    if evidence["warnings"]:
        evidence["level"] = "⚠️ 需关注"

    return evidence


def assess_资源获取() -> dict:
    evidence = {"level": "持平", "signals": [], "gaps": []}

    # 无法从文件中直接获取薪资数据，用产出活动作为代理
    evidence["signals"].append("📋 收入/职位量化数据需手动填入（工资条/绩效/OA）")

    # 职级相关信号
    入库 = CAREER_DIR / "民建与职称" / "入库与职称攻坚计划.md"
    if 入库.exists():
        content = 入库.read_text(encoding="utf-8")
        if "中级经济师" in content:
            evidence["signals"].append("✅ 职级提升路径：中级经济师备考中")

    evidence["gaps"].append("无自动收入追踪（需手动更新）")
    evidence["gaps"].append("职位/权限变动信号需手动标记")

    return evidence


def assess_资本转化() -> dict:
    evidence = {"level": "数据不足", "signals": [], "gaps": []}

    evidence["gaps"].append("储蓄率数据未接入（需手动填入月收支）")
    evidence["gaps"].append("投资账户流入数据未接入（需对接投资组合追踪器）")
    evidence["signals"].append("📋 资本转化率需手动计算：月投资额/月收入")

    return evidence


# ============================================================
# 联动判断引擎
# ============================================================

def 联动判断(产出力: dict, 经营力: dict, AI杠杆: dict,
           位置: dict, 资源: dict, 资本: dict) -> tuple:
    """三层联动判断，返回(状态, 诊断, 行动)"""

    引擎转 = 产出力["level"] != "弱" and 经营力["level"] != "弱"
    加速够 = AI杠杆["level"] == "强"
    结果涨 = 位置["level"] == "通过"  # 代理指标

    if 引擎转 and 加速够 and 结果涨:
        return ("✅ 飞轮正常", "引擎+加速器+结果三层通畅", [
            "保持产出节奏，6月按内容日历推进",
            "中级经济师备考6月第1周启动",
            "民建建言完成提交",
        ])
    elif 引擎转 and not 加速够 and 结果涨:
        return ("⚠️ 有未用杠杆", "结果在涨但AI加速不够——你还有免费杠杆没用好", [
            "将AI辅助扩展到备考场景（AI出题+知识框架梳理）",
            "将AI辅助扩展到网络经营场景（互动提醒+机会评估）",
            "目标：AI辅助场景从1个扩展到3个",
        ])
    elif 引擎转 and 加速够 and not 结果涨:
        return ("🔴 方向可能错了", "引擎在转、AI在加速，但结果不涨——产出方向可能未对准需求", [
            "检查：产出的受众是谁？他们需要什么？",
            "检查：你写的东西是否对准了'科技金融专家'的标签？",
            "检查：民建建言提交后有没有反馈？文章有没有人转发？",
        ])
    elif not 引擎转 and 加速够 and 结果涨:
        return ("🟡 引擎靠惯性", "结果在涨但引擎停转，你在吃老本", [
            "恢复产出节奏：近7天至少写1篇",
            "恢复网络互动：本周主动联系≥2个关键联系人",
        ])
    elif not 引擎转 and not 加速够 and not 结果涨:
        return ("🔴🆘 四项全红", "引擎停转+加速闲置+结果下跌，需根本性改变", [
            "立即：今天产出1篇可对外的东西",
            "立即：本周内联系3个关键人",
            "立即：用AI辅助至少1件事",
        ])
    else:
        return ("⚠️ 混合信号", "各层信号不一致，需人工判断", [
            "逐项检查六维度详细信号",
        ])


# ============================================================
# 汇总报告
# ============================================================

def build_report(assessments: dict, flywheel: tuple) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    状态, 诊断, 行动 = flywheel

    lines = [
        f"# 事业飞轮 | {now}",
        f"> 三层联动判断：{状态} — {诊断}\n",
    ]

    # 联动判断
    lines.append("## 🎯 联动判断")
    lines.append(f"**状态**：{状态}")
    lines.append(f"**诊断**：{诊断}")
    lines.append("")
    lines.append("**本周行动**：")
    for a in 行动:
        lines.append(f"- [ ] {a}")
    lines.append("")

    # 第一层：引擎
    lines.append("## 第一层：引擎（你投入什么）")

    产出力 = assessments["专业产出力"]
    lines.append(f"### 专业产出力 — {产出力['level']}")
    for s in 产出力.get("signals", []):
        lines.append(f"- {s}")
    for g in 产出力.get("gaps", []):
        lines.append(f"- ❌ {g}")
    lines.append("")

    经营力 = assessments["网络经营力"]
    lines.append(f"### 网络经营力 — {经营力['level']}")
    for s in 经营力.get("signals", []):
        lines.append(f"- {s}")
    for g in 经营力.get("gaps", []):
        lines.append(f"- ❌ {g}")
    lines.append("")

    # 第二层：加速器
    lines.append("## 第二层：加速器（什么放大了引擎）")

    AI杠杆 = assessments["AI杠杆率"]
    lines.append(f"### AI杠杆率 — {AI杠杆['level']}")
    for s in AI杠杆.get("signals", []):
        lines.append(f"- {s}")
    for g in AI杠杆.get("gaps", []):
        lines.append(f"- ❌ {g}")
    lines.append("")

    # 第三层：结果
    lines.append("## 第三层：结果（你得到什么）")

    位置 = assessments["位置安全"]
    lines.append(f"### 位置安全 — {位置['level']}")
    for s in 位置.get("signals", []):
        lines.append(f"- {s}")
    for w in 位置.get("warnings", []):
        lines.append(f"- {w}")

    资源 = assessments["资源获取"]
    lines.append(f"### 资源获取 — {资源['level']}")
    for s in 资源.get("signals", []):
        lines.append(f"- {s}")
    for g in 资源.get("gaps", []):
        lines.append(f"- ❌ {g}")

    资本 = assessments["资本转化"]
    lines.append(f"### 资本转化 — {资本['level']}")
    for s in 资本.get("signals", []):
        lines.append(f"- {s}")
    for g in 资本.get("gaps", []):
        lines.append(f"- ❌ {g}")
    lines.append("")

    # 风险信号
    lines.append("## 🔍 风险信号扫描")
    risk_count = 0
    if 产出力["level"] == "弱":
        lines.append("- ⚠️ 产出力弱：连续2月无可见产出风险")
        risk_count += 1
    if 经营力["level"] == "弱":
        lines.append("- ⚠️ 经营力弱：关键网络断联>1月")
        risk_count += 1
    if AI杠杆["level"] == "弱":
        lines.append("- ⚠️ AI杠杆闲置：连续2周未用AI辅助事业产出")
        risk_count += 1
    if 位置["level"] != "通过":
        lines.append("- 🔴 位置安全预警：存在被替代风险信号")
        risk_count += 1
    if risk_count == 0:
        lines.append("- ✅ 当前无触发风险信号")
    lines.append("")

    lines.append("## L3 质量自检")
    lines.append("- [ ] 引用的政策/法规/标准名称和条款号准确")
    lines.append("- [ ] 论证链完整，有摘要→分析→结论结构")
    lines.append("- [ ] 行动建议具体可执行（有负责人+截止日期）")
    lines.append("")

    lines.append("## L4 飞轮反思")
    lines.append("- 本周三层扫描最意外的发现：")
    lines.append("- 哪个维度的数据最薄弱：")
    lines.append("- 下次扫描可以改进的地方：")

    lines.append(f"---\n飞轮自动运行 | {now}")
    return "\n".join(lines)


# ============================================================
# 主入口
# ============================================================

def main():
    is_dry_run = "--dry-run" in sys.argv

    print("🔍 扫描事业三层结构...")
    assessments = {
        "专业产出力": assess_产出力(),
        "网络经营力": assess_经营力(),
        "AI杠杆率": assess_AI杠杆(),
        "位置安全": assess_位置安全(),
        "资源获取": assess_资源获取(),
        "资本转化": assess_资本转化(),
    }

    flywheel = 联动判断(
        assessments["专业产出力"],
        assessments["网络经营力"],
        assessments["AI杠杆率"],
        assessments["位置安全"],
        assessments["资源获取"],
        assessments["资本转化"],
    )

    report = build_report(assessments, flywheel)

    if is_dry_run:
        print(report)
        return

    状态, _, _ = flywheel
    emoji = "✅" if "正常" in 状态 else "⚠️" if "未用" in 状态 else "🔴"
    title = f"事业飞轮 {emoji} {状态}"
    success = push_to_wechat(title, report)
    if success:
        print(f"推送成功 | {状态}")
    else:
        print("推送失败")
        print(report)


if __name__ == "__main__":
    main()
