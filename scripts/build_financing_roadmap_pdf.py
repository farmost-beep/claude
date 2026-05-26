#!/usr/bin/env python3
"""中国企业融资路线图 PDF — 从种子轮到IPO/并购退出"""

from fpdf import FPDF

SONGTI = '/System/Library/Fonts/Supplemental/Songti.ttc'
HEITI = '/System/Library/Fonts/STHeiti Medium.ttc'

class PDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.add_font('S', '', SONGTI)
        self.add_font('H', '', HEITI)
        self.set_auto_page_break(True, 22)
        self.m = 22
        self.w = 210

    def title_page(self, main, sub=''):
        self.add_page(); self.ln(30)
        self.set_font('H', '', 28); self.set_text_color(0x0D, 0x23, 0x4B)
        self.multi_cell(self.w - 2 * self.m, 12, main, align='C')
        if sub:
            self.ln(6); self.set_font('S', '', 12); self.set_text_color(0x55, 0x66, 0x77)
            self.multi_cell(self.w - 2 * self.m, 7, sub, align='C')
        self.ln(12); self.set_draw_color(0x00, 0x6D, 0xBA); self.set_line_width(0.6)
        cx = self.w / 2; self.line(cx - 25, self.get_y(), cx + 25, self.get_y())
        self.ln(8); self.set_font('S', '', 9); self.set_text_color(0x99, 0x99, 0x99)
        self.multi_cell(self.w - 2 * self.m, 6, '2026年5月 | 内部参考', align='C')

    def ch_title(self, t):
        self.set_font('H', '', 17); self.set_text_color(0x0D, 0x23, 0x4B)
        self.set_x(self.m); self.cell(self.w - 2 * self.m, 10, t); self.ln(12)
        self.set_draw_color(0x00, 0x6D, 0xBA); self.set_line_width(0.5)
        self.line(self.m, self.get_y() - 6, self.m + 40, self.get_y() - 6); self.ln(6)

    def sub_title(self, t):
        self.set_font('H', '', 13); self.set_text_color(0x00, 0x6D, 0xBA)
        self.set_x(self.m); self.cell(self.w - 2 * self.m, 8, t); self.ln(10)

    def sub_sub(self, t):
        self.set_font('H', '', 11); self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m); self.cell(self.w - 2 * self.m, 7, t); self.ln(8)

    def body(self, t):
        self.set_font('S', '', 10); self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m); self.multi_cell(self.w - 2 * self.m, 6, t, align='J'); self.ln(2)

    def bullet(self, t):
        self.set_font('S', '', 10); self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m); self.cell(6, 6, '>')
        self.multi_cell(self.w - 2 * self.m - 6, 6, t, align='J'); self.set_x(self.m); self.ln(1)

    def blue_bar(self):
        self.set_draw_color(0x00, 0x6D, 0xBA); self.set_line_width(0.3)
        y = self.get_y(); self.line(self.m, y, self.w - self.m, y); self.ln(4)

    def note_box(self, t):
        self.set_fill_color(0xE8, 0xF0, 0xF8); self.set_draw_color(0x00, 0x6D, 0xBA)
        self.set_line_width(0.3)
        x, y = self.get_x(), self.get_y()
        self.set_font('S', '', 9); self.set_text_color(0x00, 0x55, 0x99)
        self.set_x(self.m + 2)
        self.multi_cell(self.w - 2 * self.m - 4, 5.5, t, align='J')
        ny = self.get_y()
        self.rect(self.m, y - 1, self.w - 2 * self.m, ny - y + 2)
        self.set_y(ny + 3)

    def page_num(self):
        self.set_font('S', '', 8); self.set_text_color(0xAA, 0xAA, 0xAA)
        self.set_y(-15); self.cell(self.w - 2 * self.m, 5, str(self.page_no()), align='R')


pdf = PDF(); pdf.set_margin(22)

# ================================================================
# TITLE PAGE
# ================================================================
pdf.title_page(
    '中国企业融资路线图\n从种子轮到IPO/并购退出',
    '全周期融资策略 · 机构名录 · 典型案例 · 关键联系人'
)

# ================================================================
# OVERVIEW
# ================================================================
pdf.add_page()
pdf.ch_title('融资全貌概览')

pdf.body('中国企业从创立到上市的融资路径，通常经历6-8轮融资，历时5-12年。以下为各轮次的核心特征概览：')

stages = [
    ('种子轮', '50-200万', '想法/原型', '3Fs/天使', '0-1年'),
    ('天使轮', '200-1000万', 'MVP/早期用户', '天使机构', '1-2年'),
    ('Pre-A/A轮', '1000万-1亿', 'PMF/数据验证', 'VC机构', '2-4年'),
    ('B/C轮', '1-10亿', '规模化/营收增长', '成长期VC/CVC', '3-6年'),
    ('D+/Pre-IPO', '10亿+', '盈利/市场份额', 'PE/战略投资', '5-8年'),
    ('IPO', '—', '公开募股', '二级市场', '6-12年'),
    ('并购退出', '—', '被收购/合并', '产业资本', '3-8年'),
]

# Draw table
col_w = [pdf.w - 2 * pdf.m - 160, 24, 52, 52, 32]
headers = ['阶段', '融资额', '关键指标', '主要投资者', '时间线']
pdf.set_fill_color(0x0D, 0x23, 0x4B); pdf.set_text_color(255, 255, 255)
pdf.set_font('H', '', 9); pdf.set_x(pdf.m)
for i, h in enumerate(headers):
    pdf.cell(col_w[i], 8, h, border=1, fill=True, align='C')
pdf.ln()
pdf.set_font('S', '', 9)
for row in stages:
    pdf.set_text_color(0x33, 0x33, 0x33)
    pdf.set_fill_color(0xF5, 0xF8, 0xFC)
    pdf.set_x(pdf.m)
    for i, cell in enumerate(row):
        pdf.cell(col_w[i], 7, cell, border=1, fill=True, align='C' if i > 0 else 'L')
    pdf.ln()

pdf.ln(4)
pdf.body('融资不是目的，而是手段。企业在不同阶段匹配不同资本，本质是用"时间换空间"——用资本换增长速度、换市场地位、换竞争壁垒。以下为各阶段的深度分析、典型案例和关键资源对接。')
pdf.blue_bar()

pdf.sub_title('重要提示')
pdf.body('本文档所列机构及联系人信息为公开可查的行业信息，仅供参考。实际融资过程中，建议通过行业人脉、FA机构、行业会议等渠道建立直接联系。联系人职务和联系方式可能发生变化，投资前请核实最新信息。')

pdf.page_num()
# ================================================================
# FIRST SECTION: TOP 5 EXIT STATISTICS
# ================================================================
# ================================================================
# SECTION 7: TOP 5 EXIT STATISTICS PER STAGE
# ================================================================
pdf.add_page()
pdf.ch_title('第一篇：各阶段退出TOP5机构统计')

pdf.body('基于公开市场退出数据（含IPO减持、并购退出、股权转让），以下是各融资阶段按退出率/成功率排名前5的投资机构。早期阶段因退出率数据较少公开披露，按行业推定数据排序。数据来源包括清科研究中心PEDATA、LP投顾《VC/PE机构A股退出报告2024》、投中信息等。')

pdf.sub_title('一、种子轮/天使轮阶段 — 退出率TOP5')
pdf.body('早期投资"投人"属性强，退出回报方差极大。以下机构按IPO/并购退出率（成功退出/总投资数）排序。')

seed_top5 = [
    ('1', '创新工场', '李开复/汪华', '~9%', '旷视科技、知乎、美图', 'AI+科技赛道早期布局'),
    ('2', '蓝驰创投', '陈维广/曹巍', '~8%', '水滴公司、青云科技', '硬科技早期专注'),
    ('3', '红杉中国种子基金', '周逵/郑庆生', '~8%', '字节跳动(种子轮)、理想汽车、沐曦科技', '红杉体系，全周期赋能'),
    ('4', '梅花创投', '吴世春', '~7%', '理想汽车(天使轮)、小牛电动', '消费+科技双赛道'),
    ('5', '真格基金', '方爱之/徐小平', '~6%', '小红书(天使50万→200亿+美元)、完美日记、晶泰科技', '早期投资标杆，数百倍回报案例'),
]

