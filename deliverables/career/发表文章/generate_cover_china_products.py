#!/usr/bin/env python3
"""Cover for AI方法论系列 ⑭: 评价国内主流AI产品."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/封面_国内AI产品评价.png"

BG = (8, 12, 30)
WHITE = (241, 245, 249)
SUB = (148, 163, 184)
DIM = (71, 85, 105)
ACCENT = (96, 165, 250)
RED = (239, 68, 68)
GOLD = (245, 158, 11)
GREEN = (52, 211, 153)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

FONT = "/System/Library/Fonts/PingFang.ttc"
if not os.path.exists(FONT):
    FONT = "/System/Library/Fonts/STHeiti Light.ttc"
def ff(s): return ImageFont.truetype(FONT, s) if os.path.exists(FONT) else ImageFont.load_default()

# === Title area ===
draw.rectangle((50, 34, 130, 36), fill=RED)
draw.text((50, 58), "评价国内主流", fill=WHITE, font=ff(36))
draw.text((50, 108), "AI产品", fill=RED, font=ff(40))
draw.text((50, 160), "管理模式成熟度视角 · 六款国产工具对比", fill=ACCENT, font=ff(20))

# === Divider ===
draw.rectangle((50, 200, 860, 202), fill=(30, 41, 59))

# === Product score bar chart on the right side ===
products = [
    ("豆包MarsCode", 49, GREEN),
    ("通义灵码", 45, ACCENT),
    ("智谱清言/CodeGeeX", 45, ACCENT),
    ("DeepSeek", 35, GOLD),
    ("文心一言/Comate", 35, GOLD),
    ("Kimi", 33, GOLD),
]

bar_start_x = 480
bar_max_w = 360
bar_h = 28
bar_gap = 6
for idx, (name, score, clr) in enumerate(products):
    by = 220 + idx * (bar_h + bar_gap)
    # Product name
    draw.text((bar_start_x - 140, by + 4), name, fill=WHITE, font=ff(13))
    # Bar background
    draw.rounded_rectangle((bar_start_x, by, bar_start_x + bar_max_w, by + bar_h), radius=6, fill=(30, 41, 59))
    # Score bar
    bw = int(bar_max_w * score / 55)
    draw.rounded_rectangle((bar_start_x, by, bar_start_x + bw, by + bar_h), radius=6, fill=clr)
    # Score text
    score_text = f"{score}%"
    draw.text((bar_start_x + bw + 8, by + 4), score_text, fill=clr, font=ff(13))

# === Left panel: visual elements ===
# China market indicator — red/gold accent
import math
# Simplified diamond shape (suggesting China market focus)
cx, cy = 120, 300
size = 60
diamond = [(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)]
draw.polygon(diamond, fill=(180, 20, 20, 80), outline=RED)

# Gold circle accent
draw.ellipse((cx - 15, cy - 15, cx + 15, cy + 15), fill=GOLD)
draw.text((cx - 4, cy - 8), "中", fill=(8, 12, 30), font=ff(14))

# Descriptive labels
desc_lines = [
    "10+1维评分体系",
    "6款国产AI产品",
    "管理模式成熟度",
    "本土生态优劣势",
]
for idx, line in enumerate(desc_lines):
    dy = 340 + idx * 24
    dot_clr = [RED, GOLD, ACCENT, GREEN][idx]
    draw.ellipse((55, dy + 6, 63, dy + 14), fill=dot_clr)
    draw.text((72, dy + 2), line, fill=SUB, font=ff(12))

# === Bottom ===
draw.rectangle((50, 430, 860, 431), fill=(30, 41, 59))
draw.text((50, 450), "作者：陈颖芳  |  2026年5月  |  AI方法论系列 ⑭", fill=DIM, font=ff(14))

# Vertical accent line on the far left
draw.rectangle((15, 34, 17, 432), fill=(30, 50, 80))

img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
