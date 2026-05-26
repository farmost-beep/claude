#!/usr/bin/env python3
"""科技金融投资框架 PDF — 哲学深度 × 方法论 × 公开演讲"""

from fpdf import FPDF

SONGTI = '/System/Library/Fonts/Supplemental/Songti.ttc'
HEITI = '/System/Library/Fonts/STHeiti Medium.ttc'
FZS = '/System/Library/Fonts/Supplemental/Songti.ttc'

class PDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.add_font('S', '', SONGTI)
        self.add_font('H', '', HEITI)
        self.set_auto_page_break(True, 22)
        self.m = 24
        self.w = 210

    def title_page(self, main, sub=''):
        self.add_page()
        self.set_fill_color(0x0D, 0x23, 0x4B)
        self.rect(0, 0, self.w, self.h, 'F')
        self.ln(40)
        self.set_font('H', '', 32); self.set_text_color(0xFF, 0xFF, 0xFF)
        self.multi_cell(self.w - 2 * self.m, 14, main, align='C')
        if sub:
            self.ln(8); self.set_font('S', '', 13); self.set_text_color(0xC9, 0xA8, 0x4C)
            self.multi_cell(self.w - 2 * self.m, 8, sub, align='C')
        self.ln(20)
        self.set_draw_color(0xC9, 0xA8, 0x4C); self.set_line_width(0.6)
        cx = self.w / 2; self.line(cx - 30, self.get_y(), cx + 30, self.get_y())
        self.ln(12)
        self.set_font('S', '', 10); self.set_text_color(0x88, 0x99, 0xAA)
        self.multi_cell(self.w - 2 * self.m, 7,
            '邮储银行上海分行科技金融事业部\n2026年5月  |  内部研讨  |  请勿对外传播', align='C')

    def divider(self):
        """纯色隔页"""
        self.add_page()
        self.set_fill_color(0x0D, 0x23, 0x4B)
        self.rect(0, 0, self.w, self.h, 'F')

    def div_text(self, big, small=''):
        self.divider()
        self.ln(60)
        self.set_font('H', '', 28); self.set_text_color(0xFF, 0xFF, 0xFF)
        self.multi_cell(self.w - 2 * self.m, 14, big, align='C')
        if small:
            self.ln(8); self.set_font('S', '', 11); self.set_text_color(0xC9, 0xA8, 0x4C)
            self.multi_cell(self.w - 2 * self.m, 7, small, align='C')

    def ch_title(self, t):
        self.ln(2)
        self.set_font('H', '', 20); self.set_text_color(0x0D, 0x23, 0x4B)
        self.set_x(self.m); self.multi_cell(self.w - 2 * self.m, 10, t); self.ln(6)
        self.set_draw_color(0x0D, 0x23, 0x4B); self.set_line_width(0.8)
        self.line(self.m, self.get_y() - 2, self.m + 50, self.get_y() - 2); self.ln(8)

    def sub_title(self, t):
        self.set_font('H', '', 14); self.set_text_color(0x00, 0x6D, 0xBA)
        self.set_x(self.m); self.cell(self.w - 2 * self.m, 8, t); self.ln(10)

    def sub_sub(self, t):
        self.set_font('H', '', 11); self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m); self.cell(self.w - 2 * self.m, 7, t); self.ln(8)

    def body(self, t):
        self.set_font('S', '', 10.5); self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m)
        self.multi_cell(self.w - 2 * self.m, 6.5, t, align='J'); self.ln(2)

    def body_q(self, t):
        """引文/名言样式"""
        self.set_fill_color(0xF0, 0xF4, 0xF8)
        self.set_font('S', '', 10); self.set_text_color(0x00, 0x55, 0x99)
        x0 = self.get_x(); y0 = self.get_y()
        self.set_x(self.m + 6)
        self.multi_cell(self.w - 2 * self.m - 12, 6, t, align='J')
        ny = self.get_y()
        self.rect(self.m + 2, y0 - 1, self.w - 2 * self.m - 4, ny - y0 + 2)
        self.set_y(ny + 3)

    def bullet(self, t):
        self.set_font('S', '', 10.5); self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m + 4); w = self.w - 2 * self.m - 10
        self.cell(5, 6.5, chr(8226))
        self.multi_cell(w, 6.5, t, align='J')
        self.set_x(self.m); self.ln(0.5)

    def bullet_sub(self, t):
        self.set_font('S', '', 9.5); self.set_text_color(0x55, 0x66, 0x77)
        self.set_x(self.m + 12); w = self.w - 2 * self.m - 18
        self.cell(5, 6, '-')
        self.multi_cell(w, 6, t, align='J')
        self.set_x(self.m); self.ln(0.3)

    def gold_bar(self):
        self.set_draw_color(0xC9, 0xA8, 0x4C); self.set_line_width(0.4)
        y = self.get_y(); self.line(self.m, y, self.w - self.m, y); self.ln(4)

    def key_insight(self, t):
        """关键洞察框"""
        self.set_fill_color(0x0D, 0x23, 0x4B)
        self.set_text_color(0xFF, 0xFF, 0xFF)
        self.set_font('S', '', 10)
        y0 = self.get_y()
        self.set_x(self.m + 4)
        self.multi_cell(self.w - 2 * self.m - 8, 6.5, t, align='J')
        ny = self.get_y()
        self.rect(self.m, y0 - 2, self.w - 2 * self.m, ny - y0 + 3, 'F')
        self.set_text_color(0x33, 0x33, 0x33)
        self.set_y(ny + 4)

    def page_num(self):
        self.set_font('S', '', 8); self.set_text_color(0xAA, 0xAA, 0xAA)
        self.set_y(-15); self.cell(self.w - 2 * self.m, 5, str(self.page_no()), align='R')


