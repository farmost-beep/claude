#!/usr/bin/env python3
"""Long Now 长现 —— 科技金融30年投资思维框架 PDF"""

from fpdf import FPDF

SONGTI = '/System/Library/Fonts/Supplemental/Songti.ttc'
HEITI = '/System/Library/Fonts/STHeiti Medium.ttc'


class PDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.add_font('S', '', SONGTI)
        self.add_font('H', '', HEITI)
        self.set_auto_page_break(True, 20)
        self.m = 22
        self.w = 210

    def title_page(self, main, sub='', sub2=''):
        self.add_page()
        self.set_fill_color(0x0D, 0x23, 0x4B)
        self.rect(0, 0, self.w, 297, 'F')
        self.ln(45)
        self.set_font('H', '', 10)
        self.set_text_color(0xC9, 0xA8, 0x4C)
        self.multi_cell(self.w - 2 * self.m, 8, 'L O N G   N O W', align='C')
        self.ln(8)
        self.set_font('H', '', 32)
        self.set_text_color(0xFF, 0xFF, 0xFF)
        self.multi_cell(self.w - 2 * self.m, 14, main, align='C')
        self.ln(6)
        self.set_font('S', '', 13)
        self.set_text_color(0xCC, 0xDD, 0xEE)
        self.multi_cell(self.w - 2 * self.m, 8, sub, align='C')
        self.ln(4)
        self.set_draw_color(0xC9, 0xA8, 0x4C)
        self.set_line_width(0.5)
        cx = self.w / 2
        self.line(cx - 20, self.get_y(), cx + 20, self.get_y())
        self.ln(6)
        self.set_font('S', '', 9)
        self.set_text_color(0x88, 0x99, 0xAA)
        self.multi_cell(self.w - 2 * self.m, 6, sub2, align='C')

    def ch_title(self, t):
        self.add_page()
        self.set_font('H', '', 18)
        self.set_text_color(0x0D, 0x23, 0x4B)
        self.set_x(self.m)
        self.cell(self.w - 2 * self.m, 10, t)
        self.ln(12)
        self.set_draw_color(0x00, 0x6D, 0xBA)
        self.set_line_width(0.5)
        self.line(self.m, self.get_y() - 4, self.m + 35, self.get_y() - 4)
        self.ln(6)

    def sub_title(self, t):
        self.set_font('H', '', 13)
        self.set_text_color(0x00, 0x6D, 0xBA)
        self.set_x(self.m)
        self.cell(self.w - 2 * self.m, 8, t)
        self.ln(10)

    def body(self, t):
        self.set_font('S', '', 10)
        self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m)
        self.multi_cell(self.w - 2 * self.m, 6, t, align='J')
        self.ln(2)

    def bold_body(self, t):
        self.set_font('H', '', 10)
        self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m)
        self.multi_cell(self.w - 2 * self.m, 6, t, align='J')
        self.ln(2)

    def bullet(self, t):
        self.set_font('S', '', 9.5)
        self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m)
        self.cell(6, 5.5, '>')
        self.multi_cell(self.w - 2 * self.m - 6, 5.8, t, align='J')
        self.set_x(self.m)
        self.ln(0.5)

    def highlight_box(self, title, content):
        self.set_fill_color(0xE8, 0xF0, 0xF8)
        self.set_draw_color(0x00, 0x6D, 0xBA)
        self.set_line_width(0.3)
        x, y = self.get_x(), self.get_y()
        self.set_font('H', '', 10)
        self.set_text_color(0x0D, 0x23, 0x4B)
        self.set_x(self.m + 3)
        self.multi_cell(self.w - 2 * self.m - 6, 6, title, align='L')
        self.set_font('S', '', 9)
        self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m + 3)
        self.multi_cell(self.w - 2 * self.m - 6, 5.5, content, align='J')
        ny = self.get_y()
        self.rect(self.m, y - 1, self.w - 2 * self.m, ny - y + 2)
        self.set_y(ny + 4)

    def gold_bar(self):
        self.set_draw_color(0xC9, 0xA8, 0x4C)
        self.set_line_width(0.4)
        y = self.get_y()
        self.line(self.m, y, self.w - self.m, y)
        self.ln(4)

    def pillar_section(self, num, name_zh, name_en, icon, desc, timeline, invest_angle, example):
        """5大支柱统一模板"""
        self.set_font('H', '', 14)
        self.set_text_color(0x0D, 0x23, 0x4B)
        self.set_x(self.m)
        self.cell(self.w - 2 * self.m, 8, f'{num}. {name_zh} / {name_en}')
        self.ln(10)
        self.set_font('S', '', 9.5)
        self.set_text_color(0x55, 0x55, 0x55)
        self.set_x(self.m)
        self.multi_cell(self.w - 2 * self.m, 5.5, desc, align='J')
        self.ln(1)
        # Timeline
        self.set_font('H', '', 9)
        self.set_text_color(0x00, 0x6D, 0xBA)
        self.set_x(self.m)
        self.cell(self.w - 2 * self.m, 5.5, f'时间窗口：{timeline}')
        self.ln(6)
        # Investment angle
        self.set_font('S', '', 9)
        self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m)
        self.cell(self.w - 2 * self.m, 5.5, f'投资视角：{invest_angle}')
        self.ln(6)
        # Example
        self.set_font('S', '', 9)
        self.set_text_color(0x55, 0x55, 0x55)
        self.set_x(self.m)
        self.cell(self.w - 2 * self.m, 5.5, f'案例：{example}')
        self.ln(8)
        self.gold_bar()

    def page_num(self):
        self.set_font('S', '', 8)
        self.set_text_color(0xAA, 0xAA, 0xAA)
        self.set_y(-15)
        self.cell(self.w - 2 * self.m, 5, str(self.page_no()), align='R')


