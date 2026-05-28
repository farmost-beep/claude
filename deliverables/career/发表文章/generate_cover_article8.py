#!/usr/bin/env python3
"""Cover for Article 8: Building a personal AI operating system."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/封面_个人AI操作系统.png"

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

# Four-layer flywheel diagram
layers = [
    ("进化层 🔄", PURPLE, "定期回顾→发现模式→更新记忆"),
    ("质量层 ✓", (239, 68, 68), "自检→交叉审查→版本控制"),
    ("指令层 📋", GREEN, "目标+上下文+验收标准+自查"),
    ("记忆层 💾", GOLD, "偏好·规范·路径·协作规则"),
]
cx, cy = 150, 250
layer_h = 42
for idx, (name, clr, desc_text) in enumerate(layers):
    ly = cy - 72 + idx * (layer_h + 8)
    tw = draw.textlength(name, font=ff(15))
    draw.rounded_rectangle((cx-80, ly, cx-80+tw+16, ly+layer_h), radius=10, fill=clr)
    draw.text((cx-72, ly+8), name, fill=WHITE, font=ff(15))
    draw.text((cx-72, ly+24), desc_text, fill=(100, 116, 139), font=ff(10))

# Feedback arrow on left side
for idx in range(3):
    ay = cy - 50 + idx * 50
    draw.text((cx-100, ay), "↑", fill=ACCENT, font=ff(16))

# Right: title
rx = 300
draw.rectangle((rx, 54, rx+80, 56), fill=ACCENT)
draw.text((rx, 80), "从方法论到个人AI操作系统", fill=WHITE, font=ff(34))
desc = "构建自进化的飞轮"
draw.text((rx, 130), desc, fill=GOLD, font=ff(26))
draw.text((rx, 185), "记忆层 · 指令层 · 质量层 · 进化层", fill=SUB, font=ff(16))

draw.rectangle((rx, 220, 840, 222), fill=(30, 41, 59))

# Launch plan
steps = [
    ("第1天", "记忆层 + 指令层（30分钟）"),
    ("第3天", "质量层：三层质量网（20分钟）"),
    ("第7天", "进化层：首次回顾+更新（17分钟）"),
]
for idx, (day, task) in enumerate(steps):
    sy = 250 + idx * 55
    draw.text((rx, sy), day, fill=GOLD, font=ff(22))
    draw.text((rx+90, sy+2), task, fill=WHITE, font=ff(16))

# 6-month signal
draw.text((rx, 420), "6个月后信号：AI记得你 · 你信任AI · 系统自进化", fill=GREEN, font=ff(16))

draw.rectangle((rx, 450, 840, 451), fill=(30, 41, 59))
draw.text((rx, 465), "作者：陈颖芳  |  2026年5月  |  AI方法论系列 ⑤/⑤", fill=DIM, font=ff(14))

img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