pdf = PDF(); pdf.set_margin(24)

# ===== COVER =====
pdf.title_page(
    '科技金融投资框架',
    'Philosophy · Methodology · Practice\n' + '道 · 法 · 术 · 势')

# ================================================================
# 前言
pdf.add_page()
pdf.ch_title('前言：为什么需要一套框架？')

pdf.body('科技金融正在成为中国金融体系中最具活力的增长极。从科创板设立到"科技金融"被写入中央金融工作会议成为五篇大文章之一，从银行科技金融事业部的遍地开花到万亿级科技贷款的爆发式增长——我们正在见证一场深刻的金融范式变革。')
pdf.body('然而，热潮之下隐含着巨大的认知鸿沟：大多数金融机构仍然用传统信贷思维评估科技企业，大多数科技企业并不真正理解金融的逻辑。这套框架的使命，就是在"科技的复杂性"与"金融的确定性追求"之间，架起一座可沟通、可执行、可复盘的桥梁。')
pdf.body('本框架的编写遵循三个原则：')
pdf.bullet('哲学深度——任何没有哲学根基的方法论都是空中楼阁。我们追溯科技金融的思想源头，从熊彼特的创新理论到复杂性科学，从王阳明的"知行合一"到凯文·凯利的"涌现"逻辑。')
pdf.bullet('方法论可操作——每一条原则都必须能够转化为具体的评估维度和决策标准，能够经得起"所以呢？"的追问。')
pdf.bullet('适合公开演讲——框架的核心概念用隐喻和格言式表达，便于口耳相传。框架的结构按照"道·法·术·势"的中国古典思维框架展开，既符合东方听众的认知习惯，又具有国际通行的逻辑严谨性。')
pdf.ln(2)
pdf.body_q('"任何足够先进的技术，初看都与魔法无异。"\n—— 阿瑟·C·克拉克\n\n"金融的第一性原理不是风险，而是信任；科技的第一性原理不是效率，而是可能。"\n—— 本文框架核心理念')

pdf.page_num()

# ================================================================
pdf.div_text('第一篇', '道 · 哲学根基')

pdf.add_page()
pdf.ch_title('一、创新的本体论：科技金融的思想源头')

pdf.sub_title('1.1 熊彼特：创新是经济演化的内生动力')
pdf.body('1912年，约瑟夫·熊彼特在《经济发展理论》中提出了一个石破天惊的观点：经济发展的根本动力不是资本积累，而是创新。创新不是外生于经济系统的偶然事件，而是内生于企业家精神的核心动力。')
pdf.body('熊彼特将创新分为五种类型：新产品、新生产方式、新市场、新原料来源、新产业组织。这五种创新形式的演进，构成了经济周期的根本驱动力。而金融系统在其中的角色——用熊彼特的原话说——是"为创新提供购买力"。')
pdf.body('科技金融的第一原理由此诞生：')
pdf.body_q('"金融的功能不是分配已有的资源，而是创造新的购买力，使其流向创新活动。"')

