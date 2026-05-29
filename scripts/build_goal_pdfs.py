#!/usr/bin/env python3
"""将幸福人生六大目标 Markdown 文档转换为专业中文排版 PDF

引擎：ReportLab Platypus（精确排版，原生 CJK 支持）
风格参考：神州信息综合金融服务建议书(2).pdf (generate_pdf_v2.py)
"""

import os, re, sys
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import mm, cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, KeepTogether)
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ====================================================================
# Font setup
# ====================================================================

FONT_DIR = "/System/Library/Fonts"
FONT_PATHS = [
    os.path.join(FONT_DIR, "STHeiti Medium.ttc"),
    os.path.join(FONT_DIR, "STHeiti Light.ttc"),
    os.path.join(FONT_DIR, "PingFang.ttc"),
]
FONT_REGISTERED = False
for fp in FONT_PATHS:
    if os.path.exists(fp):
        try:
            pdfmetrics.registerFont(TTFont('CN', fp))
            pdfmetrics.registerFont(TTFont('CNB', fp))
            FONT_REGISTERED = True
            break
        except Exception:
            continue
if not FONT_REGISTERED:
    print("ERROR: No Chinese font found.")
    sys.exit(1)

# ====================================================================
# Colors — adapted from 神州信息 reference (green → navy, gold → orange)
# ====================================================================

C_PRIMARY   = HexColor('#1A2744')    # dark navy (headings, cover title)
C_ACCENT    = HexColor('#E07B2A')    # orange accent (cover HR, H3)
C_DARK      = HexColor('#1a1a2e')    # near-black (H2)
C_GRAY      = HexColor('#808080')    # grey (subtitle, blockquote text)
C_TEXT      = black                  # body text
C_TBL_HDR   = HexColor('#1A2744')    # table header background
C_TBL_ALT   = HexColor('#F5F7FC')    # table alternating row
C_TBL_GRID  = HexColor('#cccccc')    # table grid lines
C_RED       = HexColor('#cc0000')    # confidential / emphasis
C_BLOCK_BG  = HexColor('#F5F7FC')    # blockquote background
C_INPUT_BG  = HexColor('#FCF5ED')    # input block background
C_WHITE     = white

PAGE_W, PAGE_H = A4  # (595.27, 841.89) in points
CONTENT_W = PAGE_W - 4*cm  # usable width after 2cm margins

# ====================================================================
# Paragraph styles
# ====================================================================

BODY_STYLE = ParagraphStyle('Body', fontName='CN', fontSize=10, leading=15,
    textColor=C_TEXT, spaceAfter=6, alignment=TA_JUSTIFY)

BLOCK_STYLE = ParagraphStyle('Block', fontName='CN', fontSize=9.5, leading=14,
    textColor=C_GRAY, spaceAfter=4, backColor=C_BLOCK_BG, borderPadding=8,
    leftIndent=4, rightIndent=4)

INPUT_STYLE = ParagraphStyle('Input', fontName='CNB', fontSize=10, leading=15,
    textColor=C_PRIMARY, spaceAfter=6, backColor=C_INPUT_BG, borderPadding=8,
    borderColor=C_ACCENT, borderWidth=2, leftIndent=6, rightIndent=6)

H1_STYLE = ParagraphStyle('H1', fontName='CNB', fontSize=16, leading=22,
    textColor=C_PRIMARY, spaceBefore=14, spaceAfter=8)

H2_STYLE = ParagraphStyle('H2', fontName='CNB', fontSize=13, leading=18,
    textColor=C_DARK, spaceBefore=10, spaceAfter=6)

H3_STYLE = ParagraphStyle('H3', fontName='CNB', fontSize=11, leading=15,
    textColor=C_ACCENT, spaceBefore=8, spaceAfter=4)

H4_STYLE = ParagraphStyle('H4', fontName='CNB', fontSize=10.5, leading=14,
    textColor=C_DARK, spaceBefore=6, spaceAfter=3)

COVER_TITLE_STYLE = ParagraphStyle('CTitle', fontName='CNB', fontSize=22,
    leading=30, alignment=TA_CENTER, textColor=C_PRIMARY)

COVER_SUB_STYLE = ParagraphStyle('CSub', fontName='CN', fontSize=11, leading=16,
    alignment=TA_CENTER, textColor=C_GRAY)

