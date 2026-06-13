#!/usr/bin/env python3
"""Generate Product Spec v2.0 PDF - Entrepreneur Edition."""
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
from reportlab.lib.enums import TA_CENTER

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

ORANGE = HexColor("#FF8C00")
DARK = HexColor("#1A1A2E")
DARK2 = HexColor("#2D3E50")
WHITE = white
GRAY = HexColor("#999")
GRAY2 = HexColor("#666")
LIGHT_BG = HexColor("#FFF8F0")
BORDER = HexColor("#E8E8E8")

def hf(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(ORANGE)
    canvas.setLineWidth(0.5)
    canvas.line(40, A4[1]-30, A4[0]-40, A4[1]-30)
    canvas.setFont(F, 7)
    canvas.setFillColor(GRAY)
    canvas.drawString(40, A4[1]-26, "社交关系AI管家 | 产品说明书v2.0")
    canvas.drawRightString(A4[0]-40, A4[1]-26, "2026-06-13")
    canvas.line(40, 30, A4[0]-40, 30)
    canvas.drawCentredString(A4[0]/2, 18, f"- {doc.page} -")
    canvas.restoreState()

PW = A4[0] - 40*mm

body = ParagraphStyle("B", fontName=F, fontSize=10, leading=18, textColor=HexColor("#333"), spaceAfter=6)
body2 = ParagraphStyle("B2", fontName=F, fontSize=9, leading=15, textColor=HexColor("#555"), spaceAfter=3)
h1s = ParagraphStyle("H1", fontName=F, fontSize=16, textColor=DARK, spaceBefore=18, spaceAfter=8, leading=24)
h2s = ParagraphStyle("H2", fontName=F, fontSize=12, textColor=DARK2, spaceBefore=14, spaceAfter=6, leading=18)
title = ParagraphStyle("T", fontName=F, fontSize=28, textColor=ORANGE, alignment=TA_CENTER)
sub = ParagraphStyle("S", fontName=F, fontSize=18, textColor=DARK, alignment=TA_CENTER)
dt = ParagraphStyle("D", fontName=F, fontSize=9, textColor=GRAY, alignment=TA_CENTER)
footer = ParagraphStyle("F", fontName=F, fontSize=7, textColor=GRAY, alignment=TA_CENTER)
cb = ParagraphStyle("CB", fontName=F, fontSize=9, leading=15, textColor=DARK)
cc = ParagraphStyle("CC", fontName=F, fontSize=9, leading=15, textColor=HexColor("#333"))

def div():
    t = Table([[""]], colWidths=[PW])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 1, ORANGE)]))
    return t

def row(label, value):
    t = Table(
        [[Paragraph(f"<b>{label}</b>", cb), Paragraph(str(value), cc)]],
        colWidths=[PW*0.25, PW*0.75])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t

def tbl(h, r, cw):
    d = [[Paragraph(x, ParagraphStyle("HC", fontName=F, fontSize=9, textColor=WHITE, alignment=TA_CENTER)) for x in h]]
    for row in r:
        d.append([Paragraph(str(v), cc) for v in row])
    t = Table(d, colWidths=cw)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t

