#!/usr/bin/env python3
"""不争的自由 —— 老子与伯林两种自由概念的对话 PDF"""

from fpdf import FPDF

SONGTI = '/System/Library/Fonts/Supplemental/Songti.ttc'
HEITI = '/System/Library/Fonts/STHeiti Medium.ttc'


class PDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.add_font('S', '', SONGTI)
        self.add_font('H', '', HEITI)
        self.set_auto_page_break(True, 22)
        self.m = 25
        self.w = 210

    def title_page(self):
        self.add_page()
        self.set_fill_color(0xF8, 0xF5, 0xF0)
        self.rect(0, 0, self.w, 297, 'F')
        self.set_draw_color(0x8B, 0x5E, 0x3C)
        self.set_line_width(0.4)
        cx = self.w / 2
        self.line(self.m, 60, self.w - self.m, 60)
        self.ln(35)
        self.set_font('S', '', 9)
        self.set_text_color(0xAA, 0x99, 0x88)
        self.multi_cell(self.w - 2 * self.m, 6.5, '论 文', align='C')
        self.ln(8)
        self.set_font('H', '', 22)
        self.set_text_color(0x3A, 0x20, 0x10)
        self.multi_cell(self.w - 2 * self.m, 10, '不争的自由', align='C')
        self.ln(4)
        self.set_font('S', '', 12)
        self.set_text_color(0x8B, 0x5E, 0x3C)
        self.multi_cell(self.w - 2 * self.m, 7,
            '——老子"不争"哲学与以赛亚·伯林两种自由概念的对话',
            align='C')
        self.ln(4)
        self.set_draw_color(0x8B, 0x5E, 0x3C)
        self.set_line_width(0.3)
        self.line(cx - 15, self.get_y(), cx + 15, self.get_y())
        self.ln(6)
        self.set_font('S', '', 9)
        self.set_text_color(0x99, 0x88, 0x77)
        self.multi_cell(self.w - 2 * self.m, 6,
            '陈颖芳   |   邮储银行上海分行科技金融事业部\n'
            '2026年5月', align='C')
        self.line(self.m, 235, self.w - self.m, 235)

    def abstract(self, t):
        self.set_font('H', '', 10)
        self.set_text_color(0x3A, 0x20, 0x10)
        self.set_x(self.m)
        self.cell(12, 6.5, '摘要')
        self.set_font('S', '', 9.5)
        self.set_text_color(0x44, 0x33, 0x22)
        self.multi_cell(self.w - 2 * self.m - 12, 6, t, align='J')
        self.ln(3)
        # keywords
        self.set_font('S', '', 9)
        self.set_text_color(0x8B, 0x5E, 0x3C)
        self.set_x(self.m)
        self.cell(self.w - 2 * self.m, 5.5, '关键词：老子 | 不争 | 消极自由 | 积极自由 | 以赛亚·伯林 | 内卷', align='C')

    def section_title(self, num, t):
        self.ln(4)
        self.set_font('H', '', 13)
        self.set_text_color(0x3A, 0x20, 0x10)
        self.set_x(self.m)
        self.cell(self.w - 2 * self.m, 8, f'{num}. {t}')
        self.ln(10)
        self.set_draw_color(0xC9, 0xA8, 0x4C)
        self.set_line_width(0.3)
        self.line(self.m, self.get_y() - 3, self.m + 25, self.get_y() - 3)

    def sub_title(self, t):
        self.set_font('H', '', 10.5)
        self.set_text_color(0x8B, 0x5E, 0x3C)
        self.set_x(self.m)
        self.cell(self.w - 2 * self.m, 7, t)
        self.ln(9)

    def body(self, t):
        self.set_font('S', '', 10)
        self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m)
        self.multi_cell(self.w - 2 * self.m, 6.2, t, align='J')
        self.ln(1.5)

    def quote_block(self, chinese, translation, source):
        """Block quote with original and translation"""
        self.set_fill_color(0xF8, 0xF5, 0xF0)
        self.set_draw_color(0xC9, 0xA8, 0x4C)
        self.set_line_width(0.2)
        y = self.get_y()
        self.set_font('S', '', 10)
        self.set_text_color(0x3A, 0x20, 0x10)
        self.set_x(self.m + 4)
        self.multi_cell(self.w - 2 * self.m - 8, 6.2, chinese, align='J')
        self.ln(2)
        self.set_font('S', '', 9)
        self.set_text_color(0x66, 0x55, 0x44)
        self.set_x(self.m + 4)
        self.multi_cell(self.w - 2 * self.m - 8, 5.5, translation, align='J')
        self.ln(1)
        self.set_font('S', '', 8.5)
        self.set_text_color(0xAA, 0x99, 0x88)
        self.set_x(self.m + 4)
        self.cell(self.w - 2 * self.m - 8, 5, f'—— {source}')
        self.ln(5)
        ny = self.get_y()
        self.rect(self.m, y, self.w - 2 * self.m, ny - y + 1)
        self.set_y(ny + 3)

    def footnote(self, num, t):
        self.set_font('S', '', 8)
        self.set_text_color(0x88, 0x88, 0x88)
        self.set_x(self.m)
        self.multi_cell(self.w - 2 * self.m, 5, f'[{num}] {t}', align='J')
        self.ln(0.5)

    def bullet(self, t):
        self.set_font('S', '', 10)
        self.set_text_color(0x3A, 0x20, 0x10)
        self.set_x(self.m + 4)
        w = self.w - 2 * self.m - 10
        self.cell(5, 6.5, chr(8226))
        self.multi_cell(w, 6.5, t, align='J')
        self.set_x(self.m)
        self.ln(0.5)

    def bold_body(self, t):
        self.set_font('H', '', 10)
        self.set_text_color(0x3A, 0x20, 0x10)
        self.set_x(self.m)
        self.multi_cell(self.w - 2 * self.m, 6.5, t, align='J')
        self.ln(1)

    def gold_bar(self):
        self.set_fill_color(0xC9, 0xA8, 0x4C)
        self.set_draw_color(0xC9, 0xA8, 0x4C)
        self.set_x(self.m)
        self.cell(self.w - 2 * self.m, 0.5, '', fill=True)
        self.ln(3)

    def page_num(self):
        self.set_font('S', '', 8)
        self.set_text_color(0xAA, 0xAA, 0xAA)
        self.set_y(-15)
        self.cell(self.w - 2 * self.m, 5, str(self.page_no()), align='C')


