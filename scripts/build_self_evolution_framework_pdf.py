#!/usr/bin/env python3
"""自演化 Self-Evolution —— 未来10年科技投资思维框架 PDF"""

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
        self.set_fill_color(0x0E, 0x2D, 0x40)
        self.rect(0, 0, self.w, 297, 'F')
        self.ln(40)
        self.set_font('H', '', 11)
        self.set_text_color(0xE8, 0x8D, 0x3F)
        self.multi_cell(self.w - 2 * self.m, 8, 'S E L F - E V O L U T I O N', align='C')
        self.ln(6)
        self.set_font('H', '', 30)
        self.set_text_color(0xFF, 0xFF, 0xFF)
        self.multi_cell(self.w - 2 * self.m, 13, main, align='C')
        self.ln(4)
        self.set_font('S', '', 12)
        self.set_text_color(0xCC, 0xDD, 0xEE)
        self.multi_cell(self.w - 2 * self.m, 7, sub, align='C')
        self.ln(3)
        self.set_draw_color(0xE8, 0x8D, 0x3F)
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
        self.set_text_color(0x0E, 0x2D, 0x40)
        self.set_x(self.m)
        self.cell(self.w - 2 * self.m, 10, t)
        self.ln(11)
        self.set_draw_color(0xE8, 0x8D, 0x3F)
        self.set_line_width(0.5)
        self.line(self.m, self.get_y() - 3, self.m + 32, self.get_y() - 3)
        self.ln(5)

    def sub_title(self, t):
        self.set_font('H', '', 12)
        self.set_text_color(0x1B, 0x5E, 0x8A)
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

    def quote_box(self, t):
        self.set_fill_color(0xF5, 0xF5, 0xFA)
        self.set_draw_color(0xE8, 0x8D, 0x3F)
        self.set_line_width(0.3)
        x, y = self.get_x(), self.get_y()
        self.set_font('S', '', 9)
        self.set_text_color(0x55, 0x55, 0x77)
        self.set_x(self.m + 3)
        self.multi_cell(self.w - 2 * self.m - 6, 5.5, t, align='J')
        ny = self.get_y()
        self.rect(self.m, y, self.w - 2 * self.m, ny - y + 1)
        self.set_y(ny + 3)

    def domain_box(self, num, name, icon, desc, examples):
        """四大自演化域统一模板"""
        self.set_fill_color(0xF2, 0xF5, 0xFA)
        self.set_draw_color(0xCC, 0xCC, 0xDD)
        self.set_line_width(0.2)
        x, y = self.get_x(), self.get_y()
        self.set_font('H', '', 12)
        self.set_text_color(0x0E, 0x2D, 0x40)
        self.set_x(self.m + 3)
        self.cell(6, 6, str(num))
        self.cell(self.w - 2 * self.m - 12, 6, f'{name} / {icon}')
        self.ln(8)
        self.set_font('S', '', 9.5)
        self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m + 3)
        self.multi_cell(self.w - 2 * self.m - 6, 5.5, desc, align='J')
        self.ln(2)
        self.set_font('S', '', 8.5)
        self.set_text_color(0x77, 0x77, 0x99)
        self.set_x(self.m + 3)
        self.cell(self.w - 2 * self.m - 6, 5, f'示例：{examples}')
        self.ln(7)
        ny = self.get_y()
        self.rect(self.m, y - 1, self.w - 2 * self.m, ny - y + 1)
        self.set_y(ny + 3)

    def insight_box(self, t):
        self.set_fill_color(0x0E, 0x2D, 0x40)
        self.set_text_color(0xFF, 0xFF, 0xFF)
        self.set_font('S', '', 9.5)
        y = self.get_y()
        self.set_x(self.m + 3)
        self.multi_cell(self.w - 2 * self.m - 6, 6, t, align='J')
        ny = self.get_y()
        # Fill behind
        self.set_fill_color(0x0E, 0x2D, 0x40)
        # Use set_y and rect
        self.set_y(y - 1)
        # Just do a simpler approach
        self.set_fill_color(0x0E, 0x2D, 0x40)
        # Re-draw
        self.set_font('S', '', 9.5)
        self.set_text_color(0xFF, 0xFF, 0xFF)
        self.set_x(self.m + 3)
        self.multi_cell(self.w - 2 * self.m - 6, 6, t, align='J')
        self.set_text_color(0x33, 0x33, 0x33)
        self.set_y(ny + 4)

    def gold_bar(self):
        self.set_draw_color(0xE8, 0x8D, 0x3F)
        self.set_line_width(0.4)
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
    '自演化  投资框架',
    'Self-Evolution — 人类掌控自身演化的能力正在指数级增长',
    '邮储银行上海分行科技金融事业部  |  2026年5月')

# ================================================================
# 引言
# ================================================================
pdf.ch_title('引言：拐点已至')

