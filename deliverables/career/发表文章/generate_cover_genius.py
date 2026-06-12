#!/usr/bin/env python3
"""Generate WeChat cover image for "天才的概率分布" article."""
from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/封面_天才的概率分布.png"

BG = "#0f172a"
ACCENT = "#f59e0b"
WHITE = "#f8fafc"
SUB = "#94a3b8"
DIM = "#334155"
PURPLE = "#a78bfa"
TEAL = "#2dd4bf"
PINK = "#f472b6"
PEAK_COLORS = [PURPLE, ACCENT, TEAL, PINK]

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

FONT_TTC = "/System/Library/Fonts/PingFang.ttc"
FONT_FALLBACK = "/System/Library/Fonts/STHeiti Light.ttc"
font_file = FONT_TTC if os.path.exists(FONT_TTC) else FONT_FALLBACK

def f(size):
    try: return ImageFont.truetype(font_file, size)
    except: return ImageFont.load_default()

# --- Left area: Genius distribution peaks ---
# Draw a stylized timeline with 4 peaks
peaks = [
    (70, 370, "Axial"),      # Ancient Greece area
    (180, 310, "Renaissance"),
    (290, 250, "Scientific"),
    (400, 190, "Quantum"),
]
base_y = 420

# Ground line
draw.line([(30, base_y), (440, base_y)], fill=DIM, width=1)

# Time axis labels
f_tiny = ImageFont.truetype(font_file, 11)
draw.text((35, 430), "800BC", fill=DIM, font=f_tiny)
draw.text((145, 430), "1400", fill=DIM, font=f_tiny)
draw.text((255, 430), "1600", fill=DIM, font=f_tiny)
draw.text((380, 430), "1900", fill=DIM, font=f_tiny)

# Draw four peaks as triangles/pyramids
peak_data = [
    (70, 370, 80),    # Axial - small broad
    (180, 310, 90),   # Renaissance - medium
    (290, 250, 100),  # Scientific - larger
    (400, 190, 120),  # Quantum - tallest
]

for i, (cx, top, bottom_w) in enumerate(peak_data):
    bw = bottom_w
    # Draw filled triangle
    points = [(cx, top), (cx - bw//2, base_y), (cx + bw//2, base_y)]
    draw.polygon(points, outline=PEAK_COLORS[i], fill=None)
    # Draw outline
    draw.line([(cx, top), (cx - bw//2, base_y)], fill=PEAK_COLORS[i], width=2)
    draw.line([(cx, top), (cx + bw//2, base_y)], fill=PEAK_COLORS[i], width=2)

# Dashed line showing trend going up toward right
draw.line([(400, 190), (430, 170), (460, 155), (480, 145)], fill=ACCENT, width=2)

# "AI?" label near the end
f_small = ImageFont.truetype(font_file, 13)
draw.text((480, 130), "AI Era?", fill=ACCENT, font=f_small)

# Dots at peak tops
for cx, top, _ in peak_data:
    draw.ellipse([cx-4, top-4, cx+4, top+4], fill=WHITE)

# --- Right side: Title ---
t1 = f(42)
t1w = draw.textlength("天才的概率分布", font=t1)
draw.text((W - t1w - 40, 100), "天才的概率分布", fill=WHITE, font=t1)

t2 = f(20)
t2w = draw.textlength("人类文明史上顶级头脑出现在哪？", font=t2)
draw.text((W - t2w - 40, 160), "人类文明史上'顶级头脑'出现在哪？", fill=SUB, font=t2)

# Divider
draw.line([(W - t1w - 40, 210), (W - 40, 210)], fill=DIM, width=1)

# Stats boxes
t3 = f(16)
stats = [
    ("1170亿", "总人口基数"),
    (">1000万", "理论天才"),
    ("~4000", "记录在册"),
]
for i, (num, label) in enumerate(stats):
    bx = W - t1w - 40
    by = 230 + i * 55
    # Number
    num_w = draw.textlength(num, font=t3)
    draw.text((bx, by), num, fill=ACCENT, font=t3)
    # Label
    draw.text((bx + num_w + 8, by + 2), label, fill=SUB, font=f_small)

# Bottom right: four-dimension model
t4 = f(12)
dims = "人口 × 营养 × 制度 × 知识"
dw = draw.textlength(dims, font=t4)
draw.text((W - dw - 40, 410), dims, fill=DIM, font=t4)

img.save(OUT)
print(f"✅ Cover saved: {OUT}")
