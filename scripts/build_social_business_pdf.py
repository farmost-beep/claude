#!/usr/bin/env python3
"""Generate Business Entry Point PDF for Social AI Agent - optimized layout."""
import os, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# ── Font ──
F = None
for fp in ["/System/Library/Fonts/PingFang.ttc", "/System/Library/Fonts/STHeiti Light.ttc"]:
    if os.path.exists(fp):
        try:
            pdfmetrics.registerFont(TTFont("CJK", fp))
            F = "CJK"
            break
        except:
            pass
if not F:
    print("No CJK font")
    sys.exit(1)

# ── Colors ──
GREEN = HexColor("#07C160")
DARK = HexColor("#1A1A2E")
DARK2 = HexColor("#2D3E50")
WHITE = white
GRAY = HexColor("#999")
GRAY2 = HexColor("#666")
LIGHT_BG = HexColor("#F8FAFB")
LIGHT_GREEN = HexColor("#F0FAF4")
LIGHT_BLUE = HexColor("#F0F4FF")
LIGHT_ORANGE = HexColor("#FFF8F0")
BORDER = HexColor("#E8E8E8")
ACCENT_RED = HexColor("#E74C3C")

# ── Page template ──
def header_footer(canvas, doc):
    canvas.saveState()
    # Header line
    canvas.setStrokeColor(GREEN)
    canvas.setLineWidth(0.5)
    canvas.line(40, A4[1]-30, A4[0]-40, A4[1]-30)
    # Header text
    canvas.setFont(F, 7)
    canvas.setFillColor(GRAY)
    canvas.drawString(40, A4[1]-26, "社交关系AI管家 | 商业切入点分析")
    canvas.drawRightString(A4[0]-40, A4[1]-26, "2026-06-13")
    # Footer
    canvas.line(40, 30, A4[0]-40, 30)
    canvas.drawCentredString(A4[0]/2, 18, f"- {doc.page} -")
    canvas.restoreState()

# ── Styles ──
PAGE_W = A4[0] - 40*mm

S = {
    "cover_title": ParagraphStyle("CT", fontName=F, fontSize=30, textColor=GREEN, alignment=TA_CENTER, spaceAfter=6),
    "cover_sub": ParagraphStyle("CS", fontName=F, fontSize=20, textColor=DARK, alignment=TA_CENTER, spaceAfter=4),
    "cover_date": ParagraphStyle("CD", fontName=F, fontSize=9, textColor=GRAY, alignment=TA_CENTER),
    "h1": ParagraphStyle("H1", fontName=F, fontSize=16, textColor=DARK, spaceBefore=18, spaceAfter=8, leading=24),
    "h2": ParagraphStyle("H2", fontName=F, fontSize=12, textColor=DARK2, spaceBefore=12, spaceAfter=6, leading=18),
    "body": ParagraphStyle("B", fontName=F, fontSize=10, leading=17, textColor=HexColor("#333"), spaceAfter=5),
    "body_sm": ParagraphStyle("BS", fontName=F, fontSize=9, leading=15, textColor=GRAY2, spaceAfter=3),
    "hc": ParagraphStyle("HC", fontName=F, fontSize=9, textColor=WHITE, alignment=TA_CENTER),
    "cc": ParagraphStyle("CC", fontName=F, fontSize=9, leading=14, textColor=HexColor("#333")),
    "footer": ParagraphStyle("F", fontName=F, fontSize=7, textColor=GRAY, alignment=TA_CENTER),
    "callout": ParagraphStyle("CX", fontName=F, fontSize=10, leading=17, textColor=DARK, backColor=LIGHT_GREEN, borderPadding=12),
    "highlight": ParagraphStyle("HL", fontName=F, fontSize=10, leading=16, textColor=HexColor("#555"), leftIndent=12),
    "tag_up": ParagraphStyle("TU", fontName=F, fontSize=8, textColor=GREEN, alignment=TA_CENTER),
    "tag_mid": ParagraphStyle("TM", fontName=F, fontSize=8, textColor=HexColor("#3C8CFF"), alignment=TA_CENTER),
    "tag_down": ParagraphStyle("TD", fontName=F, fontSize=8, textColor=GRAY, alignment=TA_CENTER),
}

