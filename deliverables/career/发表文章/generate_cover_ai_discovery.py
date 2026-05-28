#!/usr/bin/env python3
"""Cover for AI方法论系列 ⑬: AI能力发现方法论."""
from PIL import Image, ImageDraw, ImageFont
import math, os

W, H = 900, 500
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "封面_AI能力发现方法论.png")

# Colors
BG = (8, 12, 30)
WHITE = (241, 245, 249)
SUB = (148, 163, 184)
DIM = (71, 85, 105)
ACCENT = (96, 165, 250)
GOLD = (245, 158, 11)
GREEN = (52, 211, 153)
PURPLE = (168, 85, 247)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

# Font
FONT = "/System/Library/Fonts/PingFang.ttc"
if not os.path.exists(FONT):
    FONT = "/System/Library/Fonts/STHeiti Light.ttc"

def ff(s):
    """Get font at given size, with fallback."""
    if os.path.exists(FONT):
        return ImageFont.truetype(FONT, s)
    return ImageFont.load_default()

# ============================================================
# LEFT PANEL: Radar chart (4-quadrant discovery radar)
# ============================================================
# Arrange radar + funnel on left 42% of canvas
radar_cx, radar_cy = 215, 205
outer_r = 115
mid_r = 78
inner_r = 40

# --- Concentric rings ---
for r in [inner_r, mid_r, outer_r]:
    draw.ellipse(
        (radar_cx - r, radar_cy - r, radar_cx + r, radar_cy + r),
        outline=(30, 50, 80), width=1
    )

# Crosshair lines (subtle axes at 45-degree intervals for grid feel)
for deg in range(0, 360, 15):
    rad = math.radians(deg)
    ex = radar_cx + outer_r * math.cos(rad)
    ey = radar_cy + outer_r * math.sin(rad)
    draw.line((radar_cx, radar_cy, ex, ey), fill=(20, 30, 45), width=1)

# --- 4 main quadrant axes ---
angles_deg = [0, 90, 180, 270]  # right, down, left, up
labels_4 = ["核心区", "探索区", "惰性区", "观望区"]
colors_4 = [GOLD, ACCENT, GREEN, PURPLE]

for deg, label, clr in zip(angles_deg, labels_4, colors_4):
    rad = math.radians(deg)
    ex = radar_cx + outer_r * math.cos(rad)
    ey = radar_cy + outer_r * math.sin(rad)
    # Main axis line (brighter)
    draw.line((radar_cx, radar_cy, ex, ey), fill=(40, 60, 90), width=2)

    # Label pill beyond axis end
    label_r = outer_r + 28
    lx = radar_cx + label_r * math.cos(rad)
    ly = radar_cy + label_r * math.sin(rad)
    font_lbl = ff(13)
    tw = draw.textlength(label, font=font_lbl)
    bx, by = lx - tw / 2 - 8, ly - 9
    draw.rounded_rectangle((bx, by, bx + tw + 16, by + 22), radius=9, fill=clr)
    text_color = BG if clr == GOLD else WHITE
    draw.text((bx + 8, by + 2), label, fill=text_color, font=font_lbl)

    # Tick marks at ring intersections
    for r in [inner_r, mid_r, outer_r]:
        mx = radar_cx + r * math.cos(rad)
        my = radar_cy + r * math.sin(rad)
        draw.ellipse((mx - 2, my - 2, mx + 2, my + 2), fill=DIM, outline=DIM)

# --- Coverage polygon (example "discovery coverage") ---
coverage = [0.85, 0.65, 0.50, 0.70]  # 核心区 / 探索区 / 惰性区 / 观望区
poly_pts = []
for deg, val in zip(angles_deg, coverage):
    r = outer_r * val
    px = radar_cx + r * math.cos(math.radians(deg))
    py = radar_cy + r * math.sin(math.radians(deg))
    poly_pts.append((px, py))
draw.polygon(poly_pts, fill=(96, 165, 250, 40), outline=ACCENT)

# Highlight points on the polygon
for deg, val in zip(angles_deg, coverage):
    r = outer_r * val
    px = radar_cx + r * math.cos(math.radians(deg))
    py = radar_cy + r * math.sin(math.radians(deg))
    draw.ellipse((px - 5, py - 5, px + 5, py + 5), fill=GOLD)
    # Outer ring
    draw.ellipse((px - 8, py - 8, px + 8, py + 8), outline=(245, 158, 11, 60), width=1)

