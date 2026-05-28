#!/usr/bin/env python3
"""Generate WeChat cover image for AI methodology 18 principles article."""
from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/封面_AI方法论18条原则.png"

# Colors
BG = "#0f172a"
ACCENT = "#f59e0b"
WHITE = "#f8fafc"
SUB = "#94a3b8"
DIM = "#475569"
LAYER_COLORS = ["#ef4444", "#f97316", "#3b82f6", "#22c55e"]

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# Find font
FONT_TTC = "/System/Library/Fonts/PingFang.ttc"
FONT_FALLBACK = "/System/Library/Fonts/STHeiti Light.ttc"
font_file = FONT_TTC if os.path.exists(FONT_TTC) else FONT_FALLBACK

def f(size):
    try: return ImageFont.truetype(font_file, size)
    except: return ImageFont.load_default()

# --- Left panel: 4-layer rings ---
center_x, center_y = 180, 250
for i in range(4):
    r = 125 - i * 28
    bbox = (center_x - r, center_y - r, center_x + r, center_y + r)
    draw.arc(bbox, 0, 360, fill=LAYER_COLORS[i], width=3)

# Center: "18"
f18 = f(48)
tw = draw.textlength("18", font=f18)
draw.text((center_x - tw/2, center_y - 26), "18", fill=ACCENT, font=f18)
f_label = f(14)
lw = draw.textlength("条原则", font=f_label)
draw.text((center_x - lw/2, center_y + 24), "条原则", fill=SUB, font=f_label)

# Layer labels around left side
labels = [
    ("建立关系", 140, 100),
    ("组织任务", 215, 170),
    ("质量保障", 215, 310),
    ("持续进化", 140, 380),
]
for txt, lx, ly in labels:
    draw.text((lx, ly), txt, fill=SUB, font=f(13))

# Arrow hint at bottom of rings
draw.text((center_x-6, center_y+125+20), "△", fill=ACCENT, font=f(14))
draw.text((center_x-24, center_y+125+38), "FLYWHEEL", fill=DIM, font=f(11))

# --- Right panel: typography ---
# Divider
for i in range(3):
    y = 54 + i
    alpha = 255 - i*80
    draw.line((360, y, 860, y), fill=(148, 163, 184, max(0,alpha)), width=1)

# Title line 1
title1 = "Anthropic不公开的方法论"
draw.text((380, 100), title1, fill=WHITE, font=f(42))

# Title line 2
title2 = "我逆向推导出了"
tw2 = draw.textlength(title2, font=f(38))
draw.text((380, 150), title2, fill=WHITE, font=f(38))

# "18条原则" emphasized
draw.text((380 + tw2 + 8, 145), "18条原则", fill=ACCENT, font=f(42))

# Subtitle
draw.text((380, 220), "从问答模式 → 管理模式  ·  4层飞轮自我进化", fill=SUB, font=f(20))

# Horizontal rule
draw.rectangle((380, 260, 840, 262), fill="#1e293b")

# 5 keyword pills
keywords = [
    ("明确目标", LAYER_COLORS[0]),
    ("任务分发", LAYER_COLORS[1]),
    ("交叉审查", LAYER_COLORS[2]),
    ("自我进化", LAYER_COLORS[3]),
    ("记忆积累", ACCENT),
]

pill_y = 290
x_start = 380
for idx, (kw, color) in enumerate(keywords):
    kx = x_start + idx * 102
    # Pill background
    tw_kw = draw.textlength(kw, font=f(17))
    pad = 14
    draw.rounded_rectangle(
        (kx, pill_y, kx + tw_kw + pad*2, pill_y + 34),
        radius=17, fill=color, outline=None
    )
    draw.text((kx + pad, pill_y + 5), kw, fill=WHITE, font=f(17))

# Bottom meta
meta_parts = [
    ("作者：陈颖芳", DIM),
    (" | ", "#334155"),
    ("2026年5月", DIM),
    (" | ", "#334155"),
    ("AI方法论系列", DIM),
]
mx = 380
for txt, clr in meta_parts:
    draw.text((mx, 360), txt, fill=clr, font=f(16))
    mx += draw.textlength(txt, font=f(16))

# Bottom rule
draw.rectangle((380, 395, 840, 396), fill="#1e293b")

# Footer
footer = "从Claude Code进化轨迹逆向推导  ·  每条原则附带即时可操作指令"
draw.text((380, 415), footer, fill=DIM, font=f(15))

# Page indicator
draw.text((380, 445), "AI方法论系列 ① / ②", fill="#334155", font=f(14))

img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
print(f"Size: {W}x{H}")
