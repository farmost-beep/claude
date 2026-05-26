"""将幸福人生顶层文档 + 六大目标 Markdown 文档转换为 PDF"""
import os
import re
from fpdf import FPDF

GOALS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "deliverables")

GOAL_FILES = {
    "investment": "投资自由路线图",
    "career": "事业进阶路线图",
    "family": "子女成长支持计划",
    "health": "百岁健康计划",
    "ai": "AI能力提升路线图",
    "knowledge-base": "个人知识库与思维框架建设路线图",
}

OPS_FILES = {
    "investment": "投资自由操作手册",
    "career": "事业进阶操作手册",
    "family": "子女成长支持操作手册",
    "health": "百岁健康操作手册",
    "ai": "AI能力提升操作手册",
    "knowledge-base": "个人知识库与思维框架操作手册",
}

FONT_DIR = "/System/Library/Fonts"
FONT_REGULAR = os.path.join(FONT_DIR, "STHeiti Medium.ttc")

CONTENT_W = 170  # page width 210 - margins 20*2
LEFT_M = 20


class ChinesePDF(FPDF):
    def __init__(self, title):
        super().__init__()
        self.title_text = title
        self.add_font("CJK", "", FONT_REGULAR)
        self.add_font("CJK", "B", FONT_REGULAR)
        self.set_auto_page_break(True, 20)

    def header(self):
        self.set_font("CJK", "", 8)
        self.set_text_color(128, 128, 128)
        self.cell(CONTENT_W, 8, self.title_text, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("CJK", "", 8)
        self.set_text_color(128, 128, 128)
        self.cell(CONTENT_W, 10, f"{self.page_no()}", align="C")


def safe_multi_cell(pdf, w, h, text):
    """multi_cell that resets x to left margin first"""
    pdf.set_x(LEFT_M)
    # Filter out characters that fpdf can't render
    text = clean_text(text)
    if not text.strip():
        pdf.ln(h)
        return
    pdf.multi_cell(w, h, text)


def clean_text(text):
    """Remove markdown formatting and problematic characters"""
    text = text.replace("—", "——").replace("–", "-")
    text = text.replace(" ", " ")
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    # Italic
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    # Inline code
    text = re.sub(r"`(.+?)`", r"\1", text)
    # Links [text](url)
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    # Remove emoji and special unicode
    text = re.sub(r"[\U0001f300-\U0001f9ff]", "", text)
    # Checkbox characters
    text = text.replace("⬜", "[ ]").replace("✅", "[x]")
    # Stars
    text = text.replace("★", "*").replace("☆", "*")
    # Arrows
    text = text.replace("→", "->").replace("↓", "|").replace("→", "->")
    text = text.replace("≥", ">=").replace("≤", "<=")
    return text


def render_table_row(pdf, cells):
    col_w = CONTENT_W // len(cells)
    cleaned = [clean_text(c) for c in cells]

    # Estimate row height
    pdf.set_font("CJK", "", 8)
    max_lines = 1
    for c in cleaned:
        lines = pdf.multi_cell(col_w, 5, c, dry_run=True, output="LINES")
        max_lines = max(max_lines, len(lines))

    row_h = max_lines * 5 + 2

    if pdf.get_y() + row_h > 270:
        pdf.add_page()

    y_before = pdf.get_y()

    for i, c in enumerate(cleaned):
        pdf.set_xy(LEFT_M + i * col_w, y_before)
        if i == 0:
            pdf.set_fill_color(245, 245, 245)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.multi_cell(col_w, 5, c, border=0, fill=True)

    pdf.set_xy(LEFT_M, y_before + row_h)


def markdown_to_pdf(md_path, pdf_path, title):
    with open(md_path, "r") as f:
        lines = f.readlines()

    pdf = ChinesePDF(title)
    pdf.set_left_margin(LEFT_M)
    pdf.set_right_margin(LEFT_M)
    pdf.add_page()

    in_code = False
    skip_mermaid = False

    for line in lines:
        raw = line.rstrip()

        if skip_mermaid:
            if raw.strip().startswith("```"):
                skip_mermaid = False
            continue

        if raw.startswith("```mermaid"):
            skip_mermaid = True
            pdf.set_font("CJK", "", 9)
            pdf.set_text_color(128, 128, 128)
            safe_multi_cell(pdf, CONTENT_W, 6, "[图表略]")
            pdf.set_text_color(0, 0, 0)
            continue

        if raw.startswith("```"):
            in_code = not in_code
            continue

        if in_code:
            continue

        if raw.strip() == "---":
            pdf.set_draw_color(200, 200, 200)
            pdf.set_line_width(0.3)
            y = pdf.get_y()
            pdf.line(LEFT_M, y, LEFT_M + CONTENT_W, y)
            pdf.ln(6)
            continue

        if raw.strip() == "":
            pdf.ln(3)
            continue

        # Blockquote
        if raw.startswith("> "):
            text = raw[2:]
            pdf.set_font("CJK", "", 9)
            pdf.set_text_color(100, 100, 100)
            safe_multi_cell(pdf, CONTENT_W - 10, 5, text)
            pdf.set_text_color(0, 0, 0)
            continue

        # Table row
        if raw.startswith("|"):
            cells = [c.strip() for c in raw.split("|")[1:-1]]
            if all(re.match(r"^[-:]+$", c) for c in cells):
                continue
            render_table_row(pdf, cells)
            continue

        # Headings
        matched = False
        for level, size, bold in [(6, 8, False), (5, 9, False), (4, 10, True), (3, 12, True), (2, 14, True), (1, 18, True)]:
            prefix = "#" * level + " "
            if raw.startswith(prefix):
                text = raw[len(prefix):]
                pdf.ln(3)
                pdf.set_font("CJK", "B" if bold else "", size)
                pdf.set_text_color(0, 0, 0)
                safe_multi_cell(pdf, CONTENT_W, size * 1.3, text)
                pdf.ln(1)
                matched = True
                break

        if matched:
            continue

        # Regular paragraph
        pdf.set_font("CJK", "", 10)
        pdf.set_text_color(30, 30, 30)
        safe_multi_cell(pdf, CONTENT_W, 5.5, raw)

    pdf.output(pdf_path)


def main():
    # Top-level document
    top_md = os.path.join(GOALS_DIR, "幸福人生描述.md")
    top_pdf = os.path.join(GOALS_DIR, "幸福人生描述.pdf")
    if os.path.exists(top_md):
        print(f"Generating: 幸福人生描述.pdf ...")
        markdown_to_pdf(top_md, top_pdf, "幸福人生描述")
        print(f"  -> {top_pdf}")

    # 30-day launch plan
    launch_md = os.path.join(GOALS_DIR, "幸福人生30天启动计划.md")
    launch_pdf = os.path.join(GOALS_DIR, "幸福人生30天启动计划.pdf")
    if os.path.exists(launch_md):
        print(f"Generating: 幸福人生30天启动计划.pdf ...")
        markdown_to_pdf(launch_md, launch_pdf, "幸福人生30天启动计划")
        print(f"  -> {launch_pdf}")

    for key, name in GOAL_FILES.items():
        md_path = os.path.join(GOALS_DIR, key, f"{name}.md")
        pdf_path = os.path.join(GOALS_DIR, key, f"{name}.pdf")
        if os.path.exists(md_path):
            print(f"Generating: {name}.pdf ...")
            markdown_to_pdf(md_path, pdf_path, name)
            print(f"  -> {pdf_path}")
        else:
            print(f"SKIP (not found): {md_path}")

    for key, name in OPS_FILES.items():
        md_path = os.path.join(GOALS_DIR, key, f"{name}.md")
        pdf_path = os.path.join(GOALS_DIR, key, f"{name}.pdf")
        if os.path.exists(md_path):
            print(f"Generating: {name}.pdf ...")
            markdown_to_pdf(md_path, pdf_path, name)
            print(f"  -> {pdf_path}")
        else:
            print(f"SKIP (not found): {md_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
