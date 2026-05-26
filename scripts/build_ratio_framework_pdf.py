#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""长现·理性 —— 以西方思想重述长现投资框架 PDF"""

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
        self.set_fill_color(0x1B, 0x2A, 0x4A)
        self.rect(0, 0, self.w, 297, 'F')
        # Decorative top rule
        self.set_draw_color(0xC9, 0xA8, 0x4C)
        self.set_line_width(0.3)
        self.line(30, 55, self.w - 30, 55)
        self.ln(28)
        self.set_font('S', '', 9)
        self.set_text_color(0xC9, 0xA8, 0x4C)
        self.multi_cell(self.w - 2 * self.m, 7, 'RATIO  ·  LONG NOW', align='C')
        self.ln(6)
        self.set_font('H', '', 30)
        self.set_text_color(0xFF, 0xFF, 0xFF)
        self.multi_cell(self.w - 2 * self.m, 13, main, align='C')
        self.ln(4)
        self.set_font('S', '', 12)
        self.set_text_color(0xCC, 0xCC, 0xDD)
        self.multi_cell(self.w - 2 * self.m, 7, sub, align='C')
        self.ln(3)
        self.set_draw_color(0xC9, 0xA8, 0x4C)
        self.set_line_width(0.5)
        cx = self.w / 2
        self.line(cx - 18, self.get_y(), cx + 18, self.get_y())
        self.ln(5)
        self.set_font('S', '', 9)
        self.set_text_color(0x88, 0x99, 0xAA)
        self.multi_cell(self.w - 2 * self.m, 6, sub2, align='C')

    def ch_title(self, t):
        self.add_page()
        self.set_font('H', '', 17)
        self.set_text_color(0x1B, 0x2A, 0x4A)
        self.set_x(self.m)
        self.cell(self.w - 2 * self.m, 10, t)
        self.ln(12)
        self.set_draw_color(0xC9, 0xA8, 0x4C)
        self.set_line_width(0.4)
        self.line(self.m, self.get_y() - 3, self.m + 35, self.get_y() - 3)
        self.ln(5)

    def sub_title(self, t):
        self.set_font('H', '', 11)
        self.set_text_color(0x8B, 0x5E, 0x3C)
        self.set_x(self.m)
        self.cell(self.w - 2 * self.m, 8, t)
        self.ln(10)

    def body(self, t):
        self.set_font('S', '', 10)
        self.set_text_color(0x33, 0x33, 0x44)
        self.set_x(self.m)
        self.multi_cell(self.w - 2 * self.m, 6, t, align='J')
        self.ln(2)

    def bold_body(self, t):
        self.set_font('H', '', 10)
        self.set_text_color(0x33, 0x33, 0x44)
        self.set_x(self.m)
        self.multi_cell(self.w - 2 * self.m, 6, t, align='J')
        self.ln(2)

    def bullet(self, t):
        self.set_font('S', '', 9.5)
        self.set_text_color(0x33, 0x33, 0x44)
        self.set_x(self.m)
        self.cell(6, 5.5, '>')
        self.multi_cell(self.w - 2 * self.m - 6, 5.8, t, align='J')
        self.set_x(self.m)
        self.ln(0.5)

    def quote_card(self, text, attribution, translation=''):
        """Western quote card"""
        self.set_fill_color(0xF5, 0xF0, 0xE8)
        self.set_draw_color(0xC9, 0xA8, 0x4C)
        self.set_line_width(0.3)
        y = self.get_y()
        self.set_font('S', '', 10.5)
        self.set_text_color(0x1B, 0x2A, 0x4A)
        self.set_x(self.m + 3)
        self.multi_cell(self.w - 2 * self.m - 6, 6.2, f'“{text}”', align='J')
        self.ln(2)
        if translation:
            self.set_font('S', '', 9)
            self.set_text_color(0x66, 0x66, 0x77)
            self.set_x(self.m + 3)
            self.multi_cell(self.w - 2 * self.m - 6, 5.5, translation, align='J')
            self.ln(1)
        self.set_font('S', '', 8.5)
        self.set_text_color(0xAA, 0x99, 0x88)
        self.set_x(self.m + 3)
        self.cell(self.w - 2 * self.m - 6, 5, f'—— {attribution}')
        self.ln(6)
        ny = self.get_y()
        self.rect(self.m, y, self.w - 2 * self.m, ny - y + 1)
        self.set_y(ny + 3)

    def insight_box(self, title, content):
        """Key insight callout"""
        self.set_fill_color(0xE8, 0xEE, 0xF5)
        self.set_draw_color(0x1B, 0x2A, 0x4A)
        self.set_line_width(0.3)
        y = self.get_y()
        self.set_font('H', '', 10)
        self.set_text_color(0x1B, 0x2A, 0x4A)
        self.set_x(self.m + 3)
        self.cell(self.w - 2 * self.m - 6, 6, title)
        self.ln(7)
        self.set_font('S', '', 9)
        self.set_text_color(0x33, 0x33, 0x44)
        self.set_x(self.m + 3)
        self.multi_cell(self.w - 2 * self.m - 6, 5.5, content, align='J')
        ny = self.get_y()
        self.rect(self.m, y, self.w - 2 * self.m, ny - y + 2)
        self.set_y(ny + 4)

    def philosopher(self, name, lifespan, idea, connection):
        """Compact philosopher entry"""
        self.set_font('H', '', 9.5)
        self.set_text_color(0x1B, 0x2A, 0x4A)
        self.set_x(self.m)
        self.cell(self.w - 2 * self.m, 6, f'{name} ({lifespan})')
        self.ln(7)
        self.set_font('S', '', 9.5)
        self.set_text_color(0x55, 0x55, 0x66)
        self.set_x(self.m + 3)
        self.multi_cell(self.w - 2 * self.m - 6, 5.5, f'核心思想：{idea}', align='J')
        self.set_x(self.m + 3)
        self.multi_cell(self.w - 2 * self.m - 6, 5.5, f'投资启示：{connection}', align='J')
        self.ln(3)

    def pillar_section(self, num, name, en_name, framing, desc, invest, example):
        """Five pillars with Western philosophical framing"""
        self.set_font('H', '', 13)
        self.set_text_color(0x1B, 0x2A, 0x4A)
        self.set_x(self.m)
        self.cell(self.w - 2 * self.m, 8, f'{num}. {name} / {en_name}')
        self.ln(10)
        # Framing quote
        self.set_fill_color(0xF5, 0xF0, 0xE8)
        self.set_draw_color(0xC9, 0xA8, 0x4C)
        self.set_line_width(0.2)
        y = self.get_y()
        self.set_font('S', '', 10)
        self.set_text_color(0x1B, 0x2A, 0x4A)
        self.set_x(self.m + 3)
        self.multi_cell(self.w - 2 * self.m - 6, 6, f'“{framing}”', align='J')
        ny = self.get_y()
        self.rect(self.m, y, self.w - 2 * self.m, ny - y + 1)
        self.set_y(ny + 3)
        # Description
        self.set_font('S', '', 9.5)
        self.set_text_color(0x44, 0x44, 0x55)
        self.set_x(self.m)
        self.multi_cell(self.w - 2 * self.m, 5.8, desc, align='J')
        self.ln(1)
        self.set_font('S', '', 9)
        self.set_text_color(0x8B, 0x5E, 0x3C)
        self.set_x(self.m)
        self.multi_cell(self.w - 2 * self.m, 5.8, f'投资要义：{invest}', align='J')
        self.set_x(self.m)
        self.multi_cell(self.w - 2 * self.m, 5.8, f'例：{example}', align='J')
        self.ln(5)

    def gold_bar(self):
        self.set_draw_color(0xC9, 0xA8, 0x4C)
        self.set_line_width(0.3)
        y = self.get_y()
        self.line(self.m, y, self.w - self.m, y)
        self.ln(4)

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
    '长现 · 理性',
    'Long Now — Ratio — 以西方思想重述 30 年投资思维框架',
    '邮储银行上海分行科技金融事业部  |  2026年5月')

