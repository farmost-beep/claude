#!/usr/bin/env python3
"""Generate MVP Product Spec PDF with optimized layout."""
import os, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
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

GREEN = HexColor("#07C160")
DARK = HexColor("#1A1A2E")
DARK2 = HexColor("#2D3E50")
WHITE = white
GRAY = HexColor("#999")
GRAY2 = HexColor("#666")
LIGHT_BG = HexColor("#F8FAFB")
LIGHT_GREEN = HexColor("#F0FAF4")
BORDER = HexColor("#E8E8E8")

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
    "code": ParagraphStyle("CDE", fontName=F, fontSize=8, leading=13, textColor=HexColor("#333"), backColor=HexColor("#F5F5F5"), leftIndent=8),
    "footer": ParagraphStyle("F", fontName=F, fontSize=7, textColor=GRAY, alignment=TA_CENTER),
    "callout": ParagraphStyle("CX", fontName=F, fontSize=10, leading=17, textColor=DARK, backColor=LIGHT_GREEN, borderPadding=12),
}

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(GREEN)
    canvas.setLineWidth(0.5)
    canvas.line(40, A4[1]-30, A4[0]-40, A4[1]-30)
    canvas.setFont(F, 7)
    canvas.setFillColor(GRAY)
    canvas.drawString(40, A4[1]-26, "社交关系AI管家 | MVP产品说明书")
    canvas.drawRightString(A4[0]-40, A4[1]-26, "2026-06-13")
    canvas.line(40, 30, A4[0]-40, 30)
    canvas.drawCentredString(A4[0]/2, 18, f"- {doc.page} -")
    canvas.restoreState()

def tbl(headers, rows, col_widths):
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

def div():
    d = Table([[""]], colWidths=[PAGE_W])
    d.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 1, GREEN)]))
    return d

def build():
    doc = SimpleDocTemplate(
        "/Users/cyingfang/claude/deliverables/career/发表文章/社交关系AI管家_MVP产品说明书.pdf",
        pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=35*mm, bottomMargin=35*mm
    )
    story = [Spacer(1, 50)]
    story.append(Paragraph("社交关系AI管家", S["cover_title"]))
    story.append(Paragraph("MVP 产品说明书", S["cover_sub"]))
    story.append(Spacer(1, 6))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(Paragraph("v0.1 | 2026-06-13 | 概念验证阶段", S["cover_date"]))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "<b>一句话定义</b>：一个本地运行的AI插件，自动追踪所有社交关系中"
        "「最近干了什么」和「下一步该干什么」，帮你拟好消息，推到该去的地方。",
        ParagraphStyle("CI", fontName=F, fontSize=11, leading=18, textColor=DARK, backColor=LIGHT_GREEN, borderPadding=14)))
    story.append(Spacer(1, 6))
    story.append(Paragraph("目标用户：需要维护大量社交关系的职场人 | 核心承诺：不改变你的社交习惯，只是帮你记住。", S["body_sm"]))

    # 1. MVP Features
    story.append(Spacer(1, 14))
    story.append(Paragraph("一、MVP 功能清单", S["h1"]))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(Paragraph("P0 — MVP核心功能", S["h2"]))
    story.append(tbl(
        ["功能", "说明", "验收标准"],
        [["联系人管理", "JSON配置联系人/关系/标签", "增删改查可用"],
         ["时间线记录", "每条互动：日期/平台/摘要/联系人", "可手动添加/查看/搜索"],
         ["待办提取", "从时间线标记待跟进事项", "待办列表可见"],
         ["AI拟稿", "根据联系人+上下文生成消息草稿", "可编辑可发送"],
         ["微信推送", "提醒+消息推送到个人微信", "通过现有桥接API"]],
        [PAGE_W*0.18, PAGE_W*0.40, PAGE_W*0.42]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("P1 — 建议功能", S["h2"]))
    story.append(tbl(
        ["功能", "说明", "优先级"],
        [["关系图谱", "按关系类型/强度/标签筛选", "中"],
         ["提醒队列", "P0逾期/P1 14天/P2 30天未联系", "高"],
         ["消息模板", "自定义语气风格", "中"],
         ["数据导出", "JSON导出/导入", "低"]],
        [PAGE_W*0.18, PAGE_W*0.52, PAGE_W*0.30]
    ))

    # 2. Architecture
    story.append(Spacer(1, 14))
    story.append(Paragraph("二、技术架构", S["h1"]))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(tbl(
        ["层级", "说明"],
        [["CLI / Skill 交互层", "命令行 + 微信关键词触发"],
         ["核心引擎(Python)", "联系人管理 | 时间线引擎 | 待办队列 | AI拟稿(Claude API) | 推送"],
         ["数据层", "本地JSON (contacts.json / timeline.json / todos.json)"],
         ["连接层", "微信(桥接API) | 飞书(cc-connect预留)"]],
        [PAGE_W*0.25, PAGE_W*0.75]
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph("数据模型", S["h2"]))
    story.append(Paragraph("<b>联系人 (contacts.json)</b>", S["body"]))
    story.append(Paragraph(
        '{"id":"zhangzong","name":"张总","relation":"客户","strength":4,'
        '"tags":["科技金融"],"platforms":{"weixin":"zhang123"}}', S["code"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>时间线 (timeline.json)</b>", S["body"]))
    story.append(Paragraph(
        '{"id":"t-001","date":"2026-06-10","contact":"zhangzong",'
        '"summary":"项目验收讨论","pending":"跟进验收结果"}', S["code"]))

    # 3. CLI
    story.append(Spacer(1, 14))
    story.append(Paragraph("三、交互设计", S["h1"]))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "social add-contact 王教授 --relation 导师 --tags 学术,引荐<br/>"
        "social log 王教授 聊了引荐的事，同意安排时间<br/>"
        "social todos<br/>"
        "  P0  张总  跟进项目验收结果  逾期2天<br/>"
        "  P1  王教授  安排引荐时间  14天未联系<br/>"
        "social draft 王教授<br/>"
        "  >王教授好，上次聊到引荐的事，您方便安排时间吗？<",
        S["code"]))

    # 4. Roadmap
    story.append(Spacer(1, 14))
    story.append(Paragraph("四、开发路线图", S["h1"]))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(tbl(
        ["阶段", "时间", "交付物"],
        [["MVP", "1周", "CLI可用: 添加联系人->记录时间线->AI拟稿->微信推送"],
         ["V1.0", "+1周", "待办提醒+关系图谱+飞书接入"],
         ["V1.5", "+2周", "微信消息自动抓取+时间线自动提取"],
         ["V2.0", "+4周", "关系强度自动计算+多端同步+仪表盘"]],
        [PAGE_W*0.12, PAGE_W*0.12, PAGE_W*0.76]
    ))

    # 5. Comparison
    story.append(Spacer(1, 14))
    story.append(Paragraph("五、与现有方案的区别", S["h1"]))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(tbl(
        ["对比", "手机通讯录", "CRM软件", "本方案"],
        [["记录什么", "电话号码", "销售漏斗", "人际关系完整记忆"],
         ["谁在用", "所有人", "销售人员", "每个人"],
         ["主动性", "无", "手动提醒", "AI主动提醒+拟稿"],
         ["隐私", "本地", "上云", "本地优先"]],
        [PAGE_W*0.15, PAGE_W*0.25, PAGE_W*0.25, PAGE_W*0.35]
    ))

    story.append(Spacer(1, 30))
    story.append(Paragraph("-- End --", S["footer"]))
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print("MVP PDF generated OK")

if __name__ == "__main__":
    build()