COVER_CONF_STYLE = ParagraphStyle('CConf', fontName='CNB', fontSize=8, leading=11,
    alignment=TA_CENTER, textColor=C_RED)

TABLE_CELL_STYLE = ParagraphStyle('TCell', fontName='CN', fontSize=9, leading=13,
    textColor=C_TEXT)

TABLE_HDR_STYLE = ParagraphStyle('THdr', fontName='CNB', fontSize=9, leading=13,
    textColor=C_WHITE)

CAPTION_STYLE = ParagraphStyle('Caption', fontName='CN', fontSize=8, leading=11,
    textColor=C_GRAY, alignment=TA_CENTER, spaceBefore=4, spaceAfter=8)

SMALL_STYLE = ParagraphStyle('Small', fontName='CN', fontSize=8, leading=11,
    textColor=C_GRAY, spaceAfter=4)

# ====================================================================
# Helpers
# ====================================================================

def section_hr():
    """Full-width thin grey HR separator (matching reference)."""
    return HRFlowable(width="100%", thickness=0.5, color=C_TBL_GRID,
                       spaceAfter=6, spaceBefore=2)

def cover_hr():
    """Accent-colored HR for cover page."""
    return HRFlowable(width="100%", thickness=0.5, color=C_ACCENT,
                       spaceAfter=6, spaceBefore=6)

def clean_text(text):
    """Strip markdown formatting, emoji, and normalize punctuation."""
    text = text.replace("—", "——").replace("–", "-").replace("\xa0", " ")
    # Strip HTML comments (ReportLab XML parser chokes on <!-- ... -->)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    # Escape XML special chars to avoid parser errors
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Strip markdown formatting
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    # Strip emoji and special chars
    text = re.sub(r'[\U0001f300-\U0001f9ff\U0001fa00-\U0001ffff]', '', text)
    text = re.sub(r'[☀-➿⭐]', '', text)
    text = text.replace("✅", "[x]").replace("⬜", "[ ]").replace("❌", "[!]")
    text = text.replace("→", "→").replace("★", "★").replace("☆", "☆")
    text = text.replace("≥", "≥").replace("≤", "≤")
    text = text.replace("⚠", "!!").replace("❗", "!!")
    return text

def make_table(data, col_widths=None, header_rows=1):
    """Build a styled table matching the reference aesthetic.

    Args:
        data: list of lists (rows × cells), first rows are headers
        col_widths: optional list of column widths (points). If None, auto-equal.
        header_rows: number of header rows (styled with dark bg + white text)
    """
    if not data:
        return Spacer(1, 6)
    ncols = max(len(r) for r in data)
    norm = []
    for r in data:
        row = list(r)
        while len(row) < ncols:
            row.append("")
        norm.append(row)

    rows = []
    for ri, row in enumerate(norm):
        is_header = ri < header_rows
        st = TABLE_HDR_STYLE if is_header else TABLE_CELL_STYLE
        rows.append([Paragraph(clean_text(c), st) for c in row])

    if col_widths is None:
        col_widths = [CONTENT_W / ncols] * ncols

    t = Table(rows, colWidths=col_widths, repeatRows=header_rows)
    style_cmds = [
        ('GRID', (0, 0), (-1, -1), 0.5, C_TBL_GRID),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]
    for i in range(header_rows):
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), C_TBL_HDR))
        style_cmds.append(('TEXTCOLOR', (0, i), (-1, i), C_WHITE))
    for i in range(header_rows, len(rows)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), C_TBL_ALT))
    t.setStyle(TableStyle(style_cmds))
    return t

# ====================================================================
# Cover page builder
# ====================================================================

def build_cover(story, title_text):
    """Add a professional cover page matching the reference style."""
    story.append(Spacer(1, 60))              # 60pt top space
    # Clean title: strip date suffixes like _20260527
    display_title = re.sub(r'_\d{8}$', '', title_text)
    story.append(Paragraph(display_title, COVER_TITLE_STYLE))
    story.append(Spacer(1, 20))              # 20pt gap
    story.append(cover_hr())                 # accent HR
    story.append(Spacer(1, 10))              # 10pt gap
    story.append(Paragraph(f"陈颖芳  |  {date.today().isoformat()}", COVER_SUB_STYLE))
    story.append(Spacer(1, 20))              # 20pt gap
    story.append(Paragraph("个人资料 · 仅供学习研讨", COVER_CONF_STYLE))
    story.append(PageBreak())

