#!/usr/bin/env python3
"""长现·常道 —— 以东方智慧重述长现投资框架 PDF"""

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
        self.set_fill_color(0x3A, 0x20, 0x10)
        self.rect(0, 0, self.w, 297, 'F')
        # Decorative vertical line
        self.set_draw_color(0xC9, 0xA8, 0x4C)
        self.set_line_width(0.3)
        self.line(self.w/2, 50, self.w/2, 120)
        self.ln(32)
        self.set_font('S', '', 11)
        self.set_text_color(0xC9, 0xA8, 0x4C)
        self.multi_cell(self.w - 2 * self.m, 8, '常道·久远为功', align='C')
        self.ln(10)
        self.set_font('H', '', 28)
        self.set_text_color(0xFF, 0xFF, 0xFF)
        self.multi_cell(self.w - 2 * self.m, 12, main, align='C')
        self.ln(4)
        self.set_font('S', '', 12)
        self.set_text_color(0xCC, 0xBB, 0xAA)
        self.multi_cell(self.w - 2 * self.m, 7, sub, align='C')
        self.ln(3)
        self.set_draw_color(0xC9, 0xA8, 0x4C)
        self.set_line_width(0.5)
        cx = self.w / 2
        self.line(cx - 18, self.get_y(), cx + 18, self.get_y())
        self.ln(5)
        self.set_font('S', '', 9)
        self.set_text_color(0x99, 0x88, 0x77)
        self.multi_cell(self.w - 2 * self.m, 6, sub2, align='C')

    def ch_title(self, t):
        self.add_page()
        self.set_font('S', '', 11)
        self.set_text_color(0xC9, 0xA8, 0x4C)
        self.set_x(self.m)
        self.cell(10, 10, '·')
        self.set_font('H', '', 17)
        self.set_text_color(0x3A, 0x20, 0x10)
        self.cell(self.w - 2 * self.m - 10, 10, t)
        self.ln(12)
        self.set_draw_color(0xC9, 0xA8, 0x4C)
        self.set_line_width(0.4)
        self.line(self.m, self.get_y() - 3, self.m + 30, self.get_y() - 3)
        self.ln(5)

    def sub_title(self, t):
        self.set_font('H', '', 11)
        self.set_text_color(0x8B, 0x5E, 0x3C)
        self.set_x(self.m)
        self.cell(self.w - 2 * self.m, 8, t)
        self.ln(10)

    def body(self, t):
        self.set_font('S', '', 10)
        self.set_text_color(0x44, 0x33, 0x22)
        self.set_x(self.m)
        self.multi_cell(self.w - 2 * self.m, 6, t, align='J')
        self.ln(2)

    def bold_body(self, t):
        self.set_font('H', '', 10)
        self.set_text_color(0x44, 0x33, 0x22)
        self.set_x(self.m)
        self.multi_cell(self.w - 2 * self.m, 6, t, align='J')
        self.ln(2)

    def bullet(self, t):
        self.set_font('S', '', 9.5)
        self.set_text_color(0x44, 0x33, 0x22)
        self.set_x(self.m)
        self.cell(6, 5.5, '·')
        self.multi_cell(self.w - 2 * self.m - 6, 5.8, t, align='J')
        self.set_x(self.m)
        self.ln(0.5)

    def quote_card(self, chinese, translation, source):
        """Classical Chinese quote with translation"""
        self.set_fill_color(0xF8, 0xF3, 0xEB)
        self.set_draw_color(0xC9, 0xA8, 0x4C)
        self.set_line_width(0.3)
        y = self.get_y()
        self.set_font('H', '', 11)
        self.set_text_color(0x3A, 0x20, 0x10)
        self.set_x(self.m + 3)
        self.multi_cell(self.w - 2 * self.m - 6, 6.5, chinese, align='J')
        self.ln(2)
        self.set_font('S', '', 9)
        self.set_text_color(0x66, 0x55, 0x44)
        self.set_x(self.m + 3)
        self.multi_cell(self.w - 2 * self.m - 6, 5.5, translation, align='J')
        self.ln(1)
        self.set_font('S', '', 8)
        self.set_text_color(0xAA, 0x99, 0x88)
        self.set_x(self.m + 3)
        self.cell(self.w - 2 * self.m - 6, 5, f'—— {source}')
        self.ln(6)
        ny = self.get_y()
        self.rect(self.m, y, self.w - 2 * self.m, ny - y + 1)
        self.set_y(ny + 3)

    def pillar_section(self, num, zh_name, concept, quote, source, meaning, invest):
        """Five pillars through Eastern wisdom"""
        self.set_font('H', '', 13)
        self.set_text_color(0x8B, 0x5E, 0x3C)
        self.set_x(self.m)
        self.cell(self.w - 2 * self.m, 8, f'{num}. {zh_name} —— {concept}')
        self.ln(10)
        self.set_fill_color(0xF8, 0xF3, 0xEB)
        self.set_draw_color(0xC9, 0xA8, 0x4C)
        self.set_line_width(0.2)
        y = self.get_y()
        self.set_font('S', '', 10)
        self.set_text_color(0x3A, 0x20, 0x10)
        self.set_x(self.m + 3)
        self.multi_cell(self.w - 2 * self.m - 6, 6, f'"{quote}"', align='J')
        self.set_font('S', '', 8)
        self.set_text_color(0xAA, 0x99, 0x88)
        self.set_x(self.m + 3)
        self.cell(self.w - 2 * self.m - 6, 5.5, f'—— {source}')
        ny = self.get_y()
        self.rect(self.m, y, self.w - 2 * self.m, ny - y + 1)
        self.set_y(ny + 3)
        self.set_font('S', '', 9.5)
        self.set_text_color(0x44, 0x33, 0x22)
        self.set_x(self.m)
        self.multi_cell(self.w - 2 * self.m, 5.8, meaning, align='J')
        self.ln(1)
        self.set_font('S', '', 9)
        self.set_text_color(0x8B, 0x5E, 0x3C)
        self.set_x(self.m)
        self.multi_cell(self.w - 2 * self.m, 5.8, f'投资要义：{invest}', align='J')
        self.ln(5)

    def gold_bar(self):
        self.set_draw_color(0xC9, 0xA8, 0x4C)
        self.set_line_width(0.3)
        y = self.get_y()
        self.line(self.m, y, self.w - self.m, y)
        self.ln(4)

    def page_num(self):
        self.set_font('S', '', 8)
        self.set_text_color(0xAA, 0x99, 0x88)
        self.set_y(-15)
        self.cell(self.w - 2 * self.m, 5, str(self.page_no()), align='R')