pdf.sub_title('1.2 卡洛塔·佩雷斯：技术-经济范式')
pdf.body('委内瑞拉演化经济学家卡洛塔·佩雷斯在《技术革命与金融资本》中提出了一个更为精巧的理论：每一次技术革命都伴随着金融资本的狂热涌入，形成"技术-金融泡沫- crash- 生产资本接管"的周期循环。')
pdf.body('佩雷斯的框架解释了为什么每一次技术革命（蒸汽机、电力、信息技术、AI）都经历了金融资本的"野蛮进入"阶段——因为新技术的不确定性太高，只有风险偏好极高的金融资本才愿意为其下注。而随着技术成熟，生产资本（企业、银行等传统金融机构）逐步接管。')
pdf.ln(2)
pdf.body('这一框架对科技金融投资的启示：')
pdf.bullet('精准定位技术所处的范式阶段——是"导入期"（金融资本主导）还是"展开期"（生产资本主导）')
pdf.bullet('不同阶段的金融工具选择截然不同——早期需要股权资本，中后期需要债权资本')
pdf.bullet('银行在科技金融中的最佳角色是"展开期"的推手——在技术确定性足够高时以低成本资金加速其扩散')

pdf.sub_title('1.3 复杂性科学与涌现逻辑')
pdf.body('如果说熊彼特和佩雷斯解释的是宏观的历史规律，那么复杂性科学为我们提供了微观的创新发生机制。圣塔菲学派的布莱恩·阿瑟在《技术的本质》中指出：技术不是科学的应用，而是从已有技术的组合中"涌现"出来的。')
pdf.body('这意味着：')
pdf.bullet('创新具有不可预测性——它来自已有技术元素的重新组合，但"哪些组合会成功"无法提前预测')
pdf.bullet('生态位比个体更重要——一个创新的成功不仅取决于技术本身，更取决于它嵌入的生态系统')
pdf.bullet('投资的本质不是预测，而是构建策略性地支持多种可能组合的"投资组合"')
pdf.gold_bar()
pdf.body_q('核心启示：科技金融投资的本质不是挑选赢家，而是构建一套能够包容多种技术路径、适应不同范式阶段的"元策略"。赢家不是预测出来的，是在多元选择中涌现出来的。')

pdf.page_num()

# ================================================================
pdf.add_page()
pdf.ch_title('二、科技与金融的辩证关系')

pdf.sub_title('2.1 科技需要金融的三个理由')
pdf.bullet('时间跨度不对称——技术从研发到商业化的周期（5-15年）远超传统金融工具的期限结构（1-5年），需要"耐心资本"')
pdf.bullet('不确定性溢价——技术路线的成败概率分布不是正态的，而是幂律分布的（少数胜出、多数淘汰），需要能容忍失败的风险偏好')
pdf.bullet('正外部性——技术创新的社会收益远大于私人收益，需要政策性金融工具的介入以弥补私人投资的不足')
pdf.ln(2)

pdf.sub_title('2.2 金融需要科技的三个理由')
pdf.bullet('效率革命——AI、大数据、区块链等技术正在重塑金融基础设施，从智能风控到自动化交易，从数字人民币到分布式账本')
pdf.bullet('资产边界拓展——科技企业（尤其是硬科技企业）创造了全新的资产类别：知识产权、数据资产、算法资产、生态资产')
pdf.bullet('利率下行时代的回报来源——在全球利率中枢下移的大背景下，科技投资成为金融机构维持收益率的重要来源')
pdf.ln(2)

pdf.sub_title('2.3 核心张力与统一')
pdf.body('科技与金融之间存在一种深刻的紧张关系：')
pdf.body_q('科技的逻辑是"可能"——\n它问的是"如果......会怎样？"，追求突破边界，容忍失败，拥抱不确定性。\n\n金融的逻辑是"确定"——\n它问的是"概率多大？风险几何？"，追求可预测性，厌恶损失，需要确定性。')
pdf.body('好的科技金融框架，不是粉饰这种张力，而是设计一套机制让两者在张力中协同进化。这需要三个条件：')
pdf.bullet('翻译机制——将技术的"可能性语言"翻译为金融的"概率语言"')
pdf.bullet('时间匹配——以技术周期重构金融产品的期限结构')
pdf.bullet('风险分层——将技术的不确定性分解为可定价、可管理、可承担的不同风险层级')

pdf.gold_bar()
pdf.body_q('框架的核心命题：科技金融不是让金融变得更冒险，而是让金融更精确地理解技术的"不确定性分布"，从而做出更理性的资源配置决策。')

pdf.page_num()

# ================================================================
pdf.add_page()
pdf.ch_title('三、东方智慧与科技金融')