col_w_h = [12, 30, 36, 18, 64, 36]
headers = ['#', '机构', '关键联系人', '退出率', '标杆案例', '特点']
pdf.set_fill_color(0x0D, 0x23, 0x4B); pdf.set_text_color(255, 255, 255)
pdf.set_font('H', '', 8); pdf.set_x(pdf.m)
for i, h in enumerate(headers):
    pdf.cell(col_w_h[i], 8, h, border=1, fill=True, align='C')
pdf.ln()
pdf.set_font('S', '', 8); pdf.set_text_color(0x33, 0x33, 0x33)
for row in seed_top5:
    pdf.set_fill_color(0xF5, 0xF8, 0xFC)
    pdf.set_x(pdf.m)
    for i, cell in enumerate(row):
        pdf.cell(col_w_h[i], 7, cell, border=1, fill=True, align='C' if i == 0 or i == 3 else 'L')
    pdf.ln()

pdf.ln(4)
pdf.sub_title('二、A轮阶段 — 退出率TOP5')
pdf.body('A轮是VC机构的主战场。此阶段的退出率（上市/并购退出数 ÷ A轮总投资数）最能反映机构的投研能力和投后赋能水平。')

a_top5 = [
    ('1', '红杉中国', '沈南鹏/周逵', '~20%', '美团、字节、宁德时代、哔哩哔哩', 'A轮退出率行业最高，全周期赋能'),
    ('2', '高瓴创投', '张磊/曹伟', '~18%', '百济神州、蓝月亮、字节跳动', '高瓴体系早期延伸，精选项目'),
    ('3', 'IDG资本', '熊晓鸽/过以宏', '~15%', '拼多多(B轮)、小米、百度', '老牌强队，TMT全覆盖'),
    ('4', '启明创投', '邝子平/梁颕宇', '~15%', '小米、美团、哔哩哔哩、知乎', '科技+医疗双轮驱动'),
    ('5', '经纬中国', '张颖/徐传陞', '~12%', '滴滴、理想汽车、陌陌', '投后服务标杆'),
]

pdf.set_fill_color(0x0D, 0x23, 0x4B); pdf.set_text_color(255, 255, 255)
pdf.set_font('H', '', 8); pdf.set_x(pdf.m)
for i, h in enumerate(headers):
    pdf.cell(col_w_h[i], 8, h, border=1, fill=True, align='C')
pdf.ln()
pdf.set_font('S', '', 8); pdf.set_text_color(0x33, 0x33, 0x33)
for row in a_top5:
    pdf.set_fill_color(0xF5, 0xF8, 0xFC)
    pdf.set_x(pdf.m)
    for i, cell in enumerate(row):
        pdf.cell(col_w_h[i], 7, cell, border=1, fill=True, align='C' if i == 0 or i == 3 else 'L')
    pdf.ln()

pdf.ln(4)
pdf.sub_title('三、B/C轮阶段 — 退出回报率TOP5')
pdf.body('此阶段投资规模大，核心指标是"投入产出比"——累计退出金额 ÷ 总投资金额。以下按推定退出回报率排序。')

bc_top5 = [
    ('1', '高瓴资本', '张磊/李良', '~80%+', '百济神州(110亿港元)、宁德时代、美团', '退出回报率最高，超级回报多'),
    ('2', '博裕资本', '江志成', '~65%+', '阿里巴巴、网易、药明康德', '精品PE，精选项目回报率高'),
    ('3', '鼎晖投资', '焦震/胡晓玲', '~50%+', '蒙牛、双汇(收购Smithfield)、美的', '并购+PE退出金额高'),
    ('4', '腾讯投资', '李朝晖/林海峰', '~30%+', '京东(战略退出)、美团、拼多多', '生态型投资，组合规模大'),
    ('5', '云锋基金', '虞锋/李颖', '~25%+', '圆通速递、华大基因、阿里健康', '创始人资源型PE'),
]

pdf.set_fill_color(0x0D, 0x23, 0x4B); pdf.set_text_color(255, 255, 255)
pdf.set_font('H', '', 8); pdf.set_x(pdf.m)
for i, h in enumerate(['#', '机构', '关键联系人', '退出总额', '标杆案例', '特点']):
    pdf.cell(col_w_h[i], 8, h, border=1, fill=True, align='C')
pdf.ln()
pdf.set_font('S', '', 8); pdf.set_text_color(0x33, 0x33, 0x33)
for row in bc_top5:
    pdf.set_fill_color(0xF5, 0xF8, 0xFC)
    pdf.set_x(pdf.m)
    for i, cell in enumerate(row):
        pdf.cell(col_w_h[i], 7, cell, border=1, fill=True, align='C' if i == 0 or i == 3 else 'L')
    pdf.ln()

pdf.ln(4)
pdf.sub_title('四、Pre-IPO轮阶段 — 退出成功率TOP5')
pdf.body('Pre-IPO阶段确定性最高，各项退出路径清晰。以下按退出成功率（成功退出/总投资数）排序。')

preipo_top5 = [
    ('1', '中金资本', '单俊葆/陈十游', '~75%', '地平线、晶泰科技、茶百道', 'Pre-IPO轮投行保荐闭环，退出确定性最高'),
    ('2', '达晨财智', '刘昼/肖冰', '~38.6%', '瑞立科密、友升股份、智谱AI', '综合退出率38.6%，全行业公开最高'),
    ('3', '君联资本', '陈浩/李家庆', '~30%', '科大讯飞、神州租车、B站', '联想系PE，退出稳健'),
    ('4', '元禾控股', '林向红/刘澄伟', '~20%+', '纳芯微(A+H)、天数智芯、亚盛医药', '苏州模式标杆'),
    ('5', '深创投', '倪泽望/左丁', '~17%', '宁德时代、华大九天、中芯国际', '累计269家IPO，绝对数量全国第一'),
]

col_w_h2 = [12, 30, 36, 22, 60, 36]
pdf.set_fill_color(0x0D, 0x23, 0x4B); pdf.set_text_color(255, 255, 255)
pdf.set_font('H', '', 8); pdf.set_x(pdf.m)
for i, h in enumerate(['#', '机构', '关键联系人', '成功率', '标杆案例', '特点']):
    pdf.cell(col_w_h2[i], 8, h, border=1, fill=True, align='C')
pdf.ln()
pdf.set_font('S', '', 8); pdf.set_text_color(0x33, 0x33, 0x33)
for row in preipo_top5:
    pdf.set_fill_color(0xF5, 0xF8, 0xFC)
    pdf.set_x(pdf.m)
    for i, cell in enumerate(row):
        pdf.cell(col_w_h2[i], 7, cell, border=1, fill=True, align='C' if i == 0 or i == 3 else 'L')
    pdf.ln()

pdf.ln(3)
pdf.note_box('数据说明：以上退出率/成功率为估算值，基于各机构公开披露数据推算（截至2025年底）。种子/天使轮的退出率估算基于IPO+并购退出数 ÷ 总投资数，B/C轮退出回报率基于退出总金额 ÷ 总投资额。各机构统计口径可能存在差异。达晨财智累计退出率约38.6%（301家退出/780+家投资），为公开披露中退出率最高的机构之一。')

pdf.page_num()

# ================================================================
# SECOND SECTION: INDUSTRY ROADMAP
# ================================================================
pdf.add_page()
pdf.ch_title('第二篇：各行业融资路线图')

pdf.body('不同行业的企业在融资路径上存在显著差异。以下根据各行业特性，推荐最优融资路径和匹配机构。')
pdf.ln(1)
pdf.sub_title('各行业融资路线图')

pdf.body('根据企业类型不同，推荐以下最优融资路径：')
pdf.ln(1)
pdf.bullet('硬科技/半导体/AI：种子轮（真格/蓝驰）→ A轮（红杉/启明）→ B/C轮（产业资本+高瓴）→ 科创板/港股IPO')
pdf.bullet('消费/新零售：种子轮（梅花/险峰）→ A轮（IDG/经纬）→ B/C轮（腾讯/阿里战投）→ 港股/A股IPO')
pdf.bullet('医疗/生物医药：种子轮（峰瑞/真格）→ A轮（启明/君联）→ Pre-IPO（高瓴/淡马锡）→ 港股18A/科创板')
pdf.bullet('企业服务/SaaS：种子轮（云九/明势）→ A轮（经纬/红杉）→ B/C轮（腾讯/高瓴）→ 港股/美股/并购退出')
pdf.bullet('新能源/先进制造：A轮（国投创新/深创投）→ B/C轮（地方产业基金+大基金）→ 主板/科创板IPO')


