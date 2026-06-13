#!/usr/bin/env python3
"""Business Entry Point PDF - clean, no code blocks styling."""
import os, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT

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

GREEN = HexColor("#07C160")
DARK = HexColor("#1A1A2E")
DARK2 = HexColor("#2D3E50")
WHITE = white
GRAY = HexColor("#999")
GRAY2 = HexColor("#666")
LIGHT_BG = HexColor("#F5F7FA")
LIGHT_GREEN = HexColor("#F0FAF4")
BORDER = HexColor("#E0E0E0")

def hf(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(GREEN)
    canvas.setLineWidth(0.5)
    canvas.line(40, A4[1]-30, A4[0]-40, A4[1]-30)
    canvas.setFont(F, 7)
    canvas.setFillColor(GRAY)
    canvas.drawString(40, A4[1]-26, "社交关系AI管家 | 商业切入点分析")
    canvas.drawRightString(A4[0]-40, A4[1]-26, "2026-06-13")
    canvas.line(40, 30, A4[0]-40, 30)
    canvas.drawCentredString(A4[0]/2, 18, f"- {doc.page} -")
    canvas.restoreState()

PAGE_W = A4[0] - 40*mm

body = ParagraphStyle("B", fontName=F, fontSize=10, leading=18, textColor=HexColor("#333"), spaceAfter=6)
body2 = ParagraphStyle("B2", fontName=F, fontSize=9, leading=15, textColor=HexColor("#555"), spaceAfter=3)
h1 = ParagraphStyle("H1", fontName=F, fontSize=16, textColor=DARK, spaceBefore=18, spaceAfter=8, leading=24)
h2 = ParagraphStyle("H2", fontName=F, fontSize=12, textColor=DARK2, spaceBefore=14, spaceAfter=6, leading=18)
title = ParagraphStyle("T", fontName=F, fontSize=30, textColor=GREEN, alignment=TA_CENTER)
sub = ParagraphStyle("S", fontName=F, fontSize=20, textColor=DARK, alignment=TA_CENTER)
dt = ParagraphStyle("D", fontName=F, fontSize=9, textColor=GRAY, alignment=TA_CENTER)
footer = ParagraphStyle("F", fontName=F, fontSize=7, textColor=GRAY, alignment=TA_CENTER)

# Table cell style - clean, no borders
cell = ParagraphStyle("C", fontName=F, fontSize=9, leading=15, textColor=HexColor("#333"), alignment=TA_LEFT)
cell_bold = ParagraphStyle("CB", fontName=F, fontSize=9, leading=15, textColor=DARK, alignment=TA_LEFT)

def line():
    t = Table([[""]], colWidths=[PAGE_W])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 1, GREEN)]))
    return t

def section(label, value):
    t = Table(
        [[Paragraph(f"<b>{label}</b>", cell_bold), Paragraph(str(value), cell)]],
        colWidths=[PAGE_W*0.22, PAGE_W*0.78])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t