pdf = PDF()
pdf.set_margin(22)

# ================================================================
# TITLE
# ================================================================
pdf.title_page(
    '长现 · 常道',
    '以东方智慧重述 30 年投资思维框架',
    '邮储银行上海分行科技金融事业部  |  2026年5月')

# ================================================================
# 引言
# ================================================================
pdf.ch_title('引言：久远为功')

pdf.body('长现（Long Now）源自西方。但"以30年为尺度做决策"这个思想，在东方智慧中有更深厚的根基。')

pdf.body('中国文明是世界上唯一一个以"史"为核心的文化传统。"以史为鉴，可以知兴替"（《贞观政要》），三千年的历史意识训练了中国人用代际尺度思考问题。这种思维惯性——而非西方意义上的"耐心"——才是长现投资的东方根基。')

pdf.body('本文重述长现框架，不是披上中国话的外衣，而是回到东方思想的源头，重新理解"时间"与"投资"的关系。')

pdf.quote_card('"人无远虑，必有近忧。"',
    'If one has no long-term consideration, one will have immediate worries.',
    '《论语·卫灵公》')

pdf.body('孔子的这句话，可能是人类历史上最早关于"时间错配"的论述。远虑不是一种美德——它是一种必需。没有远虑的人，会被近忧耗尽。没有长期框架的投资，会被短期波动吞噬。')

pdf.gold_bar()

# ================================================================
# 一、道
# ================================================================
pdf.ch_title('一、道——天道与投资哲学')

pdf.sub_title('1.1 天长地久：长现之道的总纲')

pdf.quote_card('"天长地久。天地所以能长且久者，以其不自生，故能长生。"',
    'Heaven lasts long and earth endures. The reason they can last long and endure is that they do not live for themselves — therefore they can live long.',
    '《道德经》第七章')

pdf.body('老子这段话说出了长现哲学的核心。天地之所以长久，不是因为它们特别强大，而是因为"不自生"——不为自己而活。')

pdf.body('将这个概念引入投资：资本之所以能穿越周期，不是因为它的规模或技巧，而是因为它不"为己而生"。耐心资本的本质不是"等待"，而是"不为自己而活"——不追求眼前的自我证明，不追逐即时的回报确认。它像天地一样，只是在那里，让万物在其中生长。')

pdf.body('这是长现投资的第一原则：资本应如天地，不争而久。')