pdf.sub_title('3.1 老子"道法自然"与创新的自然演化')
pdf.body('《道德经》云："人法地，地法天，天法道，道法自然。"创新的发生和扩散，并非人为设计的结果，而是一个自组织、自演化的过程。正如生物进化不需要一个"总设计师"，技术进步也是无数试错、选择和组合的自然结果。')
pdf.body('这一思想对科技金融投资的启示：')
pdf.bullet('不要试图"制造"创新——真正的创新无法被计划出来，但可以被生态系统孕育出来')
pdf.bullet('投资于生态系统而非单一技术——一个健康的科技生态系统比任何单一技术都更有生命力')
pdf.bullet('耐心是最稀缺的素质——"道法自然"意味着尊重创新的自然时间节奏，不拔苗助长')

pdf.sub_title('3.2 王阳明"知行合一"与投后赋能')
pdf.body('王阳明提出"知是行之始，行是知之成"，"知行合一"的核心是认知与行动不可分割。科技金融投资中，最深刻的认知往往来自投资后的实践——只有深度参与了企业的发展，才能真正理解技术的价值和风险。')
pdf.body('这解释了为什么最成功的科技金融投资机构都在追求：')
pdf.bullet('不仅是资金的提供者，更是认知的提供者')
pdf.bullet('投后管理不是"监控风险"，而是"共同成长"')
pdf.bullet('真正理解一个行业的标准不是读过多少报告，而是深度参与过多少案例')

pdf.sub_title('3.3 "势"的智慧：顺势而为的哲学')
pdf.body('《孙子兵法》的核心思想是"善战者，求之于势"。在中国科技金融语境中，"势"是技术浪潮的方向和力度。顺势而为的核心理念是：')
pdf.bullet('识别势——理解技术演进的大方向（AI、新能源、生物科技）')
pdf.bullet('判断势的力度——区分"真势"（有坚实基础的技术浪潮）和"伪势"（概念炒作）')
pdf.bullet('在势的拐点重注——当一个技术从"实验室奇观"走向"可规模化应用"的拐点出现时，是下注的最佳时机')

pdf.gold_bar()
pdf.body_q("框架的方法论根源：‘道法自然’确保我们尊重创新的自组织规律；‘知行合一’确保我们深度参与、边干边学；‘顺势而为’确保我们抓住浪潮的拐点。这三者构成了科技金融投资的一个完整的中国哲学框架。")

pdf.page_num()

# ================================================================
pdf.div_text('第二篇', '法 · 核心方法论')

pdf.add_page()
pdf.ch_title('四、三维评估模型：TBP框架')

pdf.body('评估一家科技企业的核心框架，可以浓缩为三个维度：技术（Technology）、商业（Business）、人（People）。三者缺一不可，且相互影响。')

pdf.sub_title('4.1 技术维度（T）——技术的真实深度')
pdf.bullet('技术壁垒：是否具备可保护的、难以复制的核心技术？专利数量和质量？')
pdf.bullet('技术成熟度：TRL（技术就绪水平）评估——处于实验室/原型/Pilot/规模化哪个阶段？')
pdf.bullet('技术路线图：3-5年的技术演进路径是否清晰？迭代速度如何？')
pdf.bullet('替代风险：是否存在替代技术路线的可能性？')
pdf.bullet('可组合性：该技术能否与其他技术组合产生新的价值？')
pdf.ln(1)

pdf.sub_title('4.2 商业维度（B）——商业化路径')
pdf.bullet('市场空间：TAM（总可寻址市场）有多大？中国市场vs全球市场？')
pdf.bullet('商业模式：SaaS/项目制/硬件/平台/交易抽成？模式的可扩展性？')
pdf.bullet('客户验证：是否有付费客户？客户获取成本与生命周期价值（CAC/LTV）？')
pdf.bullet('竞争格局：波特五力分析——供应商、买家、替代品、新进入者、现有竞争')
pdf.bullet('单位经济：毛利率、客单价、复购率、净收入留存率（NRR）')
pdf.ln(1)

pdf.sub_title('4.3 人维度（P）——创始人与团队')
pdf.bullet('创始人的认知深度：对行业的理解是否超越常人的"第一性原理"级别？')
pdf.bullet('创始人的学习速度：是否有快速迭代认知的能力？')
pdf.bullet('团队的完整性：技术+市场+运营的核心三角是否健全？')
pdf.bullet('价值观与使命感：是"做一门生意"还是"解决一个真问题"？')
pdf.bullet('团队的应变能力：面对失败时的反应——是反思迭代还是推诿放弃？')
pdf.ln(4)

pdf.body_q('TBP框架的使用原则：三个维度都需要达到及格线，但总有一个维度是"决胜因素"。\n种子/天使阶段：P > T > B（人最关键）\nA/B轮阶段：T ≈ P > B（技术和人并重）\nC轮及以后：B > T > P（商业模式验证成为核心）')

pdf.page_num()