pdf = PDF()
pdf.set_margin(22)

# ================================================================
# TITLE
# ================================================================
pdf.title_page(
    '长现  投资框架',
    'Long Now — 以30年为尺度，做今天的科技金融决策',
    '邮储银行上海分行科技金融事业部  |  2026年5月')

# ================================================================
# PART 0: 为什么是30年？
# ================================================================
pdf.ch_title('引言：为什么是30年？')

pdf.body('2026年到2056年——这是一个足够长的时间跨度，让今天还在实验室里的技术变成基础设施；也是一个足够短的时间跨度，让今天的投资决策在30年后可以被回溯验证。')

pdf.body('30年的意义在于：')

pdf.bullet('技术收敛周期：从基础研究突破到商业化落地，平均需要20-30年。AI从2012年深度学习突破到2025年接近AGI，用了约13年；核聚变从实验到商用，预计需要30年。')
pdf.bullet('一代人的视野：30年恰好是一个职业金融从业者的完整职业生涯。以30年为框架做决策，意味着每一次布局都可能是职业生涯的"代表作"。')
pdf.bullet('可回溯性：30年后，今天的大多数人仍然健在。这意味着我们可以亲眼见证自己的判断是否正确——这是一个负责任的决策框架的基本要求。')
pdf.bullet('不可逆性：30年内发生的技术变革（AGI、基因编辑、核聚变）可能是不可逆的。这意味着"不投资"本身就是一个重大决定。')

pdf.gold_bar()
pdf.highlight_box('核心问题', '如果2056年回看2026年，哪些今天看起来"不合理"的决定，会被证明是明智的？这个PDF试图给出一个系统化的回答框架。')

# ================================================================
# PART 1: 哲学理念
# ================================================================
pdf.ch_title('一、哲学理念：长现 Long Now')

pdf.sub_title('1.1 Long Now 的传统')

pdf.body('"长现"（Long Now）的概念源自Stewart Brand、Brian Eno、Danny Hillis等人在1996年创立的Long Now Foundation。其核心理念是将人类决策的时间尺度从"现在"延伸到"万年"——用万年钟（10,000-Year Clock）的象征意义，提醒人类文明需要超越短期思维的局限。')

pdf.body('Brian Eno创造了"Long Now"这个词。他说："我们不仅失去了未来，也失去了过去。‘现在’变得越来越薄——我们只活在当下这一刻，忘记了前人的智慧，也忘记了对后人的责任。"')

pdf.body('将这个理念应用到科技金融投资中，就是要把"现在"从眼前的季度报告、月度KPI，扩展到30年的尺度。')

pdf.sub_title('1.2 科技金融的"时间错配"')

pdf.body('科技金融面临的根本困境是时间的错配：')

pdf.bullet('技术的逻辑：从研发到商业化的周期是5-30年，需要的是"耐心资本"（Patient Capital）')
pdf.bullet('金融的逻辑：银行产品期限结构是1-5年，追求的是"确定性"（Certainty）')
pdf.bullet('资本的逻辑：LP的出资周期是7-10年，要求的是"退出"（Exit）')

pdf.body('这个错配不是有人做错了什么，而是两个领域的本质差异。Long Now哲学的核心主张是：不要试图消除这个错配，而是用更长的时间尺度来包容它。')

pdf.sub_title('1.3 三条基石信念')

