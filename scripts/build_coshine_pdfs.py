#!/usr/bin/env python3
"""
Coshine 案例 PDF 构建器 — 简洁易读风格

专为 AI方法论案例文档设计：白底 + 石板蓝强调色，大字号，宽行距，极简封面。
与主 build_goal_pdfs.py 的金融服务建议书风格完全不同。

用法:
  python3 build_coshine_pdfs.py           # 生成全部5份Coshine PDF
  python3 build_coshine_pdfs.py --dry-run # 只列出文件不生成
"""

import os, re, sys
from datetime import date
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, KeepTogether)
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ====================================================================
# Font
# ====================================================================

FONT_DIR = "/System/Library/Fonts"
FONT_REGISTERED = False
for fp in [
    os.path.join(FONT_DIR, "STHeiti Medium.ttc"),
    os.path.join(FONT_DIR, "STHeiti Light.ttc"),
    os.path.join(FONT_DIR, "PingFang.ttc"),
]:
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
# Colors — clean slate + subtle blue accent
# ====================================================================

C_PRIMARY   = HexColor('#2C3E50')   # slate blue (headings)
C_ACCENT    = HexColor('#2980B9')   # blue accent (H3, links)
C_DARK      = HexColor('#1a1a2e')   # near-black (H2)
C_MUTED     = HexColor('#7F8C8D')   # muted grey (meta, caption)
C_TEXT      = HexColor('#2C3E50')   # body text (dark but not black)
C_TBL_HDR   = HexColor('#34495E')   # table header bg
C_TBL_ALT   = HexColor('#F8F9FA')   # table stripe (very light)
C_TBL_GRID  = HexColor('#DEE2E6')   # table grid (light border)
C_BLOCK_BG  = HexColor('#F0F4F8')   # blockquote bg
C_BORDER    = HexColor('#E9ECEF')   # light border for HR etc.
C_WHITE     = white

PAGE_W, PAGE_H = A4
CONTENT_W = PAGE_W - 2 * 2.2 * cm  # slightly tighter margins

# ====================================================================
# Paragraph styles — larger, more open
# ====================================================================

BODY_STYLE = ParagraphStyle('Body', fontName='CN', fontSize=11, leading=19,
    textColor=C_TEXT, spaceAfter=8, alignment=TA_JUSTIFY)

BLOCK_STYLE = ParagraphStyle('Block', fontName='CN', fontSize=10, leading=16,
    textColor=C_MUTED, spaceAfter=6, backColor=C_BLOCK_BG, borderPadding=10,
    leftIndent=6, rightIndent=6)

H1_STYLE = ParagraphStyle('H1', fontName='CNB', fontSize=18, leading=26,
    textColor=C_PRIMARY, spaceBefore=18, spaceAfter=10)

H2_STYLE = ParagraphStyle('H2', fontName='CNB', fontSize=14, leading=20,
    textColor=C_DARK, spaceBefore=14, spaceAfter=8)

H3_STYLE = ParagraphStyle('H3', fontName='CNB', fontSize=12, leading=17,
    textColor=C_ACCENT, spaceBefore=10, spaceAfter=6)

H4_STYLE = ParagraphStyle('H4', fontName='CNB', fontSize=11, leading=16,
    textColor=C_PRIMARY, spaceBefore=8, spaceAfter=4)

COVER_TITLE_STYLE = ParagraphStyle('CTitle', fontName='CNB', fontSize=24,
    leading=34, alignment=TA_CENTER, textColor=C_PRIMARY)

COVER_SUB_STYLE = ParagraphStyle('CSub', fontName='CN', fontSize=11, leading=16,
    alignment=TA_CENTER, textColor=C_MUTED)

COVER_TAG_STYLE = ParagraphStyle('CTag', fontName='CN', fontSize=9, leading=13,
    alignment=TA_CENTER, textColor=C_ACCENT)

TABLE_CELL_STYLE = ParagraphStyle('TCell', fontName='CN', fontSize=10, leading=14,
    textColor=C_TEXT)

TABLE_HDR_STYLE = ParagraphStyle('THdr', fontName='CNB', fontSize=10, leading=14,
    textColor=C_WHITE)