# ================================================================
pdf.add_page()
pdf.ch_title('五、技术成熟度与金融适配矩阵')

pdf.body('不同类型金融机构需要在技术不同成熟度阶段进入。以下矩阵展示了各种金融工具与技术成熟度的适配关系：')

# Draw the matrix as a table using manual drawing
items = [
    ['技术阶段', '典型时间', '适合的金融工具', '典型机构类型', '风险特征'],
    ['种子/概念', '0-2年', '种子基金/天使投资/政府补贴', '天使投资人/政府引导基金', '极高（95%+失败率）'],
    ['原型验证', '1-3年', '风险投资/A轮/Grants', 'VC/产业资本', '很高（80%+失败率）'],
    ['产品化', '2-5年', '风险投资B/C轮/银行科创贷', 'VC/PE/银行科技金融', '高（50-70%失败率）'],
    ['规模化', '3-7年', 'PE/银行授信/供应链金融/债券', 'PE/商业银行/投行', '中（20-40%失败率）'],
    ['成熟期', '5-10年', 'IPO/并购/银团贷款', '投行/商业银行/公开市场', '低（接近传统企业）'],
]

for r in items:
    pdf.set_font('H', '', 9) if r == items[0] else pdf.set_font('S', '', 8.5)
    pdf.set_fill_color(0x0D, 0x23, 0x4B) if r == items[0] else (
        pdf.set_fill_color(0xF0, 0xF4, 0xF8) if items.index(r) % 2 == 0 else pdf.set_fill_color(0xFF, 0xFF, 0xFF))
    pdf.set_text_color(0xFF, 0xFF, 0xFF) if r == items[0] else pdf.set_text_color(0x33, 0x33, 0x33)
    pdf.set_x(pdf.m)
    widths = [28, 18, 58, 48, 30]
    for j, w in enumerate(widths):
        pdf.cell(w, 6.5, r[j], border=1, fill=True)
    pdf.ln()
pdf.ln(4)

pdf.body_q('核心洞察：商业银行在科技金融中的最佳进入时点是"产品化→规模化"阶段。过早进入风险不可控，过晚进入则失去差异化竞争优势。邮储银行应重点布局C轮以后到Pre-IPO阶段的科技企业。')

pdf.sub_title('5.1 科技企业生命周期融资策略')
pdf.body('种子期（0-500万）：政策性扶持资金+天使投资。银行角色：做资源对接，不做资金投放。')
pdf.body('初创期（500万-5000万）：风险投资为主。银行角色：开立基本账户、提供结算服务，积累合作基础。')
pdf.body('成长期（5000万-5亿）：风险投资+银行科创贷+供应链金融。银行角色：以"投贷联动"模式介入，配合VC提供债权融资。')
pdf.body('扩张期（5亿-50亿）：银行综合授信+债券承销+并购贷款。银行角色：主办银行，全方位金融服务。')
pdf.body('成熟期（50亿+）：IPO/并购/银团。银行角色：资本市场服务商+战略合作伙伴。')

pdf.page_num()

# ================================================================
pdf.add_page()
pdf.ch_title('六、逆周期布局理论')

pdf.body('科技金融最大的陷阱是"追涨杀跌"——在技术泡沫的高峰最乐观，在技术寒冬的低谷最悲观。逆向思维是科技金融投资中最稀缺的能力。')

pdf.sub_title('6.1 科技投资的心理周期')
pdf.body('科技投资面临一个典型的情感曲线：')
pdf.bullet('技术突破期：媒体兴奋，专业投资者入场')
pdf.bullet('期望膨胀期：全民狂欢，大量资本涌入')
pdf.bullet('泡沫破裂期：技术未达预期，资本快速撤离')
pdf.bullet('复苏耕耘期：幸存者默默打磨产品和技术')
pdf.bullet('生产力高原期：技术真正嵌入产业，开始产生巨大价值')
pdf.ln(1)
pdf.body_q('格雷厄姆《聪明的投资者》中"市场先生"的寓言：市场先生每天来敲门报价——有时候价格远高于价值（泡沫期），有时候远低于价值（寒冬期）。你的工作不是跟随市场先生，而是利用他的非理性。')

pdf.sub_title('6.2 逆周期布局的三大原则')
pdf.bullet('第一原则：在"失望之谷"布局——当市场对某一技术领域极度悲观时（如AI在2018-2022年的"AI寒冬"），正是系统性布局的最佳时机')
pdf.bullet('第二原则：用时间换空间——逆周期布局需要忍受3-5年的"潜伏期"，在泡沫再次来临之前完成技术和商业模式验证')
pdf.bullet('第三原则：逆周期性投资需要顺周期性管理——在市场低点投资，在市场高点优化组合')