# ====================================================================
# Markdown → ReportLab story
# ====================================================================

def markdown_to_story(md_path, title_text):
    """Parse a markdown file and return a ReportLab story (list of flowables)."""
    with open(md_path, 'r') as f:
        content = f.read()

    # Pre-process: strip HTML comments (ReportLab XML parser chokes on them)
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    lines = content.splitlines()

    story = []
    build_cover(story, title_text)

    # State
    in_input = False;      input_lines = []
    in_code  = False
    skip_mermaid = False
    table_buf = []         # pipe table buffer
    kv_buf = []            # key-value → 2-col table buffer
    bullet_buf = []        # bullet → single-col table buffer
    pending_caption = None
    tbl_counter = 0

    KV_RE = re.compile(r'^(?:\d+\.\s*|[-*]\s*)\*\*(.+?)\*\*\s*[：:—]\s*(.+)$')
    KV_SIMPLE_RE = re.compile(r'^[-*]\s+([^*\s][^：:]*?)[：:]\s*(.+)$')
    BULLET_RE = re.compile(r'^[-*]\s+(.+)$')

    def flush_table():
        nonlocal table_buf, pending_caption, tbl_counter
        if not table_buf:
            return
        ncols = max(len(r) for r in table_buf)
        col_w = [CONTENT_W / ncols] * ncols
        t = make_table(table_buf, col_widths=col_w, header_rows=1)
        # Keep tables together when possible
        story.append(KeepTogether([t]))
        if pending_caption:
            tbl_counter += 1
            story.append(Paragraph(f"表{tbl_counter}：{pending_caption}", CAPTION_STYLE))
            pending_caption = None
        else:
            story.append(Spacer(1, 6))
        table_buf = []

    def flush_kv():
        nonlocal kv_buf
        if len(kv_buf) >= 2:
            data = [["项目", "内容"]]
            for k, v in kv_buf:
                data.append([k, v])
            n = len(data[0])
            story.append(make_table(data, col_widths=[CONTENT_W*0.18, CONTENT_W*0.82]))
            story.append(Spacer(1, 4))
        elif len(kv_buf) == 1:
            k, v = kv_buf[0]
            story.append(Paragraph(f"<b>{clean_text(k)}</b>：{clean_text(v)}", BODY_STYLE))
        kv_buf = []

    def flush_bullets():
        nonlocal bullet_buf
        if len(bullet_buf) >= 2:
            data = [["要点"]]
            for item in bullet_buf:
                data.append([item])
            story.append(make_table(data, col_widths=[CONTENT_W]))
            story.append(Spacer(1, 4))
        elif len(bullet_buf) == 1:
            txt = f"•  {clean_text(bullet_buf[0])}"
            story.append(Paragraph(txt, BODY_STYLE))
        bullet_buf = []

    for line in lines:
        raw = line.rstrip()

        # Mermaid blocks → placeholder
        if skip_mermaid:
            if raw.strip().startswith("```"):
                skip_mermaid = False
            continue
        if raw.startswith("```mermaid"):
            skip_mermaid = True
            story.append(Paragraph("[ 图表 ]", SMALL_STYLE))
            continue

        # Input blocks (our custom extension)
        if raw.startswith("```input"):
            in_input = True
            input_lines = []
            continue
        if in_input:
            if raw.startswith("```"):
                in_input = False
                if input_lines:
                    txt = "\n".join(input_lines)
                    story.append(Paragraph(clean_text(txt), INPUT_STYLE))
                    story.append(Spacer(1, 2))
                input_lines = []
                continue
            input_lines.append(raw)
            continue

        # Generic code blocks → skip
        if raw.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue

        # Pipe tables
        if raw.strip().startswith("|"):
            flush_kv()
            flush_bullets()
            cells = [c.strip() for c in raw.split("|")[1:-1]]
            if all(re.match(r'^[-:\s]+$', c) for c in cells):
                continue  # separator row
            table_buf.append(cells)
            continue
        else:
            flush_table()

        # Table captions
        m = re.match(r'^\*?表(\d+)[：:](.+?)\*?$', raw.strip())
        if m and not raw.strip().startswith("表现"):
            pending_caption = m.group(2).strip()
            continue

        # Horizontal rules
        if raw.strip() == "---":
            flush_kv()
            flush_bullets()
            story.append(Spacer(1, 4))
            story.append(section_hr())
            story.append(Spacer(1, 4))
            continue

        # Blank lines
        if raw.strip() == "":
            flush_kv()
            flush_bullets()
            story.append(Spacer(1, 3))
            continue

        # Blockquotes
        if raw.startswith("> "):
            flush_kv()
            flush_bullets()
            story.append(Paragraph(clean_text(raw[2:]), BLOCK_STYLE))
            continue

        # KV detection
        kv_match = KV_RE.match(raw.strip())
        if kv_match:
            kv_buf.append((kv_match.group(1).strip(), kv_match.group(2).strip()))
            continue
        kv_simple = KV_SIMPLE_RE.match(raw.strip())
        if kv_simple:
            kv_buf.append((kv_simple.group(1).strip(), kv_simple.group(2).strip()))
            continue
        flush_kv()

        # Bullet detection
        bm = BULLET_RE.match(raw.strip())
        if bm:
            bullet_buf.append(bm.group(1).strip())
            continue
        flush_bullets()

        # Headings
        matched = False
        for level in range(6, 0, -1):
            prefix = "#" * level + " "
            if raw.startswith(prefix):
                txt = clean_text(raw[len(prefix):])
                style_map = {1: H1_STYLE, 2: H2_STYLE, 3: H3_STYLE, 4: H4_STYLE}
                st = style_map.get(level)
                if st:
                    story.append(Paragraph(txt, st))
                    if level <= 2:
                        story.append(section_hr())
                matched = True
                break
        if matched:
            continue

        # Body paragraph
        txt = clean_text(raw)
        if txt.strip():
            story.append(Paragraph(txt, BODY_STYLE))

    # Flush remaining buffers
    flush_kv()
    flush_bullets()
    flush_table()

    # Disclaimer footer on last page
    story.append(Spacer(1, 12))
    story.append(section_hr())
    story.append(Paragraph(
        "本文件由AI辅助生成，内容仅供参考。｜ 个人资料 · 仅供学习研讨",
        SMALL_STYLE))

    return story

