#!/usr/bin/env python3
"""Cover for Article 7: Five structural anti-patterns in AI collaboration."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/封面_AI协作反模式.png"

BG = (8, 12, 30)
WHITE = (241, 245, 249)
SUB = (148, 163, 184)
DIM = (71, 85, 105)
ACCENT = (239, 68, 68)
GOLD = (245, 158, 11)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

FONT = "/System/Library/Fonts/PingFang.ttc"
if not os.path.exists(FONT):
    FONT = "/System/Library/Fonts/STHeiti Light.ttc"
def ff(s): return ImageFont.truetype(FONT, s) if os.path.exists(FONT) else ImageFont.load_default()

# Five interconnected traps in a death spiral pattern
patterns = ["微观管理", "全量审查", "从零开始", "孤岛使用", "用完即弃"]
colors = [(239, 68, 68), (245, 158, 11), (168, 85, 247), (52, 211, 153), (96, 165, 250)]
cx, cy = 140, 230
radius = 80
for idx, (kw, clr) in enumerate(zip(patterns, colors)):
    angle = -90 + idx * 72
    import math
    x = int(cx + radius * math.cos(math.radians(angle))) - 50
    y = int(cy + radius * math.sin(math.radians(angle))) - 18
    tw = draw.textlength(kw, font=ff(16))
    draw.rounded_rectangle((x-8, y-4, x+tw+8, y+28), radius=12, fill=clr)
    draw.text((x, y), kw, fill=WHITE, font=ff(16))

# Spiral symbol in center
draw.text((cx-15, cy-20), "死亡", fill=ACCENT, font=ff(14))
draw.text((cx-10, cy+2), "螺旋", fill=ACCENT, font=ff(14))

# Arrow circle
draw.ellipse((cx-70, cy-70, cx+70, cy+70), outline=(60, 60, 80), width=1)

# Right: title
rx = 300
draw.rectangle((rx, 54, rx+80, 56), fill=ACCENT)
draw.text((rx, 80), "AI协作的五个结构性反模式", fill=WHITE, font=ff(34))
desc = "90%的人卡在这里"
draw.text((rx, 130), desc, fill=GOLD, font=ff(26))
draw.text((rx, 185), "微观管理 · 全量审查 · 孤岛使用 · 从零开始 · 用完即弃", fill=SUB, font=ff(14))

draw.rectangle((rx, 220, 840, 222), fill=(30, 41, 59))

# Breakthrough arrows
items = [
    ("承认模式", "识别自己陷在哪个模式里"),
    ("打断循环", "用一个反直觉行动打破惯性"),
    ("建立新习惯", "用系统替代意志力"),
]
for idx, (title, desc_text) in enumerate(items):
    iy = 250 + idx * 52
    draw.text((rx, iy), f"{idx+1}. {title}", fill=GOLD, font=ff(18))
    draw.text((rx+130, iy+1), desc_text, fill=SUB, font=ff(15))

draw.rectangle((rx, 410, 840, 411), fill=(30, 41, 59))
draw.text((rx, 425), "作者：陈颖芳  |  2026年5月  |  AI方法论系列 ④/⑤", fill=DIM, font=ff(14))
draw.text((rx, 460), "不是你的问题，是协作结构的问题——每个反模式都有标准解法", fill=(51, 65, 85), font=ff(13))

img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
