#!/usr/bin/env python3
"""Cover: Mythos之后② — Daniela Amodei | 900×400 WeChat-safe."""
from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 900, 400
OUT = os.path.dirname(__file__) + "/封面_Agent失败模式.png"

BG        = (250, 248, 243)
INK       = (28, 25, 23)
SUB       = (107, 94, 83)
DIM       = (168, 156, 142)
GOLD      = (201, 169, 110)
ACCENT    = (44, 95, 124)
CARD_BG   = (240, 235, 224)
CARD_BG2  = (255, 255, 255)
SOFT_LINE = (229, 221, 208)
RED       = (180, 60, 50)
ORANGE    = (200, 110, 45)
YELLOW    = (195, 155, 55)
SKIN      = (250, 225, 195)
HAIR_BRN  = (60, 35, 20)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

FONT = "/System/Library/Fonts/PingFang.ttc"
if not os.path.exists(FONT):
    FONT = "/System/Library/Fonts/STHeiti Light.ttc"
def ff(s):
    return ImageFont.truetype(FONT, s) if os.path.exists(FONT) else ImageFont.load_default()

def draw_daniela(draw, cx, cy, scale=1.0):
    s = scale
    draw.ellipse((cx-28*s, cy-33*s, cx+28*s, cy+33*s), fill=SKIN, outline=(180,155,130), width=2)
    draw.ellipse((cx-34*s, cy-40*s, cx+34*s, cy-2*s), fill=HAIR_BRN)
    draw.ellipse((cx-28*s, cy-33*s, cx+28*s, cy-2*s), fill=SKIN)
    draw.ellipse((cx-38*s, cy-12*s, cx-20*s, cy+32*s), fill=HAIR_BRN)
    draw.ellipse((cx+20*s, cy-12*s, cx+38*s, cy+32*s), fill=HAIR_BRN)
    draw.ellipse((cx-30*s, cy-40*s, cx-12*s, cy-14*s), fill=HAIR_BRN)
    draw.ellipse((cx+12*s, cy-40*s, cx+30*s, cy-14*s), fill=HAIR_BRN)
    draw.ellipse((cx-14*s, cy-8*s, cx-2*s, cy+2*s), fill=INK)
    draw.ellipse((cx+2*s, cy-8*s, cx+14*s, cy+2*s), fill=INK)
    draw.ellipse((cx-10*s, cy-5*s, cx-6*s, cy-1*s), fill=BG)
    draw.ellipse((cx+6*s, cy-5*s, cx+10*s, cy-1*s), fill=BG)
    draw.arc((cx-15*s, cy-12*s, cx-1*s, cy-4*s), start=200, end=340, fill=(40,25,15), width=2)
    draw.arc((cx+1*s, cy-12*s, cx+15*s, cy-4*s), start=200, end=340, fill=(40,25,15), width=2)
    draw.arc((cx-16*s, cy-16*s, cx-1*s, cy-10*s), start=180, end=0, fill=(50,30,20), width=2)
    draw.arc((cx+1*s, cy-16*s, cx+16*s, cy-10*s), start=180, end=0, fill=(50,30,20), width=2)
    draw.arc((cx-4*s, cy-1*s, cx+4*s, cy+7*s), start=200, end=340, fill=(170,140,110), width=2)
    draw.arc((cx-7*s, cy+8*s, cx+7*s, cy+19*s), start=0, end=180, fill=(190,110,100), width=2)

# ============================================================
# Left panel
# ============================================================
lx = 20

draw.rounded_rectangle((lx, 14, 418, 386), radius=10, fill=CARD_BG2, outline=SOFT_LINE, width=1)
draw.rectangle((lx + 4, 17, 414, 19), fill=RED)

draw_daniela(draw, lx + 58, 64, scale=0.85)

draw.text((lx + 14, 128), "七种失败模式", fill=INK, font=ff(16))
draw.text((lx + 14, 150), "没有治理的AI会在哪里出事", fill=SUB, font=ff(10))