pdf.sub_title('6.3 邮储的机会窗口')
pdf.body('当前（2026年），中国科技金融正处于一个结构性机会窗口：')
pdf.bullet('科创板制度红利持续释放，退出渠道畅通')
pdf.bullet('AI（尤其是AI Agent和人形机器人）刚从概念炒作步入产业化初期')
pdf.bullet('国有大行纷纷设立科技金融事业部，但差异化策略尚未形成')
pdf.bullet('资本市场估值回归理性，部分优质科技企业估值处于合理区间')
pdf.bullet('逆周期布局不仅有财务回报，更有政策和社会价值')

pdf.gold_bar()
pdf.body_q('核心判断：2026-2027年是中国科技金融的"播种期"。\n邮储银行若能在这个窗口建立起系统化的科技金融投资能力，\n2028-2030年将收获一个结构性的增长曲线。')

pdf.page_num()

# ================================================================
pdf.add_page()
pdf.ch_title('七、生态位理论')

pdf.sub_title('7.1 为什么银行需要"生态位"思维？')
pdf.body('在生物进化中，两个物种如果生态位完全重叠，最终只有一个能存活（竞争排除原理）。在科技金融领域，商业银行需要找到自己的"生态位"——一个既能发挥自身核心优势，又与其他金融机构形成互补而非零和竞争的位置。')

pdf.sub_title('7.2 商业银行的独特优势')
pdf.bullet('资金成本优势——存款成本行业最低，可提供其他机构无法竞争的低成本资金')
pdf.bullet('网络效应——近4万网点、覆盖全国99%县市，企业触达能力无可匹敌')
pdf.bullet('信用背书——国有大行的品牌信用为企业提供"信用溢价"')
pdf.bullet('综合服务能力——对公+零售+投行+跨境，一站式解决企业全生命周期需求')
pdf.bullet('政策资源——作为国有大行，在政策性金融工具（科创再贷款、担保基金）方面有先发优势')

pdf.sub_title('7.3 邮储银行科技金融的差异化定位')
pdf.body('基于以上分析，邮储银行在科技金融生态中的最佳生态位是：')
pdf.body_q("“科技企业的'S型曲线'加速器”——重点关注度过技术死亡谷、\n进入S型曲线快速爬升阶段的科技企业，\n以低成本资金和综合金融服务加速其成长。")
pdf.body('这一定位的差异化优势：')
pdf.bullet('不与天使/VC在早期阶段竞争——那是他们的生态位')
pdf.bullet('不与PE在Pre-IPO阶段竞争——那是投行的生态位')
pdf.bullet('聚焦"成长期到扩张期"——这个阶段技术确定性已较高、企业最需要规模化的资金支持、且银行可以发挥资金成本优势')
pdf.bullet('以"科技金融生态合作伙伴"而非"放贷者"的身份定位——提供的不只是资金，而是完整的金融+科技生态服务')

pdf.gold_bar()
pdf.body_q('邮储银行科技金融的使命：\n让技术穿越"死亡之谷"，让创新更快地抵达产业高原。')

pdf.page_num()

# ================================================================
pdf.div_text('第三篇', '术 · 实践框架')

pdf.add_page()
pdf.ch_title('八、科技企业风险评估框架')

pdf.body('科技企业的风险评估无法套用传统工商企业模板。传统企业评估关注的是"过去"（历史财务数据），而科技企业评估关注的是"未来"（技术潜力和市场空间）。')

pdf.sub_title('8.1 三维风险评估模型')
pdf.body('技术风险：技术路线是否可行？被替代的概率多大？')
pdf.bullet('技术路线图是否清晰且有据可查')
pdf.bullet('核心团队的技术背景和行业积累')
pdf.bullet('知识产权布局的深度和广度')
pdf.bullet('技术迭代速度和能力')
pdf.ln(1)

pdf.body('市场风险：市场规模是否真实？商业化路径是否可行？')
pdf.bullet('TAM/SAM/SOM的分析是否扎实')
pdf.bullet('是否已获得付费客户/种子用户')
pdf.bullet('客户获取成本是否合理')
pdf.bullet('市场增长动力的可持续性')
pdf.ln(1)

pdf.body('信用风险：还款意愿和还款能力如何？')
pdf.bullet('实控人个人征信和历史信用记录')
pdf.bullet('企业资产质量和流动性状况')
pdf.bullet('第二还款来源的可靠性')
pdf.bullet('交叉验证信息：纳税、社保、水电、银行流水')
pdf.ln(4)

