#!/usr/bin/env python3
"""Cover for AI方法论系列 ⑰: 一年后的AI — 2027年中能力推演与个人行动纲领."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/封面_一年后AI.png"

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
def ff(s):
    return ImageFont.truetype(FONT, s) if os.path.exists(FONT) else ImageFont.load_default()

# === Left panel: 2026→2027 clock/calendar visual + 5-dimension progress bars ===

# Arrow / timeline header
draw.text((30, 36), "2026", fill=GOLD, font=ff(24))
draw.text((125, 40), "→", fill=ACCENT, font=ff(18))
draw.text((155, 36), "2027", fill=ACCENT, font=ff(24))

# 5 capability dimensions as progress bars
dimensions = [
    ("推理与抽象", "L2.0", "L2.5", 0.50),
    ("记忆与知识", "L1.5", "L2.0", 0.35),
    ("自主性",    "L1.5", "L2.0", 0.35),
    ("多模态交互", "L2.5", "L3.0", 0.60),
    ("学习与适应", "L1.5", "L1.8", 0.20),
]

bar_left = 30
bar_top = 90
bar_width = 340
bar_height = 18
bar_gap = 38

for idx, (dim_name, current_val, future_val, pct) in enumerate(dimensions):
    y = bar_top + idx * bar_gap

    # Dimension name
    draw.text((bar_left, y - 3), dim_name, fill=WHITE, font=ff(13))

    # Current level label (right-aligned above bar start)
    cur_tw = draw.textlength(current_val, font=ff(12))
    draw.text((bar_left - cur_tw - 8, y + 1), current_val, fill=GOLD, font=ff(12))

    # Background bar
    draw.rounded_rectangle(
        (bar_left, y + 20, bar_left + bar_width, y + 20 + bar_height),
        radius=5, fill=(20, 28, 50)
    )

    # Current level bar (gold)
    cur_w = int(bar_width * pct)
    if cur_w > 0:
        draw.rounded_rectangle(
            (bar_left, y + 20, bar_left + cur_w, y + 20 + bar_height),
            radius=5, fill=GOLD
        )

    # Gap to future level (dashed effect with translucent blue)
    future_pct = pct + 0.15  # one-year gain
    future_w = int(bar_width * min(future_pct, 1.0))
    if future_w > cur_w:
        draw.rounded_rectangle(
            (bar_left + cur_w, y + 20, bar_left + future_w, y + 20 + bar_height),
            radius=5, fill=(96, 165, 250, 180)
        )

    # Future level label
    fut_tw = draw.textlength(future_val, font=ff(12))
    draw.text((bar_left + bar_width + 10, y + 1), future_val, fill=ACCENT, font=ff(12))

# Legend
legend_y = bar_top + 5 * bar_gap + 10
draw.rectangle((bar_left, legend_y, bar_left + 14, legend_y + 10), fill=GOLD)
draw.text((bar_left + 20, legend_y - 2), "当前 (2026.5)", fill=GOLD, font=ff(11))
draw.rectangle((bar_left + 140, legend_y, bar_left + 154, legend_y + 10), fill=ACCENT)
draw.text((bar_left + 160, legend_y - 2), "一年后 (2027.5)", fill=ACCENT, font=ff(11))

# Progress summary at bottom of left panel
summary_y = legend_y + 32
draw.text((bar_left, summary_y), "整体进度", fill=SUB, font=ff(12))
draw.rectangle((bar_left + 80, summary_y + 7, bar_left + 320, summary_y + 9), fill=(30, 41, 59))
draw.text((bar_left, summary_y + 18), "40-50%  →   55-60%", fill=WHITE, font=ff(14))
draw.text((bar_left + 180, summary_y + 20), "离AGI有距离", fill=SUB, font=ff(11))
draw.text((bar_left + 180, summary_y + 36), "离不可或缺没有距离", fill=GREEN, font=ff(11))

# === Right panel: Title and description ===
rx = 420
draw.rectangle((rx, 34, rx + 80, 36), fill=ACCENT)
draw.text((rx, 58), "一年后的AI", fill=WHITE, font=ff(38))
draw.text((rx, 112), "2027年中能力推演", fill=GOLD, font=ff(22))
draw.text((rx, 142), "与个人行动纲领", fill=ACCENT, font=ff(22))

draw.rectangle((rx, 185, 860, 187), fill=(30, 41, 59))

# Key findings summary
findings = [
    ("约束 x 趋势", "五个约束条件 + 四个确定趋势 → 一年后画像"),
    ("核心判断", "一年内无质变，但有数量级的进步"),
    ("最大变量", "Agent编排从实验走向产品化"),
    ("行动窗口", "现在冷启动，一年后不可替代"),
]
for idx, (label, desc) in enumerate(findings):
    fy = 205 + idx * 36
    draw.text((rx, fy), label, fill=GOLD, font=ff(14))
    draw.text((rx + 90, fy), desc, fill=WHITE, font=ff(14))

# Quote line
draw.rectangle((rx, 375, 860, 377), fill=(30, 41, 59))
quote = '"AI发展太快，所以等不起"'
draw.text((rx, 395), quote, fill=SUB, font=ff(13))
draw.text((rx + draw.textlength(quote, font=ff(13)) + 10, 395), "— 陈颖芳", fill=DIM, font=ff(12))

# Bottom
draw.rectangle((rx, 435, 860, 436), fill=(30, 41, 59))
draw.text((rx, 450), "作者：陈颖芳  |  2026年5月  |  AI方法论系列 ⑰", fill=DIM, font=ff(14))

# Vertical accent line on the far left
draw.rectangle((15, 34, 17, 432), fill=(30, 50, 80))

img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
