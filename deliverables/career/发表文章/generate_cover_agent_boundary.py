#!/usr/bin/env python3
"""Cover: Mythos之后③ — 给AI设边界 / 900×400 WeChat-safe."""
from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 900, 400
OUT = os.path.dirname(__file__) + "/封面_给AI设边界.png"

BG        = (250, 248, 243)
INK       = (28, 25, 23)
SUB       = (107, 94, 83)
DIM       = (168, 156, 142)
GOLD      = (201, 169, 110)
ACCENT    = (44, 95, 124)
CARD_BG   = (240, 235, 224)
CARD_BG2  = (255, 255, 255)
SOFT_LINE = (229, 221, 208)
GREEN     = (76, 140, 120)
PURPLE    = (140, 95, 130)
SKIN      = (248, 220, 188)
HAIR_LT   = (180, 150, 120)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

FONT = "/System/Library/Fonts/PingFang.ttc"
if not os.path.exists(FONT):
    FONT = "/System/Library/Fonts/STHeiti Light.ttc"
def ff(s):
    return ImageFont.truetype(FONT, s) if os.path.exists(FONT) else ImageFont.load_default()

def draw_jack(draw, cx, cy, scale=1.0):
    s = scale
    draw.ellipse((cx-28*s, cy-33*s, cx+28*s, cy+33*s), fill=SKIN, outline=(175,150,125), width=2)
    draw.ellipse((cx-34*s, cy-40*s, cx+34*s, cy-5*s), fill=HAIR_LT)
    draw.ellipse((cx-28*s, cy-33*s, cx+28*s, cy-5*s), fill=SKIN)
    draw.ellipse((cx-36*s, cy-14*s, cx-22*s, cy+20*s), fill=HAIR_LT)
    draw.ellipse((cx+22*s, cy-14*s, cx+36*s, cy+20*s), fill=HAIR_LT)
    draw.ellipse((cx-18*s, cy+4*s, cx+18*s, cy+37*s), fill=(190, 175, 150))
    draw.ellipse((cx-16*s, cy+14*s, cx+16*s, cy+39*s), fill=(190, 175, 150))
    draw.ellipse((cx-16*s, cy-8*s, cx-4*s, cy+2*s), fill=INK)
    draw.ellipse((cx+4*s, cy-8*s, cx+16*s, cy+2*s), fill=INK)
    draw.ellipse((cx-12*s, cy-5*s, cx-8*s, cy-1*s), fill=BG)
    draw.ellipse((cx+8*s, cy-5*s, cx+12*s, cy-1*s), fill=BG)
    draw.rounded_rectangle((cx-20*s, cy-12*s, cx-1*s, cy+4*s), radius=6, fill=None, outline=(80,70,55), width=2)
    draw.rounded_rectangle((cx+1*s, cy-12*s, cx+20*s, cy+4*s), radius=6, fill=None, outline=(80,70,55), width=2)
    draw.line((cx-1*s, cy-3*s, cx+1*s, cy-3*s), fill=(80,70,55), width=2)
    draw.arc((cx-5*s, cy-1*s, cx+5*s, cy+7*s), start=190, end=350, fill=(160,130,100), width=2)
    draw.arc((cx-7*s, cy+8*s, cx+7*s, cy+17*s), start=10, end=170, fill=(150,115,95), width=2)

# ============================================================
# Left panel: 四条原则 + Jack Clark
# ============================================================
lx = 20

draw.rounded_rectangle((lx, 14, 418, 386), radius=10, fill=CARD_BG2, outline=SOFT_LINE, width=1)
draw.rectangle((lx + 4, 17, 414, 19), fill=GOLD)

draw_jack(draw, lx + 58, 62, scale=0.85)

draw.text((lx + 14, 126), "治理型Agent的四条原则", fill=INK, font=ff(16))
draw.text((lx + 14, 148), "从Karpathy/Dario/Nadella/Willison真实配置中提炼", fill=SUB, font=ff(9))

