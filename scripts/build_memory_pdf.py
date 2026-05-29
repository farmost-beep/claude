#!/usr/bin/env python3
"""生成Auto Memory全部记忆文件的合并PDF"""
import os, re, sys
from datetime import date
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak)
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_DIR = "/System/Library/Fonts"
for fp in [os.path.join(FONT_DIR, "STHeiti Medium.ttc"),
           os.path.join(FONT_DIR, "STHeiti Light.ttc"),
           os.path.join(FONT_DIR, "PingFang.ttc")]:
    if os.path.exists(fp):
        try:
            pdfmetrics.registerFont(TTFont('CN', fp))
            pdfmetrics.registerFont(TTFont('CNB', fp))
            break
        except Exception:
            continue

C_PRIMARY = HexColor('#2C3E50')
C_ACCENT  = HexColor('#2980B9')
C_MUTED   = HexColor('#7F8C8D')
C_TEXT    = HexColor('#2C3E50')
C_BORDER  = HexColor('#E9ECEF')
C_TBL_HDR = HexColor('#34495E')
C_TBL_ALT = HexColor('#F8F9FA')
C_TBL_GRID = HexColor('#DEE2E6')

PAGE_W, PAGE_H = A4
CONTENT_W = PAGE_W - 2 * 2.2 * cm

def clean(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'`(.+?)`', r'<font face="Courier">\1</font>', text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    return text

def parse_frontmatter(text):
    """Extract YAML frontmatter fields"""
    fields = {}
    if text.startswith('---'):
        end = text.find('---', 3)
        if end > 0:
            fm = text[3:end]
            for line in fm.split('\n'):
                line = line.strip()
                if ':' in line:
                    k, v = line.split(':', 1)
                    fields[k.strip()] = v.strip()
    return fields

MEMORY_DIR = Path("/Users/cyingfang/.claude/projects/-Users-cyingfang-claude/memory")
OUTPUT = Path("/Users/cyingfang/claude/deliverables/ai/Auto Memory 记忆文件汇编.pdf")

def main():
    # Collect memory files (skip MEMORY.md index)
    files = sorted([f for f in MEMORY_DIR.glob("*.md") if f.name != "MEMORY.md"])

    story = []
    # Cover
    story.append(Spacer(1, 100))
    story.append(Paragraph("Auto Memory", ParagraphStyle('ct', fontName='CNB',
        fontSize=28, leading=38, alignment=TA_CENTER, textColor=C_PRIMARY)))
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="30%", thickness=1.5, color=C_ACCENT, spaceAfter=12, spaceBefore=6))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"记忆文件汇编  |  {len(files)}份  |  {date.today().isoformat()}",
        ParagraphStyle('cs', fontName='CN', fontSize=10, leading=15, alignment=TA_CENTER, textColor=C_MUTED)))
    story.append(PageBreak())

    # TOC
    story.append(Paragraph("目录", ParagraphStyle('toc_h', fontName='CNB', fontSize=16,
        leading=24, textColor=C_PRIMARY, spaceAfter=12)))
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER, spaceAfter=10, spaceBefore=4))

    toc_data = [["#", "类型", "标题", "描述"]]
    for i, f in enumerate(files, 1):
        raw = f.read_text(encoding='utf-8')
        fm = parse_frontmatter(raw)
        mem_type = fm.get('type', '—')
        desc = fm.get('description', '—')
        name = fm.get('name', f.stem)
        toc_data.append([str(i), mem_type, name, desc[:80]])

    col_w = [CONTENT_W*0.05, CONTENT_W*0.07, CONTENT_W*0.33, CONTENT_W*0.55]
    toc_rows = []
    hdr_style = ParagraphStyle('th', fontName='CNB', fontSize=9, leading=13, textColor=white)
    cell_style = ParagraphStyle('tc', fontName='CN', fontSize=9, leading=13, textColor=C_TEXT)
    for ri, row in enumerate(toc_data):
        st = hdr_style if ri == 0 else cell_style
        toc_rows.append([Paragraph(clean(c), st) for c in row])

    t = Table(toc_rows, colWidths=col_w, repeatRows=1)
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.4, C_TBL_GRID),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,0), (-1,0), C_TBL_HDR),
    ] + [('BACKGROUND', (0,i), (-1,i), C_TBL_ALT) for i in range(2, len(toc_rows), 2)]))
    story.append(t)
    story.append(PageBreak())

    # Content
    h1 = ParagraphStyle('h1', fontName='CNB', fontSize=15, leading=22, textColor=C_PRIMARY, spaceAfter=8, spaceBefore=14)
    h2 = ParagraphStyle('h2', fontName='CNB', fontSize=12, leading=17, textColor=C_PRIMARY, spaceAfter=6, spaceBefore=10)
    body = ParagraphStyle('body', fontName='CN', fontSize=10, leading=16, textColor=C_TEXT, spaceAfter=6)
    mute = ParagraphStyle('mute', fontName='CN', fontSize=8, leading=12, textColor=C_MUTED)

    for i, f in enumerate(files, 1):
        raw = f.read_text(encoding='utf-8')
        fm = parse_frontmatter(raw)
        mem_type = fm.get('type', '—')
        name = fm.get('name', f.stem)
        desc = fm.get('description', '')

        story.append(Paragraph(f"{i}. {name}", h1))
        story.append(Paragraph(f"类型: {mem_type}  |  {desc}", mute))
        story.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER, spaceAfter=8, spaceBefore=4))

        # Strip frontmatter for body
        body_text = raw
        if raw.startswith('---'):
            end = raw.find('---', 3)
            if end > 0:
                body_text = raw[end+3:].strip()

        for line in body_text.split('\n'):
            line = line.rstrip()
            if not line.strip():
                story.append(Spacer(1, 4))
                continue
            if line.startswith('# '):
                story.append(Paragraph(clean(line[2:]), h1))
            elif line.startswith('## '):
                story.append(Paragraph(clean(line[3:]), h2))
            elif line.startswith('---'):
                story.append(HRFlowable(width="100%", thickness=0.3, color=C_BORDER, spaceAfter=6, spaceBefore=4))
            elif line.startswith('> '):
                story.append(Paragraph(clean(line[2:]), mute))
            elif line.startswith('|'):
                continue  # Skip tables in content view
            elif line.startswith('- '):
                story.append(Paragraph("  " + clean(line), body))
            else:
                story.append(Paragraph(clean(line), body))

        if i < len(files):
            story.append(PageBreak())

    # Build
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4,
        leftMargin=2.2*cm, rightMargin=2.2*cm, topMargin=1.8*cm, bottomMargin=1.8*cm,
        title="Auto Memory 记忆文件汇编", author="Chen Yingfang")

    def on_page(canvas, doc):
        if canvas.getPageNumber() == 1:
            return
        canvas.saveState()
        canvas.setStrokeColor(C_BORDER)
        canvas.setLineWidth(0.3)
        canvas.line(2.2*cm, PAGE_H-1.3*cm, PAGE_W-2.2*cm, PAGE_H-1.3*cm)
        canvas.setFont('CN', 6)
        canvas.setFillColor(C_MUTED)
        canvas.drawString(2.2*cm, PAGE_H-1.1*cm, "Auto Memory")
        canvas.drawCentredString(PAGE_W/2, 1.1*cm, str(canvas.getPageNumber()))
        canvas.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"Memory PDF: {OUTPUT} ({len(files)} files)")

if __name__ == "__main__":
    main()