pdf.sub_title('1.2 厚积薄发：从"量变"到"质变"')

pdf.quote_card('"合抱之木，生于毫末；九层之台，起于累土；千里之行，始于足下。"',
    'A tree as big as a man\'s embrace grows from a tiny sprout. A nine-story terrace rises from a pile of earth. A journey of a thousand miles begins with a single step.',
    '《道德经》第六十四章')

pdf.body('技术创新的30年周期，正如树从毫末到合抱的过程。在最初的五年，你几乎看不到变化；在第十年，变化开始显现；在第三十年，一切已经不可逆转。')

pdf.body('东方思维接受这个过程——"十年树木，百年树人"（《管子》）。但西方金融思维要求更快的反馈。这个冲突是科技金融所有困境的根源。')

pdf.body('厚积薄发不是浪漫化的"工匠精神"，而是一个物理事实：基础技术的突破必然经历漫长的积累期。理解这一点，就不会在积累期退出。')

pdf.sub_title('1.3 不争：非竞争性优势的建立')

pdf.quote_card('"夫唯不争，故天下莫能与之争。"',
    'Because he does not contend, no one in the world can contend with him.',
    '《道德经》第二十二章')

pdf.body('"不争"是老子思想中最被误读的概念之一。它不是消极退让，而是选择不在你无法获胜的战场上战斗。')

pdf.body('在投资中，这意味着：不在短期回报率上竞争，不在季度排名上竞争，不在"我们比同行赚得多"上竞争。你只在时间尺度上竞争——用30年的维度做决策，而大多数人用30天。在这个维度上，你没有竞争者。')

pdf.sub_title('1.4 上善若水：耐心资本的形态')

pdf.quote_card('"上善若水。水善利万物而不争，处众人之所恶，故几于道。"',
    'The supreme good is like water. Water benefits all things without contending, and stays in places that others disdain — therefore it is close to the Way.',
    '《道德经》第八章')

pdf.body('耐心资本的最佳形态是水。水利万物而不争功——资本滋养技术创新，但不要求立即回报。水处众人之所恶——资本流向被低估、被忽视的领域，而不是追逐已经过热的方向。水柔弱却可以穿透岩石——长期资本最终会进入任何短期资本无法到达的地方。')

pdf.body('成为水一样的资本，是长现投资者的终极修炼。')

# ================================================================
# 二、法
# ================================================================
pdf.ch_title('二、法——守时与顺势')

pdf.body('东方方法论的核心在于两个概念：时（Timing）和势（Momentum）。与西方对"时机"的线性理解不同，东方思想中的"时"是一种多维的、有机的概念——它不是钟表上的一个点，而是条件成熟的状态。')

pdf.sub_title('2.1 观势：见微知著')

pdf.quote_card('"见微知著，睹始知终。"',
    'See the subtle and know the manifest; observe the beginning and know the end.',
    '《周易·系辞下》')

pdf.body('长现投资的第一步是观察大势。30年的技术趋势不是预测出来的，是从微小的迹象中读出来的：一篇顶刊论文、一项FDA批准、一个实验室的意外发现。东方思想强调"几者，动之微"——在事物刚刚开始萌动的时刻，就感知到它的方向。')

pdf.body('这需要沉静的观察力——正是庄子所说的"用心若镜"：不预设结论，不急于行动，先让事物如其所是地呈现。')

pdf.sub_title('2.2 待时：君子藏器于身')

pdf.quote_card('"君子藏器于身，待时而动。"',
    'The noble person conceals tools on their person and waits for the right time to act.',
    '《周易·系辞下》')

pdf.body('"待时而动"不是消极等待，而是积极的准备。在孔子看来，真正的能力需要与恰当的时机配合才能发挥作用。这与长现投资的理念完全一致：不是"买了放着不管"，而是"一直在准备，在等待最佳的执行时机"。')

pdf.body('一个30年的投资框架，不是让你买了就忘记。而是让你在30年中持续观察、持续学习、每年校准——然后在条件成熟时果断行动。')

pdf.sub_title('2.3 顺势：求之于势')

pdf.quote_card('"故善战者，求之于势，不责于人。"',
    'One who excels at warfare seeks momentum, not blame people.',
    '《孙子兵法·势篇》')

pdf.body('孙子区分了"势"和"责"（对人力的依赖）。善战者求势——创造有利的态势，让胜利自然发生，而不强迫人去达成目标。')