pdf.sub_title('8.2 科技企业信用评估的"5+1"模型')
pdf.body('在传统"5C"信用评估模型（Character/能力、Capacity/还款能力、Capital/资本、Collateral/担保、Condition/条件）基础上，增加一个科技企业的核心维度：')
pdf.body_q('第6个C——Capability（技术能力）：\n企业的核心技术是否具有可保护、可扩展、可商业化的特征？\n专利质量、研发密度、技术团队的深度和厚度。')

pdf.page_num()

# ================================================================
pdf.add_page()
pdf.ch_title('九、公开演讲与沟通框架')

pdf.body('以下内容专为公开演讲场合设计。框架的核心概念用隐喻和格言形式呈现，便于口耳相传和PPT展示。')

pdf.sub_title('9.1 开场白框架：三个问题')
pdf.body('在科技金融的任何演讲中，可以先问三个问题引发思考：')
pdf.body('第一个问题：为什么中国最赚钱的银行和中国最具创新力的科技企业之间，仍然隔着一堵看不见的墙？')
pdf.body('第二个问题：为什么我们愿意为一家还没有盈利的科技企业提供数十亿贷款，却无法用一句话说清楚它的核心价值？')
pdf.body('第三个问题：如果30年后回看今天，哪些今天看起来"不合理"的决定，会被证明是明智的？')

pdf.sub_title('9.2 核心隐喻体系')
pdf.body('"科学家种下种子，企业家浇灌它，金融加速它生长。"')
pdf.body('——这不是一个浪漫的比喻，而是一个精确的功能分工。')
pdf.ln(2)
pdf.body('"科技金融不是让金融变得更冒险，而是让金融更精确。"')
pdf.body('——区分"未知的未知"和"已知的未知"。')
pdf.ln(2)
pdf.body('"投资的本质不是穿越迷雾，而是知道哪条路值得在迷雾中前行。"')
pdf.body('——TBP框架解决的就是"值得"的判断问题。')
pdf.ln(2)
pdf.body("技术的逻辑是'可能'，金融的逻辑是'确定'。好的科技金融框架，是在'可能'和'确定'之间架一座桥。")
pdf.body('——框架解决的就是这个"翻译"问题。')

pdf.sub_title('9.3 演讲结构模板（30分钟版本）')
pdf.bullet('0-3分钟：开场故事或数据震撼（用一个具体案例抓住注意力）')
pdf.bullet('3-8分钟：为什么需要一套框架？（三个问题引发思考）')
pdf.bullet('8-18分钟：核心框架介绍——道·法·术·势')
pdf.bullet('18-25分钟：实战案例——用框架分析一个具体科技企业')
pdf.bullet('25-28分钟：反问互动——邀请听众用自己的经验检验框架')
pdf.bullet('28-30分钟：收尾——回到核心隐喻+金句+行动号召')

pdf.gold_bar()

pdf.page_num()

# ================================================================
pdf.add_page()
pdf.ch_title('十、经典案例：用框架复盘')

pdf.sub_title('案例一：宁德时代（300750.SZ）')
pdf.body('2011年成立，2018年上市。从一家脱胎于ATL的电池公司，成长为中国"新三样"出口龙头、全球动力电池第一。用TBP框架复盘：')
pdf.body('T（技术）：三元锂+磷酸铁锂双技术路线布局，CTP/麒麟电池持续领先，专利壁垒深厚。')
pdf.body('B（商业）：抓住中国新能源汽车政策红利期，绑定宝马等头部车企，从B端合约走向全球布局。')
pdf.body('P（人）：曾毓群"赌性更坚强"的决策风格（在技术路线不确定时敢下重注）+ 香港科学家+工程文化的组合。')
pdf.body('复盘：宁德时代的成功本质上是T+B+P三个维度同时在"势"的拐点达到共振。2015-2017年（成长期）是银行介入的最佳窗口期。')
pdf.ln(2)

pdf.sub_title('案例二：科大讯飞（002230.SZ）')
pdf.body('1999年成立，2008年上市。中国AI语音龙头。')
pdf.body('T（技术）：语音识别技术全球领先，但技术壁垒的护城河深度有限（后来者追赶上较快）。')
pdf.body('B（商业）：to G/to B为主要商业模式，增长稳健但毛利率不及纯软件公司。')
pdf.body('P（人）：刘庆峰以技术理想主义著称，团队学术底蕴深厚。')
pdf.body('复盘：TBP三个维度中B维度始终是短板（商业化效率不足），导致股价波动较大。银行授信应以政府项目回款作为核心还款来源。')
pdf.ln(2)