pdf.bold_body('信念一：技术在收敛，不是发散')
pdf.body('未来30年，AI、生物、能源、材料、计算五大领域正在加速趋同。今天的"多领域突破"不是分散的，而是指向同一个方向：人类掌控自身演化的能力指数级增长。投资的本质是在收敛方向上提前站位。')

pdf.bold_body('信念二：基础设施比应用更值得长期持有')
pdf.body('30年维度上，应用层会经历多轮更迭（社交→电商→AI→...），但基础设施（算力、能源、网络、生物平台）的价值会持续增长。投资底层平台，而不是顶层应用。')

pdf.bold_body('信念三：最大的风险是不参与，而不是投错')
pdf.body('30年后回看，错过了AI比投错了AI的代价更大。在一个不可逆的技术变革时代，"不决策"本身就是最危险的决策。')

# ================================================================
# PART 2: 方法论
# ================================================================
pdf.ch_title('二、方法论：五步法')

pdf.body('Long Now框架的方法论由五个步骤组成，形成一个完整的决策闭环：')

steps = [
    ('Telescope 望远镜', '扫描30年科技趋势',
     '从基础研究出发，识别正在孕育的技术突破。关注Nature/Science顶刊论文、DARPA项目、诺奖级发现。不问"明年什么最火"，问"30年后什么还在"。'),
    ('Microscope 显微镜', '定位底层平台',
     '在每一个技术方向上，找到那个"所有上层应用都离不开"的底层平台。在AI中是算力和模型，在生物中是测序和编辑工具，在能源中是储能和传输。'),
    ('Compass 指南针', '判断收敛方向',
     '多个技术方向是否在指向同一个目标？AI+生物=精准医疗，AI+能源=智能电网，AI+材料=超材料。收敛处是最大的投资机会。'),
    ('Anchor 锚定', '锁定关键节点',
     '在收敛方向上找到那个不可绕过的节点——关键技术、核心企业、关键人物。30年布局只需要抓住3-5个"锚点"。'),
    ('Patience 持有', '等待价值释放',
     '这是最难的一步。持有不是被动等待，而是主动跟踪、每年校准、但不轻易退出。30年的框架意味着：进入之前要足够审慎，进入之后要足够坚定。'),
]

for i, (title_en, title_zh, desc) in enumerate(steps):
    pdf.set_fill_color(0xF5, 0xF8, 0xFC) if i % 2 == 0 else pdf.set_fill_color(0xFF, 0xFF, 0xFF)
    y0 = pdf.get_y()
    pdf.set_font('H', '', 11)
    pdf.set_text_color(0x0D, 0x23, 0x4B)
    pdf.set_x(pdf.m + 2)
    pdf.cell(6, 6, f'{i+1}')
    pdf.cell(pdf.w - 2 * pdf.m - 8, 6, f'{title_en} / {title_zh}')
    pdf.ln(7)
    pdf.set_font('S', '', 9.5)
    pdf.set_text_color(0x33, 0x33, 0x33)
    pdf.set_x(pdf.m + 10)
    pdf.multi_cell(pdf.w - 2 * pdf.m - 12, 5.5, desc, align='J')
    pdf.ln(3)

pdf.gold_bar()
pdf.highlight_box('方法论的关键',
                  '五步法的核心不是"预测未来"，而是"识别已经发生的未来"（Peter Drucker）。30年的趋势不是猜出来的，是读出来的——读论文、读专利、读实验室里正在发生的事。')

# ================================================================
# PART 3: 框架 — 5大收敛支柱
# ================================================================
pdf.ch_title('三、框架：五大收敛支柱')

pdf.body('基于对30年科技趋势的扫描，Long Now框架识别出五大技术收敛方向。每一个方向都是一条独立的投资主线，但更重要的是——它们正在加速交汇。')

pdf.gold_bar()

pdf.pillar_section(
    1, '智能收敛', 'Intelligence',
    '通用人工智能（AGI）从实验室走向经济基础设施',
    '2024-2026年，AI从"工具"进化为"智能体"（Agent），2027-2030年可能实现通用人工智能（AGI），2030年后ASI（超级智能）成为可能。AI将像今天的电力一样无处不在。',
    '2025-2035 (第一波) / 2035-2055 (第二波)',
    '算力基础设施（GPU/芯片）> 模型层 > AI Agent平台 > 行业应用',
    'NVIDIA/台积电 (算力层)；OpenAI/DeepMind (模型层)；Microsoft/Google (应用层)')