# ================================================================
# INTRODUCTION
# ================================================================
pdf.ch_title('引言：Sapere Aude ！（敢于认知）')

pdf.body('1784年，康德在一篇短文中回答了人类历史上最重大的问题之一：什么是启蒙？他的回答只有一个拉丁文短语：Sapere aude — “要有勇气运用你自己的理性！”')

pdf.body('这不仅是启蒙运动的口号，也是长现投资者的精神宣言。在所有人都用季度报告衡量成败时，用30年的尺度做决策需要的不是更多的数据或更精妙的模型 — 而是一种智识上的勇气：敢于独立思考、敢于与共识对抗、敢于为一笔30年后才能验证的决策承担责任。')

pdf.body('西方哲学史，从苏格拉底在雅典街头追问真理，到波普尔为开放社会辩护，始终贯穿着一个主题：理性的勇气。本文件试图证明，这种勇气正是长现投资最稀缺、也最必要的品质。')

pdf.quote_card(
    'Sapere aude! “Have the courage to use your own understanding!” is therefore the motto of the enlightenment.',
    'Immanuel Kant, “What is Enlightenment?” (1784)',
    '要有勇气运用你自己的理性！这就是启蒙运动的座右铭。')

pdf.body('本框架与之前的东方版本（长现·常道）构成互补：东方智慧提供了时间感 — 耐心、厚积薄发、顺势而为；西方理性提供了分析框架 — 进步的机制、范式的结构、知识的增长。两者合一，才是完整的Long Now。')

pdf.gold_bar()
pdf.insight_box('Long Now的西方内核',
    '长现（Long Now）本就源于西方。Stewart Brand、Brian Eno、Danny Hillis创立的Long Now Foundation根植于西方启蒙传统：对人类进步的信念、对理性的信任、对未来的责任感。本文件将这一隐性的西方根系显性化，拉出一张完整的哲学地图。')

