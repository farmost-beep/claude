#!/usr/bin/env python3
"""Cover for AI方法论系列 ⑫: Agent产品评价."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 500
OUT = os.path.dirname(__file__) + "/封面_Agent产品评价.png"

BG = (8, 12, 30)
WHITE = (241, 245, 249)
SUB = (148, 163, 184)
DIM = (71, 85, 105)
ACCENT = (96, 165, 250)
GOLD = (245, 158, 11)
GREEN = (52, 211, 153)
RED = (239, 68, 68)
PURPLE = (168, 85, 247)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

FONT = "/System/Library/Fonts/PingFang.ttc"
if not os.path.exists(FONT):
    FONT = "/System/Library/Fonts/STHeiti Light.ttc"
def ff(s):
    return ImageFont.truetype(FONT, s) if os.path.exists(FONT) else ImageFont.load_default()

# ============================================================
# Left panel: Leaderboard / Scoreboard
# ============================================================
lx = 28

# Panel background (subtle)
draw.rounded_rectangle((lx, 30, 428, 470), radius=12, fill=(14, 20, 40), outline=(30, 41, 59), width=1)

# Top accent bar
draw.rectangle((lx + 6, 34, 422, 36), fill=(30, 50, 80))

# Leaderboard header
draw.text((lx + 16, 48), "管理模式成熟度评分", fill=WHITE, font=ff(19))

# Sub-header
draw.text((lx + 16, 74), "10维度 x 3级评分 + 模式匹配", fill=DIM, font=ff(10))

# Product data: (rank, name, score, color, subtitle)
products = [
    (1, "Claude Code", 31, GOLD,   "自主规划+工具调用"),
    (2, "Cursor",     29, ACCENT,  "深度集成+上下文感知"),
    (3, "Copilot",    27, GREEN,   "生态广度+企业级"),
    (4, "Windsurf",   24, PURPLE,  "流式协作+智能建议"),
    (5, "Aider",      20, (100, 116, 139), "终端原生+Git集成"),
    (6, "Devin",      20, (100, 116, 139), "全自主开发Agent"),
]

row_start_y = 100
row_height = 48
bar_max_width = 130

for idx, (rank, name, score, clr, subtitle) in enumerate(products):
    ry = row_start_y + idx * row_height

    # Row background highlight for top-ranked
    if rank == 1:
        draw.rounded_rectangle((lx + 8, ry - 2, 420, ry + row_height - 3), radius=8,
                               fill=(30, 41, 59, 80))

    # Rank badge
    rank_str = f"#{rank}"
    tw_rank = draw.textlength(rank_str, font=ff(15))
    badge_x = lx + 14

    if rank <= 3:
        badge_clr = [GOLD, ACCENT, GREEN][rank - 1]
        draw.rounded_rectangle((badge_x, ry + 4, badge_x + 34, ry + 32), radius=8, fill=badge_clr)
        text_clr = BG if rank == 1 else WHITE
        draw.text((badge_x + 17 - tw_rank / 2, ry + 9), rank_str, fill=text_clr, font=ff(15))
    else:
        draw.text((badge_x + 2, ry + 10), rank_str, fill=DIM, font=ff(15))

    # Product name + subtitle
    name_x = badge_x + 48
    draw.text((name_x, ry + 4), name, fill=clr, font=ff(16))
    # Subtitle below name (smaller, dimmer)
    draw.text((name_x, ry + 26), subtitle, fill=DIM, font=ff(9))

    # Score bar
    bar_x = lx + 230
    bar_w = int(bar_max_width * score / 31)
    bar_y = ry + 12
    bar_h = 16
    # Bar background
    draw.rounded_rectangle((bar_x, bar_y, bar_x + bar_max_width, bar_y + bar_h),
                           radius=8, fill=(20, 28, 48))
    # Bar fill
    if bar_w > 0:
        draw.rounded_rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h),
                               radius=8, fill=clr)

    # Score number (on the right of bar)
    score_x = bar_x + bar_max_width + 12
    draw.text((score_x, ry + 6), str(score), fill=clr, font=ff(20))
    draw.text((score_x + 26, ry + 12), "/31", fill=DIM, font=ff(10))

# Footnote at bottom of leaderboard
footnote_y = row_start_y + len(products) * row_height + 6
draw.text((lx + 16, footnote_y), "每维度0-3分 × 10维度 + 模式匹配加分", fill=DIM, font=ff(10))
small_text = "满分 = 30(维度) + 1(模式匹配) = 31"
draw.text((lx + 16, footnote_y + 16), small_text, fill=(60, 70, 90), font=ff(9))

# ============================================================
# Right panel: Title + Framework description
# ============================================================
rx = 458

# Top decorative bar
draw.rectangle((rx, 34, rx + 80, 36), fill=ACCENT)

# Series tag badge (top-right)
badge_text = "AI方法论系列 ⑫"
bw = draw.textlength(badge_text, font=ff(12)) + 16
draw.rounded_rectangle((870 - bw, 36, 870, 56), radius=6, fill=ACCENT)
draw.text((870 - bw + 8, 39), badge_text, fill=BG, font=ff(12))

# Title
draw.text((rx, 62), "用AI方法论评价", fill=WHITE, font=ff(36))
draw.text((rx, 112), "主流Agent产品", fill=GOLD, font=ff(42))

# Small subtitle
draw.text((rx, 168), "六款产品的管理模式成熟度评分", fill=ACCENT, font=ff(18))

# Divider
draw.rectangle((rx, 202, 870, 204), fill=(30, 41, 59))

# === 10-dimension framework section ===
draw.text((rx, 218), "10维度管理框架评分", fill=GREEN, font=ff(14))

dimensions = [
    ("1", "目标设定", "Claude Code在目标分解上表现最优"),
    ("2", "任务分解", "Cursor的上下文感知让分解更精准"),
    ("3", "资源调配", "Copilot的生态支持资源最丰富"),
    ("4", "进度追踪", "Windsurf的流式追踪体验最佳"),
    ("5", "质量把控", "Claude Code内置审查机制领先"),
    ("6", "异常处理", "Devin的全自主模式容错性强"),
    ("7", "反馈循环", "Aider的终端反馈循环最紧凑"),
    ("8", "知识沉淀", "Cursor的项目级记忆有优势"),
    ("9", "协作机制", "Copilot的团队协作功能最完善"),
    ("10", "持续改进", "Claude Code的迭代升级最快"),
]

# 10 dimensions in 2 columns of 5
dot_clrs = [GOLD, ACCENT, GREEN, PURPLE, RED, GOLD, ACCENT, GREEN, PURPLE, RED]
col_w = 200
for i, (num, dim_name, dim_desc) in enumerate(dimensions):
    col = i % 2
    row = i // 2
    dx = rx + col * col_w
    dy = 248 + row * 36

    # Number dot
    draw.ellipse((dx, dy + 4, dx + 14, dy + 18), fill=dot_clrs[i])
    draw.text((dx + 5, dy + 2), num, fill=BG, font=ff(9))

    # Dimension name
    draw.text((dx + 20, dy), dim_name, fill=dot_clrs[i], font=ff(12))

    # Brief description (only show if space allows)
    if row < 4:  # skip description on last row to fit
        draw.text((dx + 20, dy + 17), dim_desc, fill=DIM, font=ff(8))
    else:
        draw.text((dx + 20, dy + 17), dim_desc, fill=DIM, font=ff(8))

# Divider before quote
draw.rectangle((rx, 428, 870, 430), fill=(30, 41, 59))

# Quote line
quote = '"不在工具多先进,而在管理模式有多成熟"'
draw.text((rx, 440), quote, fill=SUB, font=ff(13))

# Bottom bar + metadata
draw.rectangle((rx, 466, 870, 468), fill=(30, 41, 59))
draw.text((rx, 475), "作者: 陈颖芳  |  2026年5月", fill=DIM, font=ff(13))

# ============================================================
# Decorative elements
# ============================================================

# Leftmost vertical accent line
draw.rectangle((15, 34, 17, 468), fill=(30, 50, 80))

# Vertical separator between panels (subtle dashed feel using two thin lines)
draw.rectangle((442, 30, 443, 470), fill=(20, 30, 50))

# Save
img.save(OUT, dpi=(150, 150))
print(f"Cover saved: {OUT}")