def build():
    doc = SimpleDocTemplate(
        "/Users/cyingfang/claude/deliverables/career/发表文章/社交关系AI管家_产品说明书v2.0.pdf",
        pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=35*mm, bottomMargin=35*mm
    )
    story = [Spacer(1, 40)]
    story.append(Paragraph("社交关系AI管家", title))
    story.append(Paragraph("产品说明书 v2.0", sub))
    story.append(Spacer(1, 6))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(Paragraph("创业者版 · 极致体验 | 2026-06-13", dt))
    story.append(Spacer(1, 16))

    # Positioning
    story.append(Paragraph(
        "<b>一句话定义</b>：一个让你在投资人、合伙人、客户面前永远像做过功课的AI管家"
        "——而且你什么额外的事都不用做。",
        ParagraphStyle("CI", fontName=F, fontSize=11, leading=18, textColor=DARK,
                       backColor=LIGHT_BG, borderPadding=14)))
    story.append(Paragraph("目标用户：创业者、初创公司创始人、OPC社群成员", body2))
    story.append(Spacer(1, 14))

    # 1. Core Relationships
    story.append(Paragraph("一、创业者三大核心关系链", h1s))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(row("投资人关系", "天使轮跟进 / TS条款谈判 / 路演反馈 / DD配合"))
    story.append(row("合伙人关系", "股权分配 / 分工协作 / 冲突调解 / 决策同步"))
    story.append(row("客户关系", "合同进展 / 项目交付 / 复购机会 / 转介绍"))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "相比银行客户经理的100-300个标准化客户，创业者只需要管理30-80个深度关系"
        "——但每个都是高度个性化的，每个互动都需要推进实质性进展。", body))

    # 2. Three-Layer Experience
    story.append(Spacer(1, 10))
    story.append(Paragraph("二、极致体验三层设计", h1s))
    story.append(div())
    story.append(Spacer(1, 6))

    story.append(Paragraph("L1 极致自动化：你不用做任何事", h2s))
    story.append(tbl(
        ["你的行为", "AI自动完成"],
        [["跟投资人聊完微信", "提取反馈存入时间线生成待办"],
         ["收到合伙人消息", "识别事项更新进度提醒回复"],
         ["客户发了邮件", "抓取关键信息关联项目建议下一步"],
         ["什么也不做", "扫描所有关系发现需跟进生成提醒"]],
        [PW*0.30, PW*0.70]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("L2 极致精准：每条提醒恰到好处", h2s))
    story.append(tbl(
        ["场景", "提醒内容", "时机"],
        [["投资人跟进", "张总上周说等TS，建议问问进展", "约定+3天"],
         ["合伙人同步", "上次分工方案还没回复", "2天未回复"],
         ["客户回访", "项目交付两周了，该问问满意度", "交付后14天"],
         ["引荐致谢", "李总帮引荐了投资人", "会面后24h内"],
         ["关系预警", "和王总快一个月没联系了", "21天静默"]],
        [PW*0.18, PW*0.52, PW*0.30]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("L3 极致顺畅：消息拟得就像你写的", h2s))
    story.append(Paragraph(
        "支持语气调节：正式/亲切/简洁，可反复调到满意再发。", body))

    # 3. MVP Features
    story.append(Spacer(1, 10))
    story.append(Paragraph("三、MVP功能清单（1周可出）", h1s))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(Paragraph("P0 核心功能", h2s))
    story.append(tbl(
        ["功能", "说明", "交互方式"],
        [["关键关系录入", "投资人/合伙人/客户四类", "微信/Web"],
         ["互动记录", "语音/文字10秒一条", "微信对话"],
         ["AI待办提取", "准度80%+，可修正", "自动+手动"],
         ["消息拟稿", "基于上下文+语气调节", "微信触发"],
         ["提醒推送", "精准时机+直接发送", "微信消息"],
         ["关系看板", "所有关系健康度", "Web仪表盘"]],
        [PW*0.18, PW*0.40, PW*0.42]
    ))

    # 4. UX
    story.append(Spacer(1, 10))
    story.append(Paragraph("四、交互设计", h1s))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(Paragraph("主入口：微信对话（唯一入口）", h2s))
    story.append(Paragraph('创业者不需要学任何新工具，在微信里聊天就是操作。', body))
    story.append(Paragraph(
        '「记一下：和张总聊了TS，等法务回复」 自动记录+3天后提醒<br/>'
        '「张总最近啥情况？」 显示时间线+建议下一步<br/>'
        '「给张总拟条消息，轻松点」 AI生成确认发送', body2))
    story.append(Spacer(1, 6))
    story.append(Paragraph("次入口：Web仪表盘", h2s))
    story.append(Paragraph(
        '电脑端看全局：融资进度/合伙人活跃度/客户健康度/今日待办一目了然。', body))

    # 5. Business
    story.append(Spacer(1, 10))
    story.append(Paragraph("五、商业验证", h1s))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(tbl(
        ["因素", "银行客户经理", "创业者"],
        [["决策链", "自己", "自己"],
         ["付费来源", "个人收入", "公司运营费用"],
         ["价格敏感", "高", "低"],
         ["试用意愿", "低", "高"],
         ["流失成本", "低", "高（关系数据价值大）"],
         ["推荐意愿", "低", "高（圈子互通）"]],
        [PW*0.18, PW*0.36, PW*0.46]
    ))
    story.append(Spacer(1, 6))
    story.append(row("创业者版", "¥199/月，核心功能全开"))
    story.append(row("团队版", "¥999/月(5人)，合伙人共享"))
    story.append(row("冷启动路径", "自己先用 到 3个朋友试用 到 创业社群合作"))

    # 6. Roadmap
    story.append(Spacer(1, 10))
    story.append(Paragraph("六、版本路线图", h1s))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(tbl(
        ["版本", "时间", "交付物"],
        [["MVP", "1周", "微信对话记录+AI拟稿+推送"],
         ["V1.0", "+1周", "融资看板+团队协作+Email接入"],
         ["V1.5", "+2周", "微信消息自动抓取+时间线自动提取"],
         ["V2.0", "+4周", "关系健康度+关键时刻提醒"]],
        [PW*0.12, PW*0.12, PW*0.76]
    ))

    story.append(Spacer(1, 20))
    story.append(Paragraph("-- End --", footer))
    doc.build(story, onFirstPage=hf, onLaterPages=hf)
    print("PDF OK")

if __name__ == "__main__":
    build()
