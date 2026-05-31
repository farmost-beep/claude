#!/usr/bin/env python3
"""Generate 5 cover images for AI工作流 ①-⑤ | 900×400 WeChat-safe, warm editorial palette."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 400
DIR = os.path.dirname(os.path.abspath(__file__))

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
RED       = (180, 70, 65)
ORANGE    = (200, 130, 60)

FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
if not os.path.exists(FONT):
    FONT = "/System/Library/Fonts/STHeiti Light.ttc"

def ff(s):
    return ImageFont.truetype(FONT, s) if os.path.exists(FONT) else ImageFont.load_default()

def draw_icon(draw, cx, cy, icon_type, scale=1.0):
    """Draw a simple geometric icon representing each flywheel theme."""
    s = scale
    if icon_type == "invest":
        # Coin/chart - circle with upward arrow
        draw.ellipse((cx-28*s, cy-28*s, cx+28*s, cy+28*s), fill=None, outline=GOLD, width=3)
        draw.polygon([(cx, cy-20*s), (cx-14*s, cy+5*s), (cx-5*s, cy-2*s), (cx-6*s, cy+18*s),
                       (cx+6*s, cy+18*s), (cx+6*s, cy-2*s), (cx+14*s, cy+5*s)], fill=GOLD)
    elif icon_type == "write":
        # Pen - vertical line with angled tip
        draw.rectangle((cx-3*s, cy-25*s, cx+3*s, cy+20*s), fill=ACCENT)
        draw.polygon([(cx-3*s, cy+20*s), (cx+3*s, cy+20*s), (cx, cy+30*s)], fill=ACCENT)
        draw.ellipse((cx-7*s, cy-28*s, cx+7*s, cy-14*s), fill=GOLD)
    elif icon_type == "code":
        # Code brackets </>
        draw.text((cx-30*s, cy-20*s), "<", fill=ACCENT, font=ff(int(36*s)))
        draw.text((cx-8*s, cy-20*s), "/", fill=GOLD, font=ff(int(36*s)))
        draw.text((cx+12*s, cy-20*s), ">", fill=ACCENT, font=ff(int(36*s)))
    elif icon_type == "health":
        # Heart/pulse
        draw.ellipse((cx-28*s, cy-18*s, cx+28*s, cy+20*s), fill=None, outline=RED, width=3)
        draw.text((cx-12*s, cy-8*s), "♥", fill=RED, font=ff(int(32*s)))
    elif icon_type == "career":
        # Building/briefcase
        draw.rectangle((cx-22*s, cy-25*s, cx+22*s, cy+25*s), fill=None, outline=ACCENT, width=3)
        draw.rectangle((cx-22*s, cy-25*s, cx+22*s, cy-10*s), fill=ACCENT)
        draw.text((cx-8*s, cy-16*s), "B", fill=CARD_BG2, font=ff(int(22*s)))
        draw.text((cx-8*s, cy+4*s), "⚙", fill=ACCENT, font=ff(int(16*s)))

def make_cover(num, title_main, title_sub, icon_type, principles, subtitle, out_name):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img, "RGBA")

    # Left panel
    lx = 20
    draw.rounded_rectangle((lx, 14, 418, 386), radius=10, fill=CARD_BG2, outline=SOFT_LINE, width=1)
    draw.rectangle((lx + 4, 17, 414, 19), fill=GOLD)

    # Series badge
    badge = f"AI工作流 ①-⑤"
    draw.rounded_rectangle((lx + 12, 36, lx + 180, 62), radius=5, fill=GOLD)
    draw.text((lx + 24, 40), f"AI工作流 {num}", fill=BG, font=ff(14))

    # Icon
    draw_icon(draw, lx + 208, 100, icon_type, scale=1.3)

    # Principles list
    for i, (name, desc) in enumerate(principles):
        py = 160 + i * 44
        colors = [GOLD, GREEN, ACCENT, PURPLE]
        clr = colors[i % 4]
        draw.rounded_rectangle((lx + 12, py, lx + 402, py + 36), radius=7, fill=CARD_BG, outline=clr, width=1)
        draw.ellipse((lx + 20, py + 4, lx + 44, py + 28), fill=clr)
        draw.text((lx + 26, py + 7), str(i+1), fill=CARD_BG2, font=ff(13))
        draw.text((lx + 54, py + 3), name, fill=clr, font=ff(15))
        draw.text((lx + 54, py + 21), desc, fill=SUB, font=ff(10))

    # Subtitle at bottom
    draw.rounded_rectangle((lx + 12, 350, lx + 402, 374), radius=6, fill=(44, 95, 124, 10))
    draw.text((lx + 28, 357), subtitle, fill=INK, font=ff(10))

    # Right panel
    rx = 440
    draw.rectangle((rx, 17, rx + 70, 19), fill=GOLD)

    # Badge
    badge_t = f"AI工作流 {num}"
    bw = int(draw.textlength(badge_t, font=ff(11)) + 14)
    draw.rounded_rectangle((870 - bw, 17, 870, 37), radius=5, fill=GOLD)
    draw.text((870 - bw + 7, 20), badge_t, fill=BG, font=ff(11))

    draw.text((rx, 46), title_main, fill=INK, font=ff(26))
    draw.text((rx, 84), title_sub, fill=GOLD, font=ff(22))

    draw.rectangle((rx, 120, 870, 122), fill=SOFT_LINE)

    # Center quote area
    draw.rounded_rectangle((rx, 140, 870, 370), radius=10, fill=CARD_BG, outline=SOFT_LINE, width=1)

    # Show key methodology
    if num == "①":
        draw.text((rx + 16, 158), "真实配置 · 真实案例 · 真实翻车记录", fill=INK, font=ff(16))
        draw.text((rx + 16, 192), "AI负责信息收集和初步分析", fill=SUB, font=ff(13))
        draw.text((rx + 16, 220), "AI+AI负责交叉验证", fill=SUB, font=ff(13))
        draw.text((rx + 16, 248), "人只做最终决策", fill=ACCENT, font=ff(16))
        draw.text((rx + 16, 290), "没有一个决策是由单一AI输出直接触发的", fill=DIM, font=ff(12))
        draw.text((rx + 16, 320), "投资飞轮 · 每日5分钟+每周15分钟", fill=GOLD, font=ff(12))
    elif num == "②":
        draw.text((rx + 16, 158), "AI起草 · 另一个AI验证 · 我来注入经验", fill=INK, font=ff(16))
        draw.text((rx + 16, 192), "90%的字是AI码的", fill=SUB, font=ff(13))
        draw.text((rx + 16, 220), "100%的判断是我的", fill=ACCENT, font=ff(16))
        draw.text((rx + 16, 260), "数据溯源 · 语气溯源 · 观点溯源", fill=INK, font=ff(13))
        draw.text((rx + 16, 300), "任何统计数据，两个AI独立查找原始来源", fill=DIM, font=ff(11))
        draw.text((rx + 16, 330), "写作飞轮 · 30分钟/篇", fill=GOLD, font=ff(12))
    elif num == "③":
        draw.text((rx + 16, 158), "不是程序员也能指挥AI写代码", fill=INK, font=ff(16))
        draw.text((rx + 16, 192), "高信任：不看代码，看结果", fill=GREEN, font=ff(13))
        draw.text((rx + 16, 218), "低信任：逐行看diff+测试环境先跑", fill=ACCENT, font=ff(13))
        draw.text((rx + 16, 244), "不信任：删除/发邮件/改数据库→只给方案", fill=RED, font=ff(13))
        draw.text((rx + 16, 280), "信任不是放弃验证——是知道该验证什么", fill=DIM, font=ff(12))
        draw.text((rx + 16, 320), "编程飞轮 · 4级信任体系", fill=GOLD, font=ff(12))
    elif num == "④":
        draw.text((rx + 16, 158), "不是AI教我养生——是AI盯着我", fill=INK, font=ff(16))
        draw.text((rx + 16, 192), "记录 · 趋势 · 异常提醒", fill=GREEN, font=ff(14))
        draw.text((rx + 16, 224), "每天30秒打卡：步数+饮水+血压", fill=SUB, font=ff(13))
        draw.text((rx + 16, 256), "每周看一次趋势：这周比上周好？还是在退步？", fill=ACCENT, font=ff(13))
        draw.text((rx + 16, 296), "一个提醒脚本+一个打卡文件，比记忆可靠100倍", fill=DIM, font=ff(12))
        draw.text((rx + 16, 330), "健康飞轮 · 49岁，BMI 25.9", fill=GOLD, font=ff(12))
    elif num == "⑤":
        draw.text((rx + 16, 158), "AI负责信息 · 我负责判断", fill=INK, font=ff(16))
        draw.text((rx + 16, 192), "客户方案：AI起草框架→我审核心判断→AI调整→我终审", fill=SUB, font=ff(12))
        draw.text((rx + 16, 224), "20年银行经验翻译成结构化的专业输出", fill=ACCENT, font=ff(14))
        draw.text((rx + 16, 262), "从零到终稿，约40分钟", fill=INK, font=ff(13))
        draw.text((rx + 16, 296), "AI做不出的判断：需要真实接触过客户才知道", fill=DIM, font=ff(12))
        draw.text((rx + 16, 330), "事业飞轮 · 中级经济师/民建提案/产业研究", fill=GOLD, font=ff(12))

    draw.rectangle((426, 14, 428, 386), fill=SOFT_LINE)

    out_path = os.path.join(DIR, out_name)
    img.save(out_path, dpi=(150, 150))
    print(f"✅ {out_name}")


covers = [
    ("①", "我用AI管钱", "投资飞轮完整配置", "invest",
     [("双实例验证", "两个AI独立→结论一致才通过"),
      ("分级告警", "L1自动扫描→L2触发→L3反向→L4对比"),
      ("停机制", "两个AI不一致→不操作"),
      ("风险预算", "高风险配高验证，低风险不配验证")],
     "AI负责信息收集 · AI+AI交叉验证 · 人做最终决策",
     "封面_AI工作流01_投资飞轮.png"),

    ("②", "我的公众号90%是AI写的", "写作飞轮完整配置", "write",
     [("三层验证", "数据溯源·语气溯源·观点溯源"),
      ("AI二号独立", "所有统计数据→两个AI独立查→任一找不到→删"),
      ("论断分级", "A(常识)免检·B(数据)双验证·C(观点)人确认"),
      ("停机制", "任何一句话找不到原始出处→不发")],
     "发出去的每一个数据，我都知道它的来源",
     "封面_AI工作流02_写作飞轮.png"),

    ("③", "AI改代码，什么时候信任", "编程飞轮完整配置", "code",
     [("高信任", "新增独立功能→不审代码，看结果"),
      ("中信任", "修bug小改动→瞄一眼diff"),
      ("低信任", "核心逻辑/数据管道→逐行审+测试环境"),
      ("不信任", "删除/发邮件/改数据库→只给方案不执行")],
     "信任不是放弃验证——是知道该验证什么",
     "封面_AI工作流03_编程飞轮.png"),

    ("④", "49岁，让AI盯着我", "健康飞轮完整配置", "health",
     [("设基线", "体重/血压/步数/睡眠→测一次记下来"),
      ("每天30秒", "只记3个数字：步数·饮水·血压"),
      ("每周趋势", "这周比上周好？还是这周在退步？"),
      ("异常告警", "数值超出范围→触发提醒→人工确认")],
     "让AI盯你，不让AI教你。盯的三要素：记录·趋势·提醒",
     "封面_AI工作流04_健康飞轮.png"),

    ("⑤", "AI怎么放大专业输出", "事业飞轮完整配置", "career",
     [("客户方案", "AI草拟框架→人审核心判断→AI调整→人终审"),
      ("民建提案", "AI整理政策背景→人审可行性和措辞"),
      ("中级经济师", "AI出题批改→人做题看解析"),
      ("产业研究", "AI收集数据→人注入一线观察")],
     "专业输出中，区分'信息'和'判断'。AI负责信息，你负责判断",
     "封面_AI工作流05_事业飞轮.png"),
]

for args in covers:
    make_cover(*args)

print(f"\nDone: {len(covers)} covers generated")