pdf.body('2026-2036年，将是人类文明的一个分水岭。不是因为某个单一技术的突破，而是因为多个领域的同时爆发正在汇聚成一个前所未有的趋势：人类正在获得掌控自身演化的能力。')

pdf.body('这不是一个比喻。在生物学层面，CRISPR基因编辑、细胞重编程、mRNA平台让我们从"读取生命代码"进化为"编写生命代码"。在认知层面，AI从工具变为伙伴，脑机接口从实验走向临床，人类智能正在被技术扩展。在数字层面，AI Agent、数字孪生、个人AI正在创造前所未有的自我延伸。')

pdf.body('这三个方向——生物、认知、数字——不是平行发生的。它们正在加速汇合，形成一个递归增强的飞轮：AI加速生物发现，生物发现增强人类能力，更强的人类创造更强的AI。')

pdf.gold_bar()
pdf.quote_box('"未来10年最深刻的变革不是我们用什么工具，而是我们在成为什么。"')

# ================================================================
# 一、哲学理念
# ================================================================
pdf.ch_title('一、哲学理念：自演化')

pdf.sub_title('1.1 从"被演化"到"自演化"')

pdf.body('38亿年的地球上，演化一直是"盲人"。自然选择没有方向、没有意图、没有设计者。基因突变是随机的，适者生存是无情的。人类之所以独特，是因为我们第一次发展出了理解演化机制的心智能力。')

pdf.body('2026-2036年的历史意义在于：我们正在跨越从"理解演化"到"主导演化"的门槛。这个转变发生在三个层次：')

pdf.bullet('生物层次：CRISPR让我们编辑基因，细胞重编程让我们逆转衰老，合成生物让我们设计新生命形式——我们从生命"读者"变为生命"作者"')
pdf.bullet('认知层次：AI不仅增强我们的思考，还在改变思考本身的结构——我们从工具用户变为人机共生体')
pdf.bullet('社会层次：集体智能、AI治理、去中心化协作——我们从被动承受社会演化转变为主动设计社会形态')

pdf.sub_title('1.2 指数增长的根本原因')

pdf.body('为什么是"指数级"？因为自演化具有递归结构：')

pdf.bullet('AI帮助设计更好的AI（AutoML、RLHF）→ 技术进步速度自我加速')
pdf.bullet('AI加速生物发现（AlphaFold、蛋白质设计）→ 生物技术突破加速')
pdf.bullet('生物技术增强人类能力（脑机接口、基因编辑）→ 人类创新速度加速')
pdf.bullet('更强的人类创造更强的AI → 飞轮闭环')

pdf.body('传统的"S曲线"思维在此失效。自演化不是一个行业或一个技术方向的增长，而是文明底层操作系统的升级。')

pdf.sub_title('1.3 三条信念')

pdf.bold_body('信念一：编程语言变了——从Python到DNA到神经突触')
pdf.body('未来10年最重要的编程语言可能不是Python，而是DNA碱基序列和神经连接组。理解"如何编程生物"比"如何编程软件"更具长期价值。')

pdf.bold_body('信念二：平台 > 应用')
pdf.body('在每一次自演化浪潮中，底层平台比顶层应用更具投资价值。CRISPR是基因编辑的平台，Transformer是AI的平台，BCI是人机融合的平台。')

pdf.bold_body('信念三：10年后的稀缺不再是信息，而是注意力、健康和自我认同')
pdf.body('当AI可以生成无限内容和代码时，人类独有的价值在于：持续的健康状态、深度专注的能力、清晰的自我认知。自演化投资本质上是对"人类独特性"的信仰。')

# ================================================================
# 二、方法论
# ================================================================
pdf.ch_title('二、方法论：四步聚焦')

pdf.body('自演化框架的方法论围绕一个核心问题展开："在人类掌控自身演化的能力中，哪一层正在跨越从‘实验室验证’到‘商业可行’的门槛？"')

steps = [
    ('Step 1 — 扫描（Scan）', '识别正在从"实验室→临床/商用"的技术', '关注 Nature/Science/Cell 顶刊、FDA 批准、中国NMPA审批。不问"什么技术最酷"，问"哪个方向正在从可能变为可行"。'),
    ('Step 2 — 定位（Orient）', '判断属于哪个自演化层次', '将技术归入四大域：生物自演化 / 认知自演化 / 数字自演化 / 社会自演化。不同层次的风险曲线和投资逻辑不同。'),
    ('Step 3 — 分层（Layer）', '区分平台层和应用层', '平台层（工具/基础设施）具有跨周期的抗风险能力。应用层（产品/服务）爆发力强但更替快。投资组合需双层配置。'),
    ('Step 4 — 持有（Hold）', '等待递归飞轮加速', '自演化技术的价值释放不是线性的——飞轮一旦启动，加速会超预期。过早退出是最大的机会成本。'),
]