pdf.pillar_section(
    2, '生命收敛', 'Longevity',
    '生命科学从"治疗"进化为"增强"',
    '基因编辑（CRISPR 3.0）、细胞重编程、端粒酶激活、脑科学——多个方向同时突破。2030-2040年间，人类寿命可能有质的飞跃（150岁+成为可能）。这不仅是一个医学议题，将重塑养老金、保险、消费等整个经济结构。',
    '2026-2035 (技术验证) / 2035-2050 (商业化)',
    '基础工具（测序/编辑/合成）> 数据平台 > 治疗公司 > 增强应用',
    'Illumina/CG (测序)；Editas/CRISPR Therapeutics (编辑)；Altos Labs (重编程)')

pdf.pillar_section(
    3, '能源收敛', 'Energy',
    '清洁能源从"替代"走向"充裕"',
    '核聚变（2025-2035商用化）、高效光伏（钙钛矿突破）、固态电池——三种技术路径都在加速。30年后，"能源成本趋近于零"不再是幻想。这将重塑制造业、交通、农业的全球格局。',
    '2026-2035 (聚变示范) / 2035-2050 (规模商用)',
    '聚变技术 > 储能 > 智能电网 > 能源密集型产业重构',
    'Commonwealth Fusion (聚变)；CATL/QuantumScape (储能)；NextEra (电网友)')

pdf.pillar_section(
    4, '接口收敛', 'Interface',
    '人机融合从"外设"走向"嵌入"',
    '脑机接口（Neuralink、Synchron）、AR/VR（Apple Vision Pro）、神经增强芯片——三种人机交互方式正在融合。2030-2040年间，"思考即操作"成为现实。这不仅改变消费电子，更将重塑教育、医疗、军事。',
    '2026-2030 (医疗应用) / 2030-2045 (消费级)',
    '硬件（芯片/电极）> 信号解码 > 应用平台 > 神经计算',
    'Neuralink (侵入式BCI)；Synchron (血管内BCI)；Apple/Meta (空间计算)')

pdf.pillar_section(
    5, '扩张收敛', 'Expansion',
    '人类活动空间从地球走向地月系',
    'SpaceX（星舰）、蓝色起源（月球基地）、中国国家航天局（月球科研站）——多个玩家同时推动太空经济。2040年左右，地月经济圈可能形成。更长期看，小行星采矿和火星殖民成为新的增长极。',
    '2026-2035 (运力降本) / 2035-2050 (太空经济)',
    '发射服务 > 卫星网络 > 资源开采 > 空间制造',
    'SpaceX (发射/星舰)；Blue Origin (月球着陆器)；AST SpaceMobile (卫星网络)')

# ================================================================
# PART 4: 框架的应用
# ================================================================
pdf.ch_title('四、框架应用：三个维度')

pdf.sub_title('4.1 维度一：时间配置')

pdf.body('Long Now框架要求将投资组合按时间维度分层：')

pdf.set_font('S', '', 9.5)
pdf.set_text_color(0x33, 0x33, 0x33)
y = pdf.get_y()

# Time allocation table
cols = [pdf.w * 0.14, pdf.w * 0.22, pdf.w * 0.28, pdf.w * 0.36]
headers = ['层级', '时间', '重点方向', '配置逻辑']
rows = [
    ['稳定层', '1-3年', 'AI应用/金融科技', '现金流+确定性'],
    ['增长层', '3-10年', 'AI模型/生物技术', '高增长+可退出'],
    ['探索层', '10-30年', '聚变/BCI/太空', '期权价值+战略站位'],
]

for r in [headers] + rows:
    pdf.set_x(pdf.m)
    if r == headers:
        pdf.set_fill_color(0x0D, 0x23, 0x4B)
        pdf.set_text_color(0xFF, 0xFF, 0xFF)
        pdf.set_font('H', '', 9)
    else:
        pdf.set_fill_color(0xF5, 0xF8, 0xFC)
        pdf.set_text_color(0x33, 0x33, 0x33)
        pdf.set_font('S', '', 9)
    for j, c in enumerate(r):
        pdf.cell(cols[j], 7, c, border=1, fill=True)
    pdf.ln()
pdf.ln(5)

pdf.sub_title('4.2 维度二：地理配置')

pdf.body('30年维度上，科技创新的地理分布正在重构：')
pdf.bullet('美国：基础研究+资本市场驱动，AGI/BCI/太空领先')
pdf.bullet('中国：制造能力+市场规模驱动，新能源/量子/生物制造领先')
pdf.bullet('欧洲：基础科学+监管框架驱动，核聚变/生物伦理领先')
pdf.bullet('新兴地带：东南亚/印度/中东，数字基础设施+人口红利')

pdf.sub_title('4.3 维度三：风险对冲')

