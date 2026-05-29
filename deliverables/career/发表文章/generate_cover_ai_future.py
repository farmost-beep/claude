#!/usr/bin/env python3
"""Cover for AI方法论系列 ⑯: AI未来发展方向."""
from PIL import Image, ImageDraw, ImageFont
import os
import math

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/封面_AI未来方向.png"

BG = (8, 12, 30)
WHITE = (241, 245, 249)
SUB = (148, 163, 184)
DIM = (71, 85, 105)
ACCENT = (96, 165, 250)
RED = (239, 68, 68)
GOLD = (245, 158, 11)
GREEN = (52, 211, 153)
PURPLE = (167, 139, 250)
CYAN = (34, 211, 238)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

FONT = "/System/Library/Fonts/PingFang.ttc"
if not os.path.exists(FONT):
    FONT = "/System/Library/Fonts/STHeiti Light.ttc"
def ff(s): return ImageFont.truetype(FONT, s) if os.path.exists(FONT) else ImageFont.load_default()

# === Title area ===
draw.rectangle((50, 34, 130, 36), fill=CYAN)
draw.text((50, 58), "AI未来发展方向", fill=WHITE, font=ff(38))
draw.text((50, 112), "六个核心方向 · 从工具到系统 · 从执行到创造", fill=ACCENT, font=ff(20))

# === Divider ===
draw.rectangle((50, 155, 860, 157), fill=(30, 41, 59))

# === 6 Converging paths / arrows (left side → horizon) ===
# Each direction is an arrow starting from left side and converging toward right side
directions = [
    ("系统式AI", ACCENT, "对话→系统"),
    ("Agent系统化", GREEN, "个体→组织"),
    ("形式化验证", RED, "相信→证明"),
    ("多模态统一", PURPLE, "数字→物理"),
    ("个性化普适化", GOLD, "通用→专属"),
    ("独立智能体", CYAN, "工具→自主"),
]

# Arrow paths: start wide on left, converge on right
start_y_base = 180
end_y_base = 300
step_y = 32
right_limit = 600

for idx, (name, clr, subtitle) in enumerate(directions):
    sy = start_y_base + idx * step_y
    ey = end_y_base - (5 - idx) * 30  # converge toward center

    # Start at left, arc toward center-right
    sx = 55
    ex = right_limit + idx * 10  # stagger the convergence point for visual clarity

    # Draw a curved arrow from left to right
    mid_x = (sx + ex) // 2
    mid_y = (sy + ey) // 2

    # Arrow path: straight line with slight curve
    # Draw as a series of line segments forming a path
    segment_count = 12
    points = []
    for i in range(segment_count + 1):
        t = i / segment_count
        # Use bezier-like curve: start horizontal, curve upward, reach destination
        px = sx + (ex - sx) * t
        # Vertical follows a sine curve peaking at midpoint
        py = sy + (ey - sy) * t + 20 * math.sin(t * math.pi)

        points.append((int(px), int(py)))

    # Draw path line
    for i in range(len(points) - 1):
        alpha = int(120 + 60 * (i / len(points)))
        draw.line((points[i], points[i+1]), fill=clr + (alpha,), width=2)

    # Arrow head at end
    last_pt = points[-1]
    prev_pt = points[-2]
    a_angle = math.atan2(last_pt[1] - prev_pt[1], last_pt[0] - prev_pt[0])
    arrow_len = 10
    arrow_angle = math.pi / 6
    draw.polygon([
        last_pt,
        (last_pt[0] - arrow_len * math.cos(a_angle - arrow_angle),
         last_pt[1] - arrow_len * math.sin(a_angle - arrow_angle)),
        (last_pt[0] - arrow_len * math.cos(a_angle + arrow_angle),
         last_pt[1] - arrow_len * math.sin(a_angle + arrow_angle)),
    ], fill=clr)

    # Direction name at start
    draw.text((sx + 4, sy - 6), name, fill=clr, font=ff(12))

    # Subtitle at end
    tw = draw.textlength(subtitle, font=ff(10))
    draw.text((ex + 8, points[-1][1] - 6), subtitle, fill=clr, font=ff(10))

# === Horizon line ===
# Draw a subtle horizon where paths converge
horizon_y = 300
draw.line((right_limit - 20, horizon_y, 860, horizon_y), fill=(40, 60, 90, 100), width=1)

# === Timeline markings on the right ===
timeline_start_x = right_limit + 60
timeline_items = [
    (2026, ACCENT),
    (2027, GREEN),
    (2028, GOLD),
    (2030, PURPLE),
    (2030, CYAN, "+"),
]
ctx = timeline_start_x
for item in timeline_items:
    if len(item) == 2:
        year, clr = item
        suffix = ""
    else:
        year, clr, suffix = item

    year_str = f"{year}{suffix}"
    dot_y = horizon_y
    draw.ellipse((ctx, dot_y - 4, ctx + 8, dot_y + 4), fill=clr)
    tw = draw.textlength(year_str, font=ff(9))
    draw.text((ctx + 4 - tw/2, dot_y + 10), year_str, fill=clr, font=ff(9))
    ctx += 42

# === Right panel: summary ===
rx = 50
summary_y = 330
summary_items = [
    ("系统式AI", ACCENT, "交互范式根本性迁移"),
    ("Agent系统化", GREEN, "从个体工具到AI组织"),
    ("形式化验证", RED, "可验证 > 更强大"),
    ("多模态统一", PURPLE, "数字→物理→超过人类"),
    ("个性化普适化", GOLD, "通用基座+个性记忆层"),
    ("独立智能体", CYAN, "协作者→研究者→治理"),
]

for idx, (label, clr, desc) in enumerate(summary_items):
    col = idx % 3
    row = idx // 3
    ix = 50 + col * 270
    iy = summary_y + row * 42
    draw.ellipse((ix, iy + 6, ix + 6, iy + 12), fill=clr)
    draw.text((ix + 12, iy + 2), label, fill=clr, font=ff(12))
    tw = draw.textlength(label, font=ff(12))
    draw.text((ix + 16 + tw, iy + 2), desc, fill=SUB, font=ff(11))

# Key insight
draw.rectangle((50, 430, 860, 431), fill=(30, 41, 59))
draw.text((50, 410), "核心洞察: 六个方向相互加速 — 验证+Agent = 独立智能体的基石", fill=DIM, font=ff(12))

# === Bottom ===
draw.text((50, 450), "作者：陈颖芳  |  2026年5月  |  AI方法论系列 ⑯", fill=DIM, font=ff(14))

# Vertical accent line on the far left
draw.rectangle((15, 34, 17, 432), fill=(30, 50, 80))

img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
