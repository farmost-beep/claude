#!/usr/bin/env python3
"""Cover for AI方法论系列 ⑨: Personal knowledge management with AI."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/封面_知识库AI.png"

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

# === Left panel: 4-layer knowledge architecture ===
layers = [
    ("生成", GREEN),
    ("连接", PURPLE),
    ("整理", ACCENT),
    ("收集", GOLD),
]
cx, base_y = 100, 150
for idx, (name, clr) in enumerate(layers):
    ly = base_y - 40 + idx * 52
    tw = draw.textlength(name, font=ff(16))
    # Layer block
    draw.rounded_rectangle((cx - 30, ly, cx - 30 + tw + 40, ly + 42), radius=10, fill=clr)
    draw.text((cx - 5, ly + 10), name, fill=WHITE if clr != GOLD else BG, font=ff(16))
    # Arrow between layers (except last)
    if idx < 3:
        draw.text((cx + tw // 2 + 5, ly + 42), "↑", fill=DIM, font=ff(14))

# Labels on the side
draw.text((cx - 85, base_y - 132), "Obsidian", fill=GOLD, font=ff(12))
draw.text((cx - 85, base_y - 115), "Vault", fill=GOLD, font=ff(12))
draw.text((cx - 85, base_y + 90), "AI记忆", fill=PURPLE, font=ff(12))
draw.text((cx - 85, base_y + 106), "飞轮", fill=PURPLE, font=ff(12))

# Vertical bracket lines
draw.line(((cx - 75, base_y - 42), (cx - 75, base_y + 128)), fill=(50, 60, 80), width=1)
draw.line(((cx - 78, base_y - 42), (cx - 72, base_y - 42)), fill=DIM, width=1)
draw.line(((cx - 78, base_y + 128), (cx - 72, base_y + 128)), fill=DIM, width=1)

# Dual-system diagram: small boxes showing Obsidian & AI memory interaction
obsidian_items = ["笔记", "标签", "MOC", "日报"]
ai_memory_items = ["Embed", "检索", "摘要", "生成"]

for idx, (obs, ai) in enumerate(zip(obsidian_items, ai_memory_items)):
    ix = cx - 65 + idx * 42
    # Obsidian row
    draw.rounded_rectangle((ix - 3, base_y - 62, ix + 33, base_y - 38), radius=5, outline=GOLD, width=1)
    draw.text((ix + 2, base_y - 57), obs, fill=GOLD, font=ff(9))
    # AI memory row
    draw.rounded_rectangle((ix - 3, base_y + 115, ix + 33, base_y + 139), radius=5, outline=PURPLE, width=1)
    draw.text((ix + 2, base_y + 120), ai, fill=PURPLE, font=ff(9))

# Connecting dots between rows
for idx in range(4):
    ix = cx - 50 + idx * 42
    draw.ellipse((ix + 12, base_y + 98, ix + 20, base_y + 106), fill=DIM)

# === Right panel: Title and content ===
rx = 250
draw.rectangle((rx, 34, rx + 80, 36), fill=PURPLE)
draw.text((rx, 58), "AI时代的", fill=WHITE, font=ff(36))
draw.text((rx, 108), "个人知识管理", fill=GOLD, font=ff(40))
draw.text((rx, 158), "从'记不住'到'自动生成'", fill=ACCENT, font=ff(22))

draw.rectangle((rx, 195, 860, 197), fill=(30, 41, 59))

# 4-layer description
k_flows = [
    ("收集", "Obsidian笔记 + 截屏 + 链接保存"),
    ("整理", "标签 · MOC · 日记模板 · 文件夹"),
    ("连接", "AI Embedding · 语义检索 · 自动关联"),
    ("生成", "日报 · 周报 · 知识卡片 · 研究报告"),
]
for idx, (label, desc) in enumerate(k_flows):
    ky = 215 + idx * 38
    icons = ["📥", "📁", "🔗", "📤"]
    draw.text((rx, ky), icons[idx], fill=WHITE, font=ff(14))
    draw.text((rx + 30, ky), label, fill=GREEN, font=ff(14))
    draw.text((rx + 80, ky), desc, fill=WHITE, font=ff(14))

# Key insight
draw.rectangle((rx, 375, 860, 377), fill=(30, 41, 59))
quote = '"让知识流动起来，而不是堆积在文件夹里"'
draw.text((rx, 395), quote, fill=SUB, font=ff(13))
draw.text((rx + draw.textlength(quote, font=ff(13)) + 10, 395), "— 陈颖芳", fill=DIM, font=ff(12))

# Stats row
stats = [
    ("149+", "PDF文档"),
    ("6个", "知识领域"),
    ("~1秒", "智能检索"),
    ("∞", "知识连接"),
]
sx = rx
for stat_val, stat_label in stats:
    draw.text((sx, 420), stat_val, fill=GOLD, font=ff(16))
    draw.text((sx + draw.textlength(stat_val, font=ff(16)) + 6, 422), stat_label, fill=DIM, font=ff(10))
    sx += 110

# Bottom
draw.rectangle((rx, 450, 860, 451), fill=(30, 41, 59))
draw.text((rx, 465), "作者：陈颖芳  |  2026年5月  |  AI方法论系列 ⑨", fill=DIM, font=ff(14))

# Vertical accent line
draw.rectangle((15, 34, 17, 462), fill=(50, 30, 80))

img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
