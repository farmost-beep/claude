#!/usr/bin/env python3
"""Generate WeChat cover image for "推理成本趋零时" article."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/封面_推理成本趋零时.png"

# Colors
BG = "#0f172a"
ACCENT = "#22c55e"
WHITE = "#f8fafc"
SUB = "#94a3b8"
GREEN2 = "#4ade80"
GREEN3 = "#86efac"
DIM = "#1e293b"
RED = "#ef4444"

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# Font
FONT_TTC = "/System/Library/Fonts/PingFang.ttc"
FONT_FALLBACK = "/System/Library/Fonts/STHeiti Light.ttc"
font_file = FONT_TTC if os.path.exists(FONT_TTC) else FONT_FALLBACK

def f(size):
    try: return ImageFont.truetype(font_file, size)
    except: return ImageFont.load_default()

# --- Left side: Cost curve going down ---
# Draw a downward-sloping curve that approaches zero
curve_x = [60, 120, 200, 300, 380]
curve_y = [100, 130, 200, 320, 400]

# Draw the curve path (as connected segments with decreasing steepness)
draw.line([(60, 100), (120, 130)], fill=RED, width=3)  # 2024: steep
draw.line([(120, 130), (200, 200)], fill="#f97316", width=3)  # transition
draw.line([(200, 200), (300, 320)], fill=ACCENT, width=3)  # 2025: moderate
draw.line([(300, 320), (380, 400)], fill=GREEN2, width=3)  # 2026: flattening

# Dashed line extending trend toward zero (right edge)
for i in range(4):
    x1 = 380 + i*15
    x2 = 380 + (i+1)*15
    y = 400 - i*2
    if i % 2 == 0:
        draw.line([(x1, y), (x2, y-3)], fill=GREEN3, width=2)

# Labels on curve
f_small = ImageFont.truetype(font_file, 14)
draw.text((50, 85), "$30-60", fill=RED, font=f_small)
draw.text((190, 185), "$1-3", fill="#f97316", font=f_small)
draw.text((310, 305), "~$0", fill=ACCENT, font=f_small)

# Year markers on x-axis
draw.text((45, 420), "2024", fill=DIM, font=f_small)
draw.text((180, 420), "2025", fill=DIM, font=f_small)
draw.text((320, 420), "2026", fill=ACCENT, font=f_small)

# --- Right side: Title ---
t1 = f(44)
t1w = draw.textlength("推理成本趋零时", font=t1)
draw.text((W - t1w - 40, 130), "推理成本趋零时", fill=WHITE, font=t1)

# Subtitle
t2 = f(20)
draw.text((W - t1w - 40, 185), '当免费不再是少数', fill=SUB, font=t2)

# Divider
draw.line([(W - t1w - 40, 225), (W - 40, 225)], fill=DIM, width=1)

# Tags
t3 = f(16)
tags = ["杰文斯悖论", "验证力溢价", "判断力升值"]
for i, tag in enumerate(tags):
    tx = W - t1w - 40
    ty = 245 + i * 32
    # tag background
    tw = draw.textlength(tag, font=t3)
    draw.rounded_rectangle([tx-5, ty-2, tx+tw+5, ty+22], radius=4, fill=DIM)
    draw.text((tx, ty), tag, fill=ACCENT, font=t3)

# Bottom line
t4 = f(14)
draw.text((W - t1w - 40, 360), "主题12 · 涌现系列", fill=DIM, font=t4)

img.save(OUT)
print(f"✅ Cover saved: {OUT}")