# ====================================================================
# Page template (headers / footers)
# ====================================================================

def on_page(canvas, doc):
    """Draw page header and footer (skip cover)."""
    if canvas.getPageNumber() == 1:
        return
    canvas.saveState()
    # Header line
    canvas.setStrokeColor(C_TBL_GRID)
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, PAGE_H - 1.5*cm, PAGE_W - 2*cm, PAGE_H - 1.5*cm)
    canvas.setFont('CN', 7)
    canvas.setFillColor(C_GRAY)
    canvas.drawString(2*cm, PAGE_H - 1.3*cm, clean_text(doc.title))
    # Footer
    canvas.setStrokeColor(C_TBL_GRID)
    canvas.setLineWidth(0.3)
    canvas.line(2*cm, 1.8*cm, PAGE_W - 2*cm, 1.8*cm)
    canvas.setFont('CN', 7)
    canvas.drawCentredString(PAGE_W / 2, 1.3*cm, f"— {canvas.getPageNumber()} —")
    canvas.restoreState()

# ====================================================================
# Single file builder
# ====================================================================

def build_pdf(md_path, pdf_path, title_text):
    """Convert one markdown file to PDF."""
    story = markdown_to_story(md_path, title_text)
    doc = SimpleDocTemplate(
        pdf_path, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title=title_text,
        author="陈颖芳",
    )
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return pdf_path

# ====================================================================
# File inventory
# ====================================================================

GOALS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "deliverables")

GOAL_FILES = {
    "investment":     "投资框架/投资自由路线图",
    "career":         "路线图/事业进阶路线图",
    "family":         "子女成长/子女成长支持计划",
    "health":         "路线图/百岁健康计划",
    "ai":             "路线图/AI能力提升路线图",
    "knowledge-base": "路线图/个人知识库与思维框架建设路线图",
}