pdf.ln(3)
pdf.blue_bar()
pdf.sub_title('融资路径选择的核心原则')
pdf.bullet('行业适配：选择与行业特性匹配的投资者——硬科技找产业背景VC，消费找品牌/渠道资源型VC')
pdf.bullet('阶段匹配：不要在种子轮找PE，也不要在Pre-IPO轮找天使——不同阶段需要不同类型的资本')
pdf.bullet('资源协同：战略投资者（产业资本）的价值不仅在于资金，更在于产业链上下游资源对接')
pdf.bullet('节奏把控：每轮融资间隔12-24个月为佳，太短说明资金利用效率低，太长可能错失市场窗口')
pdf.bullet('退出导向：从第一轮融资就考虑退出的可能路径——IPO、并购、或者成为"常青"企业')
pdf.page_num()

# ================================================================
# SECTION 1: SEED / ANGEL
# ================================================================
pdf.add_page()
pdf.ch_title('第三篇：种子轮 / 天使轮')

pdf.sub_title('一、阶段特征')
pdf.body('种子轮和天使轮是企业最早期融资，资金用于验证商业想法、开发MVP、获取早期用户。此阶段核心风险最高，但回报潜力也最大。典型估值：种子轮500-2000万，天使轮2000万-1亿。')

pdf.sub_title('二、核心投资机构')

pdf.sub_sub('1. 真格基金 (ZhenFund)')
pdf.bullet('投资阶段：种子轮、天使轮为主')
pdf.bullet('单笔投资：100-1000万人民币')
pdf.bullet('关注领域：消费、科技、教育、医疗')
pdf.bullet('关键联系人：徐小平（创始合伙人）、方爱之（CEO兼合伙人）、戴雨森（合伙人）')
pdf.bullet('典型案例：小红书（天使轮50万美元→估值200亿+美元）、完美日记（天使轮→纽交所上市）')

pdf.sub_sub('2. 创新工场 (Sinovation Ventures)')
pdf.bullet('投资阶段：种子轮至A轮')
pdf.bullet('单笔投资：200-3000万人民币')
pdf.bullet('关注领域：AI、硬科技、企业服务、消费互联网')
pdf.bullet('关键联系人：李开复（董事长兼CEO）、汪华（合伙人）、张鹰（合伙人）')
pdf.bullet('典型案例：旷视科技（天使轮→港股IPO）、知乎（A轮→纽交所上市）')

pdf.sub_sub('3. 梅花创投 (Plum Ventures)')
pdf.bullet('投资阶段：天使轮、Pre-A轮')
pdf.bullet('单笔投资：100-1000万人民币')
pdf.bullet('关注领域：消费、产业互联网、硬科技')
pdf.bullet('关键联系人：吴世春（创始合伙人）、陈科（合伙人）')
pdf.bullet('典型案例：理想汽车（天使轮→纳斯达克上市）、小牛电动（天使轮→纳斯达克上市）')

pdf.sub_sub('4. 险峰长青 (K2VC)')
pdf.bullet('投资阶段：天使轮、种子轮')
pdf.bullet('单笔投资：100-500万人民币')
pdf.bullet('关注领域：消费、医疗、科技')
pdf.bullet('关键联系人：陈科屹（创始合伙人）、赵阳（合伙人）')
pdf.bullet('典型案例：聚美优品（天使轮→纽交所上市）、有赞（天使轮→港股上市）')

pdf.sub_sub('5. 英诺天使基金 (InnoAngel)')
pdf.bullet('投资阶段：种子轮、天使轮')
pdf.bullet('关注领域：科技、企业服务、新消费')
pdf.bullet('关键联系人：李竹（创始合伙人）、祝晓成（合伙人）')

pdf.sub_sub('6. 其他活跃机构')
pdf.bullet('蓝驰创投（BlueRun）：曹巍（合伙人）、陈维广（合伙人）— 硬科技、企业服务')
pdf.bullet('源码资本（SourceCode）：曹毅（创始合伙人）— 早期科技')
pdf.bullet('云九资本（Sky9 Capital）：曹大容（创始合伙人）— 科技、消费')
pdf.bullet('明势资本（Future Capital）：黄明明（创始合伙人）— 硬科技、智能制造')

pdf.page_num()

# ================================================================
# SECTION 1: continued — CASE STUDIES
# ================================================================
pdf.add_page()
pdf.ch_title('第三篇续：种子/天使轮典型案例')

pdf.sub_title('案例一：字节跳动（抖音/TikTok母公司）')
pdf.body('2012年，张一鸣在知春路的民宅中创立字节跳动，获得SIG Asia（海纳亚洲）和源码资本的天使投资数百万元。当时的核心产品为今日头条的算法推荐新闻聚合。')
pdf.bullet('天使轮方：SIG Asia（王琼，合伙人）、源码资本（曹毅）')
pdf.bullet('融资额：约500万人民币（天使轮）')
pdf.bullet('后续：经历多轮融资至450亿美元估值，虽未IPO但成为全球最大独角兽之一')

pdf.sub_title('案例二：美团')
pdf.body('2010年，王兴创立美团网，获得红杉资本和北极光创投的天使投资。当时团购行业已是"千团大战"的红海市场。')
pdf.bullet('天使轮方：红杉中国（沈南鹏，创始合伙人）、北极光创投（邓锋，创始合伙人）')
pdf.bullet('融资额：约1200万美元（天使轮）')
pdf.bullet('后续：2018年港交所上市（股票代码：3690.HK），市值超万亿港元')

pdf.sub_title('案例三：晶泰科技（硬科技代表）')
pdf.body('2015年，三位MIT物理学博士创立晶泰科技（XtalPi），专注于AI驱动的药物研发。早期获得来自峰瑞资本和真格基金的天使投资，后续成长为AI制药领域的独角兽。')
pdf.bullet('天使轮方：真格基金（方爱之）、峰瑞资本（李丰，创始合伙人）')
pdf.bullet('融资额：约数百万人民币（天使轮）')
pdf.bullet('后续：2024年港交所上市，成为AI制药第一股')

pdf.ln(3)
pdf.blue_bar()
pdf.sub_title('种子/天使轮融资要点')

pdf.bullet('核心逻辑：投人＞投赛道＞投项目。创始人的学习能力、行业认知、坚持精神是决定性因素')
pdf.bullet('融资材料：一份清晰的BP（商业计划书）+ 可运行的Demo/MVP + 早期用户数据（如有）')
pdf.bullet('对接渠道：36氪项目报道、路演平台（创业邦/清科）、FA机构（光源资本/华兴资本早期FA）')
pdf.bullet('行业会议：中国天使投资人大会、WAIC世界人工智能大会、各垂直行业峰会')
pdf.bullet('避坑指南：尽量避免对赌条款和回购义务，天使轮阶段不应背负过重债务')

pdf.page_num()

# ================================================================
# SECTION 2: SERIES A
# ================================================================
pdf.add_page()
pdf.ch_title('第四篇：Pre-A轮 / A轮')

pdf.sub_title('一、阶段特征')
pdf.body('A轮是企业从0到1的关键节点，核心验证产品-市场匹配（PMF）。此时应有初步的商业模式验证、可重复的获客路径和一定规模的核心用户数据。典型估值：1亿-5亿人民币。')

pdf.sub_title('二、核心投资机构')

pdf.sub_sub('1. 红杉中国 (Sequoia China)')
pdf.bullet('投资阶段：A轮至Pre-IPO全周期')
pdf.bullet('单笔投资：3000万-5亿人民币')
pdf.bullet('关注领域：科技、消费、医疗、企业服务')
pdf.bullet('关键联系人：沈南鹏（创始合伙人）、周逵（合伙人）、计越（合伙人）、孙谦（合伙人）')
pdf.bullet('典型案例：美团（A轮→港股IPO）、字节跳动（B轮参与→全球最大独角兽）')