# ================================================================
# PART 1: PHILOSOPHICAL FOUNDATIONS
# ================================================================
pdf.ch_title('一、Philosophia — 哲学根基')

pdf.body('长现投资的哲学根基不在东方也在东方。西方哲学传统中关于进步、时间、理性、自由的思考，为30年投资框架提供了同样深层的支撑。以下四位哲人构成了这个框架的四个基石。')

pdf.gold_bar()

pdf.sub_title('1.1 Francis Bacon （1561—1626）：知识即力量')

pdf.quote_card(
    'Nam et ipsa scientia potestas est. (Knowledge itself is power.)',
    'Francis Bacon, Meditationes Sacrae (1597)',
    '知识本身就是力量。')

pdf.body('培根是现代科学和实验方法之父。在《新工具》（Novum Organum, 1620）中，他提出人类要“服从自然以支配自然” — 先理解自然的规律，再运用这些规律改造世界。这个简单的公式，就是一切技术投资的哲学基础。')

pdf.body('培根还辨识了四种阻碍人类认知的“假象”（Idols），它们是系统性的认知偏见：')

pdf.bullet('种族假象（Idols of the Tribe）：人类这个物种共有的认知偏差 — 例如我们天然倾向于短期思维，因为祖先在草原上不需要考虑30年后的猎物分布')
pdf.bullet('洞穴假象（Idols of the Cave）：每个人因教育、经历形成的个人偏见 — 例如一位出身贸易银行的从业者天然不相信技术投资')
pdf.bullet('市场假象（Idols of the Marketplace）：语言和交流造成的混淆 — 例如“科技泡沫”这个词本身就扭曲了对技术价值的判断')
pdf.bullet('剧场假象（Idols of the Theatre）：被接受的哲学体系和教条 — 例如“所有投资都要在3年内退出”这个信条')

pdf.body('培根对人类认知局限的敏锐诊断，是所有长期决策者的必修课。理解这四种假象，就是长现投资的第一课。')

pdf.body('培根在《新大西岛》（New Atlantis）中描绘了一个由“所罗门宫”（Salomon’s House）领导的乌托邦 — 这是一个由国家资助的科学研究机构，是今天所有R&D实验室的原型。所罗门宫的成员不追求即时回报，他们只用一代人的时间推动知识的边界。这正是耐心资本的制度形态。')

pdf.sub_title('1.2 Martin Heidegger （1889—1976）：时间性与本真的决断')

pdf.quote_card(
    'The future is not later than the past, and the past is not earlier than the present. Temporality temporalizes itself as a future which makes present in a process of having been.',
    'Martin Heidegger, Being and Time (1927)',
    '未来不比过去更“晚”，过去也不比现在更“早”。时间性的本质是：曾在着的当前化着的未来。')

pdf.body('海德格尔的《存在与时间》（Sein und Zeit, 1927）是20世纪最深刻的关于时间性的哲学著作。他的核心洞见是：人的存在（Dasein）本质上就是时间性的 — 我们不是生活在“时间中”的物体，我们的存在方式就是时间。')

pdf.body('这个思想对长现投资有深远的意义。海德格尔区分了“非本真”（inauthentic）和“本真”（authentic）的时间体验：')

pdf.bullet('非本真状态：我们被日常事务（das Man）吞噬，活在“当下”的琐碎中。今天的投资者大多处于这个状态 — 被K线、季度财报、市场情绪推着走，失去了对时间的自主把握。')
pdf.bullet('本真状态：我们意识到自身的有限性（being-toward-death），在这个意识中做出真正属于自己的决定。海德格尔称之为“ Augenblick” — 决断性的瞬间。在这个瞬间中，过去（我们的积累）和未来（我们的可能性）同时在当前汇聚。')

pdf.body('长现投资就是本真的投资。它不是“看得更远”（那仍然是非本真状态的延续 — 只不过换了一个时间尺度上的“日常”），而是在每一个决策的瞬间，都已经将30年的维度内化到了自己的存在方式中。30年不是一个“目标”，而是你存在的时间结构本身。')

pdf.body('海德格尔的另一个关键概念是“在世存在”（Being-in-the-World）。我们的决策从来不是在真空中做出的，而是在一个具体的、历史性的世界中。技术就是这个世界的一部分。投资技术，就是投资我们存在的世界本身。')

pdf.sub_title('1.3 Friedrich Nietzsche （1844—1900）：人的自我超越')

pdf.quote_card(
    'Man is something to be overcome. What have you done to overcome him?',
    'Friedrich Nietzsche, Thus Spoke Zarathustra (1883)',
    '人是应当被超越的。你们做了什么来超越他呢？')

pdf.body('尼采是“超人”（Übermensch）哲学的创始人 — 这一概念后来深刻影响了超人类主义（Transhumanism）运动，也是AI、生命科学、脑机接口等技术方向的潜在哲学驱动力。')