pdf.body('在投资中，"求势"意味着：在技术收敛的方向上布局，而不是强迫判断哪个具体公司会赢。你不需要预测NVIDIA的股价，只需要判断AI的"势"——算力需求将持续增长30年。你不需要预测哪家生物公司会研发出抗癌药，只需要判断基因编辑的"势"。')

pdf.body('这是长现投资的核心方法论：不被每日波动的"形"所迷惑，始终关注深层结构的"势"。')

pdf.sub_title('2.4 守中：中也者，天下之大本也')

pdf.quote_card('"中也者，天下之大本也；和也者，天下之达道也。致中和，天地位焉，万物育焉。"',
    'Centrality is the great foundation of the world; harmony is the universal path. When centrality and harmony are achieved, heaven and earth are in their proper places, and all things are nourished.',
    '《中庸》')

pdf.body('中庸不是平庸的平均主义，而是"在动态中保持平衡"的能力。在30年的投资框架中，"守中"意味着：不被极端的乐观或悲观所左右，在贪婪和恐惧之间找到自己的节律。')

pdf.body('当市场狂热时不离场，当市场恐慌时不退场——不是固执，而是知道自己的"中"在哪里。')

# ================================================================
# 三、术
# ================================================================
pdf.ch_title('三、术——五大常道')

pdf.body('五大技术收敛方向，在东方智慧中可以找到各自的对应。每一个方向不只是一种投资主题，更是一种"道"的体现。')

pdf.gold_bar()

pdf.pillar_section(1, '智',
    '智能收敛 / Intelligence',
    '知者不惑，仁者不忧，勇者不惧。',
    '《论语·子罕》',
    '人工智能是"智"的体现。但它不是替代人类之智，而是扩展之。AI作为"外脑"，正如荀子所说"君子生非异也，善假于物也"——君子的本性与常人无异，只是善于借助外物。AI是我们借助的最强"物"。长现投资者要做的是：在大家还在争论AI是泡沫还是革命时，看到它作为"工具"的不可逆性。',
    '算力基础设施是"势"的所在。不追模型层赢家，而追为模型提供"器"的公司。')

pdf.pillar_section(2, '寿',
    '生命收敛 / Longevity',
    '天地之大德曰生。',
    '《周易·系辞下》',
    '"生"是天地最大的德行。生命科学的目标不是延长寿命本身，而是让"生"的活力持续更久——这是对天地大德的顺应。中医的"治未病"思想（《黄帝内经》）与此相通：不是在疾病发生后治疗，而是在健康时预防。基因编辑和细胞重编程，正是"治未病"的最高形式——在基因层面预防衰老。',
    '平台型工具（测序、编辑、合成）在30年维度上比任何单一疗法都更具价值。')

pdf.pillar_section(3, '能',
    '能源收敛 / Energy',
    '天行健，君子以自强不息。',
    '《周易·乾卦》',
    '能源是人类文明之火。从天上的太阳到地下的煤炭，从核裂变到核聚变，能源的每一次升级都是文明的跃迁。核聚变如果实现，将是"天行健"的终极版本——像太阳一样为人类提供几乎无限的能源。长现投资者的任务是在这个跃迁发生之前看清它的必然性。',
    '关注技术突破的前沿信号（聚变点火、钙钛矿效率突破），不要等到"确定性"到来时才入场。')

pdf.pillar_section(4, '通',
    '接口收敛 / Interface',
    '感而遂通天下之故。',
    '《周易·系辞上》',
    '"感而遂通"——感应万物之理，然后通达天下之事。脑机接口和人机融合正是在实现这个古老的理想。庄子说的"天地与我并生，万物与我为一"，在技术层面上正在成为可能。当思想可以直接与机器交互时，"通"达到了极致。',
    'BCI硬件和神经信号解码平台是最具长期价值的"管道"——所有上层应用都必须通过它们。')

pdf.pillar_section(5, '扩',
    '扩张收敛 / Expansion',
    '上下四方曰宇，往古来今曰宙。',
    '《尸子》',
    '"宇"是空间，"宙"是时间。人类的扩张同时发生在空间和时间两个维度。太空探索是对"宇"的扩张，寿命延长是对"宙"的扩张。两者合在一起，就是"宇宙"——人类同时拓展存在的时间和空间。这是最宏大的收敛方向，也是周期最长的。',
    '运力降本（发射成本指数级下降）是驱动整个方向的核心"势"。先在"器"（发射、卫星）层布局，再扩展到"用"层面。')

# ================================================================
# 四、例
# ================================================================
pdf.ch_title('四、例——二则东方案例')