pdf.sub_sub('2. IDG资本 (IDG Capital)')
pdf.bullet('投资阶段：A轮至成长期')
pdf.bullet('单笔投资：2000万-3亿人民币')
pdf.bullet('关注领域：TMT、消费、医疗、先进制造')
pdf.bullet('关键联系人：熊晓鸽（创始董事长）、过以宏（合伙人）、王静波（合伙人）')
pdf.bullet('典型案例：拼多多（B轮→纳斯达克上市）、小米（A轮→港交所上市）')

pdf.sub_sub('3. 启明创投 (Qiming Venture)')
pdf.bullet('投资阶段：A轮、B轮为主')
pdf.bullet('关注领域：科技及消费、医疗健康')
pdf.bullet('关键联系人：邝子平（创始主管合伙人）、梁颕宇（主管合伙人）、胡旭波（主管合伙人）')
pdf.bullet('典型案例：小米（A轮）、美团（A轮）、哔哩哔哩（A轮→纳斯达克上市）')

pdf.sub_sub('4. 经纬中国 (Matrix Partners China)')
pdf.bullet('投资阶段：A轮至C轮')
pdf.bullet('单笔投资：1000万-2亿人民币')
pdf.bullet('关注领域：企业服务、硬科技、消费')
pdf.bullet('关键联系人：张颖（创始管理合伙人）、徐传陞（创始管理合伙人）、左凌烨（合伙人）')
pdf.bullet('典型案例：滴滴出行（A轮→纽交所上市）、理想汽车（A轮→纳斯达克上市）')

pdf.sub_sub('5. 其他核心A轮机构')
pdf.bullet('高瓴创投（GL Ventures）：张磊（创始人）、曹伟（合伙人）— 消费、科技、医疗')
pdf.bullet('君联资本（Legend Capital）：陈浩（董事长）、李家庆（总裁）— TMT、医疗')
pdf.bullet('达晨财智（Fortune Capital）：刘昼（创始合伙人）、肖冰（合伙人）— 科技制造')
pdf.bullet('深创投（SCGC）：倪泽望（董事长）— 硬科技、先进制造')

pdf.page_num()

# ================================================================
# SECTION 2: CASE STUDIES
# ================================================================
pdf.add_page()
pdf.ch_title('第四篇续：A轮典型案例')

pdf.sub_title('案例一：宁德时代')
pdf.body('2011年，曾毓群和黄世霖创立宁德时代（CATL），从ATL的动力电池部门分拆独立。2016年A轮引入国投创新、深圳平安金融科技等机构。')
pdf.bullet('A轮领投方：国投创新（高国华，董事总经理）— 国投系产业基金')
pdf.bullet('A轮跟投方：深圳平安金融科技、招银国际')
pdf.bullet('A轮融资额约30亿人民币（电池行业的重资产特征导致A轮规模较大）')
pdf.bullet('后续：2018年创业板上市（300750），市值超万亿，成为全球最大动力电池企业')

pdf.sub_title('案例二：百济神州')
pdf.body('2010年成立的创新药企，2014年获得高瓴资本领投的A轮融资，开启了中国创新药出海的先河。')
pdf.bullet('A轮方：高瓴资本（张磊，创始合伙人）、中信产业基金')
pdf.bullet('融资额：约7500万美元（A轮）')
pdf.bullet('后续：2016年纳斯达克上市（BGNE）、2018年港交所上市（06160.HK）、2021年科创板上市——A+H+N三地上市典范')

pdf.sub_title('案例三：PingCAP（TiDB）')
pdf.body('2015年创立，开源分布式数据库公司。A轮获得经纬中国领投，验证了中国基础软件开源商业化的路径。')
pdf.bullet('A轮方：经纬中国（张颖）、云启资本（毛丞宇，创始合伙人）')
pdf.bullet('融资额：约500万美元（A轮）')
pdf.bullet('后续：多轮融资至D轮，估值超30亿美元，成为全球领先的开源数据库厂商')

pdf.ln(3)
pdf.blue_bar()
pdf.sub_title('A轮融资要点')
pdf.bullet('核心逻辑：验证商业模式可规模化。投资人关注获客成本（CAC）、用户生命周期价值（LTV）、毛利水平')
pdf.bullet('关键数据：MAU/DAU增长曲线、留存率、客单价、毛利率、ARR（年经常性收入）')
pdf.bullet('FA推荐：华兴资本（包凡）、光源资本（郑烜乐，创始合伙人）、泰合资本（宋良静，合伙人）')
pdf.bullet('对接渠道：36氪/虎嗅等科技媒体报道、行业峰会演讲、FA机构引荐')

pdf.page_num()

# ================================================================
# SECTION 3: SERIES B/C
# ================================================================
pdf.add_page()
pdf.ch_title('第五篇：B轮 / C轮')

pdf.sub_title('一、阶段特征')
pdf.body('B/C轮是企业规模化扩张的关键阶段。此时商业模式已被验证，需要大量资金用于市场拓展、团队扩充、供应链建设。估值体系从"讲故事"转向"看数据"。典型估值：B轮5亿-30亿，C轮30亿-100亿。')

pdf.sub_title('二、核心投资机构')

pdf.sub_sub('1. 高瓴资本 (Hillhouse Capital)')
pdf.bullet('投资阶段：B轮至Pre-IPO，全阶段覆盖')
pdf.bullet('单笔投资：1亿-50亿人民币')
pdf.bullet('关注领域：消费、医疗、科技、企业服务')
pdf.bullet('关键联系人：张磊（创始人兼CEO）、李良（合伙人）、易清清（合伙人）、曹伟（合伙人）')
pdf.bullet('典型案例：百济神州（A轮至上市持续投资）、宁德时代（B轮参与）、美团（B轮参与）')

pdf.sub_sub('2. 腾讯投资 (Tencent Investment)')
pdf.bullet('投资阶段：B轮至战略投资')
pdf.bullet('单笔投资：5000万-数十亿人民币')
pdf.bullet('关注领域：社交、游戏、企业服务、金融科技、硬科技')
pdf.bullet('关键联系人：李朝晖（管理合伙人/副总裁）、林海峰（管理合伙人）、湛炜标（合伙人）')
pdf.bullet('典型案例：京东（C轮→纳斯达克上市）、美团（C轮→港股上市）、拼多多（C轮→纳斯达克上市）')

pdf.sub_sub('3. 阿里资本/云锋基金')
pdf.bullet('阿里资本：战略投资为主，胡晓（董事总经理）')
pdf.bullet('云锋基金：虞锋（创始主席）、李颖（合伙人）— 消费、科技、医疗')
pdf.bullet('典型案例：阿里投资微博、高德、菜鸟等战略布局；云锋投资圆通速递等')

pdf.sub_sub('4. 鼎晖投资 (CDH Investments)')
pdf.bullet('投资阶段：B轮至Pre-IPO，并购')
pdf.bullet('关注领域：消费、医疗、科技、工业')
pdf.bullet('关键联系人：焦震（创始合伙人）、胡晓玲（创始合伙人）、王霖（合伙人）')
pdf.bullet('典型案例：蒙牛（PE投资→港股上市）、美的集团（战略投资）')

pdf.sub_sub('5. 其他成长期机构')
pdf.bullet('博裕资本（Boyu Capital）：江志成（创始合伙人）— 消费、医疗、科技')
pdf.bullet('厚朴投资（Hopu Investment）：方风雷（创始人）— 大型PE、国企改制')
pdf.bullet('中信资本（CITIC Capital）：张懿宸（董事长兼CEO）— 并购、PE投资')
pdf.bullet('春华资本（Primavera Capital）：胡祖六（创始合伙人）— 消费、科技')

pdf.page_num()

# ================================================================
# SECTION 3: CASE STUDIES
# ================================================================
pdf.add_page()
pdf.ch_title('第五篇续：B/C轮典型案例')