pdf.body('尼采的核心理念是：人类不是终点，而是桥梁。人的价值不在于他是什么，而在于他能够成为什么。这恰恰是技术投资的最高叙事 — 我们所投资的不是具体的产品，而是人类自我超越的过程本身。')

pdf.body('尼采在《查拉图斯特拉如是说》中批判了“末人”（the Last Man） — 这种人以舒适、安全、稳定为最高追求，没有激情、没有抱负、不再创造。末人会说：“我们发明了幸福” — 然后舒服地缩在角落里。')

pdf.body('这让人想起了今天大多数资本的态度：追求稳定收益、规避不确定性、等待“确认”后再入场。长现投资者的反面就是末人 — 而长现投资者本身，就是查拉图斯特拉意义上的“超人”：拥抱不确定性，将风险视为创造的机会，而不是威胁。')

pdf.body('尼采的“永恒轮回”（Eternal Recurrence）思想是一个极好的投资测试：如果你必须无限次地重复同一个投资决策，你还会做这个决定吗？如果答案是否定的，那这就是一个你不应该做的决定。永恒轮回过滤掉了所有基于运气和短期噪音的决策。')

pdf.sub_title('1.4 Karl Popper （1902—1994）：开放社会与可错论')

pdf.quote_card(
    'We must not forget that the progress of knowledge is the most important way in which our world has grown, and that we must not try to put a ceiling on it.',
    'Karl Popper, The Open Society and Its Enemies (1945)',
    '我们必须记住，知识的进步是我们的世界得以成长的最重要途径，我们不能为它设置天花板。')

pdf.body('波普尔的可错论（Fallibilism）是长现投资最实用的哲学工具之一。他的核心主张是：')

pdf.bullet('我们永远无法“证实”一个理论为真，我们只能“证伪”它。科学进步就是不断地提出猜想、接受反驳、修正理论。')
pdf.bullet('不存在历史发展的必然规律（反历史决定论）— 未来是真正开放的。任何声称“必然如此”的技术预测都需要被怀疑。')
pdf.bullet('开放社会的基础是批判理性主义 — 所有的信念都必须接受公开的批判和检验。')

pdf.body('将波普尔的方法论应用到投资中：')

pdf.bullet('每一个投资决策都是一个“猜想”（conjecture），不是一个已验证的真理')
pdf.bullet('定期“证伪”自己的投资假设 — 寻找那些可能证明你错了的证据')
pdf.bullet('如果证据表明你错了，就要有勇气修正 — 这就是“可错”的本质')

pdf.body('波普尔还提出了“三个世界”（Three Worlds）理论：世界1是物理世界，世界2是心理世界，世界3是客观知识世界 — 包括科学理论、技术、文化产品。长现投资本质上是在押注世界3的增长 — 即人类客观知识的不可逆积累。世界3的增长有其自身的逻辑，不依赖于任何个人的意图。这个思想为“技术不可逆”提供了坚实的哲学基础。')

# ================================================================
# PART 2: METHODOLOGY
# ================================================================
pdf.ch_title('二、Methodus — 方法论')

pdf.body('西方哲学传统不仅提供了思想根基，还提供了可操作的分析工具。以下三种方法论框架，分别对应长现投资的三种核心能力：识别变革的结构、检验理念的实用价值、理解集体智慧的形成。')

pdf.gold_bar()

pdf.sub_title('2.1 范式转移 — Thomas Kuhn (1922–1996)')

pdf.quote_card(
    'The successive transition from one paradigm to another via revolution is the usual developmental pattern of mature science.',
    'Thomas Kuhn, The Structure of Scientific Revolutions (1962)',
    '通过革命从一个范式向另一个范式的依次转换，是成熟科学的通常发展模式。')

pdf.body('库恩在《科学革命的结构》中提出，科学的发展不是线性的知识积累，而是“常规科学”和“科学革命”交替出现的过程：')

pdf.bullet('常规科学：在已有范式（框架）下解决“疑题”（puzzles）。绝大多数技术发展处于这个阶段 — 工程师在现有框架下优化产品。')
pdf.bullet('危机：反常现象积累到一定程度，现有范式无法解释。这是投资者最应该关注的阶段 — 因为它意味着范式转移的临近。')
pdf.bullet('革命：新范式取代旧范式。这不是一个逻辑推理的过程，而是一个“格式塔转换”（gestalt switch）— 看待世界的方式发生了根本变化。')
pdf.bullet('新常规：新范式确立，新一轮的常规科学开始。')

pdf.body('库恩的框架为技术投资提供了一个极其有力的分析工具：')

pdf.bullet('投资的时机不是“越早越好”，而应该是在“危机”阶段和“革命”阶段之间。太早（常规科学早期），不知道新范式是否会成功；太晚（新常规确立后），已经失去了超额收益。')
pdf.bullet('“不可通约性”（Incommensurability）：新旧范式之间不能用同样的标准来衡量。这意味着“等待确认”是一种逻辑上不可能的策略 — 因为新范式在被新标准确认之前，按照旧标准来看永远是“不够好”的。')
pdf.bullet('识别“危机”的标志：主流技术的瓶颈、异常现象无法解释、行业领军企业的焦虑。')

