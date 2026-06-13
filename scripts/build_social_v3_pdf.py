#!/usr/bin/env python3
"""Generate Product Spec v3.0 PDF - Agent Native, WeChat Embedded."""
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

GREEN = HexColor("#07C160")
DARK = HexColor("#1A1A2E")
DARK2 = HexColor("#2D3E50")
WHITE = white
GRAY = HexColor("#999")
GRAY2 = HexColor("#666")
LIGHT_BG = HexColor("#F0FAF4")
BORDER = HexColor("#E8E8E8")

def hf(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(GREEN)
    canvas.setLineWidth(0.5)
    canvas.line(40, A4[1]-30, A4[0]-40, A4[1]-30)
    canvas.setFont(F, 7)
    canvas.setFillColor(GRAY)
    canvas.drawString(40, A4[1]-26, "社交关系AI管家 | 产品说明书v3.0")
    canvas.drawRightString(A4[0]-40, A4[1]-26, "2026-06-13")
    canvas.line(40, 30, A4[0]-40, 30)
    canvas.drawCentredString(A4[0]/2, 18, f"- {doc.page} -")
    canvas.restoreState()

PW = A4[0] - 40*mm

body = ParagraphStyle("B", fontName=F, fontSize=10, leading=18, textColor=HexColor("#333"), spaceAfter=6)
body2 = ParagraphStyle("B2", fontName=F, fontSize=9, leading=15, textColor=HexColor("#555"), spaceAfter=3)
h1s = ParagraphStyle("H1", fontName=F, fontSize=16, textColor=DARK, spaceBefore=18, spaceAfter=8, leading=24)
h2s = ParagraphStyle("H2", fontName=F, fontSize=12, textColor=DARK2, spaceBefore=14, spaceAfter=6, leading=18)
title = ParagraphStyle("T", fontName=F, fontSize=28, textColor=GREEN, alignment=TA_CENTER)
sub = ParagraphStyle("S", fontName=F, fontSize=18, textColor=DARK, alignment=TA_CENTER)
dt = ParagraphStyle("D", fontName=F, fontSize=9, textColor=GRAY, alignment=TA_CENTER)
footer = ParagraphStyle("F", fontName=F, fontSize=7, textColor=GRAY, alignment=TA_CENTER)
cb = ParagraphStyle("CB", fontName=F, fontSize=9, leading=15, textColor=DARK)
cc = ParagraphStyle("CC", fontName=F, fontSize=9, leading=15, textColor=HexColor("#333"))
ci = ParagraphStyle("CI", fontName=F, fontSize=11, leading=18, textColor=DARK, backColor=LIGHT_BG, borderPadding=14)

def div():
    t = Table([[""]], colWidths=[PW])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 1, GREEN)]))
    return t

def row(label, value):
    t = Table(
        [[Paragraph(f"<b>{label}</b>", cb), Paragraph(str(value), cc)]],
        colWidths=[PW*0.22, PW*0.78])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t

def tbl(h, r, cw):
    d = [[Paragraph(x, ParagraphStyle("HC", fontName=F, fontSize=9, textColor=WHITE, alignment=TA_CENTER)) for x in h]]
    for row_data in r:
        d.append([Paragraph(str(v), cc) for v in row_data])
    t = Table(d, colWidths=cw)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t

