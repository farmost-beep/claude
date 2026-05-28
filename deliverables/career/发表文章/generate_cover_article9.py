#!/usr/bin/env python3
"""Cover for Article 9: Organizational AI transformation."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/封面_组织AI转型.png"

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

FONT = "/System/Library/Fonts/PingFang.ttc"
if not os.path.exists(FONT):
    FONT = "/System/Library/Fonts/STHeiti Light.ttc"
def ff(s): return ImageFont.truetype(FONT, s) if os.path.exists(FONT) else ImageFont.load_default()

# Left: organization layers from human to AI-native
layers = [
    ("L5  AI原生", (52, 211, 153)),
    ("L4  系统自进化", (96, 165, 250)),
    ("L3  Agent管理", (168, 85, 247)),
    ("L2  任务委托", (245, 158, 11)),
    ("L1  工具辅助", (239, 68, 68)),
]
cx, cy = 130, 250
for idx, (name, clr) in enumerate(layers):
    ly = cy - 80 + idx * 46
    tw = draw.textlength(name, font=ff(15))
    draw.rounded_rectangle((cx-80, ly, cx-80+tw+18, ly+36), radius=10, fill=clr)
    draw.text((cx-72, ly+7), name, fill=WHITE, font=ff(15))

# Arrow on the side
draw.text((cx-100, cy-95), "↑", fill=GOLD, font=ff(20))
draw.text((cx-98, cy+98), "组织成熟度", fill=DIM, font=ff(12))
# Vertical line
draw.line(((cx-92, cy-80), (cx-92, cy+95)), fill=(50, 60, 80), width=1)

# Right: title
rx = 260
draw.rectangle((rx, 54, rx+80, 56), fill=ACCENT)
draw.text((rx, 80), "为了造出Claude", fill=WHITE, font=ff(34))
draw.text((rx, 125), "Anthropic先把自己的组织变成了什么样", fill=WHITE, font=ff(28))
draw.text((rx, 175), "五个内部转型 → 外化为产品能力", fill=GOLD, font=ff(20))
draw.text((rx, 215), "人写代码→人定目标 | 串行→并行Agent | 人审查→三层自动质量网 | 文档→记忆基础设施", fill=SUB, font=ff(11))

draw.rectangle((rx, 245, 860, 247), fill=(30, 41, 59))

# 5 transformations
transforms = [
    ("转型一", "人写代码 → 人定义目标，AI执行"),
    ("转型二", "单人串行 → 一人管理多个并行Agent"),
    ("转型三", "质量靠人审查 → 三层自动质量网"),
    ("转型四", "文档是副产品 → 记忆是基础设施"),
    ("转型五", "使用工具 → 管理系统"),
]
for idx, (label, desc) in enumerate(transforms):
    ty = 268 + idx * 38
    draw.text((rx, ty), label, fill=GOLD, font=ff(15))
    draw.text((rx+70, ty), desc, fill=WHITE, font=ff(15))

draw.rectangle((rx, 460, 860, 461), fill=(30, 41, 59))
draw.text((rx, 473), "作者：陈颖芳  |  2026年5月  |  AI方法论系列 ⑥", fill=DIM, font=ff(14))

img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
