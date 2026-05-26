"""将幸福人生顶层文档 + 六大目标 Markdown 文档转换为专业中文排版 PDF"""
import os
import re
from fpdf import FPDF
from datetime import date

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

EXEC_FILES = {
    "investment": ["9月还本作战计划", "持仓分析与操作建议_20260527", "6月投资行动清单_20260527"],
    "career": ["入库与职称攻坚计划", "事业6月冲刺清单_20260527"],
    "family": ["考研暑假执行计划"],
    "health": ["6月健康启动执行包"],
    "ai": ["AI能力6月执行包"],
    "knowledge-base": ["知识库6月建设执行包"],
}

FONT_DIR = "/System/Library/Fonts"
FONT_HEITI   = os.path.join(FONT_DIR, "STHeiti Medium.ttc")
FONT_HEITI_L = os.path.join(FONT_DIR, "STHeiti Light.ttc")
FONT_SONGTI  = "/System/Library/Fonts/Supplemental/Songti.ttc"

C_ACCENT   = (0, 122, 61)
C_DARK     = (30, 33, 40)
C_GRAY     = (120, 120, 128)
C_LIGHT_BG = (248, 249, 250)
C_WHITE    = (255, 255, 255)
C_TBL_HEAD = (40, 44, 52)
C_TBL_ROW  = (245, 246, 248)

CONTENT_W = 168
LEFT_M    = 21

