#!/usr/bin/env python3
"""Cover for Article 6: Cognitive foundation of AI methodology."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/封面_AI方法论认知基础.png"

BG = (8, 12, 30)
WHITE = (241, 245, 249)
SUB = (148, 163, 184)
DIM = (71, 85, 105)
ACCENT = (52, 211, 153)
GOLD = (245, 158, 11)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

FONT = "/System/Library/Fonts/PingFang.ttc"
if not os.path.exists(FONT):
    FONT = "/System/Library/Fonts/STHeiti Light.ttc"
def ff(s): return ImageFont.truetype(FONT, s) if os.path.exists(FONT) else ImageFont.load_default()

# Left: brain hemisphere metaphor
cx, cy = 200, 250
# Left brain (System 1 - human)
draw.ellipse((cx-100, cy-90, cx, cy+90), fill=(30, 41, 59), outline=DIM, width=2)
draw.text((cx-80, cy-40), "系统1", fill=GOLD, font=ff(22))
draw.text((cx-80, cy-10), "人类", fill=GOLD, font=ff(18))
draw.text((cx-80, cy+20), "直觉·判断", fill=SUB, font=ff(13))
draw.text((cx-80, cy+42), "易疲劳·偏见多", fill=DIM, font=ff(12))

# Right brain (System 2 - AI)
draw.ellipse((cx, cy-90, cx+100, cy+90), fill=(15, 50, 40), outline=ACCENT, width=2)
draw.text((cx+14, cy-40), "系统2", fill=ACCENT, font=ff(22))
draw.text((cx+14, cy-10), "AI", fill=ACCENT, font=ff(18))
draw.text((cx+14, cy+20), "推理·执行", fill=SUB, font=ff(13))
draw.text((cx+14, cy+42), "永不疲劳·带宽∞", fill=DIM, font=ff(12))

# Connection arrow in center
draw.text((cx-10, cy-6), "⇋", fill=WHITE, font=ff(28))

# Labels
draw.text((cx-50, cy-110), "人脑", fill=GOLD, font=ff(14))
draw.text((cx+20, cy-110), "AI", fill=ACCENT, font=ff(14))

# Right: title
rx = 340
draw.rectangle((rx, 54, rx+100, 56), fill=ACCENT)
draw.text((rx, 80), "AI方法论的认知基础", fill=WHITE, font=ff(36))
desc = '为什么“管理模式”打败“问答模式”'
draw.text((rx, 132), desc, fill=GOLD, font=ff(26))
draw.text((rx, 185), "双系统理论 · 认知卸载 · 注意力经济学 · 反馈回路", fill=SUB, font=ff(16))

draw.rectangle((rx, 220, 840, 222), fill=(30, 41, 59))

# Key concepts pills
concepts = ["系统2卸载", "注意力重分配", "反馈回路结构", "判断边界"]
colors = [ACCENT, GOLD, (96, 165, 250), (168, 85, 247)]
for idx, (kw, clr) in enumerate(zip(concepts, colors)):
    kx = rx + idx * 130
    tw = draw.textlength(kw, font=ff(14))
    draw.rounded_rectangle((kx, 250, kx+tw+18, 280), radius=14, fill=clr)
    draw.text((kx+9, 253), kw, fill=WHITE, font=ff(14))

# Comparison row
comp_left = "问答模式：\n人做系统2 → 累"
comp_right = "管理模式：\nAI做系统2 → 轻"
draw.text((rx, 310), comp_left, fill=DIM, font=ff(15))
draw.text((rx+200, 310), "→", fill=ACCENT, font=ff(22))
draw.text((rx+250, 310), comp_right, fill=WHITE, font=ff(15))

draw.rectangle((rx, 380, 840, 381), fill=(30, 41, 59))
draw.text((rx, 400), "作者：陈颖芳  |  2026年5月  |  AI方法论系列 ③/⑤", fill=DIM, font=ff(14))
draw.text((rx, 435), "不是AI不够强，是你的协作模式锁死了系统2", fill=(51, 65, 85), font=ff(13))

img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