pdf.body('当前的AI革命正是一个典型的范式转移：深度学习终结了符号AI（范式革命），正在从进化到AGI（即将到来的又一次革命）。每一次革命都是投资机会重新分布的时刻。')

pdf.sub_title('2.2 实用主义 — William James (1842–1910) & C.S. Peirce (1839–1914)')

pdf.quote_card(
    'The pragmatic method... is to try to interpret each notion by tracing its respective practical consequences. What difference would it practically make to anyone if this notion rather than that notion were true?',
    'William James, Pragmatism (1907)',
    '实用主义的方法，就是试图通过追踪每个观念的实际后果来解释它。如果这个观念而非那个观念为真，对任何人会有什么实际区别？')

pdf.body('实用主义是美国人贡献给世界的最重要的哲学流派之一。它的核心方法是：一个观念的意义在于它的实际后果。不用问“这是真的吗”，而是问“如果这是真的，世界会有什么不同”。')

pdf.body('皮尔士（C.S. Peirce）在实用主义基础上提出了“溯因推理”（Abduction — 推断最佳解释）作为科学发现的逻辑。与演绎（从一般到特殊）和归纳（从特殊到一般）不同，溯因是从“令人惊讶的事实”出发，推导出最能解释这个事实的假设。')

pdf.body('这个方法对技术投资有直接的指导意义：')

pdf.bullet('不要问“这个技术会成功吗”，而应该问“如果这个技术成功了，哪些现存假设会被推翻？哪些行业会被重塑？”')
pdf.bullet('溯因法用于发现技术方向：看到令人惊讶的突破（如GPT-3的涌现能力），推理出这个突破意味着什么（如规模法则（Scaling Laws）的有效性），然后押注在这个方向上。')

pdf.body('威廉·詹姆斯还提出了“相信的意志”（The Will to Believe）: 在某些证据不足但必须做出决定的时刻，理性允许我们基于信念采取行动。这个思想的投资版本就是 — 你不能等到所有证据都齐备才入场，因为到那时窗口已经关闭。长现投资要求我们在不确定中行动，而这正是“理性”的一部分，而非它的反面。')

pdf.sub_title('2.3 集体智慧 — Hannah Arendt (1906–1975) & F.A. Hayek (1899–1992)')

pdf.quote_card(
    'The essence of action is to initiate something new, to begin something that cannot be predicted from what happened before.',
    'Hannah Arendt, The Human Condition (1958)',
    '行动的本质是开创某种全新的东西，是开始一件无法从过去预测的事情。')

pdf.body('阿伦特在《人的境况》中区分了三种人类活动：')

pdf.bullet('劳动（Labor）：满足生物需要的重复性活动 — 对应日常交易、月度汇报、季度报告')
pdf.bullet('工作（Work）：创造持久的人工制品 — 对应建立公司、开发技术、搭建平台')
pdf.bullet('行动（Action）：在公共领域中开创前所未有之事 — 对应30年尺度的投资决策')

pdf.body('长现投资属于“行动”的领域。它不是“劳动”（不是每天更勤奋地看盘），甚至不是“工作”（不是制造一个更好的量化模型）。它是“行动” — 在你意识到自己是一个公共领域中的行动者的那一刻，你做出的那个将改变格局的决定。')

pdf.body('哈耶克（F.A. Hayek）则为理解市场作为知识发现机制提供了深刻的洞见。在《知识在社会中的运用》（The Use of Knowledge in Society, 1945）中，他论证了：')

pdf.bullet('知识是分散的，没有任何中央机构能够掌握全部信息')
pdf.bullet('价格机制是传递分散知识的最有效工具')
pdf.bullet('自发秩序（Spontaneous Order）优于人为设计')

pdf.body('哈耶克对技术投资的启示：不要试图“预测”哪个具体的技术路径会获胜，而是投资那些“平台” — 让市场中的无数参与者自己去发现最佳应用的底层基础设施。平台投资是对哈耶克“分散知识”理论最忠实的实践。')

pdf.gold_bar()
pdf.insight_box('方法论核心',
    '库恩提供“何时”（范式转移的时机），詹姆斯提供“如何”（实用主义的检验），阿伦特和哈耶克提供“从什么视角”（行动者的视野和市场的智慧）。三者合一，构成了长现投资的完整方法论工具箱。')

# ================================================================
# PART 3: FIVE PILLARS THROUGH WESTERN LENS
# ================================================================
pdf.ch_title('三、五大支柱：西方思想中的投影')

pdf.body('长现框架的五大技术收敛方向，在西方思想中都有深层的哲学对应。每一个方向不只是投资主题，而是某种理性精神的具象化。')

pdf.gold_bar()

