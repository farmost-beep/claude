#!/usr/bin/env python3
"""Generate WeChat cover for: AI方法论从0到1实践指南 | 900×500, bold minimal style."""
from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 900, 500
DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(DIR, "封面_AI方法论从0到1实践指南.png")

# Bold minimal: dark navy + single pop color
BG        = (13, 17, 30)
WHITE     = (255, 255, 255)
WARM      = (235, 225, 210)
GOLD      = (234, 179, 58)
ACCENT    = (56, 182, 192)
MUTED     = (100, 110, 130)
DARK_LINE = (30, 38, 55)

FONT = "/System/Library/Fonts/PingFang.ttc"
if not os.path.exists(FONT):
    FONT = "/System/Library/Fonts/STHeiti Light.ttc"

def ff(size):
    try: return ImageFont.truetype(FONT, size)
    except: return ImageFont.load_default()

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

# ── Large centered "0→1" as the hero graphic ──
cy = 240

# Faint grid lines in background
for gx in range(60, W, 60):
    draw.line((gx, 0, gx, cy + 80), fill=DARK_LINE, width=1)
for gy in range(40, cy + 100, 40):
    draw.line((60, gy, W - 60, gy), fill=DARK_LINE, width=1)

# Big faded "0" on left
draw.text((130, cy - 90), "0", fill=MUTED[:3] + (60,), font=ff(160))

# Big bold "1" on right
draw.text((560, cy - 90), "1", fill=GOLD, font=ff(160))

# Arrow connecting
arrow_x0 = 340
arrow_x1 = 540
draw.line((arrow_x0, cy - 8, arrow_x1, cy - 8), fill=ACCENT, width=3)
# Arrow head
draw.polygon([(arrow_x1 - 12, cy - 18), (arrow_x1 + 6, cy - 8), (arrow_x1 - 12, cy + 2)], fill=ACCENT)

# Progress dots
for px in [370, 410, 450, 490]:
    draw.ellipse((px - 3, cy - 11, px + 3, cy - 5), fill=ACCENT[:3] + (150,))

# "→" label on the arrow
draw.text((420, cy + 8), "方法论转译", fill=MUTED, font=ff(13))

# ── Title overlay on the hero ──
title = "AI方法论从0到1"
tw = draw.textlength(title, font=ff(52))
tx = (W - tw) // 2
draw.text((tx, 40), title, fill=WHITE, font=ff(52))

sub = "实践指南"
tw2 = draw.textlength(sub, font=ff(28))
tx2 = (W - tw2) // 2
draw.text((tx2, 105), sub, fill=WARM, font=ff(28))

# Thin line under subtitle
draw.rectangle((tx2, 140, tx2 + tw2, 142), fill=GOLD)

# ── Three-pillar bottom ──
pillars = [
    ("拆解", "逆向工程\n5位AI领袖的工作流", ACCENT),
    ("重构", "提炼18条\n可迁移的通用原则", GOLD),
    ("落地", "7个自进化飞轮\n覆盖你的6大人生目标", WARM),
]

px0 = (W - 700) // 2
for i, (keyword, desc, clr) in enumerate(pillars):
    px = px0 + i * 240
    py = 320

    # Number badge
    draw.rounded_rectangle((px + 80, py, px + 140, py + 34), radius=17, fill=clr)
    draw.text((px + 98, py + 5), str(i + 1), fill=BG, font=ff(18))

    # Keyword
    kw = draw.textlength(keyword, font=ff(26))
    draw.text((px + (110 - kw // 2) - 30, py + 50), keyword, fill=clr, font=ff(26))

    # Description
    for j, dline in enumerate(desc.split("\n")):
        dlw = draw.textlength(dline, font=ff(13))
        draw.text((px + (110 - dlw // 2) - 30, py + 90 + j * 22), dline, fill=MUTED, font=ff(13))

# ── Bottom tagline ──
tag = "没有秘密的方法论"
twt = draw.textlength(tag, font=ff(17))
draw.text(((W - twt) // 2, H - 45), tag, fill=MUTED[:3] + (100,), font=ff(17))

img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT} ({os.path.getsize(OUT)} bytes)")