pdf.sub_title('案例一：台积电——"厚积薄发"的现代典范')

pdf.body('台积电的故事，是"厚积薄发"最完美的现代诠释。')

pdf.bullet('1987年成立时，没有人相信一个纯代工厂的商业模式。张忠谋选择了"不争"——不设计芯片、不与客户竞争，只做制造。这被当时的大多数人视为"不合理"的决定。')
pdf.bullet('前十年（1987-1997）：持续亏损或微利，所有的投入都在积累工艺能力。"合抱之木，生于毫末。"')
pdf.bullet('中间十年（1997-2007）：开始盈利，但仍是"不显眼"的公司。台积电像一个"不争"的君子，静静地建设自己的能力。')
pdf.bullet('后十五年（2007-2022）：从智能手机芯片到AI芯片，台积电成为全球最不可替代的制造平台。"夫唯不争，故天下莫能与之争。"')

pdf.body('投资启示：台积电从创立到成为"天下莫能与之争"的巨头，用了30年。长现投资者的任务，是在第5年就看到第30年。如果你在1990年理解了"制造业的OS升级"，并押注了台积电这个"平台"，你不需要再做出任何其他正确的决定。')

pdf.sub_title('案例二：宁德时代——"顺势而为"的能源变革')

pdf.body('宁德时代的故事，是"顺势而为"的东方战略思想在商业中的完美落地。')

pdf.bullet('2011年成立时，全球动力电池巨头是松下和LG。宁德时代选择了当时被人忽略的赛道——中国新能源汽车政策驱动的本土市场。"求之于势，不责于人。"')
pdf.bullet('早期（2011-2016）：在国内政策支持的"势"中生长。当时全球主流看法是中国电动车是"骗补"，但宁德时代在等待技术成熟。')
pdf.bullet('中期（2017-2022）：技术突破后，顺势扩张。特斯拉的崛起带动了全球电动车势能，宁德时代从中国第一跃升为全球第一。"待时而动。"')
pdf.bullet('当代（2023-2036）：从电池扩展到储能系统、从动力电池到能源基础设施。能源变革的大势远未结束。')

pdf.body('投资启示：宁德时代的崛起不是偶然，是在能源变革的大"势"中做出了正确的战略选择。长现投资者应该寻找的是"下一个宁德时代"——不是在已有的势中追高，而是在新的势尚未被广泛认知时，就已经进入了观势、待时、顺势的循环。')

# ================================================================
# 五、结语
# ================================================================
pdf.ch_title('五、结语：与天地相似')

pdf.quote_card('"易与天地准，故能弥纶天地之道。"',
    'The Book of Changes corresponds to heaven and earth, therefore it can encompass the Way of all.',
    '《周易·系辞上》')

pdf.body('长现框架的核心主张——以30年为尺度做科技金融决策——如果用一句话总结，就是"与天地相似"。')

pdf.body('天地不做短期决策。天地不急。天地不争。天地利万物而不自生。天地以万年为尺度运行着最宏大的"投资组合"——让万物在其中生长、竞争、进化、消亡。')

pdf.body('长现投资者的修炼，就是让自己越来越"与天地相似"：')

pdf.bullet('用30年理解一个技术方向，而不是用30天判断一个K线')
pdf.bullet('追求资本的"厚生"——滋养技术生态，而不是追求资本自身的膨胀')
pdf.bullet('在不被理解的阶段进入，在被追捧的阶段保持清醒')
pdf.bullet('不争做最快的，而争做最久的')

pdf.gold_bar()

pdf.set_font('S', '', 10)
pdf.set_text_color(0x8B, 0x5E, 0x3C)
pdf.multi_cell(pdf.w - 2 * pdf.m, 6.5,
    '长现·常道\n'
    '久远为功，道法自然',
    align='C')
pdf.ln(2)
pdf.set_font('S', '', 9)
pdf.set_text_color(0xAA, 0x99, 0x88)
pdf.multi_cell(pdf.w - 2 * pdf.m, 5.5,
    '邮储银行上海分行科技金融事业部  |  2026年5月\n'
    '思考框架  |  内部参考',
    align='C')

pdf.page_num()

# Save
import os
OUTPUT_DIR = '/Users/cyingfang/WorkBuddy/20260429082054'
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT = os.path.join(OUTPUT_DIR, '长现·常道_东方智慧投资框架.pdf')
pdf.output(OUTPUT)
print(f'Saved: {OUTPUT} | Pages: {pdf.page_no()}')
