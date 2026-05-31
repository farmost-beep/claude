#!/usr/bin/env python3
"""Generate PDF for a single 公众号文章 using ReportLab."""
import os, re, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.colors import HexColor, black
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak)
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Font setup
FONT_DIR = "/System/Library/Fonts"
for fp in [os.path.join(FONT_DIR, "STHeiti Medium.ttc"),
           os.path.join(FONT_DIR, "PingFang.ttc")]:
    if os.path.exists(fp):
        try:
            pdfmetrics.registerFont(TTFont('CN', fp))
            pdfmetrics.registerFont(TTFont('CNB', fp))
            break
        except: continue

C_PRIMARY = HexColor('#1A2744')
C_ACCENT = HexColor('#c9a96e')
C_DARK = HexColor('#1a1a2e')
C_GRAY = HexColor('#808080')
C_TEXT = black
C_TBL_HDR = HexColor('#1A2744')
C_TBL_ALT = HexColor('#F5F7FC')
C_TBL_GRID = HexColor('#cccccc')
C_BLOCK_BG = HexColor('#F5F7FC')
C_WHITE = HexColor('#ffffff')

PAGE_W, PAGE_H = A4
CONTENT_W = PAGE_W - 4*cm

STYLES = {
    'body': ParagraphStyle('Body', fontName='CN', fontSize=10, leading=15,
        textColor=C_TEXT, spaceAfter=6, alignment=TA_JUSTIFY),
    'h1': ParagraphStyle('H1', fontName='CNB', fontSize=20, leading=26,
        textColor=C_PRIMARY, spaceAfter=10, spaceBefore=20),
    'h2': ParagraphStyle('H2', fontName='CNB', fontSize=14, leading=20,
        textColor=C_DARK, spaceAfter=8, spaceBefore=16),
    'quote': ParagraphStyle('Quote', fontName='CN', fontSize=9.5, leading=14,
        textColor=C_GRAY, spaceAfter=4, backColor=C_BLOCK_BG, borderPadding=8,
        leftIndent=8, rightIndent=8),
    'td': ParagraphStyle('TD', fontName='CN', fontSize=8.5, leading=12,
        textColor=C_TEXT),
    'th': ParagraphStyle('TH', fontName='CNB', fontSize=8.5, leading=12,
        textColor=C_WHITE),
}

def bold_text(text):
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)

def parse_md(filepath):
    """Parse markdown into flowables."""
    with open(filepath, encoding='utf-8') as f:
        lines = f.readlines()

    story = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        if not line.strip():
            story.append(Spacer(1, 6))
            i += 1; continue

        if line.strip() == '---':
            story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor('#dddddd')))
            story.append(Spacer(1, 4))
            i += 1; continue

        # H1
        if line.startswith('# '):
            t = bold_text(line[2:].strip())
            story.append(Paragraph(t, STYLES['h1']))
            i += 1; continue

        # H2
        if line.startswith('## '):
            t = bold_text(line[2:].strip())
            t = re.sub(r'<b>(.*?)</b>', r'<b>\1</b>', t)
            story.append(Paragraph(t, STYLES['h2']))
            i += 1; continue

        # Blockquote
        if line.startswith('>'):
            bq_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                c = lines[i].strip()[1:].strip()
                if c:
                    bq_lines.append(bold_text(c))
                i += 1
            story.append(Paragraph('<br/>'.join(bq_lines), STYLES['quote']))
            story.append(Spacer(1, 4))
            continue

        # Table
        if line.startswith('|') and line.strip().endswith('|'):
            tbl_rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                row_line = lines[i].strip()
                if re.match(r'^\|[\s:|-]+\|', row_line):
                    i += 1; continue  # skip separator
                cells = [c.strip() for c in row_line.split('|')[1:-1]]
                cells = [bold_text(c) for c in cells]
                tbl_rows.append(cells)
                i += 1
            if tbl_rows:
                col_w = CONTENT_W / len(tbl_rows[0])
                tbl_data = []
                for ri, row in enumerate(tbl_rows):
                    sty = STYLES['th'] if ri == 0 else STYLES['td']
                    tbl_data.append([Paragraph(c, sty) for c in row])
                t = Table(tbl_data, colWidths=[col_w]*len(tbl_rows[0]))
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), C_TBL_HDR),
                    ('TEXTCOLOR', (0,0), (-1,0), C_WHITE),
                    ('GRID', (0,0), (-1,-1), 0.5, C_TBL_GRID),
                    ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_TBL_ALT]),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('TOPPADDING', (0,0), (-1,-1), 4),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                    ('LEFTPADDING', (0,0), (-1,-1), 6),
                ]))
                story.append(t)
                story.append(Spacer(1, 8))
            continue

        # Bullet list
        if line.strip().startswith('- '):
            while i < len(lines) and lines[i].strip().startswith('- '):
                c = bold_text(lines[i].strip()[2:])
                story.append(Paragraph(f'  •  {c}', STYLES['body']))
                i += 1
            continue

        # Regular paragraph
        para_lines = []
        while i < len(lines) and lines[i].strip() and \
              not lines[i].strip().startswith('#') and \
              not lines[i].strip().startswith('>') and \
              not lines[i].strip().startswith('|') and \
              not lines[i].strip().startswith('- ') and \
              lines[i].strip() != '---':
            para_lines.append(lines[i].strip())
            i += 1
        t = bold_text(' '.join(para_lines))
        story.append(Paragraph(t, STYLES['body']))

    return story

if __name__ == '__main__':
    if len(sys.argv) < 2:
        md_path = '/Users/cyingfang/claude/deliverables/career/发表文章/公众号文章_给AI设边界_20260530.md'
    else:
        md_path = sys.argv[1]

    out_path = md_path.replace('.md', '.pdf')
    story = parse_md(md_path)

    doc = SimpleDocTemplate(out_path, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm,
        title='Mythos之后③：给AI设边界', author='陈颖芳')

    # Page number on every page
    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont('CN', 8)
        canvas.drawCentredString(PAGE_W/2, 1.5*cm, str(canvas.getPageNumber()))
        canvas.restoreState()

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"PDF saved: {out_path} ({os.path.getsize(out_path)} bytes)")