def build():
    doc = SimpleDocTemplate(
        "/Users/cyingfang/claude/deliverables/career/发表文章/社交关系AI管家_产品说明书v3.0.pdf",
        pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=35*mm, bottomMargin=35*mm
    )
    story = [Spacer(1, 40)]
    story.append(Paragraph("社交关系AI管家", title))
    story.append(Paragraph("产品说明书 v3.0", sub))
    story.append(Spacer(1, 6))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(Paragraph("Agent原生 · 微信生态深度嵌入 | 2026-06-13", dt))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "<b>一句话定义</b>：一个住在你微信里的AI管家——你不需要学任何东西，跟它聊天就够。<br/>"
        "使用方式：在微信里像跟朋友聊天一样跟它说话，它自动帮你打理所有人际关系。", ci))
    story.append(Spacer(1, 14))

    # 1. Core Experience
    story.append(Paragraph("一、核心体验：Agent原生，入口即聊天", h1s))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(Paragraph("它主动找你", h2s))
    story.append(tbl(
        ["AI行为", "触发时机"],
        [["张总的TS进展到哪了，需要今天问问吗？", "约定时间+2天"],
         ["你和王教授14天没联系了", "静默超过14天"],
         ["明天下午3点跟李总在国贸见面", "会面前一天"],
         ["检测到你刚给张总发了消息，要记录吗？", "发送消息后自动"]],
        [PW*0.50, PW*0.50]
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph("你找它说话", h2s))
    story.append(Paragraph(
        "跟它聊天就像跟一个特别细心的助理说话：不需要任何命令、斜杠指令或按钮。"
        "对话即操作。", body))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '"记一下：和张总聊了TS"  AI自动记录+提取待办<br/>'
        '"最近有啥要跟进的"  显示待办列表<br/>'
        '"帮我想想该联系谁"  分析冷却关系+推荐<br/>'
        '"给王教授拟个消息"  生成确认发送', body2))
    story.append(Spacer(1, 8))

    # 2. Auto Import
    story.append(Paragraph("二、自动导入微信通讯录", h1s))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(Paragraph("首次使用零配置：", h2s))
    story.append(Paragraph(
        "用户添加AI管家为微信好友 AI自动扫描通讯录 按频率排序推荐"
        " 用户勾选确认  AI开始为每个关键联系人建立档案", body2))
    story.append(Spacer(1, 4))
    story.append(Paragraph("自动提取的信息：", h2s))
    story.append(row("联系人备注/标签", "自动读取微信备注和标签分组"))
    story.append(row("最近聊天摘要", "仅限用户已参与的对话"))
    story.append(row("关系网络", "共同群聊和共同联系人"))
    story.append(Spacer(1, 4))
    story.append(Paragraph("隐私边界：只读取用户已参与的对话，不扫描未参与的群聊，所有数据本地处理，可随时删除。", body2))
    story.append(Spacer(1, 8))

    # 3. Architecture
    story.append(Paragraph("三、AI Agent 架构", h1s))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(row("用户层", "微信聊天界面（唯一的交互入口）"))
    story.append(row("AI管家Agent", "主动提醒(proactive) + 被动应答(reactive) + 消息生成发送"))
    story.append(row("核心引擎", "关系图谱(自动构建) + 时间线(自动记录) + 待办提醒(智能触发)"))
    story.append(row("连接层", "微信iLink + 通讯录导入 + 消息推送"))
    story.append(Spacer(1, 8))

    # 4. Conversation Design
    story.append(Paragraph("四、对话交互设计", h1s))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(Paragraph("每日节奏：不多不少，每天2-3条", h2s))
    story.append(Paragraph(
        "09:00 今日概览（待办+冷却关系）<br/>"
        "14:00 建议联系（基于地理位置或上下文）<br/>"
        "21:00 今日回顾（总结+建议）", body2))
    story.append(Spacer(1, 4))
    story.append(Paragraph('语音同样支持：发语音说"记一下"，AI回复文字确认。', body))
    story.append(Spacer(1, 8))

    # 5. Tech
    story.append(Paragraph("五、技术实现", h1s))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(row("已有基础设施", "cc-connect(微信接入) + wechat_push.py + engine.py + ai.py"))
    story.append(row("新增组件", "通讯录导入模块 + 对话意图识别 + 主动提醒引擎"))
    story.append(row("意图映射", "用户自然语言 AI判断意图 执行操作 回复结果"))
    story.append(Spacer(1, 8))

    # 6. User Acquisition
    story.append(Paragraph("六、用户获取", h1s))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(Paragraph("最简路径：加好友即用", h2s))
    story.append(Paragraph(
        '搜索添加好友 发送「你好」 AI回复说明 发送「导入通讯录」 开始自动扫描 发送「开始」 AI正式上岗', body2))
    story.append(Spacer(1, 4))
    story.append(Paragraph("推荐路径：朋友圈分享即用。用户分享使用体验到朋友圈，好友扫码直接添加。", body))
    story.append(Spacer(1, 8))

    # 7. Comparison
    story.append(Paragraph("七、v2.0 vs v3.0", h1s))
    story.append(div())
    story.append(Spacer(1, 6))
    story.append(tbl(
        ["维度", "v2.0 (CLI+Web)", "v3.0 (Agent原生)"],
        [["交互方式", "命令行/Web表单", "微信聊天/语音"],
         ["学习成本", "需记住命令", "零学习成本"],
         ["主动性", "用户发起", "AI主动发起"],
         ["通讯录", "手动录入", "自动导入"],
         ["入口", "终端/浏览器", "微信好友"],
         ["场景", "工作间隙打开", "融入日常聊天流"]],
        [PW*0.16, PW*0.37, PW*0.47]
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "<b>一句话</b>：你不用学怎么用——跟它聊天就行。",
        ParagraphStyle("OUT", fontName=F, fontSize=11, leading=18, textColor=DARK, backColor=LIGHT_BG, borderPadding=14)))
    story.append(Spacer(1, 20))
    story.append(Paragraph("-- End --", footer))
    doc.build(story, onFirstPage=hf, onLaterPages=hf)
    print("PDF OK")

if __name__ == "__main__":
    build()
