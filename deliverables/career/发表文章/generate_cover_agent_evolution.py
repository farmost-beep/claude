#!/usr/bin/env python3
"""Cover: Mythos之后① — Dario Amodei | 900×400 WeChat-safe."""
from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 900, 400
OUT = os.path.dirname(__file__) + "/封面_Agent演化路径.png"

BG        = (250, 248, 243)
INK       = (28, 25, 23)
SUB       = (107, 94, 83)
DIM       = (168, 156, 142)
GOLD      = (201, 169, 110)
ACCENT    = (44, 95, 124)
CARD_BG   = (240, 235, 224)
CARD_BG2  = (255, 255, 255)
SOFT_LINE = (229, 221, 208)
SKIN      = (245, 225, 195)
HAIR_DK   = (45, 35, 25)
BEARD_CLR = (70, 55, 40)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

FONT = "/System/Library/Fonts/PingFang.ttc"
if not os.path.exists(FONT):
    FONT = "/System/Library/Fonts/STHeiti Light.ttc"
def ff(s):
    return ImageFont.truetype(FONT, s) if os.path.exists(FONT) else ImageFont.load_default()

def draw_dario(draw, cx, cy, scale=1.0):
    s = scale
    draw.ellipse((cx-30*s, cy-34*s, cx+30*s, cy+34*s), fill=SKIN, outline=(180,160,130), width=2)
    draw.ellipse((cx-34*s, cy-42*s, cx+34*s, cy-8*s), fill=HAIR_DK)
    draw.ellipse((cx-30*s, cy-34*s, cx+30*s, cy-8*s), fill=SKIN)
    draw.ellipse((cx-38*s, cy-14*s, cx-22*s, cy+22*s), fill=HAIR_DK)
    draw.ellipse((cx+22*s, cy-14*s, cx+38*s, cy+22*s), fill=HAIR_DK)
    for angle in range(-50, 60, 14):
        rx = cx + 28*s * math.cos(math.radians(angle+90))
        ry = cy - 28*s * math.sin(math.radians(angle+90))
        draw.arc((cx-36*s, cy-48*s, cx+36*s, cy+16*s),
                 start=180-angle-12, end=180-angle+22, fill=HAIR_DK, width=7)
    draw.ellipse((cx-18*s, cy+4*s, cx+18*s, cy+38*s), fill=BEARD_CLR)
    draw.ellipse((cx-16*s, cy+14*s, cx+16*s, cy+40*s), fill=BEARD_CLR)
    draw.ellipse((cx-16*s, cy-8*s, cx-4*s, cy+2*s), fill=INK)
    draw.ellipse((cx+4*s, cy-8*s, cx+16*s, cy+2*s), fill=INK)
    draw.ellipse((cx-12*s, cy-5*s, cx-8*s, cy-1*s), fill=BG)
    draw.ellipse((cx+8*s, cy-5*s, cx+12*s, cy-1*s), fill=BG)
    draw.rounded_rectangle((cx-22*s, cy-12*s, cx-2*s, cy+4*s), radius=6, fill=None, outline=(60,50,40), width=2)
    draw.rounded_rectangle((cx+2*s, cy-12*s, cx+22*s, cy+4*s), radius=6, fill=None, outline=(60,50,40), width=2)
    draw.line((cx-2*s, cy-3*s, cx+2*s, cy-3*s), fill=(60,50,40), width=2)
    draw.arc((cx-5*s, cy-1*s, cx+5*s, cy+7*s), start=180, end=270, fill=(160,130,100), width=2)

# ============================================================
# Left panel
# ============================================================
lx = 20

draw.rounded_rectangle((lx, 14, 418, 386), radius=10, fill=CARD_BG2, outline=SOFT_LINE, width=1)
draw.rectangle((lx + 4, 17, 414, 19), fill=GOLD)

# Tighter layout: portrait top-left corner
draw_dario(draw, lx + 62, 68, scale=0.85)

draw.text((lx + 14, 132), "Agent的成人礼：从执行到判断时机", fill=INK, font=ff(16))

