#!/usr/bin/env python3
"""Cover for AI方法论系列 ⑩: 30-day management mode startup checklist."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/封面_管理模式落地手册.png"

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

# === Left panel: 4-week roadmap with calendar feel ===
weeks = [
    ("W1", "选场景 + 建记忆", GREEN),
    ("W2", "拆任务 + 跑并行", ACCENT),
    ("W3", "交叉审查 + 异常聚焦", (239, 68, 68)),
    ("W4", "回顾优化 + 固化习惯", PURPLE),
]

# Week cards stacked vertically with connecting arrows
wx, wy = 30, 80
card_w, card_h = 180, 65
for idx, (label, desc, clr) in enumerate(weeks):
    cy_w = wy + idx * (card_h + 12)
    # Card background
    draw.rounded_rectangle((wx, cy_w, wx + card_w, cy_w + card_h), radius=10, fill=clr)
    # Week number
    draw.text((wx + 10, cy_w + 8), label, fill=WHITE, font=ff(22))
    # Description
    draw.text((wx + 10, cy_w + 35), desc, fill=WHITE, font=ff(11))
    # Arrow between weeks
    if idx < 3:
        arrow_y = cy_w + card_h
        draw.text((wx + card_w // 2 - 5, arrow_y + 2), "↓", fill=GOLD, font=ff(14))

# Day-by-day sample for Week 1 on the right of left panel
day_labels = ["Mon 选场景", "Tue 装工具", "Wed 建记忆", "Thu 跑测试", "Fri 复盘"]
dx_base = wx + card_w + 25
for idx, day in enumerate(day_labels):
    dy = wy + idx * 28
    check = "☑" if idx < 3 else "☐"
    clr = GREEN if idx < 3 else DIM
    draw.text((dx_base, dy), check, fill=clr, font=ff(12))
    draw.text((dx_base + 18, dy), day, fill=SUB if idx < 3 else DIM, font=ff(9))

# Progression bar at bottom of left panel
bar_x, bar_y = wx, wy + 4 * (65 + 12) + 10
segments = [(0, 60, GREEN), (60, 120, ACCENT), (120, 180, (239, 68, 68)), (180, 240, PURPLE)]
for seg_x, seg_x2, seg_clr in segments:
    rx1 = bar_x + seg_x
    rx2 = bar_x + seg_x2
    draw.rectangle((rx1, bar_y, rx2 - 2, bar_y + 8), fill=seg_clr)
draw.text((bar_x - 5, bar_y + 12), "进度  —————————  →", fill=DIM, font=ff(9))

# Milestone markers
milestones = ["Day0", "Day7", "Day14", "Day21", "Day30"]
for idx, ms in enumerate(milestones):
    mx = bar_x + idx * 60 - 10
    draw.text((mx, bar_y + 25), ms, fill=DIM, font=ff(8))

# === Right panel: Title and content ===
rx = 380
draw.rectangle((rx, 34, rx + 80, 36), fill=GREEN)
draw.text((rx, 58), "管理模式", fill=WHITE, font=ff(36))
draw.text((rx, 108), "30天启动清单", fill=GOLD, font=ff(40))
draw.text((rx, 158), "从'问答模式'到'管理模式'的最小行动路径", fill=ACCENT, font=ff(18))

draw.rectangle((rx, 195, 860, 197), fill=(30, 41, 59))

# What you get in each week
week_details = [
    ("第1周", "选1个高频场景 │ 建立Agent记忆层 │ 跑通第一次自主执行"),
    ("第2周", "拆解任务为子步骤 │ 并行启动多个Agent │ 观察协作效率"),
    ("第3周", "引入交叉审查 │ 自动标记异常输出 │ 人类只聚焦差异点"),
    ("第4周", "回顾30天数据 │ 优化Agent配置 │ 制定长期习惯计划"),
]
for idx, (label, desc) in enumerate(week_details):
    wy2 = 215 + idx * 42
    draw.text((rx, wy2), label, fill=GREEN, font=ff(14))
    draw.text((rx + 60, wy2), desc, fill=WHITE, font=ff(13))

# Core principle
draw.rectangle((rx, 390, 860, 392), fill=(30, 41, 59))
principle = '"从工具到系统的进化，从30天开始"'
draw.text((rx, 408), principle, fill=SUB, font=ff(13))
draw.text((rx + draw.textlength(principle, font=ff(13)) + 10, 408), "— 陈颖芳", fill=DIM, font=ff(12))

# Checklist feel: 3 stages
stages = ["启动", "加速", "自动化"]
sx = rx
stage_clrs = [ACCENT, GOLD, GREEN]
for idx, stage in enumerate(stages):
    draw.rounded_rectangle((sx, 432, sx + 60, 454), radius=8, fill=stage_clrs[idx])
    draw.text((sx + 10, 435), stage, fill=BG, font=ff(11))
    sx += 72

# Bottom
draw.rectangle((rx, 465, 860, 466), fill=(30, 41, 59))
draw.text((rx, 478), "作者：陈颖芳  |  2026年5月  |  AI方法论系列 ⑩", fill=DIM, font=ff(14))

# Vertical accent line
draw.rectangle((15, 34, 17, 475), fill=(30, 60, 50))

img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