for i, (title, subtitle, desc) in enumerate(steps):
    pdf.set_fill_color(0xF8, 0xF8, 0xFC) if i % 2 == 0 else pdf.set_fill_color(0xFF, 0xFF, 0xFF)
    y0 = pdf.get_y()
    pdf.set_font('H', '', 10)
    pdf.set_text_color(0x0E, 0x2D, 0x40)
    pdf.set_x(pdf.m + 2)
    pdf.cell(6, 6, f'{i+1}')
    pdf.cell(pdf.w - 2 * pdf.m - 8, 6, title)
    pdf.ln(6)
    pdf.set_font('S', '', 9)
    pdf.set_text_color(0x1B, 0x5E, 0x8A)
    pdf.set_x(pdf.m + 10)
    pdf.cell(pdf.w - 2 * pdf.m - 12, 5.5, subtitle)
    pdf.ln(6)
    pdf.set_font('S', '', 8.5)
    pdf.set_text_color(0x55, 0x55, 0x55)
    pdf.set_x(pdf.m + 10)
    pdf.multi_cell(pdf.w - 2 * pdf.m - 12, 5.5, desc, align='J')
    pdf.ln(3)

pdf.gold_bar()
pdf.quote_box('方法论的关键：所有技术都指向同一个方向——人类更深入地掌控自身的生命、认知和存在方式。这四个步骤是帮你找到"在正确的时间点，站在正确的层次上"。')

# ================================================================
# 三、框架
# ================================================================
pdf.ch_title('三、框架：四大自演化域')

pdf.body('自演化框架将未来10年的科技突破归纳为四个相互关联的领域。每个域代表人类掌控自身演化的一个维度，它们正在以不同的速度但相同的方向前进。')

pdf.gold_bar()

pdf.domain_box(1, '生物自演化', '🧬',
    '我们从"读基因"进化为"写基因"。2023-2025年，CRISPR疗法开始获批（Casgevy治疗镰状细胞），mRNA平台验证了"快速编程生命"的可行性。未来10年的关键跳跃：',
    'CRISPR Therapeutics (编辑治疗)、Moderna/BioNTech (mRNA平台)、Altos Labs (细胞重编程)、Illumina (测序平台)')

pdf.domain_box(2, '认知自演化', '🧠',
    'AI从"工具"进化为"认知伴侣"。2024-2026年，AI Agent 和多模态模型已改变工作方式；脑机接口（Neuralink、Synchron）开始人体试验。未来10年的关键跳跃：',
    'OpenAI/Google DeepMind (基础模型)、Neuralink/Synchron (BCI)、Apple/Meta (空间计算+AI)、Anthropic (AI安全+对齐)')

pdf.domain_box(3, '数字自演化', '💻',
    '每个人都将拥有"数字分身"——个性化的AI Agent管理信息流、执行任务、代表你进行交互。这是"自我"在数字空间的延伸。未来10年的关键跳跃：',
    'Microsoft Copilot、Google Gemini、Character.AI、数字孪生平台')

pdf.domain_box(4, '社会自演化', '🌐',
    'AI正在改变人类协作的方式：从"层级组织"到"网络化协作"，从"中心化决策"到"AI辅助共识"。DAO、AI中介的治理、算法匹配的劳动力市场——社会形态本身正在成为设计对象。未来10年的关键跳跃：',
    '治理技术平台、AI调解系统、去中心化科学(DeSci)、全球协作基础设施')

# ================================================================
# 四、递归飞轮
# ================================================================
pdf.ch_title('四、递归飞轮：自演化的加速机制')

pdf.body('四大自演化域不是独立运行的。它们形成一个递归飞轮，每一层的输出都是下一层的输入：')

pdf.set_font('S', '', 9.5)
pdf.set_text_color(0x33, 0x33, 0x33)

# Flywheel visualization
flywheel = [
    'AI 加速生物发现       (AI → 蛋白质折叠/药物设计/基因编辑)',
    '            ↓',
    '生物增强人类认知       (基因编辑抗衰老 → 大脑更健康 → 认知能力提升)',
    '            ↓',
    '更强认知创造更强 AI   (更好的算法/更大的模型/更优的架构)',
    '            ↓',
    'AI 再度加速生物发现   (飞轮循环加速)',
]

for line in flywheel:
    pdf.set_font('S', '', 9)
    pdf.set_text_color(0x0E, 0x2D, 0x40) if '↓' not in line else pdf.set_text_color(0xE8, 0x8D, 0x3F)
    pdf.set_x(pdf.m + 5)
    pdf.cell(pdf.w - 2 * pdf.m - 10, 6.5, line)
    pdf.ln()