class ProfPDF(FPDF):
    def __init__(self, title, author="陈颖芳"):
        super().__init__()
        self.title_text = title
        self.author = author
        self.today = date.today().isoformat()

        ok = lambda p: os.path.exists(p)
        self.add_font("HT",  "",  FONT_HEITI)
        self.add_font("HT",  "B", FONT_HEITI)
        self.add_font("HTL", "",  FONT_HEITI_L if ok(FONT_HEITI_L) else FONT_HEITI)
        self.add_font("ST",  "",  FONT_SONGTI if ok(FONT_SONGTI) else FONT_HEITI)
        self.add_font("ST",  "B", FONT_SONGTI if ok(FONT_SONGTI) else FONT_HEITI)

        self.set_auto_page_break(True, 28)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_draw_color(*C_ACCENT)
        self.set_line_width(0.5)
        self.line(LEFT_M, 13, LEFT_M + CONTENT_W, 13)
        self.set_font("HT", "", 6.5)
        self.set_text_color(*C_GRAY)
        self.set_y(15)
        self.cell(CONTENT_W, 4, self.title_text, align="L")
        self.ln(7)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-22)
        self.set_draw_color(210, 210, 215)
        self.set_line_width(0.15)
        self.line(LEFT_M, self.get_y(), LEFT_M + CONTENT_W, self.get_y())
        self.ln(3)
        self.set_font("HT", "", 7)
        self.set_text_color(*C_GRAY)
        self.cell(CONTENT_W, 7, f"— {self.page_no()} —", align="C")

    def cover_page(self, show_author=True, show_goals=True):
        self.add_page()
        self.set_fill_color(*C_ACCENT)
        self.rect(0, 0, 210, 100, "F")
        self.set_y(28)
        self.set_font("HT", "B", 26)
        self.set_text_color(*C_WHITE)
        self.multi_cell(CONTENT_W, 15, self.title_text, align="C")
        self.ln(5)
        self.set_draw_color(*C_WHITE)
        self.set_line_width(0.3)
        mid = 105
        self.line(mid - 30, self.get_y(), mid + 30, self.get_y())
        self.ln(12)
        if show_author:
            self.set_font("ST", "", 12)
            self.set_text_color(*C_WHITE)
            self.cell(CONTENT_W, 9, f"{self.author}   {self.today}", align="C")
            self.ln(24)
        if show_goals:
            self.set_font("HT", "", 10)
            self.set_text_color(*C_GRAY)
            self.cell(CONTENT_W, 7, "投资成功 · 事业进阶 · 家庭支持 · 百岁健康 · AI能力 · 知识库", align="C")

    def body(self, text):
        self.set_font("ST", "", 10.5)
        self.set_text_color(*C_DARK)
        self.set_x(LEFT_M)
        text = clean_text(text)
        if not text.strip():
            self.ln(4)
            return
        # Indent first line with 2-em space for body paragraphs
        stripped = text.lstrip()
        if stripped and not stripped.startswith(("-", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "0.", "┌", "├", "│", "└", " ")):
            indent = "　　"  # 2 full-width spaces = 2em
            text = indent + stripped
        self.multi_cell(CONTENT_W, 5.9, text)

    def heading(self, level, text):
        font_specs = {
            1: ("HT", "B", 22, 12),
            2: ("HT", "B", 15, 9),
            3: ("HT", "B", 12, 7),
            4: ("HT", "B", 11, 6),
            5: ("HT", "B", 10.5, 5),
        }
        font, style, sz, gap = font_specs.get(level, ("HT", "B", 10.5, 4))
        self.ln(gap)
        if level <= 2:
            self.set_fill_color(*C_ACCENT)
            y = self.get_y()
            self.rect(LEFT_M, y + (sz * 0.12), 2.5, sz * 0.32, "F")
            self.set_x(LEFT_M + 6)
        self.set_font(font, style, sz)
        self.set_text_color(*C_DARK)
        w = CONTENT_W - (6 if level <= 2 else 0)
        self.multi_cell(w, sz * 0.56, text)
        self.ln(1.5 if level <= 2 else 0.5)

    def blockquote(self, text):
        text = clean_text(text)
        self.set_font("ST", "", 10)
        self.set_text_color(55, 65, 60)
        y0 = self.get_y()
        self.set_x(LEFT_M)
        # Measure height by writing invisible text first, then draw
        self.set_font("ST", "", 10)
        # Estimate: each line takes ~7pt, count approximate lines
        chars_per_line = int((CONTENT_W - 10) / 3.53)  # CJK char ~10pt=3.53mm wide
        lines = max(1, len(text) // chars_per_line + text.count("\n") + 1)
        est_h = lines * 7.5 + 6

        # Draw left accent bar
        self.set_fill_color(*C_ACCENT)
        self.set_draw_color(*C_ACCENT)
        self.rect(LEFT_M, y0, 2.5, est_h, "F")
        # Light bg
        self.set_fill_color(243, 248, 244)
        self.rect(LEFT_M + 2.5, y0, CONTENT_W - 2.5, est_h, "F")
        self.set_xy(LEFT_M + 8, y0 + 4)
        self.multi_cell(CONTENT_W - 10, 7, text)
        self.set_text_color(*C_DARK)
        self.ln(3)

    def hr(self):
        self.ln(3)
        y = self.get_y()
        self.set_draw_color(210, 210, 215)
        self.set_line_width(0.15)
        self.set_x(LEFT_M)
        self.line(LEFT_M, y, LEFT_M + 60, y)
        self.ln(5)

    def table(self, rows):
        if not rows:
            return
        # Normalize all rows to same column count
        ncols = max(len(r) for r in rows)
        norm = []
        for r in rows:
            row = [clean_text(c) for c in r]
            while len(row) < ncols:
                row.append("")
            norm.append(row)

        # Estimate CJK-aware character width per column
        def cjk_len(s):
            n = 0
            for ch in s:
                n += 2 if '一' <= ch <= '鿿' or '　' <= ch <= '〿' or '＀' <= ch <= '￯' else 1
            return max(n, 1)

        col_weights = []
        for ci in range(ncols):
            max_len = max(cjk_len(r[ci]) for r in norm)
            col_weights.append(max_len)

        total_w = sum(col_weights)
        min_w = 22  # minimum column width in mm
        col_w = []
        for w in col_weights:
            cw = max(min_w, (w / total_w) * CONTENT_W)
            col_w.append(cw)

        # Scale down if total exceeds CONTENT_W
        scale = CONTENT_W / sum(col_w)
        if scale < 1.0:
            col_w = [w * scale for w in col_w]

        tbl_font_sz = 8.5
        line_h = 5.5
        pad = 1.8  # cell padding each side

        def draw_cell(x, y, w, text, font_style="", fill_color=None, align="L"):
            self.set_xy(x + pad, y + 0.8)
            if fill_color:
                self.set_fill_color(*fill_color)
            self.set_font("HT" if font_style == "B" else "ST", font_style, tbl_font_sz)
            self.multi_cell(w - pad * 2, line_h, text, border=0, fill=fill_color is not None, align=align)
            return self.get_y()

        def draw_row_border(y, heights):
            self.set_draw_color(220, 224, 228)
            self.set_line_width(0.08)
            row_h = max(heights) + 1.6
            x = LEFT_M
            for ci in range(ncols):
                self.rect(x, y, col_w[ci], row_h, "D")
                x += col_w[ci]

        # Header
        self.set_text_color(*C_WHITE)
        y_start = self.get_y()
        h_heights = []
        x = LEFT_M
        for ci in range(ncols):
            cell_h = draw_cell(x, y_start, col_w[ci], norm[0][ci], "B", C_TBL_HEAD, "C") - y_start
            h_heights.append(cell_h)
            x += col_w[ci]
        draw_row_border(y_start, h_heights)
        self.set_y(y_start + max(h_heights) + 1.6)

        # Data rows
        for ri, row in enumerate(norm[1:], 1):
            if all(re.match(r"^[-:\s]+$", c) for c in row):
                continue
            fill = C_TBL_ROW if ri % 2 == 0 else C_WHITE
            self.set_text_color(*C_DARK)
            yr = self.get_y()
            d_heights = []
            x = LEFT_M
            for ci in range(ncols):
                ch = draw_cell(x, yr, col_w[ci], row[ci], "", fill) - yr
                d_heights.append(ch)
                x += col_w[ci]
            draw_row_border(yr, d_heights)
            self.set_y(yr + max(d_heights) + 1.6)

        self.ln(3)


def clean_text(text):
    text = text.replace("—", "——").replace("–", "-")
    text = text.replace("\xa0", " ")
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    text = re.sub(r"[\U0001f300-\U0001f9ff]", "", text)
    text = text.replace("⬜", "[ ]").replace("✅", "[x]")
    text = text.replace("★", "*").replace("☆", "*")
    text = text.replace("→", "->").replace("↓", "|")
    text = text.replace("≥", ">=").replace("≤", "<=")
    text = text.replace("⭐", "*").replace("⚠", "!!").replace("❗", "!!")
    text = text.replace("✏", "").replace("\U0001f4cc", "").replace("\U0001f4a1", "")
    text = text.replace("\U0001f4ca", "").replace("\U0001f4c5", "").replace("\U0001f3c6", "")
    return text


def markdown_to_pdf(md_path, pdf_path, title, **kwargs):
    with open(md_path, "r") as f:
        lines = f.readlines()

    pdf = ProfPDF(title)
    pdf.set_left_margin(LEFT_M)
    pdf.set_right_margin(LEFT_M)
    pdf.cover_page(**kwargs)

    in_code = False
    skip_mermaid = False
    table_buffer = []

    def flush_table():
        nonlocal table_buffer
        if table_buffer:
            pdf.table(table_buffer)
            pdf.ln(4)
            table_buffer = []

    for line in lines:
        raw = line.rstrip()

        if skip_mermaid:
            if raw.strip().startswith("```"):
                skip_mermaid = False
            continue
        if raw.startswith("```mermaid"):
            skip_mermaid = True
            pdf.set_font("HT", "", 8)
            pdf.set_text_color(*C_GRAY)
            pdf.set_x(LEFT_M)
            pdf.cell(CONTENT_W, 6, "[ 图表 ]", align="C")
            pdf.set_text_color(*C_DARK)
            pdf.ln(8)
            continue

        if raw.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue

        if raw.strip().startswith("|") and not raw.strip().startswith("| "):
            cells = [c.strip() for c in raw.split("|")[1:-1]]
            if all(re.match(r"^[-:\s]+$", c) for c in cells):
                continue
            table_buffer.append(cells)
            continue
        else:
            flush_table()

        if raw.strip() == "---":
            pdf.hr()
            continue

        if raw.strip() == "":
            pdf.ln(3)
            continue

        if raw.startswith("> "):
            pdf.blockquote(raw[2:])
            continue

        matched = False
        for level in range(6, 0, -1):
            prefix = "#" * level + " "
            if raw.startswith(prefix):
                pdf.heading(level, raw[len(prefix):])
                matched = True
                break
        if matched:
            continue

        pdf.body(raw)

    flush_table()
    pdf.output(pdf_path)


def main():
    total = 0
    today_label = date.today().isoformat()

    def build(md_path, pdf_path, label, **kwargs):
        nonlocal total
        if os.path.exists(md_path):
            print(f"  [{label}] {os.path.basename(md_path)} -> {os.path.basename(pdf_path)}")
            markdown_to_pdf(md_path, pdf_path, label, **kwargs)
            total += 1
        else:
            print(f"  SKIP (not found): {md_path}")

    print(f"=== 幸福人生 PDF 构建 ({today_label}) ===\n")

    build(os.path.join(GOALS_DIR, "幸福人生描述.md"),
          os.path.join(GOALS_DIR, "幸福人生描述.pdf"), "幸福人生描述")
    build(os.path.join(GOALS_DIR, "幸福人生30天启动计划.md"),
          os.path.join(GOALS_DIR, "幸福人生30天启动计划.pdf"), "幸福人生30天启动计划")
    build(os.path.join(GOALS_DIR, "6月综合行动仪表盘_20260527.md"),
          os.path.join(GOALS_DIR, "6月综合行动仪表盘_20260527.pdf"), "6月综合行动仪表盘")
    build(os.path.join(GOALS_DIR, "能力圈短板报告与改进方案_20260527.md"),
          os.path.join(GOALS_DIR, "能力圈短板报告与改进方案_20260527.pdf"), "能力圈短板报告与改进方案")

    for key, name in GOAL_FILES.items():
        build(os.path.join(GOALS_DIR, key, f"{name}.md"),
              os.path.join(GOALS_DIR, key, f"{name}.pdf"), name)
    for key, name in OPS_FILES.items():
        build(os.path.join(GOALS_DIR, key, f"{name}.md"),
              os.path.join(GOALS_DIR, key, f"{name}.pdf"), name)
    for key, names in EXEC_FILES.items():
        for name in names:
            build(os.path.join(GOALS_DIR, key, f"{name}.md"),
                  os.path.join(GOALS_DIR, key, f"{name}.pdf"), name)

    cc_manuals = [
        "Claude Code使用精通手册", "Claude Code命令使用场景手册",
        "Claude Code内建命令手册", "Claude插件使用场景手册",
    ]
    for name in cc_manuals:
        build(os.path.join(GOALS_DIR, "ai", f"{name}.md"),
              os.path.join(GOALS_DIR, "ai", f"{name}.pdf"), name)

    standalone = [
        ("career", "科技金融方法论"),
        ("career", "中国科技金融市场全景_20260527"),
        ("career", "客户拜访简报_神州信息_20260527"),
        ("career", "交易筛查备忘录_AI芯片公司_20260527"),
        ("career", "事业AI加速方案_20260527"),
        ("career", "发表文章_科技金融生态方法论_20260527"),
        ("career", "AI产业链事业加速方案_20260527"),
        ("investment", "30年个人投资框架_哲学与底层逻辑"),
        ("investment", "量化策略框架_20260527"),
        ("investment", "AI全产业链研究报告_20260527"),
        ("investment", "AI产业链投资行动方案_20260527"),
        ("investment", "6月第1周投资执行清单_20260527"),
        ("ai", "AI与知识库升级方案_20260527"),
        ("ai", "AI产业链学习与知识库方案_20260527"),
        ("family", "家庭AI支持方案_20260527"),
        ("family", "考研AI辅助系统_启动包"),
        ("family", "考研AI辅助系统_错题库"),
        ("family", "考研AI辅助系统_进度周报"),
        ("family", "AI工具推荐_家庭场景_20260527"),
        ("health", "健康AI支持方案_20260527"),
        ("health", "6月1日基线采集清单_20260527"),
        ("health", "AI健康工具推荐_20260527"),
        ("career", "上海光机所杭州光机所合作方案_20260527"),
        ("career", "神州信息综合金融服务方案_20260527"),
        ("investment", "投资思维框架_Margin_Discipline_Freedom_演讲稿_20260527"),
        ("ai", "快速掌握AI手册_20260527", False, False),
        ("ai", "快速学习Claude_Code手册_20260527", False, False),
        ("ai", "快速学习Harness手册_20260527", False, False),
        ("ai", "一天学会Claude_Code_20260527", False, False),
        ("ai", "每日AI前沿收集_20260527", False, False),
        ("family", "上海大学考研完全手册_20260527"),
    ]
    for entry in standalone:
        folder, name = entry[0], entry[1]
        kwargs = {}
        if len(entry) >= 4:
            kwargs = {"show_author": entry[2], "show_goals": entry[3]}
        build(os.path.join(GOALS_DIR, folder, f"{name}.md"),
              os.path.join(GOALS_DIR, folder, f"{name}.pdf"), name, **kwargs)

    crosscut = [
        "幸福人生AI增强仪表盘_20260527",
        "AI产业链驱动_幸福人生总方案_20260527",
        "中科大校友资源_六目标行动方案_20260527",
        "浙江籍贯资源_六目标行动方案_20260527",
        "民建会员资源_六目标行动方案_20260527",
        "资源圈拓展方案_20260527",
        "人脉资源手册_20260527",
    ]
    for name in crosscut:
        build(os.path.join(GOALS_DIR, f"{name}.md"),
              os.path.join(GOALS_DIR, f"{name}.pdf"), name)

    print(f"\nDone. {total} PDFs generated.")


if __name__ == "__main__":
    main()