pdf.sub_title('案例三：商汤科技（0020.HK）')
pdf.body('2014年成立，2021年港股上市。')
pdf.body('T（技术）：计算机视觉技术全球前列，SenseCore大装置构建AI基础设施。')
pdf.body('B（商业）：营收增长快但亏损巨大，商业化路径不够清晰，to G占比过高。')
pdf.body('P（人）：汤晓鸥学术泰斗+徐立商业执行力的组合，但在2023年汤晓鸥离世后团队稳定性受到考验。')
pdf.body('复盘：P维度的突然恶化（核心人物离世）和B维度的长期不确定性（变现路径不清晰）叠加，导致投资价值大幅下降。警示：科技投资中P维度的"关键人风险"需要特别关注。')
pdf.gold_bar()
pdf.body_q('三个案例的共性启示：\n最好的科技投资机会是"T+B+P三维共振+势的拐点"同时出现。\n最危险的投资是"T很强但B很弱(P有不确定性)"——技术浪漫主义最容易导致投资失误。')

pdf.page_num()

# ================================================================
pdf.div_text('第四篇', '势 · 趋势与远见')

pdf.add_page()
pdf.ch_title('十一、2026-2030年科技金融趋势展望')

pdf.sub_title('11.1 六大确定性趋势')
pdf.bullet('AI产业化的"iPhone时刻"过去，现在是"App Store时刻"——基础设施已就绪，应用层爆发刚刚开始')
pdf.bullet('硬科技国产替代从"能做"到"好用"——半导体、操作系统、工业软件进入替代深水区')
pdf.bullet('科技企业的金融需求从"单一融资"到"综合金融"——从拿贷款到上市/并购/出海的全周期服务')
pdf.bullet('银行的科技金融从"职能部门"到"核心战略"——从事业部独立到全行级科技金融战略')
pdf.bullet('数据要素资产的金融化——数据资产入表、数据质押融资、数据信托等新金融形态将涌现')
pdf.bullet('ESG与科技金融的融合——绿色科技投资将成为科技金融的重要增长极')

pdf.sub_title('11.2 邮储银行科技金融的战略建议')
pdf.bullet('短期（2026-2027）：聚焦AI+半导体+新能源三大赛道，建立行业专长和品牌认知')
pdf.bullet('中期（2027-2029）：构建"投贷债租保"五位一体的科技金融产品体系，打造科技金融的生态平台')
pdf.bullet('长期（2029-2030）：从资金提供者进化为科技企业的"战略合伙人"，实现从FPA到战略价值的跨越')

pdf.gold_bar()

# ===== 结语 =====
pdf.ln(4)
pdf.ch_title('结语：回到起点')

pdf.body('让我们回到最初的三个问题：')
pdf.body('为什么中国最赚钱的银行和中国最具创新力的科技企业之间，仍然隔着一堵看不见的墙？——因为这堵墙不是砖瓦砌成的，而是认知差异筑就的。拆掉这堵墙的工具，不是更多的钱，而是更好的框架。')
pdf.body('为什么我们愿意为一家还没有盈利的科技企业提供数十亿贷款，却无法用一句话说清楚它的核心价值？——因为我们习惯于用"过去"为资产定价，而科技企业的价值存在于"未来"。TBP框架试图提供一种新的语言，让我们能够更精确地描述这个"未来"。')
pdf.body('如果30年后回看今天，哪些今天看起来"不合理"的决定，会被证明是明智的？——我们不知道答案，但我们可以确定的是：那些在"确定"和"可能"之间找到平衡的人，在"泡沫"和"寒冬"之间保持定力的人，在"短期"和"长期"之间选择忍耐的人——他们的决定，会被时间证明。')

pdf.ln(4)
pdf.body_q('科技金融不是一个产品，而是一种世界观。')
pdf.ln(1)
pdf.page_num()
pdf.set_font('S', '', 9); pdf.set_text_color(0x88, 0x99, 0xAA)
pdf.multi_cell(pdf.w - 2 * pdf.m, 6,
    '邮储银行上海分行科技金融事业部  |  2026年5月\n'
    '框架版本 1.0  |  内部研讨材料  |  请勿对外传播\n'
    '参考文献：熊彼特《经济发展理论》、佩雷斯《技术革命与金融资本》、\n'
    '阿瑟《技术的本质》、孙子《孙子兵法》、王阳明《传习录》', align='C')

import os
OUTPUT = '/Users/cyingfang/WorkBuddy/20260429082054/科技金融投资框架.pdf'
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
pdf.output(OUTPUT)
print(f'Saved: {OUTPUT} | Pages: {pdf.page_no()}')