pdf.pillar_section(1,
    '智能收敛', 'Intelligence',
    'Cogito, ergo sum. — René Descartes (1596–1650)\n\n“我思故我在。”',
    '笛卡尔的“我思”是现代哲学和科学的基础。他的“我思故我在”将理性确立为一切确定性的起点。300多年后，人类正在将自己的“思”外化到硅基载体上。\n\nAI不是“另一种技术” — 它是理性自身的外化（externalization of reason）。从这个角度看，AI的发展不是“一个行业”的扩张，而是人类这个物种将自身最本质的能力—理性—投射到外部世界的过程。\n\n长现投资者应当理解：正如当年培根说的“知识即力量”，今天我们要说“计算即力量”。AI的投资价值不在于它能取代多少工作，而在于它是一个文明级的基础设施 — 就像文字、印刷术、电力一样。',
    '算力基础设施是“思”的载体。最确定的长期仓位是 GPU/芯片等“计算即力量”的实现者。模型层要识别谁能定义下范式。',
    'NVIDIA（算力层）+ OpenAI/DeepMind（模型层）+ Microsoft（应用化）')

pdf.pillar_section(2,
    '生命收敛', 'Longevity',
    'To be, or not to be, that is the question. — William Shakespeare, Hamlet (c. 1600)\n\n“生存还是毁灭，这是一个问题。”',
    '哈姆雷特的问题是人类境况的原问题。今天，生物技术正在将这个形而上学问题变成技术问题。\n\n尼采说“人是应当被超越的” — 生命科学就是超越的手段。基因编辑（CRISPR）、细胞重编程（Yamanaka因子）、端粒延长 — 这些技术共同指向一个方向：将生命从“给定”变成“可编程”。\n\n笛卡尔的“我思故我在”预设了一个不变的“我”。但如果“我”的身体（包括大脑）可以被修改、升级、重建呢？生命科学挑战了西方哲学中最深的假设之一 — “人”是什么。\n\n对投资者而言，更直接的叙事是：延长人类健康寿命意味着延长经济生产力。如果2035–2050年间预期寿命突破100–120岁，养老金、保险、医疗、消费等整个经济结构将被重塑。这是一个系统性的价值重估。',
    '工具层（测序/编辑/合成）是“编程”的基础设施。在范式转移早期，押注“工具”比押注“疗法”更安全。',
    'Illumina（测序）+ Editas/CRISPR Tx（编辑）+ Altos Labs（重编程）')

pdf.pillar_section(3,
    '能源收敛', 'Energy',
    'Prometheus, the bringer of fire. — Aeschylus, Prometheus Bound (c. 415 BC)\n\n“普罗米修斯，盗火者。”',
    '普罗米修斯盗火给人类的神话，是西方文明对能源最原初的隐喻。火是第一种被人类掌控的能源。每一次能源升级 — 从木材到煤炭、从煤炭到石油、从石油到核裂变 — 都意味着人类获得了更大的“火”。\n\n培根说“服从自然以支配自然” — 核聚变就是这句格言的终极表达。它完全遵从自然规律（爱因斯坦的E=mc²），却实现了近乎无限的能量输出。\n\n这是康德式的“二律背反”（Antinomy）的实际解法：人类拥有自由的意志，却生活在一个受自然规律支配的身体中。能源技术的每一次突破，都在扩大这个“自由”的空间。\n\n30年维度上，能源的成本结构变化将是最具确定性的趋势之一。当能源成本趋近于零，所有依赖能源的产业都将被重塑 — 也就是几乎所有产业。',
    '关注“使能技术”（enabling tech）：聚变点火、钙钛矿效率、储能密度。不是预测赢家，而是押注“能源充裕”这个方向本身。',
    'Commonwealth Fusion（聚变）+ CATL/QuantumScape（储能）+ NextEra（电网友）')

pdf.pillar_section(4,
    '接口收敛', 'Interface',
    'The medium is the message. — Marshall McLuhan (1911–1980)\n\n“媒介即讯息。”',
    '麦克卢汉的洞见是：真正影响文明的不是媒介承载的内容，而是媒介本身的形态。印刷术改变了思维方式，电视改变了注意力结构，互联网改变了知识分布。\n\n麦克卢汉还提出了“媒介是人的延伸”（extensions of man）: 车轮是腿的延伸，衣服是皮肤的延伸，书籍是记忆的延伸。按这个逻辑，脑机接口（BCI）是神经系统的延伸 — 所有延伸中最彻底的一种。\n\n安迪·克拉克和戴维·查尔默斯（1998）提出了“延展心灵论题”（Extended Mind Thesis）：认知过程不局限于大脑和身体，而是延伸到我们使用的工具和环境中。智能手机已经是心灵的一部分。BCI将把这个“部分”变成“全部”。\n\n黑格尔的“绝对精神”通过人类历史实现自身的恢弘叙事，在技术史上得到了一个惊人的回响：人类在“接口”上的每一次突破（语言、文字、印刷、互联网、AI、BCI），都是“精神”的一次自我外化。',
    '硬件（芯片/电极）和信号解码平台是“管道”。在早期，管道比内容更有价值。',
    'Neuralink（侵入式BCI）+ Synchron（血管内BCI）+ Apple/Meta（空间计算）')