pdf = PDF()
pdf.set_margin(25)

# ================================================================
# TITLE PAGE
# ================================================================
pdf.title_page()

# ================================================================
# ABSTRACT (on title page)
# ================================================================
pdf.ln(8)
pdf.abstract(
    '老子"不争"哲学常被简化为消极退让的处世之道。本文以以赛亚·伯林（Isaiah Berlin）1958年提出的"两种自由概念"为分析框架，'
    '重新审视"夫唯不争，故天下莫能与之争"的深层结构。本文论证："不争"的本质是以赛亚·伯林意义上的"消极自由"——免于被竞争逻辑所强制；'
    '而"天下莫能与之争"则指向一种高阶的"积极自由"——在摆脱竞争束缚后，在自主选择的维度上达到无可替代的境地。'
    '两种自由在老子这里不是对立关系，而是递进与辩证的统一：消极自由是积极自由的前提，'
    '"不争"是"莫能与之争"的基础。这一解读不仅在哲学上揭示了老子思想的现代性，'
    '更在实践上为"内卷"时代的个体提供了一条超越竞争困境的思想路径。')

# ================================================================
# 一、引言
# ================================================================
pdf.add_page()
pdf.section_title('一', '引言：两种自由，一个老子')

pdf.body('1958年10月，以赛亚·伯林在牛津大学发表了他那篇注定成为经典的演讲——《两种自由概念》（Two Concepts of Liberty）。在这篇演讲中，伯林区分了两种根本不同的自由：消极自由（negative liberty），即"免于……的自由"（freedom from），指个人不受他人干涉的领域；积极自由（positive liberty），即"去做……的自由"（freedom to），指个人成为自己主人的自主状态。¹')

pdf.body('伯林的区分迅速成为政治哲学的核心议题，但他本人可能没有预料到，这一分析框架可以被用来重新理解——甚至重新发现——一个古老的东方思想。')

pdf.body('两千五百年前，老子在《道德经》中留下了这样一段话：')

pdf.quote_block(
    '"夫唯不争，故天下莫能与之争。"',
    '"Because he does not contend, no one in the world can contend with him."',
    '《道德经》第二十二章')

