#!/usr/bin/env python3
"""Generate PDF for Startup Edition - Social Relationship AI Agent."""
import os, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
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
BORDER = HexColor("#E8E8E8")
ORANGE = HexColor("#FF8C00")

def hf(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(GREEN)
    canvas.setLineWidth(0.5)
    canvas.line(40, A4[1]-30, A4[0]-40, A4[1]-30)
    canvas.setFont(F, 7)
    canvas.setFillColor(GRAY)
    canvas.drawString(40, A4[1]-26, "社交关系AI管家 | 创业者版极致体验")
    canvas.drawRightString(A4[0]-40, A4[1]-26, "2026-06-13")
    canvas.line(40, 30, A4[0]-40, 30)
    canvas.drawCentredString(A4[0]/2, 18, f"- {doc.page} -")
    canvas.restoreState()

PAGE_W = A4[0] - 40*mm
body = ParagraphStyle("B", fontName=F, fontSize=10, leading=18, textColor=HexColor("#333"), spaceAfter=6)
body2 = ParagraphStyle("B2", fontName=F, fontSize=9, leading=15, textColor=HexColor("#555"), spaceAfter=3)
h1 = ParagraphStyle("H1", fontName=F, fontSize=16, textColor=DARK, spaceBefore=18, spaceAfter=8, leading=24)
h2 = ParagraphStyle("H2", fontName=F, fontSize=12, textColor=DARK2, spaceBefore=14, spaceAfter=6, leading=18)
title = ParagraphStyle("T", fontName=F, fontSize=30, textColor=ORANGE, alignment=TA_CENTER)
sub = ParagraphStyle("S", fontName=F, fontSize=20, textColor=DARK, alignment=TA_CENTER)
dt = ParagraphStyle("D", fontName=F, fontSize=9, textColor=GRAY, alignment=TA_CENTER)
footer = ParagraphStyle("F", fontName=F, fontSize=7, textColor=GRAY, alignment=TA_CENTER)
ct = ParagraphStyle("CI", fontName=F, fontSize=11, leading=18, textColor=DARK, backColor=HexColor("#FFF8F0"), borderPadding=14)
cb = ParagraphStyle("CB", fontName=F, fontSize=9, leading=15, textColor=DARK)
cc = ParagraphStyle("CC", fontName=F, fontSize=9, leading=15, textColor=HexColor("#333"))

def line():
    t = Table([[""]], colWidths=[PAGE_W])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 1, ORANGE)]))
    return t

def sec(label, value):
    t = Table(
        [[Paragraph(f"<b>{label}</b>", cb), Paragraph(str(value), cc)]],
        colWidths=[PAGE_W*0.25, PAGE_W*0.75])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t