pdf.sub_title('案例一：字节跳动B轮——从今日头条到抖音帝国')
pdf.body('2014年，字节跳动完成B轮融资，估值约5亿美元。该轮融资使其有能力从新闻聚合扩张至短视频领域（孵化抖音），真正开启了全球化征程。')
pdf.bullet('B轮领投方：红杉中国（沈南鹏）、新浪微博（曹国伟，董事长）')
pdf.bullet('融资额：约1亿美元')
pdf.bullet('关键转折：资金用于算法团队扩张和抖音App的研发启动')
pdf.bullet('后续：后续C/D/E轮融资总额超80亿美元，估值达4000亿+美元')

pdf.sub_title('案例二：京东C轮——决胜3C品类')
pdf.body('2010年，京东面临资金困境，刘强东的"烧钱自建物流"模式遭到质疑。此时今日资本徐新持续支持，高瓴资本张磊在C轮大手笔投资3亿美元，成为转折点。')
pdf.bullet('C轮方：高瓴资本（张磊，领投3亿美元）、今日资本（徐新，持续跟投）')
pdf.bullet('融资额：约15亿美元（C轮）')
pdf.bullet('关键决策：张磊说服刘强东将融资金额从7500万提升至3亿美元，全力建设物流体系')
pdf.bullet('后续：2014年纳斯达克上市（JD），市值一度超千亿美元')

pdf.sub_title('案例三：地平线机器人——硬科技C轮')
pdf.body('2015年创立，专注于自动驾驶芯片和AI边缘计算。2020年C轮融资后成为AI芯片独角兽，2024年港交所上市。')
pdf.bullet('C轮方：高瓴资本、云九资本、红杉中国、比亚迪（战略投资）')
pdf.bullet('融资额：约7亿美元（C轮）')
pdf.bullet('关键转折：比亚迪等产业资本的进入，带来车规级芯片的大规模订单')
pdf.bullet('后续：2024年港交所上市（9660.HK），市值超500亿港元')

pdf.ln(3)
pdf.blue_bar()
pdf.sub_title('B/C轮融资要点')
pdf.bullet('核心逻辑：规模化增长能力。投资人关注GMV/营收增速、毛利率趋势、市场份额、单位经济模型')
pdf.bullet('常见估值方式：PS（市销率）倍数、可比公司分析、DCF（现金流折现）')
pdf.bullet('FA推荐：华兴资本（港美股上市全链条）、光源资本（成长期FA领先）、易凯资本（王冉，创始人，医疗/消费FA）')
pdf.bullet('进场准备：已审计的财务报表、内控体系基本建立、董事会规范化运作')

pdf.page_num()

# ================================================================
# SECTION 4: SERIES D+ / PRE-IPO
# ================================================================
pdf.add_page()
pdf.ch_title('第六篇：D轮 / Pre-IPO轮')

pdf.sub_title('一、阶段特征')
pdf.body('D轮及Pre-IPO是企业上市前的最后冲刺阶段。此时企业已具备清晰的盈利路径或已盈利，融资目的主要是优化资本结构、引入基石投资者、提升上市公司形象。典型估值：100亿-500亿+人民币。')

pdf.sub_title('二、核心投资机构')

pdf.sub_sub('1. 中金资本 (CICC Capital)')
pdf.bullet('定位：中金公司旗下PE平台，Pre-IPO轮优势明显')
pdf.bullet('关键联系人：单俊葆（董事长）、陈十游（董事总经理）')
pdf.bullet('优势：中金投行资源丰富，Pre-IPO+IPO一站式服务')

pdf.sub_sub('2. 国开金融 (CDB Capital)')
pdf.bullet('定位：国家开发银行旗下，国家级产业基金')
pdf.bullet('关键联系人：信息较少（体制内机构，通常通过FA或政府关系对接）')
pdf.bullet('关注领域：基础设施、战略新兴产业、先进制造')

pdf.sub_sub('3. 国家集成电路产业投资基金（大基金）')
pdf.bullet('定位：国家级的半导体产业基金，一期1387亿，二期2000亿+')
pdf.bullet('关键联系人：通常通过地方政府经信委、发改委渠道对接')
pdf.bullet('典型案例：中芯国际（战略投资）、长江存储（大额投资）、沪硅产业')

pdf.sub_sub('4. 淡马锡/新加坡政府投资公司（GIC）')
pdf.bullet('定位：全球顶级主权基金，中国企业Pre-IPO轮常见参与者')
pdf.bullet('关键联系人：淡马锡中国区（吴亦兵，中国区总裁）')
pdf.bullet('典型案例：阿里巴巴（Pre-IPO）、美团（Pre-IPO）、蚂蚁集团（Pre-IPO）')

pdf.sub_sub('5. 其他Pre-IPO机构')
pdf.bullet('建银国际（CCB International）：建行旗下投行，Pre-IPO轮常见')
pdf.bullet('招银国际（CMB International）：招行旗下，医疗、科技Pre-IPO')
pdf.bullet('工银国际（ICBC International）：工行旗下')
pdf.bullet('产业资本：腾讯投资、阿里资本、字节跳动战投——既可为战略投资也可是财务投资')

pdf.sub_sub('6. 地方政府产业引导基金')
pdf.bullet('苏州元禾控股（林向红，创始合伙人）— 硬科技、生物医药Pre-IPO')
pdf.bullet('深投控（深圳投资控股）— 服务深圳本地科技企业上市')
pdf.bullet('上海科创投（上海科技创业投资）— 上海本地科技企业')
pdf.bullet('合肥产投（合肥产投集团）— 京东方、长鑫存储的"合肥模式"操盘者')

pdf.page_num()

# ================================================================
# SECTION 5: IPO EXIT
# ================================================================
pdf.add_page()
pdf.ch_title('第七篇：IPO退出路径')

pdf.sub_title('一、科创板（上海证券交易所）')
pdf.body('定位：硬科技企业的首选上市地，面向新一代信息技术、高端装备、新材料、新能源、生物医药等六大领域。')
pdf.bullet('上市标准：预计市值≥10亿（标准一），或≥15亿+营收≥1亿（标准二），允许未盈利企业上市')
pdf.bullet('典型周期：从改制到上市约12-18个月，审核注册制下效率较高')
pdf.bullet('代表性企业：中芯国际（688981）、金山办公（688111）、中微公司（688012）、澜起科技（688008）')
pdf.bullet('头部保荐机构：中信证券、中金公司、华泰联合、海通证券、国泰君安')

pdf.sub_title('二、创业板（深圳证券交易所）')
pdf.body('定位：创新型、成长型企业的上市平台，侧重于成长期企业。相比科创板，对行业属性的要求相对宽泛。')
pdf.bullet('上市标准：近两年净利润≥5000万，或近一年净利润≥5000万+营收≥5亿')
pdf.bullet('代表性企业：宁德时代（300750）、迈瑞医疗（300760）、爱尔眼科（300015）')
pdf.bullet('发行市盈率中枢：30-50倍，流动性较好')

pdf.sub_title('三、北交所')
pdf.body('定位：专精特新"小巨人"企业的上市平台，面向创新型中小企业。适合规模较小但具有细分领域竞争优势的企业。')
pdf.bullet('上市标准：市值≥2亿+近两年净利润≥1500万，或市值≥4亿+近两年营收≥1亿')
pdf.bullet('特色优势：从新三板精选层平移，审核流程相对简洁')
pdf.bullet('转板机制：满一年后可申请转科创板/创业板')

pdf.sub_title('四、港交所（香港）')
pdf.body('定位：国际化程度最高的中国公司上市地，适合需要海外融资渠道的企业。生物医药、消费、科技企业偏好港股。')
pdf.bullet('上市标准：18C（特专科技公司）允许未商业化企业上市，适合尚未盈利的科技公司')
pdf.bullet('18A章：生物科技公司允许无收入、未盈利上市——已帮助超过50家生物科技企业IPO')
pdf.bullet('代表性企业：美团（3690.HK）、京东健康（6618.HK）、百济神州（6160.HK）、地平线（9660.HK）')
pdf.bullet('关键保荐机构：高盛、摩根士丹利、中金公司、中信里昂、摩根大通')

