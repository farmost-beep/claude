#!/usr/bin/env python3
"""Generate WeChat cover image for Article 5: reverse-engineering Anthropic methodology."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/封面_逆向推导Anthropic方法论.png"

# All colors as tuples to avoid PIL hex issues
BG = (10, 22, 40)
WHITE = (241, 245, 249)
SUB = (148, 163, 184)
DIM = (71, 85, 105)
ACCENT = (96, 165, 250)
S1, S2, S3, S4 = (245, 158, 11), (249, 115, 22), (239, 68, 68), (168, 85, 247)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

FONT = "/System/Library/Fonts/PingFang.ttc"
if not os.path.exists(FONT):
    FONT = "/System/Library/Fonts/STHeiti Light.ttc"

def ff(size):
    try: return ImageFont.truetype(FONT, size)
    except: return ImageFont.load_default()

# ── Left: 4-stage vertical timeline ──
tl_x = 55
tl_y0 = 65
stages = [
    ("Stage 1", "基础代理", "2024末—2025中", "3项原则", S1),
    ("Stage 2", "协作代理", "2025中—2025末", "5项原则", S2),
    ("Stage 3", "自主代理", "2025末—2026初", "5项原则", S3),
    ("Stage 4", "元认知代理", "2026.5—现在", "5项原则", S4),
]

for i, (stag, name, yr, count, clr) in enumerate(stages):
    y = tl_y0 + i * 95
    # Dot
    draw.ellipse((tl_x-5, y+8, tl_x+7, y+20), fill=clr)
    # Line to next
    if i < 3:
        draw.line((tl_x+1, y+24, tl_x+1, y+95), fill=clr, width=2)
    # Labels
    draw.text((tl_x+22, y), stag, fill=clr, font=ff(12))
    draw.text((tl_x+22, y+16), name, fill=WHITE, font=ff(18))
    draw.text((tl_x+22, y+42), yr, fill=DIM, font=ff(11))
    draw.text((tl_x+22, y+60), count, fill=SUB, font=ff(11))

# ── Right: title & keywords ──
rx = 330

# Accent line top
draw.rectangle((rx, 54, rx+100, 56), fill=ACCENT)

draw.text((rx, 80), "从Claude Code进化轨迹", fill=WHITE, font=ff(36))
tw = draw.textlength("我逆向推导出了", font=ff(36))
draw.text((rx, 126), "我逆向推导出了", fill=WHITE, font=ff(36))
draw.text((rx + tw + 6, 120), "Anthropic", fill=ACCENT, font=ff(40))
draw.text((rx, 170), "不公开的AI方法论", fill=WHITE, font=ff(36))

draw.text((rx, 230), "4个阶段 · 18个能力 · 1个飞轮 · 完整推导框架", fill=SUB, font=ff(17))

# Divider
draw.rectangle((rx, 260, 840, 262), fill=(30, 41, 59))

# Keywords row 1 — filled pills
kw1 = ["Dreaming", "Outcomes", "Multiagent", "/goal", "Ultraplan"]
colors1 = [S4, S4, S2, S3, S4]
for idx, (kw, clr) in enumerate(zip(kw1, colors1)):
    kx = rx + idx * 106
    tw_k = draw.textlength(kw, font=ff(14))
    draw.rounded_rectangle((kx, 285, kx+tw_k+20, 313), radius=14, fill=clr)
    draw.text((kx+10, 288), kw, fill=WHITE, font=ff(14))

# Keywords row 2 — outlined pills
kw2 = ["Routines", "PR自修", "交叉审查", "记忆积累", "自进化"]
colors2 = [S1, S2, S3, S4, ACCENT]
for idx, (kw, clr) in enumerate(zip(kw2, colors2)):
    kx = rx + idx * 106
    tw_k = draw.textlength(kw, font=ff(14))
    draw.rounded_rectangle((kx, 325, kx+tw_k+20, 353), radius=14, outline=clr, width=2)
    draw.text((kx+10, 328), kw, fill=clr, font=ff(14))

# Bottom
draw.rectangle((rx, 390, 840, 391), fill=(30, 41, 59))
draw.text((rx, 410), "作者：陈颖芳  |  2026年5月  |  AI方法论系列 ②/②", fill=DIM, font=ff(14))
draw.text((rx, 440), "以Claude Code四个阶段为观测窗口，还原Anthropic内部AI工作哲学", fill=(51, 65, 85), font=ff(13))

img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