# --- Radar sweep beam (semi-transparent wedge) ---
# Several thin pie slices to suggest scanning motion
for base_deg in [25, 55, 145, 235, 310]:
    for offset in [0, 3, 6]:
        rad_start = math.radians(base_deg + offset - 2)
        rad_end = math.radians(base_deg + offset + 2)
        # Draw as a thin polygon
        pts = [(radar_cx, radar_cy)]
        steps = 10
        r_step = outer_r / steps
        for s in range(steps + 1):
            r = s * r_step
            px = radar_cx + r * math.cos(rad_start)
            py = radar_cy + r * math.sin(rad_start)
            pts.append((px, py))
        for s in range(steps, -1, -1):
            r = s * r_step
            px = radar_cx + r * math.cos(rad_end)
            py = radar_cy + r * math.sin(rad_end)
            pts.append((px, py))
        alpha = 30 if offset == 3 else 15
        draw.polygon(pts, fill=(96, 165, 250, alpha))

# --- Center dot ---
draw.ellipse((radar_cx - 5, radar_cy - 5, radar_cx + 5, radar_cy + 5), fill=WHITE)
draw.ellipse((radar_cx - 3, radar_cy - 3, radar_cx + 3, radar_cy + 3), fill=GOLD)

# --- Scattered information dots around the radar ---
scatter_dots = [
    (140, 120, GREEN), (280, 135, ACCENT), (310, 200, GOLD),
    (170, 150, PURPLE), (250, 105, ACCENT), (120, 190, GREEN),
    (150, 280, PURPLE), (290, 270, GOLD), (130, 240, ACCENT),
    (300, 240, GREEN), (260, 290, PURPLE), (175, 310, ACCENT),
]
for sx, sy, sc in scatter_dots:
    draw.ellipse((sx - 2, sy - 2, sx + 2, sy + 2), fill=sc)
    # Subtle connection line toward center
    draw.line((sx, sy, radar_cx, radar_cy), fill=(sc[0], sc[1], sc[2], 20), width=1)

# ============================================================
# FUNNEL: Below the radar — 4 sources → evaluation → radar
# ============================================================
funnel_cx = 215
funnel_top_y = 350

