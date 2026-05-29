#!/usr/bin/env python3
"""Cover for AI方法论系列 ⑮: AGI定义文件."""
from PIL import Image, ImageDraw, ImageFont
import os
import math

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/封面_AGI定义.png"

BG = (8, 12, 30)
WHITE = (241, 245, 249)
SUB = (148, 163, 184)
DIM = (71, 85, 105)
ACCENT = (96, 165, 250)
RED = (239, 68, 68)
GOLD = (245, 158, 11)
GREEN = (52, 211, 153)
PURPLE = (167, 139, 250)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

FONT = "/System/Library/Fonts/PingFang.ttc"
if not os.path.exists(FONT):
    FONT = "/System/Library/Fonts/STHeiti Light.ttc"
def ff(s): return ImageFont.truetype(FONT, s) if os.path.exists(FONT) else ImageFont.load_default()

# === Title area ===
draw.rectangle((50, 34, 130, 36), fill=PURPLE)
draw.text((50, 58), "AGI定义文件", fill=WHITE, font=ff(38))
draw.text((50, 112), "五个维度 x 六个等级 · 清晰可测的边界", fill=ACCENT, font=ff(20))

# === Divider ===
draw.rectangle((50, 155, 860, 157), fill=(30, 41, 59))

# === Radar/Pentagon chart (left side) ===
# Canvas area for pentagon
radar_cx, radar_cy = 150, 300
radar_r = 110

# 5 dimensions placed in pentagon orientation
dim_names = ["推理\n与抽象", "记忆\n与知识", "自主性\n目标管理", "多模态\n交互", "学习\n与适应"]
dim_colors = [ACCENT, GREEN, GOLD, PURPLE, RED]
n = 5

# Draw 6 concentric rings (L0-L5)
ring_colors = [
    (30, 41, 59, 180),   # L0
    (30, 50, 70, 150),   # L1
    (30, 60, 85, 120),   # L2
    (40, 70, 100, 90),   # L3
    (50, 85, 115, 60),   # L4
    (60, 100, 130, 40),  # L5
]
for level in range(6):
    ratio = (level + 1) / 6
    r = int(radar_r * ratio)
    pts = []
    for i in range(n):
        angle = -math.pi / 2 + 2 * math.pi * i / n
        x = radar_cx + r * math.cos(angle)
        y = radar_cy + r * math.sin(angle)
        pts.append((x, y))
    draw.polygon(pts, outline=(50, 70, 100, 80), fill=ring_colors[level])

# Draw axis lines
for i in range(n):
    angle = -math.pi / 2 + 2 * math.pi * i / n
    x = radar_cx + radar_r * 1.05 * math.cos(angle)
    y = radar_cy + radar_r * 1.05 * math.sin(angle)
    draw.line((radar_cx, radar_cy, int(x), int(y)), fill=(50, 70, 100, 100), width=1)

# Draw pentagon vertices (L6 = current outline)
r6 = int(radar_r * 0.6)  # roughly L2-L3 level
pts6 = []
for i in range(n):
    angle = -math.pi / 2 + 2 * math.pi * i / n
    x = radar_cx + r6 * math.cos(angle)
    y = radar_cy + r6 * math.sin(angle)
    pts6.append((int(x), int(y)))
draw.polygon(pts6, outline=GOLD, fill=(245, 158, 11, 40), width=2)

# Draw dimension labels
for i in range(n):
    angle = -math.pi / 2 + 2 * math.pi * i / n
    lx = radar_cx + (radar_r + 40) * math.cos(angle)
    ly = radar_cy + (radar_r + 40) * math.sin(angle)
    label = dim_names[i]
    lines = label.split("\n")
    tl = 0
    for li, line in enumerate(lines):
        tw = draw.textlength(line, font=ff(10))
        tl = max(tl, tw)
    for li, line in enumerate(lines):
        tw = draw.textlength(line, font=ff(10))
        draw.text((lx - tw / 2, ly - 6 + li * 12), line, fill=dim_colors[i], font=ff(10))

# Level labels on the top axis
for level in range(6):
    ratio = (level + 1) / 6
    r = int(radar_r * ratio)
    lx = radar_cx - 18
    ly = radar_cy - r + 2
    draw.text((lx, ly), f"L{level}", fill=DIM, font=ff(7))

# === Right panel: text description ===
rx = 340
desc_y = 185
descriptions = [
    (GOLD, "AGI = 五个维度全部达到 L3"),
    (GREEN, "  可测量 · 不模糊 · 分阶段 · 可追踪"),
    (DIM, ""),
    (WHITE, "当前进度: 40-50%"),
    (ACCENT, "多模态最近 (L2.5)  学习最远 (L1.5)"),
    (DIM, ""),
    (GOLD, "ASI = 五个维度全部达到 L5"),
    (SUB, "预计AGI: 2029-2031年"),
]
for idx, (clr, line) in enumerate(descriptions):
    dy = desc_y + idx * 30
    draw.text((rx, dy), line, fill=clr, font=ff(15 if idx < 2 else 12))

# Level legend
legend_y = 400
legend_items = [
    (ACCENT, "L0-L2 = 当前AI能力范围"),
    (GOLD, "L3 = AGI门槛"),
    (PURPLE, "L4-L5 = ASI能力范围"),
]
for idx, (clr, label) in enumerate(legend_items):
    lx = rx + idx * 180
    draw.ellipse((lx, legend_y + 4, lx + 8, legend_y + 12), fill=clr)
    draw.text((lx + 14, legend_y), label, fill=SUB, font=ff(11))

# === Bottom ===
draw.rectangle((50, 435, 860, 436), fill=(30, 41, 59))
draw.text((50, 450), "作者：陈颖芳  |  2026年5月  |  AI方法论系列 ⑮", fill=DIM, font=ff(14))

# Vertical accent line on the far left
draw.rectangle((15, 34, 17, 432), fill=(30, 50, 80))

img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