principles = [
    ("①", "判断权不可委托", "AI出信息，人出判断", GOLD),
    ("②", "验证与生成分离", "不让同一个AI检查自己的输出", GREEN),
    ("③", "按风险分级授权", "按后果严重程度配验证强度", ACCENT),
    ("④", "人审异常不审常态", "AI盯一切，人只看标记的异常", PURPLE),
]

for i, (num, name, desc, clr) in enumerate(principles):
    py = 168 + i * 44
    draw.rounded_rectangle((lx + 12, py, lx + 402, py + 36), radius=7, fill=CARD_BG, outline=clr, width=1)
    draw.ellipse((lx + 20, py + 4, lx + 44, py + 28), fill=clr)
    draw.text((lx + 26, py + 7), num, fill=CARD_BG2, font=ff(13))
    draw.text((lx + 54, py + 3), name, fill=clr, font=ff(15))
    draw.text((lx + 54, py + 21), desc, fill=SUB, font=ff(10))

# Bottom
draw.rounded_rectangle((lx + 12, 350, lx + 402, 374), radius=6, fill=(44, 95, 124, 10))
draw.text((lx + 28, 357), "终审→验证→配置→监控，四层围合，就是治理体系", fill=INK, font=ff(10))
draw.text((lx + 125, 378), "Jack Clark · Anthropic 政策与安全", fill=DIM, font=ff(8))

# ============================================================
# Right panel: Title
# ============================================================
rx = 440

draw.rectangle((rx, 17, rx + 70, 19), fill=GOLD)
badge_text = "Mythos之后 ③"
bw = int(draw.textlength(badge_text, font=ff(11)) + 14)
draw.rounded_rectangle((870 - bw, 17, 870, 37), radius=5, fill=GOLD)
draw.text((870 - bw + 7, 20), badge_text, fill=BG, font=ff(11))

draw.text((rx, 46), "Mythos发布以后，怎么给AI设边界", fill=INK, font=ff(26))
draw.text((rx, 84), "治理型Agent的四条原则", fill=GOLD, font=ff(24))

draw.text((rx, 120), "业界领袖的真实做法 × 四条可操作的原则 × 10分钟启动清单", fill=SUB, font=ff(12))

draw.rectangle((rx, 146, 870, 148), fill=SOFT_LINE)

draw.text((rx, 160), "四条原则围住的同一个东西：AI的判断边界", fill=INK, font=ff(14))

# Four icons row: principles summary
icons = [
    ("判断权", "人做决定", GOLD),
    ("验证", "独立审查", GREEN),
    ("分级", "后果匹配", ACCENT),
    ("监控", "只审异常", PURPLE),
]

for i, (label, desc, clr) in enumerate(icons):
    px = rx + i * 110
    draw.rounded_rectangle((px, 186, px + 94, 270), radius=8, fill=CARD_BG, outline=clr, width=1)
    draw.text((px + 12, 198), label, fill=clr, font=ff(18))
    draw.text((px + 12, 228), desc, fill=INK, font=ff(14))
    draw.text((px + 12, 252), "原则" + str(i+1), fill=DIM, font=ff(9))

draw.rounded_rectangle((rx, 286, 870, 370), radius=10, fill=CARD_BG, outline=SOFT_LINE, width=1)
draw.text((rx + 16, 302), "AI负责信息，人负责判断。验证独立于生成。按后果配强度。常态自动化，异常人介入。", fill=INK, font=ff(14))
draw.text((rx + 16, 332), "你不需要成为Karpathy。今天就能用这四条原则。", fill=SUB, font=ff(12))
draw.text((rx + 16, 354), "10分钟启动：列出AI任务→双实例交叉验证→写一条停机制", fill=ACCENT, font=ff(11))

draw.rectangle((rx, 376, 870, 378), fill=SOFT_LINE)
draw.text((rx, 383), "作者：陈颖芳  |  2026年5月  |  Mythos之后·第三篇（终篇）", fill=DIM, font=ff(11))

draw.rectangle((426, 14, 428, 386), fill=SOFT_LINE)

img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