pdf.body('这段话在中国思想史上被无数次引用，但其确切含义从未被充分澄清。最常见的理解是将其简化为一种"以退为进"的策略——不与人争，反而没有人能与你争，这是以退为进的权谋之术。这一解读将老子降格为马基雅维利式的谋略家，是对其哲学深度的极大矮化。')

pdf.body('本文试图证明："不争"与"莫能与之争"之间的关系，恰恰是伯林意义上消极自由与积极自由之间关系的东方表达。老子不是在教授一种获胜的技巧，而是在揭示一个关于自由的哲学真理：真正的自由始于摆脱竞争逻辑的强制（消极自由），终于在自己选择的维度上达到不可替代的境地（积极自由）。两种自由不是对立的——在老子这里，它们是同一个运动过程的两个环节。')

pdf.footnote('1', 'Isaiah Berlin, "Two Concepts of Liberty," in Four Essays on Liberty (Oxford: Oxford University Press, 1969), pp. 118-172.')

pdf.footnote('2', '本文所引《道德经》原文均据王弼本。英译为作者结合多种通行英译本的自译，力求准确传达原意而非文学优美。')

# ================================================================
# 二、不争作为消极自由
# ================================================================
pdf.add_page()
pdf.section_title('二', '"不争"即消极自由')

pdf.sub_title('2.1 消极自由的本质')

pdf.body('伯林对消极自由的定义是："一个人能够不被他人阻碍地行动的领域。如果别人阻止我做我本来能够做的事，那么我就是不自由的；如果我的不被干涉的行动的领域被别人挤压到某种最低限度，那么我就是被强制的。"³ 消极自由的核心是"免于强制"——特别是免于被他人意志所支配。')

pdf.body('消极自由不回答"我应该做什么"的问题，它只回答"谁在决定我做什么"。只要决定权在我自己手中——即使我做了一个糟糕的决定——我就拥有消极自由。伯林深刻地指出，消极自由的价值不在于它能带来好的结果，而在于它是人之为人所不可或缺的自主空间。')

pdf.sub_title('2.2 "不争"作为免于竞争逻辑的强制')

pdf.body('将伯林的框架应用于老子，"不争"首先应当被理解为一种消极自由——免于被竞争逻辑所强制。')

pdf.body('老子所处的春秋战国时代，"争"是生存的常态。诸侯争霸、士人争名、商人争利——竞争逻辑渗透到社会的每一个毛孔。在这个语境中，"争"不仅仅是一种行为选择，更是一种社会强制力。你不争，别人会争；你退出，别人会占据。竞争逻辑的可怕之处在于，它用"不争就会失去一切"的恐惧来支配每一个人。')

pdf.body('老子在第八十一章中写道：')

pdf.quote_block(
    '"圣人不积，既以为人己愈有，既以与人己愈多。天之道，利而不害；圣人之道，为而不争。"',
    '"The sage does not hoard. Having given all to others, he has more; having given all to others, he is richer. The Way of heaven benefits without harming. The Way of the sage acts without contending."',
    '《道德经》第八十一章')

pdf.body('注意"为而不争"（acts without contending）——老子没有说"不为"，他说的是"为而不争"。"为"是行动，"争"是竞争。两者的区别在于：行动是我按照自己的意愿做事，竞争是按照他人的游戏规则做事。当一个人"争"时，他的行动逻辑是由对手定义的；当一个人"为"时，他的行动逻辑是由自己定义的。')

pdf.body('这正是消极自由的核心。当你"不争"时，你不是不行动，而是拒绝让竞争逻辑定义你的行动。你收回了对自己行动的主权——我的行动不再取决于别人做什么，而是取决于我自己要什么。')

pdf.sub_title('2.3 不争作为"免于干涉"')

pdf.body('老子在第六十六章进一步阐述了这一思想：')

pdf.quote_block(
    '"江海所以能为百谷王者，以其善下之，故能为百谷王。……以其不争，故天下莫能与之争。"',
    '"The reason the river and sea can be king of all valleys is that they excel at being lower than them. …… Because they do not contend, no one in the world can contend with them."',
    '《道德经》第六十六章')

pdf.body('江海"不争"的方式是"善下之"——处众人之所恶。它不是不作为，而是选择了一个不被竞争逻辑覆盖的位置。当所有人都争着往高处走时，江海选择了低处。这个选择本身就是一种消极自由的行使——摆脱了"向上竞争"的强制。')

pdf.body('老子在第三章中说得更为直接：')