SMALL_STYLE = ParagraphStyle('Small', fontName='CN', fontSize=8, leading=12,
    textColor=C_MUTED, spaceAfter=4)

# ====================================================================
# Helpers
# ====================================================================

def thin_hr():
    return HRFlowable(width="100%", thickness=0.5, color=C_BORDER,
                       spaceAfter=8, spaceBefore=4)

def accent_hr():
    return HRFlowable(width="40%", thickness=1.5, color=C_ACCENT,
                       spaceAfter=12, spaceBefore=6)

def clean_text(text):
    text = text.replace("—", "——").replace("–", "-").replace("\xa0", " ")
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'`(.+?)`', r'<font face="Courier">\1</font>', text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    text = re.sub(r'[\U0001f300-\U0001f9ff\U0001fa00-\U0001ffff]', '', text)
    emoji_map = {"✅": "[OK]", "❌": "[--]", "⚠️": "[!!]", "📋": "[>>]", "🔴": "[!!]",
                 "🟡": "[~~]", "🟢": "[OK]", "⭐": "*", "📝": "[>>]", "📊": "[>>]",
                 "📐": "[>>]", "🎯": ">", "🔍": ">"}
    for k, v in emoji_map.items():
        text = text.replace(k, v)
    return text

def make_table(data, col_widths=None, header_rows=1):
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
        ('GRID', (0, 0), (-1, -1), 0.4, C_TBL_GRID),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
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
# Cover — minimal, clean
# ====================================================================

def build_cover(story, title_text):
    story.append(Spacer(1, 80))
    # Tag line
    story.append(Paragraph("AI Methodology Case Study", COVER_TAG_STYLE))
    story.append(Spacer(1, 16))
    # Main title
    display_title = re.sub(r'_\d{8}$', '', title_text)
    story.append(Paragraph(display_title, COVER_TITLE_STYLE))
    story.append(Spacer(1, 14))
    story.append(accent_hr())
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Chen Yingfang  /  {date.today().isoformat()}", COVER_SUB_STYLE))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Coshine  KaiXian  Payment Processor", COVER_TAG_STYLE))
    story.append(PageBreak())

# ====================================================================
# Markdown to story — same parser, different styles
# ====================================================================

def markdown_to_story(md_path, title_text):
    with open(md_path, 'r') as f:
        content = f.read()
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    lines = content.splitlines()
    story = []
    build_cover(story, title_text)

    in_code = False
    skip_mermaid = False
    table_buf = []
    kv_buf = []

    KV_RE = re.compile(r'^(?:\d+\.\s*|[-*]\s*)\*\*(.+?)\*\*\s*[：:-]\s*(.+)$')
    KV_SIMPLE_RE = re.compile(r'^[-*]\s+([^*\s][^：:]*?)[：:]\s*(.+)$')
    BULLET_RE = re.compile(r'^[-*]\s+(.+)$')
    bullet_buf = []

    def flush_table():
        nonlocal table_buf
        if not table_buf:
            return
        ncols = max(len(r) for r in table_buf)
        col_w = [CONTENT_W / ncols] * ncols
        t = make_table(table_buf, col_widths=col_w, header_rows=1)
        story.append(KeepTogether([t]))
        story.append(Spacer(1, 8))
        table_buf = []

    def flush_kv():
        nonlocal kv_buf
        if len(kv_buf) >= 2:
            data = [["Item", "Detail"]]
            for k, v in kv_buf:
                data.append([k, v])
            story.append(make_table(data, col_widths=[CONTENT_W * 0.2, CONTENT_W * 0.8]))
            story.append(Spacer(1, 6))
        elif len(kv_buf) == 1:
            k, v = kv_buf[0]
            story.append(Paragraph(f"<b>{clean_text(k)}</b>  {clean_text(v)}", BODY_STYLE))
        kv_buf = []

    def flush_bullets():
        nonlocal bullet_buf
        if len(bullet_buf) >= 2:
            data = [["Key Points"]]
            for item in bullet_buf:
                data.append([item])
            story.append(make_table(data, col_widths=[CONTENT_W]))
            story.append(Spacer(1, 6))
        elif len(bullet_buf) == 1:
            story.append(Paragraph(f"•  {clean_text(bullet_buf[0])}", BODY_STYLE))
        bullet_buf = []

    for line in lines:
        raw = line.rstrip()

        if skip_mermaid:
            if raw.strip().startswith("```"):
                skip_mermaid = False
            continue
        if raw.startswith("```mermaid"):
            skip_mermaid = True
            story.append(Paragraph("[ Diagram ]", SMALL_STYLE))
            continue

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
                continue
            table_buf.append(cells)
            continue
        else:
            flush_table()

        # HR
        if raw.strip() == "---":
            flush_kv()
            flush_bullets()
            story.append(Spacer(1, 4))
            story.append(thin_hr())
            story.append(Spacer(1, 4))
            continue

        # Blank lines
        if raw.strip() == "":
            flush_kv()
            flush_bullets()
            story.append(Spacer(1, 4))
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

        # Bullets
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
                        story.append(thin_hr())
                matched = True
                break
        if matched:
            continue

        # Body
        txt = clean_text(raw)
        if txt.strip():
            story.append(Paragraph(txt, BODY_STYLE))

    flush_kv()
    flush_bullets()
    flush_table()

    story.append(Spacer(1, 16))
    story.append(thin_hr())
    story.append(Paragraph(
        "Generated by AI  /  Coshine Case Study  /  Internal Use Only",
        SMALL_STYLE))
    return story

