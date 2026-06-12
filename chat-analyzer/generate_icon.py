#!/usr/bin/env python3
"""Generate 144x144 mini-program app icon for 线下聊."""
from PIL import Image, ImageDraw, ImageFont
import os

SIZE = 144
OUT = os.path.dirname(__file__) + "/miniprogram/images/app_icon.png"

img = Image.new("RGB", (SIZE, SIZE), "#F97316")
draw = ImageDraw.Draw(img)

FNT = "/System/Library/Fonts/PingFang.ttc"
font_file = FNT if os.path.exists(FNT) else "/System/Library/Fonts/STHeiti Light.ttc"

# Inner circle background
draw.ellipse([8, 8, 136, 136], fill="#1A2744")

# Handshake emoji in center
fnt = ImageFont.truetype(font_file, 60)
draw.text((42, 30), "🤝", font=fnt)

# Text
fnt2 = ImageFont.truetype(font_file, 26)
tw = draw.textlength("线下聊", font=fnt2)
draw.text(((SIZE - tw) / 2, 100), "线下聊", fill="#FFFFFF", font=fnt2)

img.save(OUT)
print(f"✅ Icon saved: {OUT}")