OPS_FILES = {
    "investment":     "投资框架/投资自由操作手册",
    "career":         "路线图/事业进阶操作手册",
    "family":         "子女成长/子女成长支持操作手册",
    "health":         "路线图/百岁健康操作手册",
    "ai":             "路线图/AI能力提升操作手册",
    "knowledge-base": "路线图/个人知识库与思维框架操作手册",
}

EXEC_FILES = {
    "investment": ["执行清单/9月还本作战计划", "执行清单/持仓分析与操作建议_20260527", "执行清单/6月投资行动清单_20260527", "执行清单/银行电话询问脚本_20260528"],
    "career":     ["民建与职称/入库与职称攻坚计划", "执行清单/事业6月冲刺清单_20260527"],
    "family":     ["考研支持/考研暑假执行计划"],
    "health":     ["执行清单/6月健康启动执行包"],
    "ai":         ["执行与简报/AI能力6月执行包"],
    "knowledge-base": ["执行清单/知识库6月建设执行包"],
}

STANDALONE = [
    ("career", "科技金融/科技金融方法论"),
    ("career", "科技金融方法论/中级经济师_经济学基础_学习笔记"),
    ("career", "科技金融/中国科技金融市场全景_20260527"),
    ("career", "科技金融/上海孵化基地调研报告_20260527"),
    ("career", "客户方案/客户拜访简报_神州信息_20260527"),
    ("career", "客户方案/客户拜访简报_上海微电子设计_20260527"),
    ("career", "客户方案/交易筛查备忘录_AI芯片公司_20260527"),
    ("career", "执行清单/事业AI加速方案_20260527"),
    ("career", "科技金融/发表文章_科技金融生态方法论_20260527"),
    ("career", "科技金融/AI产业链事业加速方案_20260527"),
    ("career", "民建与职称/民建社情民意-并购贷款与科创金融生态"),
    ("career", "客户方案/上海光机所杭州光机所合作方案_20260527"),
    ("career", "客户方案/神州信息综合金融服务方案_20260527"),
    ("career", "客户方案/上海微电子设计有限公司_综合金融服务方案_20260527"),
    ("career", "客户方案/张江高科895孵化器_综合金融服务方案_20260527"),
    ("career", "客户方案/莘泽智星港孵化器_综合金融服务方案_20260527"),
    ("career", "客户方案/司南半导体超级孵化器_综合金融服务方案_20260527"),
    ("career", "客户方案/杭州光机所孵化器_综合金融服务方案_20260527"),
    ("career", "客户方案/羲和光谷光电产业孵化器_综合金融服务方案_20260527"),
    ("career", "客户方案/上海芯旺微电子_综合金融服务方案_20260527"),
    ("career", "客户方案/脑虎科技_综合金融服务方案_20260527"),
    ("career", "客户方案/南京先进激光技术研究院_综合金融服务方案_20260527"),
    ("ai", "执行与简报/每日AI简报_202605"),
    ("ai", "执行与简报/每日AI前沿收集_20260527"),
    ("ai", "AI方法论/逆向探索Anthropic方法论_20260527"),
    ("ai", "AI方法论/快速掌握AI手册_20260527"),
    ("ai", "AI方法论/快速学习Harness手册_20260527"),
    ("ai", "AI方法论/AI方法论完整手册_20260529"),
    ("ai", "AI方法论/Boris Cherny工作方式手册_20260529"),
    ("ai", "绿色工厂/2026中国绿色工厂科技创新指数白皮书_重构版"),
    ("ai", "AI与知识库/AI与知识库升级方案_20260527"),
    ("ai", "AI与知识库/AI产业链学习与知识库方案_20260527"),
    ("ai", "Claude_Code/Claude Code使用精通手册"),
    ("ai", "Claude_Code/Claude Code命令使用场景手册"),
    ("ai", "Claude_Code/Claude Code内建命令手册"),
    ("ai", "Claude_Code/Claude插件使用场景手册"),
    ("ai", "Claude_Code/快速学习Claude_Code手册_20260527"),
    ("ai", "Claude_Code/一天学会Claude_Code_20260527"),
    ("investment", "投资框架/30年个人投资框架_哲学与底层逻辑"),
    ("investment", "投资框架/投资思维框架_Margin_Discipline_Freedom_演讲稿_20260527"),
    ("investment", "量化与AI产业链/量化策略框架_20260527"),
    ("investment", "量化与AI产业链/AI全产业链研究报告_20260527"),
    ("investment", "量化与AI产业链/AI产业链投资行动方案_20260527"),
    ("investment", "量化与AI产业链/脑机接口行业研究报告_20260527"),
    ("investment", "量化与AI产业链/昆仑万维首次覆盖报告_20260527"),
    ("investment", "执行清单/6月第1周投资执行清单_20260527"),
    ("family", "家庭AI/家庭AI支持方案_20260527"),
    ("family", "家庭AI/AI工具推荐_家庭场景_20260527"),
    ("family", "考研支持/考研AI辅助系统_启动包"),
    ("family", "考研支持/考研AI辅助系统_错题库"),
    ("family", "考研支持/考研AI辅助系统_进度周报"),
    ("family", "考研支持/上海大学考研完全手册_20260527"),
    ("health", "AI健康/健康AI支持方案_20260527"),
    ("health", "AI健康/AI健康工具推荐_20260527"),
    ("health", "执行清单/6月1日基线采集清单_20260527"),
]