# ====================================================================
# Page template
# ====================================================================

def on_page(canvas, doc):
    if canvas.getPageNumber() == 1:
        return
    canvas.saveState()
    canvas.setStrokeColor(C_BORDER)
    canvas.setLineWidth(0.3)
    canvas.line(2.2 * cm, PAGE_H - 1.3 * cm, PAGE_W - 2.2 * cm, PAGE_H - 1.3 * cm)
    canvas.setFont('CN', 7)
    canvas.setFillColor(C_MUTED)
    canvas.drawString(2.2 * cm, PAGE_H - 1.1 * cm, clean_text(doc.title))
    canvas.line(2.2 * cm, 1.6 * cm, PAGE_W - 2.2 * cm, 1.6 * cm)
    canvas.drawCentredString(PAGE_W / 2, 1.1 * cm, str(canvas.getPageNumber()))
    canvas.restoreState()

# ====================================================================
# Build
# ====================================================================

def build_pdf(md_path, pdf_path, title_text):
    story = markdown_to_story(md_path, title_text)
    doc = SimpleDocTemplate(
        pdf_path, pagesize=A4,
        leftMargin=2.2 * cm, rightMargin=2.2 * cm,
        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        title=title_text,
        author="Chen Yingfang",
    )
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return pdf_path


CASE_DIR = Path("/Users/cyingfang/claude/deliverables/ai/AI方法论/案例/coshine")

FILES = [
    ("coshine_ai_strategy.md",         "Coshine AI Strategy Blueprint"),
    ("coshine_ai_progress.md",         "Coshine AI Implementation Progress"),
    ("coshine_phase_gates.md",         "Coshine AI Phase Gate Definitions"),
    ("coshine_methodology_mapping.md", "Coshine x AI Methodology Mapping"),
    ("coshine_competitive_scan.md",    "Coshine Competitive Intelligence"),
]

def main():
    is_dry = "--dry-run" in sys.argv
    generated = 0
    for fname, title in FILES:
        md = CASE_DIR / fname
        pdf = CASE_DIR / fname.replace(".md", ".pdf")
        if not md.exists():
            print(f"  SKIP: {fname} not found")
            continue
        if is_dry:
            print(f"  [DRY] {fname}  ->  {pdf.name}")
        else:
            build_pdf(str(md), str(pdf), title)
            print(f"  {fname}  ->  {pdf.name}")
        generated += 1
    tag = "(dry-run)" if is_dry else ""
    print(f"\nDone. {generated} PDFs {tag}")

if __name__ == "__main__":
    main()