def build():
    doc = SimpleDocTemplate(
        "/Users/cyingfang/claude/deliverables/career/发表文章/社交关系AI管家_创业者版极致体验.pdf",
        pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=35*mm, bottomMargin=35*mm
    )
    story = [Spacer(1, 40)]
    story.append(Paragraph("社交关系AI管家", title))
    story.append(Paragraph("创业者版 · 极致体验", sub))
    story.append(Spacer(1, 6))
    story.append(line())
    story.append(Spacer(1, 6))
    story.append(Paragraph("v1.0 | 2026-06-13 | OPC/创业者聚焦版", dt))
    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "<b>核心价值主张</b><br/>"
        "让创业者在投资人、合伙人、客户面前，永远像做过功课——而且什么额外的事都不用做。", ct))
    story.append(Spacer(1, 14))

    # 1. Scenarios
    story.append(Paragraph("一、创业者社交关系的独特场景", h1))
    story.append(line())
    story.append(Spacer(1, 6))
    story.append(Paragraph("三大核心关系链", h2))
    story.append(sec("投资人关系", "天使轮跟进 / TS条款谈判 / 路演反馈 / DD配合"))
    story.append(sec("创始人/合伙关系", "股权分配 / 分工协作 / 冲突调解 / 决策同步"))
    story.append(sec("客户/合作伙伴", "合同进展 / 项目交付 / 复购机会 / 转介绍"))
    story.append(Spacer(1, 8))
    story.append(Paragraph("创业者vs银行客户经理的核心差异", h2))
    story.append(sec("关系数量", "30-80个关键关系，高度个性化"))
    story.append(sec("关注点", "每次联系都有价值，推进实质性进展"))
    story.append(sec("技术接受度", "高，可接受CLI和新工具"))
    story.append(sec("付费来源", "公司运营费用，决策快"))
    story.append(Spacer(1, 8))

    # 2. Experience
    story.append(Paragraph("二、极致体验设计", h1))
    story.append(line())
    story.append(Spacer(1, 6))

    story.append(Paragraph("1. 极致自动化：不需要手动记录", h2))
    story.append(Paragraph("每次关键互动后自动提取关键反馈、生成待办、建议下次沟通时机。用户只管聊天。", body))
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. 极致精准：每次提醒恰到好处", h2))
    story.append(sec("投资人跟进", "约定时间+3天提醒"))
    story.append(sec("合伙人同步", "2天未回复提醒"))
    story.append(sec("客户回访", "交付后14天提醒"))
    story.append(sec("引荐致谢", "会面后24h内提醒"))
    story.append(Spacer(1, 4))

    story.append(Paragraph("3. 极致顺畅：消息拟得就像你写的", h2))
    story.append(Paragraph("支持语气调节：正式/亲切/简洁，一次不满意可以再调。修改不超过2次就能发。", body))
    story.append(Spacer(1, 8))

    # 3. Features
    story.append(Paragraph("三、功能设计", h1))
    story.append(line())
    story.append(Spacer(1, 6))
    story.append(Paragraph("MVP核心功能（1周）", h2))
    story.append(sec("关键关系录入", "投资人/合伙人/客户/导师四类，30秒一个"))
    story.append(sec("互动快速记录", "语音/文字/转发消息自动解析，10秒一条"))
    story.append(sec("AI待办提取", "从记录自动提炼，准确度80%+"))
    story.append(sec("消息拟稿", "基于上下文，支持语气调节"))
    story.append(sec("微信推送", "提醒+消息即时送达"))
    story.append(Spacer(1, 4))
    story.append(Paragraph("V1.0新增（+1周）", h2))
    story.append(sec("融资跟进看板", "当前TS/条款/进度一目了然"))
    story.append(sec("团队协作同步", "合伙人间共享关键进度"))
    story.append(sec("Email接入", "自动抓取邮件往来"))
    story.append(Spacer(1, 8))

    # 4. UX
    story.append(Paragraph("四、交互设计：极致简单", h1))
    story.append(line())
    story.append(Spacer(1, 6))
    story.append(Paragraph("主入口：微信对话", h2))
    story.append(Paragraph("创业者不需要学任何新工具，在微信里完成一切：", body2))
    story.append(Paragraph('「记一下：和张总聊了TS，等法务回复」自动记录+设提醒<br/>'
                           '「张总最近啥情况？」显示时间线+建议下一步<br/>'
                           '「给张总拟条消息」AI生成确认发送', body2))
    story.append(Spacer(1, 4))
    story.append(Paragraph("次入口：Web仪表盘", h2))
    story.append(Paragraph("电脑端看板式全局视图，融资进度/合伙人活跃度/客户健康度一目了然。", body))
    story.append(Spacer(1, 8))

    # 5. Business
    story.append(Paragraph("五、商业验证", h1))
    story.append(line())
    story.append(Spacer(1, 6))
    story.append(sec("决策链", "创业者自己决定，公司报销"))
    story.append(sec("价格敏感度", "低，每月几百块不算事"))
    story.append(sec("试用意愿", "高，愿意尝新工具"))
    story.append(sec("流失成本", "高，关系数据价值大"))
    story.append(sec("推荐意愿", "高，创业者圈子互通"))
    story.append(Spacer(1, 6))
    story.append(sec("创业者版 ¥199/月", "核心功能全开"))
    story.append(sec("团队版 ¥999/月(5人)", "合伙人共享"))
    story.append(sec("投资人机构版 定制", "批量管理被投企业"))
    story.append(Spacer(1, 6))
    story.append(sec("冷启动路径", "自己先用→找3个创业者朋友→创业社群合作→工具集联动"))

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "<b>一句话定位</b>：让创业者在投资人、合伙人、客户面前，永远像做过功课——"
        "而且什么额外的事都不用做。",
        ParagraphStyle("OUT", fontName=F, fontSize=11, leading=18, textColor=DARK,
                       backColor=HexColor("#FFF8F0"), borderPadding=14)))
    story.append(Spacer(1, 20))
    story.append(Paragraph("-- End --", footer))
    doc.build(story, onFirstPage=hf, onLaterPages=hf)
    print("PDF OK")

if __name__ == "__main__":
    build()