pdf.pillar_section(5,
    '扩张收敛', 'Expansion',
    'Two things fill the mind with ever new and increasing admiration and reverence... the starry heavens above me and the moral law within me. — Immanuel Kant, Critique of Practical Reason (1788)\n\n“有两样东西，越是经常而持久地思索，心灵就越是充满常新而日增的赞叹和敬畏 — 头顶的星空和心中的道德律。”',
    '对于康德来说，头顶的星空是人类永恒的惊叹之源。两个世纪后，我们不仅惊叹它，还在计划前往它。\n\n阿伦特在《人的境况》中描述了人类“地球异化”（earth alienation）的过程 — 从哥白尼开始，人类逐渐认识到地球不是宇宙的中心。而太空探索是这个过程的最高阶段：不仅在思想上离开地球中心主义，而且在物理上离开地球。\n\n培根的“所罗门宫”最终也可能出现在太空 — 在零重力环境下进行新材料研发、在月球基地进行天文观测。太空经济是“知识即力量”在最大尺度上的延伸。\n\n这是最宏大的收敛方向，也是周期最长的。它要求最坚定的长现目光。在2040–2050年间，地月经济圈可能形成，小行星采矿可能成为现实。这需要今天的资本开始“播种”。',
    '运力降本是核心驱动力。先布局发射服务（SpaceX/ULA）和卫星网络（AST SpaceMobile），再扩展到资源开采和空间制造。',
    'SpaceX（发射/星舰）+ Blue Origin（月球着陆器）+ AST SpaceMobile（卫星网络）')

# ================================================================
# PART 4: WESTERN CASE STUDIES
# ================================================================
pdf.ch_title('四、Exempla — 西方经典案例')

pdf.body('四个跨越不同时代的西方案例，分别对应长现框架的不同侧面。它们共同说明：最伟大的技术投资回报，来自最长的持有期和最坚定的信念。')

pdf.gold_bar()

pdf.sub_title('案例一：贝尔实验室 — “所罗门宫”的现代版本')

pdf.body('培根在1627年想象了一个由科学家和工程师组成的机构 “所罗门宫”，致力于“探究事物的终极原因和运行的隐秘机制，拓展人类能力的边界，使一切成为可能”。')

pdf.body('1925年成立的贝尔实验室（Bell Labs），就是这个想象的完美实现：')

pdf.bullet('7项诺贝尔物理学奖、9项美国国家科学奖章、3项图灵奖')
pdf.bullet('发明了晶体管（1947）、激光（1958）、Unix操作系统（1969）、C语言（1972）')
pdf.bullet('发现了宇宙微波背景辐射（1965）、验证了量子力学的贝尔不等式（1982）')

pdf.body('贝尔实验室成功的秘诀：')

pdf.bullet('AT&T的垄断利润提供了“耐心资本” — 不需要实验室产生即时商业回报')
pdf.bullet('自由的学术氛围 — 研究人员可以追求任何基础科学问题，无论它是否直接相关于电话业务')
pdf.bullet('跨学科结构 — 物理学家、数学家、工程师、心理学家在同一栋楼里工作')

pdf.body('投资启示：贝尔实验室最辉煌的时代，正是AT&T垄断最稳固的时代。反垄断拆分（1984）终结了贝尔实验室。这个案例告诉我们：耐心资本需要制度保障。今天，哪些机构扮演着“所罗门宫”的角色？OpenAI？DeepMind？Altos Labs？他们是新时代的贝尔实验室吗？')

pdf.sub_title('案例二：摩尔定律 — 自我实现的预言')

pdf.body('1965年，戈登·摩尔在《电子学》杂志上发表了一篇简短的文章。他观察到：自集成电路发明以来，芯片上的晶体管数量每年翻一番。他预测这个趋势会“至少持续10年”。')

pdf.body('这个预测—后来修正为每18–24个月翻一番—被称为“摩尔定律”。但摩尔定律不是物理定律。它是一个“自我实现的预言”（self-fulfilling prophecy）：')

pdf.bullet('整个半导体行业围绕摩尔定律组织研发：每个公司都承诺在18个月内使晶体管密度翻倍')
pdf.bullet('没有公司敢落后 — 落后就意味着失去市场地位')
pdf.bullet('最终，这个“预测”变成了一个集体承诺。它之所以成真，是因为每个人都相信它、并围绕它组织行动')

pdf.body('投资启示：最大的技术趋势往往不是“发现”的，而是“创造”的。长现投资者的任务是在一个自我实现预言形成之前识别它。今天的AI规模法则（Scaling Laws）正在成为新的“摩尔定律” — 许多人正在努力让它成真。押注这个方向，就是押注人类集体行动的力量。')

pdf.sub_title('案例三：苹果的沉浮 — 尼采式超越的现代寓言')

pdf.body('苹果公司的历史，是一曲尼采式的“超人”戏剧：')

