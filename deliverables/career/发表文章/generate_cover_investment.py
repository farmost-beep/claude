#!/usr/bin/env python3
"""Cover for AI方法论系列 ⑧: Investment management mode."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/封面_投资管理模式.png"

BG = (8, 12, 30)
WHITE = (241, 245, 249)
SUB = (148, 163, 184)
DIM = (71, 85, 105)
ACCENT = (96, 165, 250)
GOLD = (245, 158, 11)
GREEN = (52, 211, 153)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

FONT = "/System/Library/Fonts/PingFang.ttc"
if not os.path.exists(FONT):
    FONT = "/System/Library/Fonts/STHeiti Light.ttc"
def ff(s): return ImageFont.truetype(FONT, s) if os.path.exists(FONT) else ImageFont.load_default()

# === Left panel: Investment pipeline (20 companies → agent groups → anomaly → judgment) ===
pipeline = [
    ("20家公司", GREEN),
    ("→", GOLD),
    ("4组并行Agent", ACCENT),
    ("→", GOLD),
    ("异常聚焦", (239, 68, 68)),
    ("→", GOLD),
    ("人工判断", GOLD),
]

# Draw pipeline as horizontal flow on the left
start_x, cy = 30, 180
px = start_x
for label, clr in pipeline:
    if label.startswith("→"):
        draw.text((px, cy + 7), label, fill=clr, font=ff(18))
        px += 25
    else:
        tw = draw.textlength(label, font=ff(15))
        draw.rounded_rectangle((px, cy, px + tw + 20, cy + 36), radius=10, fill=clr)
        draw.text((px + 10, cy + 7), label, fill=WHITE if clr != GOLD else BG, font=ff(15))
        px += tw + 28

# Pipeline description below
pipeline_notes = [
    "每家公司 → 4个Agent并行分析",
    "财务 · 估值 · 竞争力 · 风险",
    "自动交叉验证，只标记异常",
    "人类聚焦审查高价值信号",
]
for idx, note in enumerate(pipeline_notes):
    ny = cy + 50 + idx * 20
    dot_clr = [GREEN, ACCENT, (239, 68, 68), GOLD][idx]
    draw.ellipse((start_x, ny + 6, start_x + 6, ny + 12), fill=dot_clr)
    draw.text((start_x + 14, ny + 2), note, fill=SUB, font=ff(11))

# === Right panel: Title and content ===
rx = 50
draw.rectangle((rx, 34, rx + 80, 36), fill=ACCENT)
draw.text((rx, 58), "当投资遇到", fill=WHITE, font=ff(36))
draw.text((rx, 108), "管理模式", fill=GOLD, font=ff(40))
draw.text((rx, 158), "量化分析从5天到半天", fill=ACCENT, font=ff(22))

draw.rectangle((rx, 195, 860, 197), fill=(30, 41, 59))

# Agent architecture summary
arch_items = [
    ("输入层", "20家标的 · 财报+行情+舆情"),
    ("并行层", "4组Agent · 自动分工+交叉审查"),
    ("聚焦层", "异常标记 · 置信度排序"),
    ("决策层", "人工判断 · 只关注差异信号"),
]
for idx, (label, desc) in enumerate(arch_items):
    ay = 215 + idx * 38
    draw.text((rx, ay), label, fill=GREEN, font=ff(14))
    draw.text((rx + 70, ay), desc, fill=WHITE, font=ff(14))

# Quote line
draw.rectangle((rx, 375, 860, 377), fill=(30, 41, 59))
quote = '"AI不替代人类判断,而是让人类只做值得判断的事"'
draw.text((rx, 395), quote, fill=SUB, font=ff(13))
draw.text((rx + draw.textlength(quote, font=ff(13)) + 10, 395), "— 陈颖芳", fill=DIM, font=ff(12))

# Bottom
draw.rectangle((rx, 435, 860, 436), fill=(30, 41, 59))
draw.text((rx, 450), "作者：陈颖芳  |  2026年5月  |  AI方法论系列 ⑧", fill=DIM, font=ff(14))

# Vertical accent line on the far left
draw.rectangle((15, 34, 17, 432), fill=(30, 50, 80))

img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