pdf.body('30年框架的风险逻辑与传统金融不同：')
pdf.bullet('最大风险：误判收敛方向（如认为AGI不会发生）——通过定期校准应对')
pdf.bullet('次大风险：过早退出（如2023年卖掉NVIDIA）——通过"锚定"机制锁定长期持有')
pdf.bullet('常规风险：单一企业失败——通过投资底层平台（非单个公司）对冲')
pdf.bullet('黑天鹅：技术逆转（如AI安全导致全面监管）——保持10%现金+灵活仓位')

# ================================================================
# PART 5: 案例深度分析
# ================================================================
pdf.ch_title('五、案例深度分析')

pdf.sub_title('案例一：AI算力——从"芯片"到"智能基础设施"')

pdf.body('2023年，当大多数人将AI视为"又一个科技泡沫"时，以30年尺度看，这恰恰是智能收敛的起点。')
pdf.bullet('2023-2024：训练算力需求每18个月增长10倍（远超摩尔定律）')
pdf.bullet('2025-2026：推理算力需求超过训练，AI进入"消费级"阶段')
pdf.bullet('2027-2030：AGI训练需要百万级GPU集群，算力成为国家战略资源')
pdf.bullet('投资启示：算力是AI的"石油"，硬件层的机会比应用层更确定')

pdf.sub_title('案例二：生命科学——从"基因测序"到"寿命重构"')

pdf.body('2010年代基因测序成本下降10万倍（从1亿美元到1000美元），这预示了生命科学的数据化革命。')
pdf.bullet('2020-2025：CRISPR基因编辑进入临床，mRNA平台验证成功')
pdf.bullet('2026-2035：细胞重编程、端粒延长、表观遗传重编程进入人体试验')
pdf.bullet('2035-2050：衰老可逆化，人类预期寿命突破120岁')
pdf.bullet('投资启示：生命科学正处于"测序→理解→编辑→编程"的第四阶段，底层工具公司最值得长期持有')

pdf.sub_title('案例三：能源——从"替代能源"到"充裕能源"')

pdf.body('能源范式转变是最慢但最确定的30年趋势。2000-2025年太阳能成本下降90%，但这只是开始。')
pdf.bullet('2025-2030：钙钛矿光伏突破+固态电池量产，光伏+储能平替化石能源')
pdf.bullet('2030-2040：核聚变从实验到并网发电，能源成本趋近于零')
pdf.bullet('2040-2050：充裕能源重塑制造业（海水淡化、垂直农业、直接空气碳捕获）')
pdf.bullet('投资启示：每一轮能源革命都催生了新的基础设施巨头——从标准石油到埃克森到NextEra，30年的赢家往往不是能源生产商，而是能源技术平台')

# ================================================================
# PART 6: 结语
# ================================================================
pdf.ch_title('六、结语：成为长现投资者')

pdf.body('Long Now框架的核心不是预测未来，而是建立一个能够容纳未来的思维结构。')

pdf.body('30年后回看今天：')

pdf.bullet('那些选择了"等待确认再入场"的人，会发现等待本身就是成本——因为技术不会等人')
pdf.bullet('那些追求"完美时机"的人，会发现完美的时机不存在——只有"足够早"和"太晚"之分')
pdf.bullet('那些在不确定性面前退缩的人，会发现不确定性是最大的进入壁垒——也是最大的回报来源')

pdf.body('成为"长现投资者"意味着：')

pdf.body('你用30年的尺度做今天的决定。你不追求明天的涨停，而是追求30年后你的决策被证明是明智的。你的认知框架不是一个可以随时丢弃的工具，而是一个需要终身打磨的思维习惯。')

pdf.gold_bar()

pdf.set_font('H', '', 11)
pdf.set_text_color(0x0D, 0x23, 0x4B)
pdf.multi_cell(pdf.w - 2 * pdf.m, 7,
               'Long Now 长现\n'
               '以30年为尺度，做今天的科技金融决策',
               align='C')
pdf.ln(3)
pdf.set_font('S', '', 9)
pdf.set_text_color(0x88, 0x99, 0xAA)
pdf.multi_cell(pdf.w - 2 * pdf.m, 5.5,
               '邮储银行上海分行科技金融事业部  |  2026年5月\n'
               '思考框架  |  内部参考  |  欢迎交流',
               align='C')

pdf.page_num()

# Save
import os
OUTPUT_DIR = '/Users/cyingfang/WorkBuddy/20260429082054'
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT = os.path.join(OUTPUT_DIR, 'LongNow_长现投资框架.pdf')
pdf.output(OUTPUT)
print(f'Saved: {OUTPUT} | Pages: {pdf.page_no()}')