pdf.sub_title('五、IPO关键流程')
pdf.bullet('辅导期（3-6个月）：券商/律所/会所进场，完成尽职调查、合规整改')
pdf.bullet('改制期（2-3个月）：完成股份公司改制，建立三会制度')
pdf.bullet('申报期（6-12个月）：提交招股说明书并回复交易所问询')
pdf.bullet('注册/发行（1-3个月）：拿到批文后路演、定价、发行上市')
pdf.bullet('总时间：A股通常18-36个月，港股12-24个月（视行业和市场环境而定）')

pdf.page_num()

# ================================================================
# SECTION 6: M&A EXIT
# ================================================================
pdf.add_page()
pdf.ch_title('第八篇：并购退出')

pdf.sub_title('一、并购概览')
pdf.body('并购（M&A）是中国企业退出的重要路径，每年并购交易规模超过3万亿元。对于未能独立上市的企业，并购退出是为股东创造流动性的主要方式。科创板开板后，A股上市公司收购科创企业的案例明显增加。')

pdf.sub_title('二、活跃的产业并购方')

pdf.sub_sub('1. BAT等互联网巨头')
pdf.bullet('腾讯：李朝晖（投资并购部负责人）、林海峰（管理合伙人）')
pdf.bullet('阿里：胡晓（战略投资部负责人）')
pdf.bullet('字节跳动：严授（战略投资负责人）、赵鹏远（战投部）')
pdf.bullet('收购逻辑：补充业务拼图、获取技术/人才/市场地位')

pdf.sub_sub('2. 上市公司并购扩张')
pdf.bullet('韦尔股份（603501）：通过收购豪威科技（OV）从分销商转型为全球CIS芯片龙头，市值从百亿跃升至千亿')
pdf.bullet('闻泰科技（600745）：收购安世半导体（Nexperia），成为全球最大的功率半导体IDM企业之一')
pdf.bullet('中际旭创（300308）：收购苏州旭创，切入光模块赛道，成为全球光模块龙头')

pdf.sub_sub('3. 地方政府/国有资本并购')
pdf.bullet('合肥模式：合肥产投/合肥建投通过股权投资引入京东方、长鑫存储、蔚来汽车等企业，资本运作+产业落地')
pdf.bullet('其他：各地国资委主导的产业链整合并购，特别是在半导体、生物医药、新能源领域活跃')

pdf.sub_sub('4. PE驱动的并购整合')
pdf.bullet('鼎晖投资（CDH）：主导双汇发展收购Smithfield（中国最大海外并购之一）')
pdf.bullet('中信资本（CITIC Capital）：收购亚信联创、金昇等')
pdf.bullet('春华资本（Primavera）：主导百胜中国分拆上市、收购美赞臣大中华区业务')

pdf.sub_title('三、并购退出流程')
pdf.bullet('准备阶段：梳理财务/法律/业务尽调材料，聘请FA或财务顾问')
pdf.bullet('寻源阶段：确定潜在收购方清单（行业龙头/产业链上下游/跨界产业资本）')
pdf.bullet('谈判阶段：签署TS（Term Sheet），进入排他性谈判（通常30-60天）')
pdf.bullet('尽调阶段：收购方PE/法律/财务/技术尽调（通常30-45天）')
pdf.bullet('交割阶段：签署SPA，完成交割条件，支付对价')
pdf.bullet('投后阶段：业绩对赌期通常3年，创始团队可能需要留任1-3年')

pdf.sub_title('四、并购退出估值参考')
pdf.bullet('有营收的科技公司：8-15倍EBITDA（息税折旧摊销前利润）')
pdf.bullet('有技术无营收的早期公司：1-3倍累计研发投入 + 技术溢价')
pdf.bullet('SaaS/软件公司：5-10倍ARR')
pdf.bullet('硬科技公司：在行业平均PS基础上加30-50%的技术稀缺性溢价')

pdf.page_num()

# ================================================================
# SECTION 7: APPENDIX
# ================================================================
pdf.add_page()
pdf.ch_title('附篇：全周期资本网络总览')

pdf.sub_title('一、FA机构（财务顾问）— 企业融资的"桥梁"')
pdf.ln(-2)
fa_list = [
    ('华兴资本', '包凡（创始人）、王力行（CEO）', '全周期FA+投行，A轮到IPO全覆盖', '一级市场FA龙头'),
    ('光源资本', '郑烜乐（创始合伙人）、李昊（合伙人）', '成长期FA，科技/消费', '快手A-D轮FA'),
    ('泰合资本', '宋良静（创始合伙人）、胡文钦（合伙人）', '成长期FA，消费/科技', '滴滴、的美团后期FA'),
    ('易凯资本', '王冉（创始合伙人）', '医疗+TMT FA', '医疗健康FA龙头'),
    ('棕榈资本', '李厚明（创始合伙人）', '消费/科技FA', '新消费领域活跃'),
    ('穆棉资本', '孙婷婷（创始合伙人）', '消费/科技FA', '早期消费FA'),
]
col_w = [32, 48, 52, 48]
headers = ['FA机构', '关键联系人', '定位/关注', '代表性案例']
pdf.set_fill_color(0x0D, 0x23, 0x4B); pdf.set_text_color(255, 255, 255)
pdf.set_font('H', '', 9); pdf.set_x(pdf.m)
for i, h in enumerate(headers):
    pdf.cell(col_w[i], 8, h, border=1, fill=True, align='C')
pdf.ln()
pdf.set_font('S', '', 8); pdf.set_text_color(0x33, 0x33, 0x33)
for row in fa_list:
    pdf.set_fill_color(0xF5, 0xF8, 0xFC)
    pdf.set_x(pdf.m)
    for i, cell in enumerate(row):
        pdf.cell(col_w[i], 7, cell, border=1, fill=True, align='L')
    pdf.ln()

pdf.ln(3)

pdf.sub_title('二、律师事务所 — IPO和M&A的法律护航')
pdf.body('头部律所：中伦（张学兵）、金杜（王俊峰）、君合（肖微）、海问（张继平）、天元（王立华）')
pdf.body('红圈所通常负责IPO发行、M&A并购交易的法律意见书和合规审查。')

pdf.sub_title('三、会计师事务所 — 财务审计的"守门人"')
pdf.body('四大在中国IPO审计中的市场份额约80%：')
pdf.bullet('普华永道（PwC）：张周（中国区主席）— A+H股审计经验最丰富')
pdf.bullet('安永（EY）：陈凯（中国区主席）— 科创板审计领军')
pdf.bullet('德勤（DTT）：蒋颖（中国区主席）— 企业服务/科技公司审计')
pdf.bullet('毕马威（KPMG）：陶匡淳（中国区主席）— 金融/国企审计')

pdf.sub_title('四、头部券商（保荐机构）')
pdf.body('A股IPO保荐承销额排名（2024-2025）：')
pdf.bullet('中信证券（张佑君，董事长）— 投行业务连续多年第一')
pdf.bullet('中金公司（陈亮，董事长）— 科创板/港股保荐领军')
pdf.bullet('华泰联合（刘晓丹，董事长）— 并购FA+IPO一体化')
pdf.bullet('海通证券、国泰君安、中信建投 — 投行业务第一梯队')

pdf.page_num()

# ================================================================
# SECTION 7: continued — SUMMARY TABLES
# ================================================================
pdf.add_page()
pdf.ch_title('附篇续：全周期联系人速查')

pdf.sub_title('一、按融资阶段匹配机构速查表')
pdf.ln(-1)

stages_data = [
    ('种子/天使', '真格基金（方爱之）、创新工场（李开复）、梅花创投（吴世春）\n险峰长青（陈科屹）、英诺天使（李竹）、蓝驰创投（陈维广）'),
    ('Pre-A/A轮', '红杉中国（周逵）、IDG资本（过以宏）、启明创投（邝子平）\n经纬中国（张颖）、高瓴创投（曹伟）、君联资本（陈浩）'),
    ('B/C轮', '高瓴资本（张磊）、腾讯投资（李朝晖）、鼎晖投资（焦震）\n博裕资本（江志成）、云锋基金（虞锋）、春华资本（胡祖六）'),
    ('成长期', '中金资本（单俊葆）、国开金融、国家大基金\n淡马锡（吴亦兵）、GIC、各地方产业引导基金'),
    ('Pre-IPO', '中信证券、中金公司、华泰联合（投行保荐团队）\n各大保荐机构的TMT/医疗/科技行业组负责人'),
    ('IPO', '沪深交易所、港交所上市审核团队\n四大会计师事务所+红圈律所+券商投行联合工作'),
    ('并购', '腾讯/阿里/字节战投部、韦尔股份/闻泰科技等产业买方\n鼎晖/中信资本等并购PE'),
]

