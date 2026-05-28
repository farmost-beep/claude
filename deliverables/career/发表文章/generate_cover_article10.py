#!/usr/bin/env python3
"""Cover for Article 10: Banking AI management mode transformation."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/封面_银行管理模式.png"

BG = (8, 12, 30)
WHITE = (241, 245, 249)
SUB = (148, 163, 184)
DIM = (71, 85, 105)
ACCENT = (96, 165, 250)
GOLD = (245, 158, 11)
GREEN = (52, 211, 153)
RED = (239, 68, 68)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

FONT = "/System/Library/Fonts/PingFang.ttc"
if not os.path.exists(FONT):
    FONT = "/System/Library/Fonts/STHeiti Light.ttc"
def ff(s): return ImageFont.truetype(FONT, s) if os.path.exists(FONT) else ImageFont.load_default()

# Left: three banking scenario cards
scenarios = [
    ("授信报告", "3天→3小时", GOLD),
    ("合规审查", "200页→问题清单", GREEN),
    ("财报分析", "5天→半天", ACCENT),
]
cx = 160
for idx, (name, desc, clr) in enumerate(scenarios):
    cy = 120 + idx * 100
    tw = draw.textlength(name, font=ff(20))
    draw.rounded_rectangle((cx-90, cy, cx-90+tw+24, cy+50), radius=12, fill=clr)
    draw.text((cx-78, cy+10), name, fill=WHITE, font=ff(20))
    draw.text((cx-78, cy+46), desc, fill=SUB, font=ff(14))
    if idx < 2:
        draw.text((cx-6, cy+58), "↓", fill=DIM, font=ff(18))

# From Q&A mode to management mode arrow
draw.text((cx-30, 410), "问答模式 → 管理模式", fill=ACCENT, font=ff(15))

# Right: title
rx = 220
draw.rectangle((rx, 54, rx+80, 56), fill=GOLD)
draw.text((rx, 80), "当银行遇到管理模式", fill=WHITE, font=ff(34))
draw.text((rx, 125), "科技金融的AI重构不是换工具，是换运作方式", fill=SUB, font=ff(20))
draw.text((rx, 170), "三个真实业务场景：授信·合规·分析", fill=GREEN, font=ff(16))

draw.rectangle((rx, 205, 860, 207), fill=(30, 41, 59))

# Key numbers
nums = [
    ("3天→3小时", "授信报告"),
    ("200页→问题清单", "合规审查"),
    ("5天→半天", "20家财报"),
    ("4个障碍+破解", "真实痛点"),
]
for idx, (num, label) in enumerate(nums):
    nx = rx + idx * 155
    draw.text((nx, 225), num, fill=GOLD, font=ff(22))
    draw.text((nx, 255), label, fill=SUB, font=ff(13))

draw.rectangle((rx, 290, 860, 291), fill=(30, 41, 59))

# 4 obstacles
obstacles = [
    ("合规责任", "AI不替决策，替准备"),
    ("模板固化", "模板发AI，只换内容"),
    ("数据敏感", "脱敏→本地→还原"),
    ("人的抗拒", "判断+关系+谈判=你的价值"),
]
for idx, (title, desc) in enumerate(obstacles):
    oy = 310 + idx * 40
    draw.text((rx, oy), f"障碍{idx+1}: {title}", fill=RED, font=ff(16))
    draw.text((rx+190, oy), desc, fill=WHITE, font=ff(15))

draw.rectangle((rx, 465, 860, 466), fill=(30, 41, 59))
draw.text((rx, 476), "作者：陈颖芳  |  2026年5月  |  AI方法论系列 ⑦", fill=DIM, font=ff(14))

img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