def build():
    doc = SimpleDocTemplate(
        "/Users/cyingfang/claude/deliverables/career/发表文章/社交关系AI管家_商业切入点分析.pdf",
        pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=35*mm, bottomMargin=35*mm
    )
    story = [Spacer(1, 40)]
    story.append(Paragraph("社交关系AI管家", title))
    story.append(Paragraph("商业切入点分析", sub))
    story.append(Spacer(1, 6))
    story.append(line())
    story.append(Spacer(1, 6))
    story.append(Paragraph("v1.0 | 2026-06-13 | 内部讨论版", dt))
    story.append(Spacer(1, 20))

    # Callout
    story.append(Paragraph(
        "<b>核心切入逻辑</b><br/>"
        "先从金融行业最痛的人（客户经理）切入，用AI帮他们记住每一个客户，"
        "验证后做成银行客户经理专用版，再复制到保险/房产/创业者市场。",
        ParagraphStyle("CI", fontName=F, fontSize=11, leading=18, textColor=DARK,
                       backColor=LIGHT_GREEN, borderPadding=14)))

    # 1. Users
    story.append(Spacer(1, 16))
    story.append(Paragraph("一、谁愿意为此付费？", h1))
    story.append(line())
    story.append(Spacer(1, 6))
    story.append(Paragraph('从「最痛的人」开始切入，而不是服务所有人。', body))
    story.append(Spacer(1, 4))
    story.append(section("T1 银行客户经理", "痛点极强，每人维护100-300个客户，付费意愿高，全国约200万人"))
    story.append(section("T2 保险/理财顾问", "痛点强，约800万人"))
    story.append(section("T3 创业者/商务BD", "痛点中等，约5000万人"))
    story.append(section("T4 普通职场人", "痛点弱，适合免费版"))
    story.append(Spacer(1, 8))

    story.append(Paragraph("为什么银行客户经理是黄金切入点？", h2))
    story.append(Paragraph(
        "每人维护100-300个客户，每月至少联系一次。97%的人用Excel管关系，"
        "跨设备不可查，离职了客户关系就断。此痛点极强。", body))
    story.append(Spacer(1, 6))
    story.append(Paragraph("最小可验证产品", h2))
    story.append(Paragraph(
        "一个JSON文件加一个Python脚本加微信推送，不需要App，不需要后台。", body))

    # 2. Entry Path
    story.append(Spacer(1, 10))
    story.append(Paragraph("二、切入路径", h1))
    story.append(line())
    story.append(Spacer(1, 6))
    story.append(section("Phase 0 原型验证（1周）", "自己先用，跑通闭环"))
    story.append(section("Phase 1 内部试点（1个月）", "找3-5个目标用户，使用率大于60%为验证通过"))
    story.append(section("Phase 2 产品化（3个月）", "客户经理专用版，99元/月"))
    story.append(section("Phase 3 跨行业复制（6个月后）", "保险代理人、房产中介、创业者市场"))

    # 3. Business Model
    story.append(Spacer(1, 10))
    story.append(Paragraph("三、商业模式", h1))
    story.append(line())
    story.append(Spacer(1, 6))
    story.append(section("免费版 ¥0", "个人试用，20联系人，基础提醒"))
    story.append(section("Pro版 ¥99/月", "客户经理，不限联系人+AI拟稿+推送"))
    story.append(section("团队版 ¥1,999/年(10人)", "支行/团队，共享时间线+任务分配"))
    story.append(section("企业版 定制", "金融机构，API接入+内网部署"))

    # 4. Revenue
    story.append(Spacer(1, 10))
    story.append(Paragraph("四、收入估算", h1))
    story.append(line())
    story.append(Spacer(1, 6))
    story.append(section("Pilot（3个月）50人", "0元测试，收入¥0"))
    story.append(section("Launch（6个月）500人", "20%付费率，月收入约¥9,900"))
    story.append(section("Scale（12个月）5,000人", "15%付费率+50团队，月收入约¥156,000"))
    story.append(section("成熟期 50,000人", "10%付费率+500团队，月收入约¥1,380,000"))

    # 5. Moat
    story.append(Spacer(1, 10))
    story.append(Paragraph("五、护城河", h1))
    story.append(line())
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "真正的护城河不是技术，是用户在你这存的时间线数据——换工具的成本是所有社交记忆的丢失。", body))
    story.append(Spacer(1, 4))
    story.append(section("场景know-how", "懂银行客户经理真实工作流，可维持6个月"))
    story.append(section("先发数据", "用户时间线数据有强粘性，可维持12个月"))
    story.append(section("AI拟稿质量", "基于Claude场景微调，可维持3个月"))
    story.append(section("渠道优势", "金融行业合作网络，持续性优势"))

    # 6. Risk
    story.append(Spacer(1, 10))
    story.append(Paragraph("六、风险与化解", h1))
    story.append(line())
    story.append(Spacer(1, 6))
    story.append(section("用户懒不记录互动（概率高）", "V1.5自动抓取微信消息，降低录入成本"))
    story.append(section("银行合规不允许（概率中）", "全部本地存储不上云，过等保"))
    story.append(section("客户经理离职带不走数据（概率中）", "支持一键导出，数据属于用户"))
    story.append(section("AI拟稿语气不对（概率低）", "预置多种语气模板，用户可调"))

    story.append(Spacer(1, 30))
    story.append(Paragraph("-- End --", footer))

    doc.build(story, onFirstPage=hf, onLaterPages=hf)
    print("PDF OK")

if __name__ == "__main__":
    build()
