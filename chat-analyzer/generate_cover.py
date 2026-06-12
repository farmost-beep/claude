#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os, random

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/线下聊_封面.png"
BG = "#FFF7ED"
ACCENT = "#F97316"
PURPLE = "#8B5CF6"
PINK = "#EC4899"
TEAL = "#14B8A6"
DARK = "#1A2744"
WHITE = "#FFFFFF"

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)
FNT = "/System/Library/Fonts/PingFang.ttc"
font_file = FNT if os.path.exists(FNT) else "/System/Library/Fonts/STHeiti Light.ttc"
def f(s): return ImageFont.truetype(font_file, s)

random.seed(42)
for _ in range(30):
    x, y = random.randint(0, W), random.randint(0, H)
    r = random.randint(5, 25)
    c = random.choice(["#FEF3C7","#FDE68A","#FED7AA","#FECACA","#E0E7FF","#D1FAE5"])
    draw.ellipse([x-r, y-r, x+r, y+r], fill=c)

colors = [PINK, PURPLE, TEAL, ACCENT, "#FBBF24"]
labels = ["约饭吗🍽️", "出来走走🚶", "喝咖啡☕", "运动一下⚽", "聊聊吧💬"]
for i, (col, lab) in enumerate(zip(colors, labels)):
    cx, cy = 80 + i*95, 70 + i*15
    draw.rounded_rectangle([cx, cy, cx+75, cy+28], radius=14, fill=col)
    draw.text((cx+6, cy+4), lab, fill=WHITE, font=f(10))

draw.rounded_rectangle([60, 230, 180, 330], radius=24, fill=PURPLE)
draw.text((75, 255), "💬", font=f(40))
draw.text((90, 305), "群里喊", fill=WHITE, font=f(16))

draw.line([(190, 280), (250, 280)], fill=ACCENT, width=4)
draw.polygon([(250, 275), (265, 280), (250, 285)], fill=ACCENT)

draw.rounded_rectangle([275, 230, 395, 330], radius=24, fill=ACCENT)
draw.text((290, 255), "📅", font=f(40))
draw.text((302, 305), "定时间", fill=WHITE, font=f(16))

draw.line([(400, 280), (460, 280)], fill=ACCENT, width=4)
draw.polygon([(460, 275), (475, 280), (460, 285)], fill=ACCENT)

draw.rounded_rectangle([480, 230, 600, 330], radius=24, fill=TEAL)
draw.text((495, 255), "🤝", font=f(40))
draw.text((510, 305), "线下见", fill=WHITE, font=f(16))

t1 = f(56)
t1w = draw.textlength("线下聊", font=t1)
draw.rounded_rectangle([W - t1w - 55, 100, W - 20, 170], radius=16, fill=DARK)
draw.text((W - t1w - 40, 115), "线下聊", fill=WHITE, font=t1)

draw.text((W - t1w - 50, 190), "💥 别只在群里聊天了", fill=ACCENT, font=f(20))
draw.line([(W - t1w - 50, 225), (W - 30, 225)], fill="#FED7AA", width=2)

features = [("🎯","一键约局",PINK),("📤","发到群聊",PURPLE),("🙋","接龙报名",TEAL),("🏆","见面榜",ACCENT)]
xs = W - t1w - 50
for i, (ic, tx, co) in enumerate(features):
    y = 245 + i*50
    draw.rounded_rectangle([xs, y, xs+180, y+35], radius=18, fill=co)
    draw.text((xs+12, y+4), f"{ic}  {tx}", fill=WHITE, font=f(18))

cta = "📱 转发到群 → 选时间 → 出来见面"
cw = draw.textlength(cta, font=f(14))
draw.rounded_rectangle([W - cw - 50, 436, W - 20, 465], radius=12, fill="#FEF3C7")
draw.text((W - cw - 40, 442), cta, fill=ACCENT, font=f(14))

for x, y, e in [(20,420,"🎉"),(850,40,"✨"),(30,30,"🔥"),(700,460,"💪"),(420,40,"🤗")]:
    draw.text((x, y), e, font=f(24))

img.save(OUT)
print(f"✅ 封面已生成: {OUT}")