failures = [
    ("01", "目标歧义", RED),
    ("02", "上下文污染", ORANGE),
    ("03", "工具误用", YELLOW),
    ("04", "权限越界", RED),
    ("05", "状态漂移", ORANGE),
    ("06", "幻觉连锁", YELLOW),
    ("07", "过早收敛", DIM),
]

# 7 modes in a compact grid: 4 left + 3 right
for i, (num, name, clr) in enumerate(failures):
    if i < 4:
        col_x = lx + 12
        ry = 172 + i * 38
    else:
        col_x = lx + 210
        ry = 172 + (i - 4) * 38

    draw.rounded_rectangle((col_x, ry, col_x + 30, ry + 24), radius=6, fill=clr)
    draw.text((col_x + 5, ry + 4), num, fill=CARD_BG2, font=ff(10))
    draw.text((col_x + 38, ry + 3), name, fill=clr, font=ff(14))

# Bottom insight
draw.rounded_rectangle((lx + 12, 332, lx + 402, 374), radius=6, fill=(200, 185, 165, 35), outline=(180, 60, 50, 50), width=1)
draw.text((lx + 24, 340), "这些不是bug，是优化目标时的自主选择", fill=RED, font=ff(12))
draw.text((lx + 24, 358), "每发现一种失败模式 → 为治理型Agent找到一条设计原则", fill=SUB, font=ff(10))

draw.text((lx + 130, 380), "Daniela Amodei · Anthropic President", fill=DIM, font=ff(8))

# ============================================================
# Right panel: Title
# ============================================================
rx = 440

draw.rectangle((rx, 17, rx + 70, 19), fill=RED)
badge_text = "Mythos之后 ②"
bw = int(draw.textlength(badge_text, font=ff(11)) + 14)
draw.rounded_rectangle((870 - bw, 17, 870, 37), radius=5, fill=RED)
draw.text((870 - bw + 7, 20), badge_text, fill=BG, font=ff(11))

draw.text((rx, 46), "Agent的七种失败模式", fill=INK, font=ff(30))
draw.text((rx, 90), "——它不出事才奇怪", fill=RED, font=ff(24))

draw.text((rx, 128), "没有治理的AI，每一步都可能踏进陷阱", fill=SUB, font=ff(13))

draw.rectangle((rx, 154, 870, 156), fill=SOFT_LINE)

# 3 risk categories
risk_cats = [
    ("认知失败", "目标歧义\n上下文污染\n幻觉连锁", RED),
    ("行为失败", "工具误用\n权限越界\n状态漂移", ORANGE),
    ("决策失败", "过早收敛", YELLOW),
]

for i, (cat_name, items, clr) in enumerate(risk_cats):
    cx = rx + i * 148
    draw.rounded_rectangle((cx, 168, cx + 134, 280), radius=8, fill=CARD_BG, outline=clr, width=1)
    draw.text((cx + 10, 176), cat_name, fill=clr, font=ff(13))
    for j, line in enumerate(items.split("\n")):
        draw.text((cx + 10, 198 + j * 24), f"• {line}", fill=SUB, font=ff(11))

# Key message
draw.rounded_rectangle((rx, 296, 870, 370), radius=10, fill=(44, 95, 124, 15), outline=GOLD, width=1)
draw.text((rx + 16, 310), "每发现一种失败模式，就为治理型Agent找到一条设计原则", fill=INK, font=ff(15))
draw.text((rx + 16, 340), "七种模式覆盖：认知失败 + 行为失败 + 决策失败", fill=ACCENT, font=ff(12))

draw.rectangle((rx, 376, 870, 378), fill=SOFT_LINE)
draw.text((rx, 383), "作者：陈颖芳  |  2026年5月  |  Mythos之后·第二篇", fill=DIM, font=ff(11))

draw.rectangle((426, 14, 428, 386), fill=SOFT_LINE)

img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