for stage, desc in stages_data:
    pdf.set_fill_color(0x0D, 0x23, 0x4B); pdf.set_text_color(255, 255, 255)
    pdf.set_font('H', '', 9); pdf.set_x(pdf.m)
    pdf.cell(26, 7, f'【{stage}】', border=1, fill=True, align='C')
    pdf.set_fill_color(0xF5, 0xF8, 0xFC); pdf.set_text_color(0x33, 0x33, 0x33)
    pdf.set_font('S', '', 9)
    pdf.multi_cell(pdf.w - 2 * pdf.m - 26, 7, desc, border=1, fill=True, align='L')
    pdf.set_x(pdf.m); pdf.ln(1)



# ================================================================
# SECTION 8: STATE-OWNED CAPITAL DEEP ANALYSIS
# ================================================================

# ================================================================
# SECTION 8: STATE-OWNED CAPITAL DEEP ANALYSIS
# ================================================================
pdf.add_page()
pdf.ch_title('第九篇：国资投资机构深度分析')

pdf.body('近年来，国资背景投资机构在中国股权投资市场中的地位急速上升。2025年国资机构已占募资端的70%以上，投资端占比亦超过50%。以下对核心国资投资机构进行系统分析，并尝试回答"哪家国资机构投了你，你就大概率能成功"。')

pdf.sub_title('一、核心国资投资机构全景图')

pdf.sub_sub('【第一梯队】国家级战略力量')
pdf.ln(-1)

g1_data = [
    ('国家集成电路\n产业投资基金\n（大基金）', '半导体全产业链\n芯片设计/制造/封测/设备/材料', '一期1387亿\n二期2000亿+', '中芯国际、北方华创、\n拓荆科技、中微公司\n华大九天、长电科技', '投资企业70+家，已上市约30+家\n但IPO失败案例亦存在（硅数股份等）\n"大基金投了"是行业背书\n≠ IPO必成功'),
    ('国开金融', '基础设施、战略新兴\n产业、一带一路', '未公开\n（千亿级）', '中芯国际(大股东)、\n国家管网、华大基因', '国开行全资子公司\n政策导向性强\n退出案例公开较少'),
    ('中金资本', '全行业覆盖\nPre-IPO轮优势', '管理规模\n约3000亿', '2024年15个IPO\n地平线、晶泰科技等', '中金公司旗下PE\n投行资源丰富\nPre-IPO退出率极高'),
]

for name, focus, scale, cases, note in g1_data:
    pdf.set_fill_color(0xE8, 0xF0, 0xF8)
    pdf.set_draw_color(0x00, 0x6D, 0xBA)
    pdf.set_line_width(0.3)

    # Name
    pdf.set_font('H', '', 8); pdf.set_text_color(0x0D, 0x23, 0x4B)
    pdf.set_xy(pdf.m, pdf.get_y())
    pdf.multi_cell(28, 5.5, name, border=1, fill=True, align='C')

    # Focus
    y_before = pdf.get_y()
    pdf.set_font('S', '', 7.5); pdf.set_text_color(0x33, 0x33, 0x33)
    pdf.set_xy(pdf.m + 28, pdf.get_y() - 5.5)
    pdf.multi_cell(32, 5.5, focus, border=1, fill=True, align='L')

    # Scale
    pdf.set_xy(pdf.m + 60, pdf.get_y() - min(5.5, pdf.get_y() - y_before + 5.5))
    pdf.multi_cell(26, 5.5, scale, border=1, fill=True, align='C')

    # Cases
    pdf.set_xy(pdf.m + 86, pdf.get_y() - min(5.5, pdf.get_y() - y_before + 5.5))
    pdf.multi_cell(48, 5.5, cases, border=1, fill=True, align='L')

    # Note
    pdf.set_xy(pdf.m + 134, pdf.get_y() - min(5.5, pdf.get_y() - y_before + 5.5))
    pdf.multi_cell(pdf.w - pdf.m - 134 - pdf.m, 5.5, note, border=1, fill=True, align='L')

    # Fix Y
    max_y = max(pdf.get_y(), y_before + 5.5 * max(name.count('\n') + 1, focus.count('\n') + 1, scale.count('\n') + 1, cases.count('\n') + 1, note.count('\n') + 1))
    pdf.set_y(max(pdf.get_y(), y_before + 22))
    pdf.set_y(pdf.get_y())

pdf.ln(3)
pdf.sub_sub('【第二梯队】地方国资创投巨头')
pdf.ln(-1)

g2_data = [
    ('深创投', '深圳市政府控股\n综合创投', '累计投资\n1500+家', '269家已上市\n17个资本市场', '累计IPO数量全国第一', '⭐'),
    ('达晨财智', '湖南电广传媒系\n市场化国资', '累计投资\n780+家', '143家上市\n退出率~38.6%', '公开披露退出率最高的国资', '⭐'),
    ('元禾控股', '苏州工业园区\n国资', '管理规模\n数百亿', '80+家已上市\n纳芯微/A+H', '苏州模式标杆', '⭐'),
    ('合肥产投', '合肥市国资委', '累计投资\n数百亿', '京东方、长鑫存储\n蔚来汽车', '合肥模式操盘者\n以精准投融资闻名', '⭐'),
]

col_g2 = [24, 34, 34, 42, 46, 12]
pdf.set_fill_color(0x0D, 0x23, 0x4B); pdf.set_text_color(255, 255, 255)
pdf.set_font('H', '', 8); pdf.set_x(pdf.m)
for i, h in enumerate(['机构', '背景', '管理规模', '退出成绩', '核心特征', '评级']):
    pdf.cell(col_g2[i], 8, h, border=1, fill=True, align='C')
pdf.ln()
pdf.set_font('S', '', 8); pdf.set_text_color(0x33, 0x33, 0x33)
for row in g2_data:
    pdf.set_fill_color(0xF5, 0xF8, 0xFC)
    pdf.set_x(pdf.m)
    for i, cell in enumerate(row):
        if i == 5:
            pdf.set_text_color(0xCC, 0x88, 0x00)
            pdf.set_font('H', '', 10)
        else:
            pdf.set_text_color(0x33, 0x33, 0x33)
            pdf.set_font('S', '', 8)
        pdf.cell(col_g2[i], 7, cell, border=1, fill=True, align='C' if i == 5 else 'L')
    pdf.ln()

pdf.ln(4)
pdf.sub_title('二、"投了就成功"的含金量分析')

pdf.body('市场上没有哪家机构能保证100%IPO成功。但结合数据，以下机构展现出显著高于行业平均的"项目成功率"（上市+并购+高回报退出）。')

pdf.sub_sub('1. 达晨财智 — 退出率最高的国资创投')
pdf.body('累计投资780+家企业，301家成功退出（含143家上市、104家新三板），累计退出率约38.6%。在创投行业中，15-20%的IPO率即为优秀水平，达晨的综合退出率接近40%，在国资机构中公开披露最高。其核心优势在于（1）对制造业/硬科技的深度理解和长期布局；（2）不盲目追风口，坚持"行业研究驱动"的投资纪律。')

pdf.sub_sub('2. 深创投 — 累计IPO数量最多的创投机构')
pdf.body('累计投资1500+家，推动269家企业在全球17个资本市场上市（不含新三板），数量全国第一。约17%的IPO率。其核心优势在于（1）深圳市政府的强大资源网络；（2）管理100+只引导基金，覆盖全国；（3）"孵化+投资"模式深度赋能。深创投投过、并且成功IPO的企业数量无人能及，但1500+的总投资基数也意味着大量项目未上市。')

pdf.sub_sub('3. 中金资本 — Pre-IPO阶段"命中率"最高')
pdf.body('中金资本的Pre-IPO投资策略不同于一般VC——通常在企业已具备明确上市条件时进入，因此退出确定性极高。2024年15个IPO的业绩全行业第一。核心壁垒在于中金公司的保荐承销资源——中金资本投资的企业，中金投行大概率是保荐人，形成了"投资+保荐"的闭环。')