# Evolution mini cards — side by side
draw.rounded_rectangle((lx + 12, 160, lx + 188, 240), radius=8, fill=CARD_BG, outline=SOFT_LINE, width=1)
draw.text((lx + 26, 170), "操作型 Agent", fill=SUB, font=ff(15))
draw.text((lx + 26, 194), "保姆  帮AI做得更好", fill=DIM, font=ff(11))
draw.text((lx + 26, 214), "模型不够强，需要帮忙", fill=DIM, font=ff(10))

# Arrow between
draw.polygon([(lx + 200, 195), (lx + 218, 200), (lx + 200, 205)], fill=GOLD)

draw.rounded_rectangle((lx + 226, 160, lx + 402, 240), radius=8, fill=(44, 95, 124, 22), outline=ACCENT, width=2)
draw.text((lx + 240, 170), "治理型 Agent", fill=ACCENT, font=ff(15))
draw.text((lx + 240, 194), "制衡者  兼具操作+判断", fill=INK, font=ff(11))
draw.text((lx + 240, 214), "模型太强，需要制衡", fill=SUB, font=ff(10))

# Key insight — compact strip
draw.rounded_rectangle((lx + 12, 254, lx + 402, 310), radius=8, fill=CARD_BG, outline=SOFT_LINE, width=1)
draw.text((lx + 24, 264), "核心洞察", fill=GOLD, font=ff(11))
draw.text((lx + 24, 282), "操作型Agent没有消失，它长大了——从帮AI做事，到知道何时该管", fill=INK, font=ff(13))

# Bottom row
draw.text((lx + 120, 330), "手（执行）→ 脑（判断）", fill=ACCENT, font=ff(11))
draw.text((lx + 100, 356), "Dario Amodei · Anthropic CEO", fill=DIM, font=ff(9))

# ============================================================
# Right panel: Title
# ============================================================
rx = 440

draw.rectangle((rx, 17, rx + 70, 19), fill=GOLD)
badge_text = "Mythos之后 ①"
bw = int(draw.textlength(badge_text, font=ff(11)) + 14)
draw.rounded_rectangle((870 - bw, 17, 870, 37), radius=5, fill=GOLD)
draw.text((870 - bw + 7, 20), badge_text, fill=BG, font=ff(11))

draw.text((rx, 46), "Mythos发布以后", fill=INK, font=ff(30))
draw.text((rx, 90), "Agent从「操作型」到「治理型」", fill=GOLD, font=ff(26))

draw.text((rx, 134), "该做，还是该管——每一步都要判断", fill=SUB, font=ff(14))

draw.rectangle((rx, 162, 870, 164), fill=SOFT_LINE)

concepts = [
    ("▸ 保姆 → 制衡者（角色转变）", ""),
    ("▸ 执行 → 判断时机（能力升级）", ""),
    ("▸ 操作型没消失，它长大了", "核心洞察"),
]
for i, (concept, note) in enumerate(concepts):
    cy = 176 + i * 30
    draw.text((rx, cy), concept, fill=INK, font=ff(15))
    if note:
        cw = draw.textlength(concept, font=ff(15))
        draw.text((rx + cw + 10, cy + 1), note, fill=DIM, font=ff(11))

# Comparison bar
draw.rounded_rectangle((rx, 272, 870, 296), fill=CARD_BG, radius=6)
draw.text((rx + 12, 278), "操作型：模型不够强，需要帮忙", fill=SUB, font=ff(11))
draw.text((rx + 280, 278), "→", fill=GOLD, font=ff(14))
draw.text((rx + 300, 278), "治理型：模型太强，需要制衡", fill=ACCENT, font=ff(11))

draw.rectangle((rx, 376, 870, 378), fill=SOFT_LINE)
draw.text((rx, 383), "作者：陈颖芳  |  2026年5月  |  Mythos之后·第一篇", fill=DIM, font=ff(11))

draw.rectangle((426, 14, 428, 386), fill=SOFT_LINE)

img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
