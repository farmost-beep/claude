#!/usr/bin/env python3
"""将AI工作流10篇文章转为微信HTML格式"""
from pathlib import Path
import re

DIR = Path("/Users/cyingfang/claude/deliverables/career/发表文章")

ARTICLES = [
    # AI工作流 ①-⑤
    ("公众号文章_AI工作流01_投资飞轮_20260530.md", "公众号HTML_AI工作流01_投资飞轮_20260530.html"),
    ("公众号文章_AI工作流02_写作飞轮_20260530.md", "公众号HTML_AI工作流02_写作飞轮_20260530.html"),
    ("公众号文章_AI工作流03_编程飞轮_20260530.md", "公众号HTML_AI工作流03_编程飞轮_20260530.html"),
    ("公众号文章_AI工作流04_健康飞轮_20260530.md", "公众号HTML_AI工作流04_健康飞轮_20260530.html"),
    ("公众号文章_AI工作流05_事业飞轮_20260530.md", "公众号HTML_AI工作流05_事业飞轮_20260530.html"),
    # AI工作流·人物篇 ⑥-⑩
    ("公众号文章_AI工作流06_Karpathy编程飞轮_20260530.md", "公众号HTML_AI工作流06_Karpathy_20260530.html"),
    ("公众号文章_AI工作流07_Dario_CEO飞轮_20260530.md", "公众号HTML_AI工作流07_Dario_20260530.html"),
    ("公众号文章_AI工作流08_Simon_工程飞轮_20260530.md", "公众号HTML_AI工作流08_Simon_20260530.html"),
    ("公众号文章_AI工作流09_Nadella_决策飞轮_20260530.md", "公众号HTML_AI工作流09_Nadella_20260530.html"),
    ("公众号文章_AI工作流10_创业CEO_20260530.md", "公众号HTML_AI工作流10_创业CEO_20260530.html"),
]

SECTION_STYLE = "font-size:16px;color:#333;line-height:1.8;letter-spacing:0.5px;"
H2_STYLE = "font-size:20px;color:#1a3a5c;margin:20px 0 10px;border-left:4px solid #d4a853;padding-left:10px;"
BQ_STYLE = "border-left:4px solid #d4a853;padding:8px 12px;margin:8px 0;background:#f9f7f2;color:#666;"
TABLE_STYLE = "width:100%;border-collapse:collapse;font-size:14px;margin:10px 0;"
TD_STYLE = "border:1px solid #ddd;padding:6px 8px;"


def md_to_html(text: str) -> str:
    lines = text.split("\n")
    out = []
    in_table = False
    in_bq = False
    bq_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]

        if in_bq and not line.startswith(">") and line.strip() != "":
            out.append(
                f'<blockquote style="{BQ_STYLE}">'
                + "<br/>".join(bq_lines)
                + "</blockquote>"
            )
            out.append("<br/>")
            bq_lines = []
            in_bq = False

        if line.startswith(">"):
            in_bq = True
            content = line.lstrip("> ").strip()
            if content:
                content = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", content)
                bq_lines.append(f"<p>{content}</p>")
            else:
                bq_lines.append("<br/>")
            i += 1
            continue

        if line.strip() == "":
            if in_table:
                out.append("</table><br/>")
                in_table = False
            i += 1
            continue

        if line.strip() == "---":
            out.append("<br/>")
            i += 1
            continue

        if in_table and re.match(r"^\|[\s:|-]+\|", line):
            i += 1
            continue

        if line.startswith("|") and line.endswith("|"):
            if not in_table:
                out.append(f'<table style="{TABLE_STYLE}">')
                in_table = True
            cells = [c.strip() for c in line.split("|")[1:-1]]
            out.append("<tr>")
            for c in cells:
                c = c.replace("**", "<strong>").replace("**", "</strong>")
                out.append(f'<td style="{TD_STYLE}">{c}</td>')
            out.append("</tr>")
            i += 1
            continue

        if line.startswith("## "):
            if in_table:
                out.append("</table><br/>")
                in_table = False
            title = line[3:].strip().replace("**", "")
            out.append(f'<h2 style="{H2_STYLE}">{title}</h2>')
            out.append("<br/>")
            i += 1
            continue

        if line.startswith("# "):
            title = line[2:].strip().replace("**", "")
            out.append(f'<h2 style="{H2_STYLE}">{title}</h2>')
            out.append("<br/>")
            i += 1
            continue

        if in_table:
            out.append("</table><br/>")
            in_table = False

        processed = line.strip()
        processed = re.sub(r"~~(.+?)~~", r"<del>\1</del>", processed)
        processed = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", processed)
        processed = re.sub(r"\*(.+?)\*", r"<em>\1</em>", processed)
        processed = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2" style="color:#1a3a5c;">\1</a>', processed)

        if processed:
            out.append(f"<p>{processed}</p>")
        else:
            out.append("<br/>")

        i += 1

    if in_bq and bq_lines:
        out.append(
            f'<blockquote style="{BQ_STYLE}">'
            + "<br/>".join(bq_lines)
            + "</blockquote>"
        )
        out.append("<br/>")

    if in_table:
        out.append("</table><br/>")

    return "\n".join(out)


def main():
    for md_name, html_name in ARTICLES:
        md_path = DIR / md_name
        html_path = DIR / html_name
        if not md_path.exists():
            print(f"⚠️  SKIP: {md_name} (not found)")
            continue
        text = md_path.read_text(encoding="utf-8")
        body = md_to_html(text)
        html = f'<section style="{SECTION_STYLE}">\n{body}\n</section>'
        html_path.write_text(html, encoding="utf-8")
        print(f"✅ {html_name} ({len(html)} chars)")
    print(f"\nDone: {len([1 for _, h in ARTICLES if (DIR/h).exists()])} HTML files generated")

if __name__ == "__main__":
    main()