# Level 1: "4类信息源"
l1_w, l1_h = 260, 32
l1_x = funnel_cx - l1_w // 2
l1_y = funnel_top_y
draw.rounded_rectangle((l1_x, l1_y, l1_x + l1_w, l1_y + l1_h), radius=8, fill=(25, 40, 60), outline=(40, 60, 90))
draw.text((funnel_cx - ff(13).getlength("4类信息源") // 2, l1_y + 6), "4类信息源", fill=WHITE, font=ff(13))
# Sub-labels inside
sub_sources = ["新闻", "论文", "工具", "社区"]
sub_w = l1_w // 4
for i, src in enumerate(sub_sources):
    sx = l1_x + i * sub_w + sub_w // 2 - ff(9).getlength(src) // 2
    draw.text((sx, l1_y + 18), src, fill=GOLD, font=ff(9))

# Arrow 1
arrow1_y = l1_y + l1_h + 2
arrow1_cx = funnel_cx
draw.polygon(
    [(arrow1_cx - 8, arrow1_y), (arrow1_cx + 8, arrow1_y), (arrow1_cx, arrow1_y + 12)],
    fill=DIM
)

# Level 2: "AI能力评估"
l2_w, l2_h = 200, 30
l2_x = funnel_cx - l2_w // 2
l2_y = arrow1_y + 14
draw.rounded_rectangle((l2_x, l2_y, l2_x + l2_w, l2_y + l2_h), radius=8, fill=(30, 50, 75), outline=ACCENT)
l2_text = "AI 能力评估与筛选"
draw.text((funnel_cx - ff(13).getlength(l2_text) // 2, l2_y + 5), l2_text, fill=ACCENT, font=ff(13))

# Arrow 2
arrow2_y = l2_y + l2_h + 2
draw.polygon(
    [(arrow1_cx - 8, arrow2_y), (arrow1_cx + 8, arrow2_y), (arrow1_cx, arrow2_y + 12)],
    fill=DIM
)

# Level 3: "能力雷达分类"
l3_w, l3_h = 140, 30
l3_x = funnel_cx - l3_w // 2
l3_y = arrow2_y + 14
draw.rounded_rectangle((l3_x, l3_y, l3_x + l3_w, l3_y + l3_h), radius=8, fill=(40, 30, 60), outline=PURPLE)
l3_text = "四象限雷达分类"
draw.text((funnel_cx - ff(13).getlength(l3_text) // 2, l3_y + 5), l3_text, fill=PURPLE, font=ff(13))

# ============================================================
# RIGHT PANEL: Title, subtitle, evaluation cycle, metadata
# ============================================================
rx = 460  # right-content origin x

# --- Vertical accent line ---
draw.rectangle((425, 34, 427, 465), fill=(30, 50, 80))

# --- Top accent bar ---
draw.rectangle((rx, 34, rx + 80, 36), fill=GOLD)

# --- Title ---
title_font = ff(34)
title_text = "AI能力发现方法论"
draw.text((rx, 56), title_text, fill=WHITE, font=title_font)

# --- Subtitle ---
subtitle_font = ff(17)
subtitle_text = "在信息洪流中系统化捕捉真正重要的东西"
draw.text((rx, 105), subtitle_text, fill=ACCENT, font=subtitle_font)

# --- Separator ---
sep1_y = 142
draw.rectangle((rx, sep1_y, 870, sep1_y + 1), fill=(30, 41, 59))

# --- 4-step evaluation cycle (Day 1/2/3) ---
cycle_y = 158
cycle_title = "四步评估循环"
draw.text((rx, cycle_y), cycle_title, fill=GOLD, font=ff(14))

# Day boxes
day_data = [
    ("Day 1", "信息采集", "多源扫描\n关键词匹配\n初筛过滤", ACCENT),
    ("Day 2", "深度评估", "能力验证\n交叉比对\n置信度打分", GREEN),
    ("Day 3", "纳入迭代", "雷达分类\n体系归档\n持续更新", PURPLE),
]

box_w, box_h = 125, 78
box_gap = 10
arrow_gap = 8
day_start_x = rx
day_y = cycle_y + 26

for i, (day, title, desc, clr) in enumerate(day_data):
    bx = day_start_x + i * (box_w + box_gap + 14)  # 14 for arrow between
    by = day_y

    # Box background
    draw.rounded_rectangle((bx, by, bx + box_w, by + box_h), radius=10,
                           fill=(15, 25, 45), outline=clr, width=1)

    # Day label (top-left badge)
    draw.text((bx + 10, by + 8), day, fill=clr, font=ff(12))
    # Title
    draw.text((bx + 10, by + 28), title, fill=WHITE, font=ff(13))
    # Description lines
    desc_lines = desc.split("\n")
    for di, dline in enumerate(desc_lines):
        draw.text((bx + 10, by + 48 + di * 16), dline, fill=SUB, font=ff(10))

    # Arrow between boxes
    if i < len(day_data) - 1:
        arrow_x = bx + box_w + 2
        arrow_y = by + box_h // 2
        draw.polygon(
            [(arrow_x, arrow_y - 5), (arrow_x + 8, arrow_y), (arrow_x, arrow_y + 5)],
            fill=DIM
        )

# --- Separator 2 ---
sep2_y = day_y + box_h + 22
draw.rectangle((rx, sep2_y, 870, sep2_y + 1), fill=(30, 41, 59))

# --- Methodology highlights ---
highlight_y = sep2_y + 16
highlights = [
    ("发现", "信息洪流中识别信号", GOLD),
    ("评估", "多维度交叉验证能力", ACCENT),
    ("分类", "四象限雷达定位归档", GREEN),
    ("迭代", "持续更新保持鲜活", PURPLE),
]

for i, (label, desc, clr) in enumerate(highlights):
    hy = highlight_y + i * 28
    # Bullet dot
    draw.ellipse((rx, hy + 5, rx + 7, hy + 12), fill=clr)
    draw.text((rx + 14, hy + 2), label, fill=clr, font=ff(13))
    draw.text((rx + 55, hy + 2), desc, fill=WHITE, font=ff(13))

# --- Bottom separator ---
bot_y = highlight_y + len(highlights) * 28 + 10
draw.rectangle((rx, bot_y, 870, bot_y + 1), fill=(30, 41, 59))

# --- Quote ---
quote_y = bot_y + 14
quote = '"最重要的不是看到多少信息，而是识别出多少真正重要的信号"'
draw.text((rx, quote_y), quote, fill=SUB, font=ff(12))
qw = draw.textlength(quote, font=ff(12))
draw.text((rx + qw + 8, quote_y), "— 陈颖芳", fill=DIM, font=ff(11))

# --- Metadata ---
meta_y = quote_y + 28
draw.rectangle((rx, meta_y - 4, 870, meta_y - 3), fill=(30, 41, 59))
draw.text((rx, meta_y + 6), "作者：陈颖芳  |  2026年5月  |  AI方法论系列 ⑬", fill=DIM, font=ff(14))

# ============================================================
# SAVE
# ============================================================
img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
