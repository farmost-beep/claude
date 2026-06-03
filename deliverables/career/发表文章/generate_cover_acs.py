#!/usr/bin/env python3
"""Generate WeChat cover image for ACS article: 你的AI需要红绿灯."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/封面_Agent红绿灯.png"

# Colors
BG = "#0f172a"
ACCENT = "#f59e0b"
WHITE = "#f8fafc"
SUB = "#94a3b8"
RED = "#ef4444"
YELLOW = "#eab308"
GREEN = "#22c55e"
DIM = "#1e293b"

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# Font
FONT_TTC = "/System/Library/Fonts/PingFang.ttc"
FONT_FALLBACK = "/System/Library/Fonts/STHeiti Light.ttc"
font_file = FONT_TTC if os.path.exists(FONT_TTC) else FONT_FALLBACK

def f(size):
    try: return ImageFont.truetype(font_file, size)
    except: return ImageFont.load_default()

# --- Traffic light pole ---
pole_x, pole_y0, pole_y1 = 120, 100, 400
draw.rectangle([pole_x-5, pole_y0, pole_x+5, pole_y1], fill="#475569")

# --- Traffic light box ---
box_x0, box_y0 = pole_x - 35, 125
box_x1, box_y1 = pole_x + 35, 345
draw.rectangle([box_x0, box_y0, box_x1, box_y1], fill="#1e293b", outline="#475569", width=2)

# --- Three lights (red yellow green) ---
cx, spacing = pole_x, 55
light_states = [(RED, "R"), (YELLOW, "Y"), (GREEN, "G")]
for i, (color, label) in enumerate(light_states):
    cy = box_y0 + 40 + i * spacing
    radius = 18
    # outer glow
    draw.ellipse([cx-radius-3, cy-radius-3, cx+radius+3, cy+radius+3], fill="#1e293b")
    draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius], fill=color)
    # inner highlight (shiny effect)
    draw.ellipse([cx-radius//2, cy-radius//2, cx+radius//4, cy+radius//4], fill="#ffffff" if label in ("R","Y") else "#ffffff")

# --- Cap on top of pole ---
draw.rectangle([pole_x-15, pole_y0-10, pole_x+15, pole_y0], fill="#475569")

# --- Ground line ---
draw.line([(0, 420), (W, 420)], fill="#334155", width=1)

# --- Right side: Title ---
t1 = f(42)
t1w = draw.textlength("你的AI需要红绿灯", font=t1)
draw.text((W - t1w - 40, 140), "你的AI需要红绿灯", fill=ACCENT, font=t1)

# Subtitle
t2 = f(24)
draw.text((W - t1w - 40 + 5, 195), "——Agent行为规范", fill=WHITE, font=t2)

# Divider line
draw.line([(W - t1w - 40, 240), (W - 40, 240)], fill="#475569", width=1)

# Tagline
t3 = f(18)
tagline = "权限分级  ·  审计追溯  ·  人工干预"
tw = draw.textlength(tagline, font=t3)
draw.text((W - tw - 42, 260), tagline, fill=SUB, font=t3)

# Bottom line
t4 = f(14)
draw.text((W - t1w - 40, 310), "基于 Microsoft Agent Control Specification (ACS)", fill=DIM, font=t4)
draw.text((W - t1w - 40, 335), "主题11 · 涌现系列", fill=DIM, font=t4)

img.save(OUT)
print(f"✅ Cover saved: {OUT}")