pdf.quote_block(
    '"不尚贤，使民不争。不贵难得之货，使民不为盗。不见可欲，使民心不乱。"',
    '"Do not exalt the worthy, and the people will not contend. Do not value rare goods, and the people will not steal. Do not display what is desirable, and the people\'s hearts will not be disturbed."',
    '《道德经》第三章')

pdf.body('这里的"不尚贤"是一个极其深刻的洞察。"尚贤"——推崇贤能——看似公平，实际上制造了一种新的强制。当社会开始推崇某种品质（贤能、财富、地位）时，人们被迫去争夺这种品质的认可。"尚贤"把"争"从外部强制内化为了自我强制。老子看穿了这一点：消除竞争的根源，不是靠压制竞争行为，而是靠消除"尚"——消除对那些诱发竞争的价值标准的崇拜。')

pdf.body('这恰恰是伯林消极自由概念的极致表达。消极自由追求的是"最小化的强制领域"——一个不受外部意志支配的空间。老子将这种强制追溯到"尚"——社会对某些价值的推崇本身就是一种强制，因为它定义了什么是"值得追求的"，从而限定了人的行动方向。')

pdf.footnote('3', 'Isaiah Berlin, "Two Concepts of Liberty," p. 122.')

# ================================================================
# 三、莫能与之争作为积极自由
# ================================================================
pdf.add_page()
pdf.section_title('三', '"莫能与之争"即积极自由')

pdf.sub_title('3.1 积极自由的本质')

pdf.body('伯林对积极自由的定义是："成为自己的主人。我希望我的生活和决定取决于我自己，而不是取决于任何外部力量。我希望成为我自己的工具，而不是他人意志的工具。我希望成为一个主体，而不是一个客体。"⁴ 积极自由的核心是"自主"——不仅仅是免于外部干预，而是真正成为自己行动的主宰。')

pdf.body('与消极自由不同，积极自由追问"我应该做什么"和"我想成为什么"。它不仅仅是摆脱了什么，更是实现了什么。伯林对积极自由持深刻的怀疑态度，因为他担忧"成为自己的主人"可能异化为"成为更理性（或更正确）的自我的仆人"——即黑格尔-马克思传统中的"积极自由"可能被极权主义利用。')

pdf.body('但伯林的担忧不应让我们忽视积极自由的合理内核：自主选择和自我实现的自由。而这恰恰是"天下莫能与之争"所指向的境地。')

pdf.sub_title('3.2 "莫能与之争"作为自主性')

pdf.body('"天下莫能与之争"常被理解为一种竞争的胜利——你赢了，赢到没有人能与你竞争。这种理解仍然是"争"的逻辑，只是换了一种方式。')

pdf.body('但老子的逻辑恰恰相反。"莫能与之争"不是一个竞争的结果，而是一个"不竞争"的结果。它不是"我赢了所有人"，而是"我不在任何人竞争的维度上"。当你不参与比赛时，你不可能输，但也无所谓"赢"——你只是不在那个游戏里。')

pdf.body('这是更高阶的自主性。积极自由意味着选择自己的游戏规则，而不是在别人设定的规则中获胜。"莫能与之争"描述了这样一种状态：一个人已经摆脱了竞争逻辑的束缚，完全按照自己的意志行动，以至于没有人可以在"他的维度"上与他竞争——因为那个维度是他自己所定义的。')

pdf.body('第七十七章提供了一个形象的例证：')

pdf.quote_block(
    '"天之道，其犹张弓与？高者抑之，下者举之；有余者损之，不足者补之。天之道，损有余而补不足。人之道则不然，损不足以奉有余。"',
    '"The Way of heaven — is it not like drawing a bow? The high is brought down, the low is raised up. What is excessive is reduced, what is insufficient is supplemented. The Way of heaven reduces excess and supplements insufficiency. The way of humans is not like this — it reduces the insufficient to serve the excessive."',
    '《道德经》第七十七章')

pdf.body('"人之道"就是竞争的逻辑：强者愈强、弱者愈弱——成功吸引更多成功，失败导致更多失败。而"天之道"是反竞争的：在高处的东西会被压低，在低处的东西会被抬高。老子认为，"人之道"是对"天之道"的偏离，而真正的自主——真正的自由——在于回归"天之道"。')

