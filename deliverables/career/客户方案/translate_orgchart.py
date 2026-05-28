#!/usr/bin/env python3
"""Translate CB组织架构 SmartArt org chart to English and Japanese.

The docx contains a SmartArt diagram whose text lives in:
  word/diagrams/data1.xml    — data model (hierarchical structure + text)
  word/diagrams/drawing1.xml — visual layout (positions + text)

Strategy: unzip → replace text in both diagram XMLs → rezip.
"""
import zipfile, os, re, io, shutil, copy
from xml.sax.saxutils import escape as xml_escape

SRC = "/Users/cyingfang/claude/deliverables/career/客户方案/CB组织架构原始架构20260512(1).docx"
OUT_DIR = "/Users/cyingfang/claude/deliverables/career/客户方案/"

# ── Translation maps ──────────────────────────────────────────────
# Keys sorted longest-first. Includes split-text fragments ("、五轴" etc.)

EN_MAP = {
    # Top level
    "董事长": "Chairman",
    "总经理": "General Manager",
    "副总经理": "Deputy GM",
    "管代 ": "Mgmt Rep ",
    # Departments
    "品质部 ": "Quality Dept ",
    "品质部 ": "Quality Dept ",
    "供应商管理": "Supplier Mgmt",
    "过程质量": "Process QC",
    "售后质量": "After-Sales QC",
    "后工序": "Post-Process",
    "体系": "System",
    "钣金": "Sheet Metal",
    "部": " Dept",
    "拆图工艺": "Drawing Review",
    "激光切割": "Laser Cutting",
    "激光折弯": "Laser Bending",
    "焊接": "Welding",
    "打磨": "Grinding",
    "装配": "Assembly",
    "制造部": "Manufacturing Dept",
    "一车间": "Workshop 1",
    "一车间工艺组": "WS1 Process Team",
    "一车间龙门加工中心": "WS1 Gantry MC",
    "一车间卧加": "WS1 Horizontal MC",
    "、五轴": " / 5-Axis",
    "加工中心": " MC",
    "一车间攻牙": "WS1 Tapping",
    "二车间": "Workshop 2",
    "二车间工艺组": "WS2 Process Team",
    "二车间技术员": "WS2 Technicians",
    "A": "A",
    "区 ": "Zone ",
    "二车间 ": "WS2 ",
    "B": "B",
    "区 ": "Zone ",
    "二车间数控车组": "WS2 CNC Lathe",
    "三车间": "Workshop 3",
    "磨床组": "Grinding Group",
    "铣床组": "Milling Group",
    "线割组": "Wire EDM Group",
    "装配组": "Assembly Group",
    "业务中心": "Business Center",
    "业务部中心": "Business Ctr",
    "业务": "Business",
    "经理": "Manager",
    "业务助理": "Business Asst.",
    "技术中心": "Technical Center",
    "设计组": "Design Team",
    "报价组": "Quotation Team",
    "工艺组": "Process Team",
    "综合办": "General Office",
    "行政部": "Admin Dept",
    "人事": "HR",
    "筹建维修维护": "Construct. & Maint.",
    "后勤保洁": "Logist. & Cleaning",
    "采购部": "Purchasing Dept",
    "物料采购": "Material Procure.",
    "外发跟单": "Outsource Coord.",
    "总经办": "GM Office",
    "数据文员": "Data Clerk",
    "财务部": "Finance Dept",
    "会计": "Accounting",
    "出纳": "Cashier",
    "仓库": "Warehouse",
    "物流": "Logistics",
    "仓储": "Storage",
}

JA_MAP = {
    "董事长": "会長",
    "总经理": "総経理",
    "副总经理": "副総経理",
    "管代 ": "管理代表 ",
    "品质部 ": "品質部 ",
    "品质部 ": "品質部 ",
    "供应商管理": "サプライヤー管理",
    "过程质量": "工程品質",
    "售后质量": "アフター品質",
    "后工序": "後工程",
    "体系": "システム",
    "钣金": "板金",
    "部": "部",
    "拆图工艺": "図面展開",
    "激光切割": "レーザー切断",
    "激光折弯": "レーザー曲げ",
    "焊接": "溶接",
    "打磨": "研磨",
    "装配": "組立",
    "制造部": "製造部",
    "一车间": "第一工場",
    "一车间工艺组": "第一工場工程Gr",
    "一车间龙门加工中心": "第一工場門形MC",
    "一车间卧加": "第一工場横形MC",
    "、五轴": "・5軸",
    "加工中心": "MC",
    "一车间攻牙": "第一工場タップ",
    "二车间": "第二工場",
    "二车间工艺组": "第二工場工程Gr",
    "二车间技术员": "第二工場技術員",
    "A": "A",
    "区 ": "区 ",
    "二车间 ": "第二工場 ",
    "B": "B",
    "区 ": "区 ",
    "二车间数控车组": "第二工場CNC旋盤Gr",
    "三车间": "第三工場",
    "磨床组": "研削Gr",
    "铣床组": "フライスGr",
    "线割组": "WEDM Gr",
    "装配组": "組立Gr",
    "业务中心": "営業センター",
    "业务部中心": "営業部センター",
    "业务": "営業",
    "经理": "経理",
    "业务助理": "営業助理",
    "技术中心": "技術センター",
    "设计组": "設計Gr",
    "报价组": "見積Gr",
    "工艺组": "工程Gr",
    "综合办": "総務室",
    "行政部": "総務部",
    "人事": "人事",
    "筹建维修维护": "建設・保守管理",
    "后勤保洁": "後方・清掃",
    "采购部": "購買部",
    "物料采购": "資材購買",
    "外发跟单": "外注管理",
    "总经办": "総経理室",
    "数据文员": "データ事務",
    "财务部": "財務部",
    "会计": "会計",
    "出纳": "出納",
    "仓库": "倉庫",
    "物流": "物流",
    "仓储": "保管",
}