pdf.bullet('1976年创立：乔布斯和沃兹尼亚克在车库里组装第一台个人电脑 — 这是“创造者”的诞生')
pdf.bullet('1985年被驱逐：乔布斯被斯卡利赶出自己创立的公司 — 这是“超人”的放逐')
pdf.bullet('1997年回归：苹果濒临破产，乔布斯回归 — 这是“永恒轮回”中的回归')
pdf.bullet('1998–2011年巅峰：iMac、iPod、iPhone、iPad — 连续创造全新品类。尼采的“权力意志”在这里表现为“重新定义行业的能力”')
pdf.bullet('2011年后：库克时代的苹果在商业上更成功（市值从3000亿到3万亿），但“创造力”明显下降 — 这是从“超人”到“末人”的转变')

pdf.body('投资启示：苹果1997年濒临破产时，它的市值不到30亿美元。如果你在当时看到了乔布斯回归的意义，并相信他能重演尼采式的“自我超越”，你的回报超过100倍。但真正的长现投资者不会在苹果3万亿时买入 — 那是庆祝，不是投资。长现投资者寻找的是那个“正在回归的乔布斯” — 今天被低估但拥有“权力意志”的公司或技术。')

pdf.sub_title('案例四：太空竞赛 — 康德式的敬畏')

pdf.body('1969年阿波罗11号登月，是人类历史上最伟大的成就之一。康德说“头顶的星空”是人类敬畏的源泉。阿波罗计划将敬畏变成了行动。')

pdf.bullet('1961年肯尼迪宣布登月目标 — 是一个政治决定，不是一个技术路线图')
pdf.bullet('1961–1969年：8年时间，动员40万人、2万家企业、耗资250亿美元（相当于今天2000亿美元以上）')
pdf.bullet('阿波罗计划证明了：当意志足够强烈时，技术突破可以被“推动”发生')

pdf.body('今天，新一輪太空竞赛正在上演：')

pdf.bullet('SpaceX的星舰（Starship）是人类历史上最大的运载火箭，目标是火星殖民')
pdf.bullet('蓝色起源的月球着陆器被NASA选中，月球基地不再是科幻')
pdf.bullet('中国月球科研站计划2030年代建成')

pdf.body('投资启示：太空经济的催生剂是运力成本。SpaceX将发射成本从每公斤1万美元降到了当时的2000美元以下，星舰全复用后将降到100美元以下。成本的指数级下降是长现投资最可靠的信号。当某个东西的成本在10年内降了一个数量级，不要关注它今天“值不值” — 关注10年后它“能做什么”。')

# ================================================================
# PART 5: CONCLUSION
# ================================================================
pdf.ch_title('五、结语：理性的勇气')

pdf.quote_card(
    'The only thing necessary for the triumph of evil is for good men to do nothing.',
    'Attributed to Edmund Burke (1729–1797)',
    '邪恶获胜的唯一必要条件，是好人什么也不做。')

pdf.body('柏林墙倒塌后，弗朗西斯·福山宣布了“历史的终结” — 人类意识形态的演化已经到达终点。但30年后的今天，我们知道历史远未终结。技术正在以前所未有的速度重构人类生存的每一个维度。')

pdf.body('在这样的时代，不参与本身就是一个决定。正如波普尔所言，开放社会需要公民的积极参与。长现投资就是对人类开放未来的一种参与方式。')

pdf.body('当你以30年为尺度做决策：')

pdf.bullet('你不受困于季度噪音 — 因为你知道30年后没人记得这一季度的涨跌')
pdf.bullet('你不被市场情绪裹挟 — 因为你用康德的“理性”和海德格尔的“本真性”超越了“大众”（das Man）')
pdf.bullet('你不回避不确定性 — 因为你用波普尔的“可错论”和詹姆斯的“实用主义”将不确定性转化为认知工具')
pdf.bullet('你不畏惧范式的崩溃 — 因为你用库恩的框架理解并拥抱革命性的变化')

pdf.body('在西方哲学最深的传统中，理性的勇气一直是人类最珍贵的品质。苏格拉底选择饮鸩而非沉默。培根选择观察自然而非沉迷书本。康德选择“敢于认知”而非服从权威。尼采选择“成为你自己”而非随波逐流。波普尔选择开放社会而非封闭的确定性。')

pdf.body('长现投资不是一种更好的“赚钱方法”。它是一种面对未来的存在方式 — 用30年的尺度做今天的决定，不是因为30年后能赚更多的钱，而是因为这是理性存在者应有的尊严。')

pdf.gold_bar()

pdf.set_font('H', '', 11)
pdf.set_text_color(0x1B, 0x2A, 0x4A)
pdf.multi_cell(pdf.w - 2 * pdf.m, 7,
    '长现 · 理性\n'
    'Long Now — Ratio — 以西方思想重述30年投资思维框架',
    align='C')
pdf.ln(2)
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
OUTPUT = os.path.join(OUTPUT_DIR, '长现·理性_西方思想投资框架.pdf')
pdf.output(OUTPUT)
print(f'Saved: {OUTPUT} | Pages: {pdf.page_no()}')