pdf.body('这里的"天之道"可以理解为一种"自然自由"——不是与他人的比较中获得的自由，而是在与自然的一致中获得的自在。"莫能与之争"不是因为没有对手，而是因为对手这个概念本身已经消失了。')

pdf.sub_title('3.3 从"无为"到"无不为"')

pdf.body('"无为而无不为"（第四十八章）是老子哲学的另一个核心命题。它与"不争而莫能与之争"是同一个结构：')

pdf.quote_block(
    '"无为而无不为。取天下常以无事，及其有事，不足以取天下。"',
    '"Non-action, yet nothing is left undone. To take hold of the world, always act from non-interference; when there is interference, it is not enough to take hold of the world."',
    '《道德经》第四十八章')

pdf.body('这里的"无为"不是什么事都不做，而是"不人为地干预"——不把自己的意志强加于事物的自然进程。"无不为"不是什么事都做了，而是"没有什么是做不成的"。')

pdf.body('以伯林的概念框架来理解："无为"是消极自由——免于人为干预的冲动（免于"妄为"的自由）；"无不为"是积极自由——在顺应自然的过程中成就一切的能力。消极自由为积极自由提供了条件：只有当你停止强行干预事物的自然进程时，你才能让事物的潜能充分实现。')

pdf.body('这与"不争而莫能与之争"完全同构。"不争"（消极自由）为"莫能与之争"（积极自由）提供了条件。这不是一个悖论，而是一个深刻的哲学洞见：真正的积极自由（自主性的充分实现）必须以消极自由（免于外部强制）为前提。没有消极自由作为基础的"积极自由"，不过是在一种强制下选择了另一种强制——从一个游戏规则跳入了另一个游戏规则。')

pdf.footnote('4', 'Isaiah Berlin, "Two Concepts of Liberty," p. 131.')

# ================================================================
# 四、辩证统一
# ================================================================
pdf.add_page()
pdf.section_title('四', '辩证统一：两种自由的圆融')

pdf.sub_title('4.1 伯林的困境与老子的解答')

pdf.body('伯林的核心担忧是：积极自由容易被滥用。当一个人说"我想成为自己的主人"时，很容易演变成"我的‘理性自我’应该统治我的‘冲动自我’"——而这个"理性自我"最终可能被外部的权威（国家、党派、意识形态）所代言。这就是伯林所说的"积极自由的倒置"：追求自主反而导致了最彻底的奴役。')

pdf.body('因此，伯林认为消极自由与积极自由之间存在一种紧张关系。他倾向于消极自由，认为它更安全——它不追问"什么是好的生活"，只守卫"我不被干涉的领域"。')

pdf.body('老子提供了一个超越伯林困境的路径。在老子这里，消极自由与积极自由不是两个需要平衡的紧张概念，而是同一个过程的前后环节：')

pdf.body('"不争"（消极自由）→ "莫能与之争"（积极自由）')

pdf.body('这个序列的关键在于：积极自由不是消极自由的"对立面"或"补充"，而是消极自由的自然结果。当你真正实践了"不争"——彻底摆脱了竞争逻辑的强制——你自然就进入了"莫能与之争"的境界。你不需要"去追求"自主性，自主性是在你放弃竞争的那一刻自动到来的。')

pdf.body('这就是"无为而无不为"的深层含义。你不必"去做"一切——你"不做"（不妄为、不争）之后，一切自然成就。')

pdf.sub_title('4.2 "上善若水"：两种自由的统一')

pdf.quote_block(
    '"上善若水。水善利万物而不争，处众人之所恶，故几于道。"',
    '"The supreme good is like water. Water benefits all things without contending, and stays in places that others disdain — therefore it is close to the Way."',
    '《道德经》第八章')

pdf.body('水是老子哲学中最重要的意象。水"不争"——它不与万物竞争，不争高、不争先、不争强。但水"利万物"——它是积极的、给予的、滋养的。在"不争"（消极自由）中，水实现了"利万物"（积极自由）。')

pdf.body('水"处众人之所恶"——它处在被鄙视的低处。这是消极自由的极端表达：不仅不参与游戏，而且不在游戏的任何位置上。但恰恰是这种彻底的退出，使水成为了"几于道"的存在——接近了最根本的自由。')

pdf.body('在水这里，消极自由与积极自由的统一是如此完美，以至于区分本身都失去了意义。水的自由不是"免于什么"或"去做什么"，而是一种存在的状态。')