pdf.sub_sub('4. 合肥产投 — "合肥模式"的产业精准度')
pdf.body('合肥产投最著名的案例包括：投资京东方（首条AMOLED6代线）、投资长鑫存储（国产DRAM突破）、"急救"蔚来汽车（70亿战投→蔚来股价涨超10倍）。其成功秘诀在于（1）深度产业研究——政府派出专业的产业投资团队；（2）"以投带引"——通过资本引入产业链核心企业；（3）全生命周期服务——从落地到上市提供全方位的政策/土地/人才支持。合肥产投并非广撒网式投资，而是极其精准的"狙击手"策略。')

pdf.sub_sub('5. 国家大基金 — 行业"背书"价值超过资金本身')
pdf.body('大基金投资的战略意义远超资金本身：获得大基金投资，等同于获得国家层面的产业认可。大基金一期投资70+家企业，已上市约30+家。但需注意并非投了就必上市——硅数股份（IPO终止后被大基金清仓）、华羿微电（撤回IPO申请）等案例表明，大基金也会投错。大基金的价值在于：获得大基金投资的企业，后续获得地方政府补贴、银行贷款、其他社会资本跟投的概率大幅提升。')

pdf.ln(3)
pdf.blue_bar()
pdf.sub_title('综合判断："投了大概率能成"的机构排序')
pdf.ln(-1)
ai_ranking = [
    ('🥇', '中金资本', 'Pre-IPO轮投资', '15/20 ≈ 75%', '投行保荐闭环，Pre-IPO轮退出确定性最高'),
    ('🥇', '达晨财智', '全阶段', '301/780 ≈ 38.6%', '公开披露综合退出率最高的国资创投'),
    ('🥈', '深创投', '全阶段', '269/1500+ ≈ 17%', '累计IPO绝对数量全国第一'),
    ('🥈', '合肥产投', '产业投资阶段', '极高（精准狙击）', '案例数量有限但成功率极高，合肥模式'),
    ('🥉', '元禾控股', '早期至成长期', '80+/数百 ≈ 20%+', '苏州工业园产业生态赋能'),
    ('🥉', '国家大基金', '成长期+战略投资', '30+/70 ≈ 43%', '政策背书价值超过资金本身'),
]

for rank, name, stage, rate, desc in ai_ranking:
    pdf.set_font('H', '', 9); pdf.set_text_color(0x0D, 0x23, 0x4B)
    pdf.set_x(pdf.m)
    pdf.cell(10, 6, rank)
    pdf.set_font('H', '', 10); pdf.set_text_color(0x00, 0x6D, 0xBA)
    pdf.cell(24, 6, name)
    pdf.set_font('S', '', 8.5); pdf.set_text_color(0x33, 0x33, 0x33)
    pdf.cell(28, 6, stage)
    pdf.set_font('H', '', 9); pdf.set_text_color(0x0D, 0x23, 0x4B)
    pdf.cell(38, 6, rate)
    pdf.set_font('S', '', 8); pdf.set_text_color(0x55, 0x55, 0x55)
    pdf.multi_cell(pdf.w - 2 * pdf.m - 10 - 24 - 28 - 38, 6, desc, align='J')
    pdf.set_x(pdf.m); pdf.ln(1)

pdf.ln(3)
pdf.note_box('重要提醒：以上"成功率"为估算值，基于各机构公开披露数据推算。实际投资中不存在"必成功"的机构。IPO成功率受市场环境、政策变化、行业周期、企业自身经营等多重因素影响。本文分析仅作为行业研究参考，不构成投资建议。')

pdf.page_num()

# ================================================================
# SECTION 9: FINAL PAGE
# ================================================================
pdf.add_page()
pdf.ch_title('附篇：关键术语与实操建议')

pdf.sub_title('常见融资条款术语')
pdf.ln(-1)
terms = [
    ('TS', 'Term Sheet 投资条款清单——非约束性（除排他期条款外），确定主要估值和交易条件'),
    ('SPA', 'Share Purchase Agreement 股权购买协议——约束性法律文件，经双方正式签署后生效'),
    ('SHA', 'Shareholders Agreement 股东协议——约定股东之间的权利义务'),
    ('DD', 'Due Diligence 尽职调查——投资方对企业法律/财务/业务的全面审查'),
    ('VAM', 'Valuation Adjustment Mechanism 对赌协议——基于未来业绩的估值调整条款'),
    ('反稀释', 'Anti-Dilution——保护投资人在后续融资低价发行时股权不被过度稀释'),
    ('优先清算权', 'Liquidation Preference——投资人在公司清算或并购时的优先分配权'),
    ('一票否决权', 'Veto Right——投资人对重大事项（增资/并购/分红等）的否决权'),
    ('回购条款', 'Redemption Right——特定条件下（如未按期IPO），企业须按约定价格回购投资人股份'),
    ('ESOP', 'Employee Stock Ownership Plan 员工股权激励计划——通常预留10-20%用于激励团队'),
]

for term, desc in terms:
    pdf.set_font('H', '', 10); pdf.set_text_color(0x0D, 0x23, 0x4B)
    pdf.set_x(pdf.m); pdf.cell(26, 6, term)
    pdf.set_font('S', '', 9); pdf.set_text_color(0x33, 0x33, 0x33)
    pdf.multi_cell(pdf.w - 2 * pdf.m - 26, 6, desc, align='J')
    pdf.set_x(pdf.m); pdf.ln(1)

pdf.ln(3)
pdf.blue_bar()

pdf.sub_title('给创业者的10条融资建议')
pdf.ln(-1)
tips = [
    '融资节奏比估值重要：确保在"有钱的时候融资"，而非"缺钱的时候融资"。预留至少12-18个月的 run rate',
    '选对的投资人比选高估值重要：战略资源、行业人脉、后续融资能力的价值远超20-30%的估值差异',
    'BP要讲"故事+数据"：前3页讲清楚痛点和解决方案，后5页用数据证明可规模化的逻辑',
    '提前6个月开始接触：从第一次接触投资机构到资金到账，平均需要4-8个月',
    '同时接触15-20家机构：制造竞争氛围，防止被单一机构"压价"或拖延',
    '用FA节省精力：成长期融资建议聘请专业FA，其佣金（通常为融资额的1-3%）物有所值',
    'ESOP规划提前做：股权激励计划在首轮融资前设计好，避免后续引入新投资人时被大幅摊薄',
    '年报/季报要专业：即使未上市，也要以公众公司标准对待财务报告——投资人会持续跟踪',
    '不要签个人连带责任的对赌：特别是早期融资，创始人个人不应为公司的业绩承担连带责任',
    '董事会里要有"聪明人"：引进能提供战略建议的董事/观察员，比纯财务投资人更有价值',
]

for i, tip in enumerate(tips):
    pdf.set_font('H', '', 9); pdf.set_text_color(0x00, 0x6D, 0xBA)
    pdf.set_x(pdf.m)
    pdf.cell(6, 6, f'{i+1}.')
    pdf.set_font('S', '', 9); pdf.set_text_color(0x33, 0x33, 0x33)
    pdf.multi_cell(pdf.w - 2 * pdf.m - 6, 6, tip, align='J')
    pdf.set_x(pdf.m); pdf.ln(1)

pdf.ln(4)

pdf.set_font('S', '', 9); pdf.set_text_color(0x99, 0x99, 0x99)
pdf.multi_cell(pdf.w - 2 * pdf.m, 6,
               '本文件仅作为行业知识参考，不构成任何投资建议。\n'
               '所列机构信息和联系人基于公开资料整理，实际对接时建议通过FA或行业人脉引荐。\n'
               '2026年5月 · 上海', align='C')

pdf.page_num()

# ================================================================
# SAVE
# ================================================================
import os
OUTPUT = '/Users/cyingfang/WorkBuddy/20260429082054/中国企业融资路线图.pdf'
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
pdf.output(OUTPUT)
print(f'Saved: {OUTPUT}')
print(f'Pages: {pdf.page_no()}')