CROSSCUT = [
    "幸福人生AI增强仪表盘_20260527",
    "AI产业链驱动_幸福人生总方案_20260527",
    "中科大校友资源_六目标行动方案_20260527",
    "浙江籍贯资源_六目标行动方案_20260527",
    "民建会员资源_六目标行动方案_20260527",
    "资源圈拓展方案_20260527",
    "人脉资源手册_20260527",
]

# ====================================================================
# Main
# ====================================================================

def main():
    total = 0
    today_label = date.today().isoformat()

    def build(folder, name, label):
        nonlocal total
        md_path = os.path.join(GOALS_DIR, folder, f"{name}.md")
        pdf_path = os.path.join(GOALS_DIR, folder, f"{name}.pdf")
        if os.path.exists(md_path):
            print(f"  [{label}] {name}.md → {name}.pdf")
            build_pdf(md_path, pdf_path, label)
            total += 1
        else:
            print(f"  SKIP (not found): {md_path}")

    def build_root(name, label):
        nonlocal total
        md_path = os.path.join(GOALS_DIR, f"{name}.md")
        pdf_path = os.path.join(GOALS_DIR, f"{name}.pdf")
        if os.path.exists(md_path):
            print(f"  [{label}] {name}.md → {name}.pdf")
            build_pdf(md_path, pdf_path, label)
            total += 1
        else:
            print(f"  SKIP (not found): {md_path}")

    print(f"=== 幸福人生 PDF 构建 ({today_label}) — ReportLab 引擎 ===\n")

    # Root cross-cutting docs
    build_root("幸福人生描述", "幸福人生描述")
    build_root("幸福人生30天启动计划", "幸福人生30天启动计划")
    build_root("能力圈短板报告与改进方案_20260527", "能力圈短板报告与改进方案")

    # Goal framework + operations + exec
    for key, name in GOAL_FILES.items():
        build(key, name, name)
    for key, name in OPS_FILES.items():
        build(key, name, name)
    for key, names in EXEC_FILES.items():
        for name in names:
            build(key, name, name)

    # Standalone files
    for folder, name in STANDALONE:
        build(folder, name, name)

    # Root cross-cutting
    for name in CROSSCUT:
        build_root(name, name)

    # Auto-discover any remaining .md files not yet processed
    auto_count = 0
    for root, dirs, files in os.walk(GOALS_DIR):
        for f in files:
            if not f.endswith('.md'):
                continue
            md_path = os.path.join(root, f)
            pdf_path = md_path.replace('.md', '.pdf')
            if not os.path.exists(pdf_path):
                rel = os.path.relpath(md_path, GOALS_DIR)
                folder = os.path.dirname(rel)
                name = f[:-3]  # strip .md
                label = name.replace('_', ' ')[:40]
                if folder:
                    build(folder, name, label)
                else:
                    build_root(name, label)
                auto_count += 1

    if auto_count:
        print(f"\n(Auto-discovered {auto_count} new files.)")

    print(f"\nDone. {total} PDFs generated.")

if __name__ == "__main__":
    main()