pdf.sub_title('4.3 从对立到圆融')

pdf.body('如果将伯林和老子视为一场跨越两千五百年的对话，我们可以说：伯林犀利地诊断了两种自由的紧张关系，但他没有提供一个解决方案。而他给出的方案——偏重消极自由——实际上也是一种选择，不是真正的超越。')

pdf.body('老子提供的方案则是：将两种自由视为同一运动的两个环节。消极自由不是终点，而是进入真正积极自由的必经之路。积极自由不是消极自由的否定，而是它的完成。')

pdf.body('这意味着：')

pdf.bullet('你不必在"不争"和"争"之间二选一')
pdf.bullet('你也不必在"消极"和"积极"之间寻找平衡')
pdf.bullet('你需要做的是：先"不争"——彻底摆脱竞争逻辑的强制')
pdf.bullet('然后——在"不争"的基础上——在任何你自主选择的维度上达到"莫能与之争"')

pdf.body('这就是"不争的自由"的完整意义：它不是消极退缩的自由，也不是积极进取的自由，而是从消极自由上升到积极自由的完整过程。')

# ================================================================
# 五、现代启示
# ================================================================
pdf.add_page()
pdf.section_title('五', '现代启示：从"内卷"到"不争的自由"')

pdf.sub_title('5.1 "内卷"作为积极自由的暴政')

pdf.body('2020年以来，"内卷"一词在中国社会引起广泛共鸣。内卷描述的是这样一种困境：在资源有限、竞争者众多的系统中，个体必须投入越来越多的努力才能维持原有的位置——结果是所有人都在拼命，但没有人因此受益。')

pdf.body('从伯林的角度看，内卷是一种典型的消极自由的丧失。"卷"的强制力来自系统本身——你不"卷"，别人会"卷"，你就会被淘汰。你已经没有"不参与"的选择了。')

pdf.body('而从老子的角度看，内卷更深层的问题是"尚"——社会对某些价值（学历、职位、财富）的过度推崇。这些被推崇的价值成为了一根指挥棒，所有人的努力都被引导到了同一个方向上。竞争越激烈，指挥棒的力量就越强；指挥棒的力量越强，个体的自主性就越弱。')

pdf.body('内卷是一个关于"积极自由的暴政"的当代案例。当一群人都在追求同一个被社会定义的目标时，他们看似在"积极进取"，实际上每一个"积极"的行为都是在强化那个压迫自己的系统。这就是伯林所警示的"积极自由的倒置"。')

pdf.sub_title('5.2 老子对"内卷"的批判')

pdf.body('老子对"尚贤"的批判，是对内卷最深刻的理论回应。他说"不尚贤，使民不争"——这八个字如果展开，是一个完整的社会批判理论：')

pdf.body('社会定义了"贤"的标准（好大学、好工作、好收入）→ 人们被引导去追求这个标准 → 在追求中，人们失去了对自己生活的定义权 → 人们"自愿"地接受了竞争逻辑的统治 → 人们"积极"地参与了对自己的压迫。')

pdf.body('破解之道不是"更努力地卷"，而是"不尚贤"——质疑那些被社会奉为圭臬的价值标准。这不是否定努力的价值，而是重新定义什么值得努力。')

pdf.sub_title('5.3 实践路径：从消极自由到积极自由')

pdf.body('在"内卷"时代实践"不争的自由"，可以分为三步：')

pdf.bold_body('第一步：识"尚"（认识强制）')
pdf.body('识别出那些你以为是"自己的目标"、实则是社会强加给你的价值标准。这是消极自由的第一步——知道自己被什么所强制。')

pdf.bold_body('第二步：解"争"（退出游戏）')
pdf.body('在有意识地选择之后，退出某些你本不想参与但被卷入的竞争。这可能意味着放弃某些被社会认可的"成功路径"。这是消极自由的实践——收缩"被强制"的领域，扩大"自主选择"的领域。')

pdf.bold_body('第三步：立"己"（重新定义）')
pdf.body('在摆脱了竞争逻辑的强制之后，在自己真正认同和热爱的维度上建立自己的标准。这不是在另一个赛道上继续竞争，而是在自己定义了"胜负"的领域中按照自己的节奏行动。这是积极自由的实现。')