pdf.ln(3)
pdf.body('这个飞轮的每一轮循环都在加速。因为AI自身的进步也在加速（硬件改进 + 算法改进 + 数据飞轮），所以由AI驱动的生物发现和认知增强也在加速。')

pdf.insight_box('核心洞见：自演化框架的投资逻辑不是"押注单一技术"，而是"做多整个递归飞轮"。只要飞轮在转，每一个域中都会持续产生投资机会。飞轮一旦启动，很难停下来。')

# ================================================================
# 五、案例
# ================================================================
pdf.ch_title('五、深度案例')

pdf.sub_title('案例一：mRNA平台——编程生命的"编译器"')

pdf.body('mRNA疫苗在2020年证明了"快速编程生命"的可行性。但这不是终点，而是起点。')
pdf.bullet('2023-2025：mRNA技术从COVID扩展到流感、RSV、癌症疫苗')
pdf.bullet('2026-2028：个性化癌症mRNA疫苗进入主流治疗（Moderna/Merck的mRNA-4157）')
pdf.bullet('2029-2032：mRNA从"疫苗"进化为"治疗平台"——罕见病、自身免疫、再生医学')
pdf.bullet('投资启示：mRNA不是一种药物，而是一个"编译器"——输入抗原序列，输出免疫响应。平台价值远大于单个产品。')

pdf.sub_title('案例二：AI Agent——认知的"外挂硬盘"')

pdf.body('2024年是AI Agent元年，但真正的影响在10年后。')
pdf.bullet('2024-2026：单任务Agent（代码生成、客服、数据分析）')
pdf.bullet('2027-2029：多Agent协作系统（企业运营的AI中台）')
pdf.bullet('2030-2036：个人AI Agent成为"数字自我"——管理日程、财务、健康、社交')
pdf.bullet('投资启示：Agent基础设施（记忆系统、工具调用、安全框架）比Agent应用本身更有长期价值。')

pdf.sub_title('案例三：CRISPR 3.0——从"编辑"到"编程"')

pdf.body('第一代CRISPR（2012-2020）证明了基因编辑的可行性。第二代（2020-2026）进入了临床。第三代（2026-2036）将从根本上改变我们与基因的关系。')
pdf.bullet('2024：Casgevy（镰状细胞病）获批——CRISPR疗法的里程碑')
pdf.bullet('2026-2030：体内编辑（in vivo）取代体外编辑——无需取出细胞，直接体内修复')
pdf.bullet('2030-2036：碱基编辑（Base Editing）+先导编辑（Prime Editing）精确修改单碱基')
pdf.bullet('投资启示：编辑工具（CRISPR 3.0）> 递送系统（AAV/LNP）> 管线产品。底层工具公司有跨周期的抗风险能力。')

# ================================================================
# 六、结语
# ================================================================
pdf.ch_title('六、结语：成为自演化投资者')

pdf.body('自演化框架的核心主张是：未来10年最大的投资主题不是某个行业或技术，而是人类掌控自身演化能力的指数级增长。')

pdf.body('这意味着：')

pdf.bullet('你在投资的不是一家公司，而是一个物种的自我升级进程')
pdf.bullet('你在评估的不是一个市场，而是一种文明操作系统的版本迭代')
pdf.bullet('你的回报不是来自市场波动，而是来自对递归飞轮的理解和站位')

pdf.body('自演化投资者的三个特征：')

pdf.bullet('他们用"10年后人将变成什么"来倒推今天的决策，而不是用"去年增长了多少"来推算未来')
pdf.bullet('他们专注于底层平台——生物编译器、认知基础设施、数字自我框架——而不是追逐每一波应用浪潮')
pdf.bullet('他们对"非共识"有耐受性。自演化在初期看起来总是不合理的——就像2023年重仓AI，就像2015年相信mRNA')

pdf.gold_bar()

pdf.set_font('H', '', 11)
pdf.set_text_color(0x0E, 0x2D, 0x40)
pdf.multi_cell(pdf.w - 2 * pdf.m, 7,
               'Self-Evolution 自演化\n'
               '人类掌控自身演化的能力正在指数级增长',
               align='C')
pdf.ln(3)
pdf.set_font('S', '', 9)
pdf.set_text_color(0x88, 0x99, 0xAA)
pdf.multi_cell(pdf.w - 2 * pdf.m, 5.5,
               '邮储银行上海分行科技金融事业部  |  2026年5月\n'
               '思考框架  |  内部参考',
               align='C')

pdf.page_num()

# Save
import os
OUTPUT_DIR = '/Users/cyingfang/WorkBuddy/20260429082054'
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT = os.path.join(OUTPUT_DIR, 'SelfEvolution_自演化投资框架.pdf')
pdf.output(OUTPUT)
print(f'Saved: {OUTPUT} | Pages: {pdf.page_no()}')
