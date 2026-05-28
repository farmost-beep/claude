#!/usr/bin/env python3
"""Cover for AI methodology series ⑪: Claude Code product future evolution."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/封面_Claude产品未来.png"

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
def ff(s):
    return ImageFont.truetype(FONT, s) if os.path.exists(FONT) else ImageFont.load_default()


# ============================================================
# Left panel: Three-stage evolution timeline (问答→管理→目标)
# ============================================================
lx = 50   # left-panel x origin
ly_start = 80

# Section header
draw.text((lx, 40), "Claude Code 演进路线", fill=ACCENT, font=ff(15))

# Three evolution stages – stacked vertically with connecting arrows
stages = [
    ("目标模式", "人定目标 · AI自主执行", GOLD),
    ("管理模式", "人管流程 · AI并行执行", ACCENT),
    ("问答模式", "人提问 · AI回答", GREEN),
]

# Draw a subtle timeline line on the left
draw.line(((lx - 18, ly_start + 28), (lx - 18, ly_start + 270)), fill=(30, 50, 80), width=2)

for idx, (name, desc, clr) in enumerate(stages):
    sy = ly_start + idx * 120
    # Timeline dot
    r = 7
    draw.ellipse((lx - 18 - r, sy + 20 - r, lx - 18 + r, sy + 20 + r), fill=clr)
    # Stage name in rounded rectangle
    tw_name = draw.textlength(name, font=ff(22))
    draw.rounded_rectangle((lx, sy, lx + tw_name + 30, sy + 45), radius=14, fill=clr)
    draw.text((lx + 15, sy + 8), name, fill=WHITE if clr != GOLD else BG, font=ff(22))
    # Description below
    draw.text((lx + 15, sy + 52), desc, fill=SUB, font=ff(12))
    # Arrow between stages
    if idx < 2:
        arrow_y = sy + 85
        draw.text((lx + int(tw_name / 2) + 5, arrow_y), "↓", fill=DIM, font=ff(16))

# Arrow from 管理模式 pointing right
arrow_start_y = ly_start + 120 + 22
draw.text((lx + 200, arrow_start_y - 12), "当前实现 ▸", fill=GREEN, font=ff(11))

# Description of current state
notes_y = ly_start + 280
draw.text((lx, notes_y), "管理模式已实现：", fill=ACCENT, font=ff(13))
draw.text((lx, notes_y + 22), "文件系统感知 · 规则自检 · 并行Agent · 记忆基础设施", fill=SUB, font=ff(11))
draw.text((lx, notes_y + 44), "下一步：向目标模式演进", fill=GOLD, font=ff(12))


# ============================================================
# Separator bar between left and right panels
# ============================================================
sep_x = 435
draw.line(((sep_x, 40), (sep_x, 470)), fill=(30, 41, 59), width=1)


# ============================================================
# Right panel: Title + 7 Evolution Directions
# ============================================================
rx = 460

# Title area
draw.rectangle((rx, 34, rx + 80, 36), fill=GOLD)
draw.text((rx, 58), "从AI方法论推演", fill=WHITE, font=ff(36))
draw.text((rx, 105), "Claude Code的产品未来", fill=GOLD, font=ff(38))
draw.text((rx, 158), "管理模式视角下的七个演进方向", fill=ACCENT, font=ff(22))

# Separator
draw.rectangle((rx, 195, 870, 197), fill=(30, 41, 59))

# 7 evolution directions – two columns: 4 left + 3 right
directions = [
    ("① 无限上下文",  "从128K会话突破到项目级长记忆", ACCENT),
    ("② 持续协作",    "从单次问答到跨会话持续项目管理", GREEN),
    ("③ 多模态交互",  "从纯文本到代码+图表+UI一体化", PURPLE),
    ("④ 主动建议",    "从被动响应到主动提醒+风险预警", GOLD),
    ("⑤ 自主操作",    "从工具调用到沙箱内自主完成多步任务", ACCENT),
    ("⑥ 领域专业化",  "从通用编程到金融/法律垂直深度", GREEN),
    ("⑦ 多Agent协作", "从单一Agent到Agent团队分工评审", PURPLE),
]

col1_x = rx
col2_x = rx + 215
col_width = 195

for idx, (name, desc, clr) in enumerate(directions):
    if idx < 4:
        dx = col1_x
        dy = 215 + idx * 63
    else:
        dx = col2_x
        dy = 215 + (idx - 4) * 63

    # Direction number pill
    tw_name = draw.textlength(name, font=ff(12))
    draw.rounded_rectangle((dx, dy, dx + tw_name + 16, dy + 28), radius=8, fill=clr)
    draw.text((dx + 8, dy + 4), name, fill=WHITE if clr not in (GOLD,) else BG, font=ff(12))
    # Description
    draw.text((dx, dy + 32), desc, fill=SUB, font=ff(11))

# Bottom
draw.rectangle((rx, 465, 870, 466), fill=(30, 41, 59))
draw.text((rx, 476), "作者：陈颖芳  |  2026年5月  |  AI方法论系列 ⑪", fill=DIM, font=ff(14))

# Vertical accent line on the far left
draw.rectangle((15, 34, 17, 470), fill=(30, 50, 80))

# ============================================================
# Save
# ============================================================
img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