def table(headers, rows, col_widths):
    data = [[Paragraph(h, S["hc"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(v), S["cc"]) for v in row])
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t

def divider():
    d = Table([[""]], colWidths=[PAGE_W])
    d.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 1, GREEN)]))
    return d

def build():
    doc = SimpleDocTemplate(
        "/Users/cyingfang/claude/deliverables/career/发表文章/社交关系AI管家_商业切入点分析.pdf",
        pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=35*mm, bottomMargin=35*mm
    )
    story = []

    # ── Cover ──
    story.append(Spacer(1, 50))
    story.append(Paragraph("社交关系AI管家", S["cover_title"]))
    story.append(Paragraph("商业切入点分析", S["cover_sub"]))
    story.append(Spacer(1, 6))
    story.append(divider())
    story.append(Spacer(1, 6))
    story.append(Paragraph("v1.0 | 2026-06-13 | 内部讨论版", S["cover_date"]))
    story.append(Spacer(1, 24))

    # Core insight box
    story.append(Paragraph(
        "<b>核心切入逻辑</b><br/>"
        "先从金融行业最痛的人（客户经理）切入，用AI帮他们记住每一个客户，"
        "验证后做成银行客户经理专用版，再复制到保险/房产/创业者市场。",
        ParagraphStyle("CI", fontName=F, fontSize=11, leading=18, textColor=DARK,
                       backColor=LIGHT_GREEN, borderPadding=14, borderColor=GREEN, borderWidth=1)))

    # ── 1. Target Users ──
    story.append(Spacer(1, 18))
    story.append(Paragraph("一、谁愿意为此付费？", S["h1"]))
    story.append(divider())
    story.append(Spacer(1, 8))
    story.append(Paragraph('从「最痛的人」开始切入，而不是服务所有人。', S["body"]))
    story.append(Spacer(1, 6))

    story.append(table(
        ["层级", "人群", "痛点强度", "付费意愿", "市场规模"],
        [
            ["T1", "银行客户经理", Paragraph("极强", S["tag_up"]), Paragraph("$$$", S["tag_up"]), "~200万人"],
            ["T2", "保险/理财顾问", Paragraph("强", S["tag_mid"]), Paragraph("$$", S["tag_mid"]), "~800万人"],
            ["T3", "创业者/商务BD", "中", "$", "~5,000万人"],
            ["T4", "普通职场人", "弱", "免费", "~2亿人"],
        ],
        [PAGE_W*0.08, PAGE_W*0.20, PAGE_W*0.16, PAGE_W*0.16, PAGE_W*0.40]
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph("为什么银行客户经理是黄金切入点？", S["h2"]))
    story.append(Paragraph(
        '银行客户经理每人维护100-300个客户，每月至少联系一次"有效户"。97%的人用Excel管客户关系，'
        '跨设备不可查，离职了客户关系就断。此痛点极强。', S["body"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("最小可验证产品：", S["h2"]))
    story.append(Paragraph(
        "一个JSON文件 + 一个Python脚本 + 微信推送。不需要App，不需要后台，一条微信推送就够了。", S["body"]))

    # ── 2. Entry Path ──
    story.append(Spacer(1, 12))
    story.append(Paragraph("二、切入路径", S["h1"]))
    story.append(divider())
    story.append(Spacer(1, 6))
    story.append(table(
        ["阶段", "动作", "验证目标", "周期"],
        [
            [Paragraph("Phase 0", S["tag_up"]), "自己先用", "跑通闭环", "本周"],
            [Paragraph("Phase 1", S["tag_mid"]), "内部试点3-5个目标用户", "使用率>60%", "1个月"],
            [Paragraph("Phase 2", S["tag_up"]), "产品化 99元/月", "客户经理版上线", "3个月"],
            [Paragraph("Phase 3", S["tag_mid"]), "跨行业复制", "保险/房产/创业者", "6个月"],
        ],
        [PAGE_W*0.14, PAGE_W*0.30, PAGE_W*0.30, PAGE_W*0.26]
    ))

    # ── 3. Business Model ──
    story.append(Spacer(1, 12))
    story.append(Paragraph("三、商业模式", S["h1"]))
    story.append(divider())
    story.append(Spacer(1, 6))
    story.append(table(
        ["版本", "价格", "目标用户", "核心功能"],
        [
            ["免费版", "¥0", "个人试用", "20联系人，基础提醒"],
            [Paragraph("Pro版", S["tag_up"]), Paragraph("¥99/月", S["tag_up"]), "客户经理", "不限联系人 + AI拟稿 + 推送"],
            [Paragraph("团队版", S["tag_mid"]), "¥1,999/年(10人)", "支行/团队", "共享时间线 + 任务分配"],
            ["企业版", "定制", "金融机构", "API接入 + 内网部署"],
        ],
        [PAGE_W*0.14, PAGE_W*0.18, PAGE_W*0.20, PAGE_W*0.48]
    ))

    # ── 4. Revenue ──
    story.append(Spacer(1, 12))
    story.append(Paragraph("四、收入估算", S["h1"]))
    story.append(divider())
    story.append(Spacer(1, 6))
    story.append(table(
        ["阶段", "用户数", "付费模型", "月收入"],
        [
            ["Pilot（3个月）", "50人", "0元测试", "¥0"],
            ["Launch（6个月）", "500人", "20% x 99", Paragraph("~¥9,900", S["tag_up"])],
            ["Scale（12个月）", "5,000人", "15% x 99 + 50团队", Paragraph("~¥156,000", S["tag_up"])],
            ["成熟期", "50,000人", "10% x 99 + 500团队", Paragraph("~¥1,380,000", S["tag_up"])],
        ],
        [PAGE_W*0.20, PAGE_W*0.16, PAGE_W*0.30, PAGE_W*0.34]
    ))

    # ── 5. Moat ──
    story.append(Spacer(1, 12))
    story.append(Paragraph("五、护城河", S["h1"]))
    story.append(divider())
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "真正的护城河不是技术，是用户在你这存的时间线数据——换工具的成本是所有社交记忆的丢失。", S["body"]))
    story.append(Spacer(1, 6))
    story.append(table(
        ["护城河", "说明", "可维持时间"],
        [
            [Paragraph("场景know-how", S["tag_up"]), "懂银行客户经理真实工作流", "6个月"],
            [Paragraph("先发数据", S["tag_mid"]), "用户时间线数据有强粘性", "12个月"],
            ["AI拟稿质量", "基于Claude场景微调", "3个月"],
            [Paragraph("渠道优势", S["tag_up"]), "金融行业合作网络", "持续性"],
        ],
        [PAGE_W*0.16, PAGE_W*0.54, PAGE_W*0.30]
    ))

    # ── 6. Risk ──
    story.append(Spacer(1, 12))
    story.append(Paragraph("六、风险与化解", S["h1"]))
    story.append(divider())
    story.append(Spacer(1, 6))
    story.append(table(
        ["风险", "概率", "化解方案"],
        [
            ["用户懒，不记录互动", Paragraph("高", S["tag_up"]), "V1.5自动抓取微信消息"],
            ["银行合规不允许", Paragraph("中", S["tag_mid"]), "全部本地存储，不上云"],
            ["客户经理离职带不走", "中", "支持一键导出"],
            ["AI拟稿语气不对", "低", "预置多种语气模板"],
        ],
        [PAGE_W*0.24, PAGE_W*0.12, PAGE_W*0.64]
    ))

    story.append(Spacer(1, 30))
    story.append(Paragraph("-- End --", S["footer"]))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print("PDF generated OK")

if __name__ == "__main__":
    build()