DIAGRAM_FILES = ["word/diagrams/data1.xml", "word/diagrams/drawing1.xml"]


def translate_diagram_xml(xml_content, trans_map):
    """Replace text inside <a:t> tags using translation map (longest-key-first).
    XML-escapes replacement text to prevent broken XML from &, <, > characters."""
    keys_sorted = sorted(trans_map.keys(), key=len, reverse=True)

    def replace_text(match):
        text = match.group(2)
        for key in keys_sorted:
            if key in text:
                text = text.replace(key, trans_map[key])
        text = xml_escape(text)
        return f"<a:t{match.group(1)}>{text}</a:t>"

    # Match <a:t attributes>text</a:t> — group(1)=attributes, group(2)=text
    return re.sub(r'<a:t([^>]*)>([^<]*)</a:t>', replace_text, xml_content)


def fix_font_sizes(xml_str, min_pt=8):
    """Reduce font sizes in drawing1.xml so English text fits within text boxes.

    SmartArt boxes are sized for compact Chinese. English is 2-3x wider per char.
    This recalculates sz= values in <a:rPr> for each text shape.
    """
    def calc_fit(text, box_cx_emu, current_fs_hundredths):
        """Return the font size (in hundredths) needed to fit text in box width."""
        if not text or box_cx_emu == 0:
            return current_fs_hundredths
        box_w_inches = box_cx_emu / 914400
        current_pt = current_fs_hundredths / 100
        # Estimated text width: len * pt * 0.52 / 72 (0.52 = avg char width factor)
        est_w = len(text) * current_pt * 0.52 / 72
        if est_w <= box_w_inches * 0.95:
            return current_fs_hundredths
        # Calculate needed pt size
        needed_pt = box_w_inches * 72 / (len(text) * 0.52) * 0.95
        needed_pt = max(min_pt, needed_pt)
        return int(needed_pt * 100)

    # Process each <dsp:sp> text shape
    def process_sp(match):
        sp_xml = match.group(0)
        # Extract text from all <a:t> tags inside this sp
        texts = re.findall(r'<a:t[^>]*>([^<]+)</a:t>', sp_xml)
        full_text = ''.join(texts).strip()
        if not full_text or full_text == '/':
            return sp_xml

        # Get box width from <dsp:txXfrm>
        ext_m = re.search(r'<dsp:txXfrm>.*?<a:ext\s+cx="(\d+)"', sp_xml, re.DOTALL)
        if not ext_m:
            return sp_xml
        box_cx = int(ext_m.group(1))

        # Get current font size(s) and replace with fitted size
        rprs = re.findall(r'(<a:rPr[^>]*?sz=")(\d+)(")', sp_xml)
        if not rprs:
            return sp_xml

        # Use the largest font size as reference
        current_max = max(int(sz) for _, sz, _ in rprs)
        new_sz = calc_fit(full_text, box_cx, current_max)

        if new_sz >= current_max:
            return sp_xml  # no change needed

        # Replace all sz="..." values within this sp
        result = sp_xml
        for prefix, old_sz, suffix in rprs:
            result = result.replace(f'{prefix}{old_sz}{suffix}', f'{prefix}{new_sz}{suffix}')

        # Also fix endParaRPr if present
        result = re.sub(r'(<a:endParaRPr[^>]*?sz=")(\d+)(")', rf'\g<1>{new_sz}\g<3>', result)

        return result

    return re.sub(r'<dsp:sp\b.*?</dsp:sp>', process_sp, xml_str, flags=re.DOTALL)


def translate_docx(src_path, out_path, trans_map, fix_fonts=False):
    """Translate diagram text in a docx file. Optionally fix font sizes for English."""
    with zipfile.ZipFile(src_path, 'r') as zin:
        zip_data = {}
        for name in zin.namelist():
            zip_data[name] = zin.read(name)

    for diag_file in DIAGRAM_FILES:
        if diag_file in zip_data:
            xml_str = zip_data[diag_file].decode('utf-8')
            xml_str = translate_diagram_xml(xml_str, trans_map)
            if fix_fonts and 'drawing' in diag_file:
                xml_str = fix_font_sizes(xml_str)
            zip_data[diag_file] = xml_str.encode('utf-8')

    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for name, data in zip_data.items():
            zout.writestr(name, data)

    print(f"  Saved: {out_path}")


def verify_docx(path, label):
    """Check translated text in diagram XMLs."""
    with zipfile.ZipFile(path, 'r') as z:
        for diag_file in DIAGRAM_FILES:
            if diag_file in z.namelist():
                xml_str = z.read(diag_file).decode('utf-8')
                texts = re.findall(r'<a:t[^>]*>([^<]+)</a:t>', xml_str)
                print(f"  [{label}] {diag_file}: {len(texts)} text nodes")
                for t in texts[:5]:
                    print(f"    '{t}'")
                if len(texts) > 5:
                    print(f"    ... ({len(texts)-5} more)")


if __name__ == "__main__":
    print("Generating English version (with font size fix)...")
    translate_docx(SRC, OUT_DIR + "CB_Organization_Chart_EN.docx", EN_MAP, fix_fonts=True)
    verify_docx(OUT_DIR + "CB_Organization_Chart_EN.docx", "EN")

    print("\nGenerating Japanese version...")
    translate_docx(SRC, OUT_DIR + "CB_Organization_Chart_JA.docx", JA_MAP)
    verify_docx(OUT_DIR + "CB_Organization_Chart_JA.docx", "JA")

    print("\nDone!")