pdf.body('这三步恰好对应了老子的"不争"→"莫能与之争"的辩证结构，也对应了伯林的消极自由→积极自由的分析框架。它们不是线性的三个阶段，而是一个持续的循环——在不断的解构和重建中维持个人的自主性。')

# ================================================================
# 六、结语
# ================================================================
pdf.add_page()
pdf.section_title('六', '结论')

pdf.body('本文以以赛亚·伯林的两种自由概念为分析框架，重新审视了老子"夫唯不争，故天下莫能与之争"的哲学内涵。本文的核心论点是：')

pdf.body('第一，"不争"的本质是伯林意义上的"消极自由"——免于被竞争逻辑所强制。老子所批判的"争"不是行动本身，而是行动被外部标准所定义的状态。老子的"不争"不是不行动，而是收回对自己行动的定义权——这正是消极自由的核心。')

pdf.body('第二，"天下莫能与之争"的本质是伯林意义上的"积极自由"——在摆脱外部强制之后，在自主选择的维度上实现自身的潜能。它不是竞争性的胜利，而是对竞争框架本身的超越。')

pdf.body('第三，在老子这里，消极自由与积极自由不是伯林所担忧的对立关系，而是一个辩证统一的运动过程。"不争"是"莫能与之争"的前提，"无为"是"无不为"的基础。这个结构表明，在老子看来，真正的积极自由只能以消极自由为基础——离开消极自由的"积极自由"只是换了一种形式的奴役。')

pdf.body('这一解读的意义在于：')

pdf.bullet('在哲学层面，它为伯林两种自由概念的紧张关系提供了一个东方的解决方案——这个方案不是"平衡"或"调和"，而是对两种自由的内在统一的揭示')
pdf.bullet('在实践层面，它为"内卷"时代的个体提供了一条超越之道——不是"更努力地卷"，而是先退出竞争逻辑的强制，再在自己选择的维度上追求卓越')
pdf.bullet('在跨文化对话层面，它展示了中国传统哲学与现代西方政治哲学之间的可对话性——老子不是博物馆里的古董，他关于自由的思考与伯林一样深刻、一样现代')

pdf.body('回到本文开篇的那句话：')

pdf.set_fill_color(0xF8, 0xF5, 0xF0)
pdf.set_font('S', '', 10)
pdf.set_text_color(0x3A, 0x20, 0x10)
pdf.set_x(pdf.m + 4)
pdf.multi_cell(pdf.w - 2 * pdf.m - 8, 6.2,
    '"夫唯不争，故天下莫能与之争。"',
    align='J')
pdf.ln(2)
pdf.set_font('S', '', 9)
pdf.set_text_color(0x66, 0x55, 0x44)
pdf.set_x(pdf.m + 4)
pdf.multi_cell(pdf.w - 2 * pdf.m - 8, 5.5,
    '翻译成伯林的语言，就是：只有当你摆脱了竞争逻辑的强制（消极自由），你才有可能在真正属于自己的维度上达到无可替代的境地（积极自由）。',
    align='J')

pdf.body('这不是一种策略。这是一个关于自由的哲学真理。')

pdf.ln(5)
pdf.gold_bar()

pdf.set_font('S', '', 9)
pdf.set_text_color(0x8B, 0x5E, 0x3C)
pdf.multi_cell(pdf.w - 2 * pdf.m, 6,
    '参考文献\n\n'
    '[1] Berlin, Isaiah. "Two Concepts of Liberty." In Four Essays on Liberty. Oxford: Oxford University Press, 1969.\n'
    '[2] 王弼注.《老子道德经注》. 楼宇烈校释. 北京: 中华书局, 2008.\n'
    '[3] 陈鼓应.《老子注释及评介》. 北京: 中华书局, 1984.\n'
    '[4] Berlin, Isaiah. Liberty. Edited by Henry Hardy. Oxford: Oxford University Press, 2002.\n'
    '[5] 刘笑敢.《老子古今》. 北京: 中国社会科学出版社, 2006.\n'
    '[6] 冯友兰.《中国哲学简史》. 北京: 北京大学出版社, 2013.',
    align='J')

pdf.page_num()

# Save
import os
OUTPUT_DIR = '/Users/cyingfang/WorkBuddy/20260429082054'
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT = os.path.join(OUTPUT_DIR, '不争的自由_老子与伯林两种自由概念的对话.pdf')
pdf.output(OUTPUT)
print(f'Saved: {OUTPUT} | Pages: {pdf.page_no()}')
