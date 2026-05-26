#!/usr/bin/env python3
"""Civilization OS 文明操作系统 —— 投资思维框架 PDF"""

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
        self.set_fill_color(0x1A, 0x1A, 0x2E)
        self.rect(0, 0, self.w, 297, 'F')
        self.ln(38)
        self.set_font('H', '', 10)
        self.set_text_color(0xE8, 0x8D, 0x3F)
        self.multi_cell(self.w - 2 * self.m, 8, 'C I V I L I Z A T I O N   O S', align='C')
        self.ln(6)
        self.set_font('H', '', 30)
        self.set_text_color(0xFF, 0xFF, 0xFF)
        self.multi_cell(self.w - 2 * self.m, 13, main, align='C')
        self.ln(4)
        self.set_font('S', '', 12)
        self.set_text_color(0xBB, 0xCC, 0xDD)
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
        self.set_text_color(0x1A, 0x1A, 0x2E)
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
        y = self.get_y()
        self.set_font('S', '', 9)
        self.set_text_color(0x55, 0x55, 0x77)
        self.set_x(self.m + 3)
        self.multi_cell(self.w - 2 * self.m - 6, 5.5, t, align='J')
        ny = self.get_y()
        self.rect(self.m, y, self.w - 2 * self.m, ny - y + 1)
        self.set_y(ny + 3)

    def gold_bar(self):
        self.set_draw_color(0xE8, 0x8D, 0x3F)
        self.set_line_width(0.4)
        y = self.get_y()
        self.line(self.m, y, self.w - self.m, y)
        self.ln(4)

    def dark_box(self, t):
        self.set_fill_color(0x1A, 0x1A, 0x2E)
        self.set_text_color(0xFF, 0xFF, 0xFF)
        self.set_font('S', '', 10)
        self.set_x(self.m + 3)
        self.multi_cell(self.w - 2 * self.m - 6, 6, t, align='J')
        self.ln(3)
        self.set_text_color(0x33, 0x33, 0x33)

    def os_card(self, ver, title, time, desc, items):
        """OS version history card"""
        self.set_fill_color(0xF2, 0xF5, 0xFA)
        self.set_draw_color(0xCC, 0xCC, 0xDD)
        self.set_line_width(0.2)
        y = self.get_y()
        # Version number
        self.set_font('H', '', 11)
        self.set_text_color(0x1B, 0x5E, 0x8A)
        self.set_x(self.m + 3)
        self.cell(10, 6, ver)
        self.set_font('S', '', 10)
        self.set_text_color(0x33, 0x33, 0x33)
        self.cell(self.w - 2 * self.m - 20, 6, f'{title}  ({time})')
        self.ln(7)
        self.set_font('S', '', 9)
        self.set_text_color(0x55, 0x55, 0x55)
        self.set_x(self.m + 3)
        self.multi_cell(self.w - 2 * self.m - 6, 5.5, desc, align='J')
        self.ln(1)
        for item in items:
            self.set_font('S', '', 8.5)
            self.set_text_color(0x55, 0x55, 0x55)
            self.set_x(self.m + 6)
            self.multi_cell(self.w - 2 * self.m - 9, 5, f'* {item}', align='J')
            self.ln(0.5)
        ny = self.get_y()
        self.rect(self.m, y, self.w - 2 * self.m, ny - y + 1)
        self.set_y(ny + 3)

    def layer_card(self, name, desc, examples, color_bg, color_accent):
        """OS stack layer card"""
        self.set_fill_color(*color_bg)
        self.set_draw_color(*color_accent)
        self.set_line_width(0.2)
        y = self.get_y()
        self.set_font('H', '', 11)
        self.set_text_color(*color_accent)
        self.set_x(self.m + 3)
        self.cell(self.w - 2 * self.m - 6, 6, name)
        self.ln(8)
        self.set_font('S', '', 9)
        self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m + 3)
        self.multi_cell(self.w - 2 * self.m - 6, 5.5, desc, align='J')
        self.ln(2)
        self.set_font('S', '', 8)
        self.set_text_color(0x77, 0x77, 0x99)
        self.set_x(self.m + 3)
        self.multi_cell(self.w - 2 * self.m - 6, 5, f'示例：{examples}', align='J')
        ny = self.get_y()
        self.rect(self.m, y, self.w - 2 * self.m, ny - y + 1)
        self.set_y(ny + 3)

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
    '文明操作系统  投资框架',
    'Civilization OS — 当文明的底层平台升级时，一切都在其上重建',
    '邮储银行上海分行科技金融事业部  |  2026年5月')

# ================================================================
# 引言
# ================================================================
pdf.ch_title('引言：每一次OS升级，都是一次财富重分配')

pdf.body('如果用一个概念来理解2026-2036年的投资机会，那就是"文明操作系统升级"。就像计算机的操作系统——Windows、iOS、Android——决定了什么样的应用能跑在上面，文明的"操作系统"决定了什么样的经济、政治、文化模式是可能的。')

pdf.body('当操作系统升级时，旧的应用必须被重写，新的应用成批涌现，新的巨头崛起，旧的巨头衰落。这不是渐进式的改良，而是平台级的替换。')

pdf.body('关键洞察：每一次文明OS升级，都伴随着一次大规模的财富重分配。那些理解新OS底层逻辑的人，成为新世界的构建者。那些固守旧OS思维的人，无论曾经多么成功，都会被边缘化。')

pdf.gold_bar()
pdf.quote_box('"我们不是在经历一个技术变革。我们是生活在一个文明操作系统的版本升级之中。"')

# ================================================================
# 一、哲学理念
# ================================================================
pdf.ch_title('一、哲学理念：平台思维')

pdf.sub_title('1.1 什么是"文明操作系统"？')

pdf.body('文明的"操作系统"由三层构成，每一层都是更上一层的运行基础：')

pdf.bullet('技术基础层：能源、交通、通信、计算——文明如何操控物质、能量和信息')
pdf.bullet('制度协调层：市场、法律、组织、货币——文明如何协调大规模协作')
pdf.bullet('意义生成层：信仰、叙事、价值观——文明如何解释自身和世界')

pdf.body('当这三层同时发生根本性改变时——就像现在——我们正在见证一次操作系统升级。')

pdf.sub_title('1.2 操作系统升级的特征')

pdf.body('文明的OS升级有几条关键规律，对投资决策至关重要：')

pdf.bullet('规律一：不可逆。一旦升级，无法回退。2025年之后的AI能力不会被"关掉"——正如互联网不会被"断开"。')
pdf.bullet('规律二：非均匀。新OS的各个部分以不同速度落地，但最终会整体切换。先发优势在早期不明显，后期加速。')
pdf.bullet('规律三：平台捕获最大价值。在每一次OS升级中，底层平台（协议、基础设施）的长期价值超过所有上层应用的总和。')
pdf.bullet('规律四：旧OS的精英通常是最晚理解的。因为他们的一切优势都建立在旧OS之上。')

pdf.sub_title('1.3 三条信念')

pdf.bold_body('信念一：新操作系统的"内核"是通用人工智能（AGI）')
pdf.body('就像微处理器是PC的内核、TCP/IP是互联网的内核、搜索引擎是Web 2.0的内核——AGI是OS 6.0的内核。一切上层应用都将围绕这个内核重建。')

pdf.bold_body('信念二：每一个传统行业都将被"重新编译"')
pdf.body('教育、医疗、金融、法律、制造——没有一个行业能免于被新OS重新编译。就像PC时代重写了办公室工作，互联网时代重写了零售和媒体。')

pdf.bold_body('信念三：最大的投资机会不在"应用层"，而在"协议层"')
pdf.body('在PC时代，最大的赢家不是应用软件公司，而是微软（操作系统）和英特尔（芯片）。在互联网时代，最大的赢家不是网站，而是谷歌（搜索协议）和亚马逊（电商协议）。在AI时代亦然。')

# ================================================================
# 二、六次升级简史
# ================================================================
pdf.ch_title('二、六次OS升级：从农业到智能')

pdf.body('人类文明经历了五次主要的操作系统升级，每一次都将文明带到了全新的复杂性水平。每一次都创造了空前的财富——也毁灭了拒绝升级的文明。')

pdf.gold_bar()

pdf.os_card('OS 1.0', '农业', '公元前8000年',
    '狩猎采集社会→农业定居社会。核心创新：农作物驯化、动物驯养、永久定居。',
    ['技术基础：耕作工具、灌溉系统、天文历法',
     '制度创新：私有财产、城市国家、官僚体系、文字',
     '意义生成：多神教、祖先崇拜、王权神授',
     '投资逻辑：土地是最核心的资产'])

pdf.os_card('OS 2.0', '文字与法律', '公元前3000年',
    '从口传社会→文字社会。核心创新：楔形文字、字母表、成文法。',
    ['技术基础：书写工具、莎草纸/泥板',
     '制度创新：法典（汉谟拉比）、契约、记录保存',
     '意义生成：一神教、普世伦理',
     '投资逻辑：读写能力和知识成为新的权力来源'])

pdf.os_card('OS 3.0', '科学', '1500-1700年',
    '从神启社会→实验科学社会。核心创新：科学方法、印刷术、望远镜/显微镜。',
    ['技术基础：印刷机（1450）、远洋航行、实验设备',
     '制度创新：大学、科学院、专利制度、有限责任公司',
     '意义生成：启蒙思想、理性主义、个人主义',
     '投资逻辑：科学知识成为生产力，研发投入产生超额回报'])

pdf.os_card('OS 4.0', '工业', '1760-1900年',
    '从农业社会→工业社会。核心创新：蒸汽机、电力、内燃机、流水线。',
    ['技术基础：化石能源、钢铁、铁路、电报',
     '制度创新：现代公司、工会、中央银行、社会保障',
     '意义生成：进步主义、民族主义、消费主义',
     '投资逻辑：资本密集型工业成为财富引擎'])

pdf.os_card('OS 5.0', '数字', '1960-2020年',
    '从工业社会→信息社会。核心创新：晶体管、计算机、互联网、移动通信。',
    ['技术基础：半导体、个人电脑、光纤、无线网络',
     '制度创新：电子商务、社交媒体、开源运动、加密货币',
     '意义生成：信息自由、网络效应、全球化',
     '投资逻辑：数据和用户网络成为核心资产'])

pdf.os_card('OS 6.0', '智能', '2024-2036年',
    '从信息社会→智能社会。核心创新：大语言模型、通用人工智能、AI Agent、脑机融合。',
    ['技术基础：GPU集群、基础模型、海量数据',
     '制度创新：正在形成中（AI治理、数字身份、后稀缺经济）',
     '意义生成：正在形成中（人机关系、意识、自我认知的重塑）',
     '投资逻辑：智能本身成为最核心的资产'])

# ================================================================
# 三、方法论
# ================================================================
pdf.ch_title('三、方法论：在OS升级中投资')

pdf.body('文明OS升级的投资方法论建立在五个核心步骤之上——不是预测未来，而是理解"平台迁移"的结构性必然性。')

steps = [
    ('Step 1', '读懂栈（Read the Stack）',
     '将投资标的映射到OS栈中：它在哪一层？是硬件、基础设施、协议、还是应用？底层比上层更抗周期，上层比底层爆发力更强。'),
    ('Step 2', '找内核（Find the Kernel）',
     '新OS的"内核"是什么？OS 6.0的内核不是某个应用，而是"智能"本身——基础模型和计算基础设施。内核层的赢家最确定。'),
    ('Step 3', '算迁移（Map the Migration）',
     '旧OS上的应用如何迁移到新OS？教育→AI个性化学习，医疗→AI诊断+精准医疗，金融→AI风控+DeFi。迁移速度×市场规模=投资回报。'),
    ('Step 4', '辨协议（Identify the Protocol）',
     '新OS中将会出现哪些"协议层"赢家？类似PC时代的Wintel、互联网时代的Google搜索。协议层具有自然垄断特征和跨周期价值。'),
    ('Step 5', '等加速（Wait for Acceleration）',
     'OS升级的初期总是缓慢且充满噪音。但当安装量越过临界点，采用曲线会陡然加速。耐心不是美德，是策略。'),
]

for i, (step, title, desc) in enumerate(steps):
    pdf.set_fill_color(0xF8, 0xF8, 0xFC) if i % 2 == 0 else pdf.set_fill_color(0xFF, 0xFF, 0xFF)
    pdf.set_font('H', '', 10)
    pdf.set_text_color(0x1A, 0x1A, 0x2E)
    pdf.set_x(pdf.m + 2)
    pdf.cell(6, 6, f'{i+1}')
    pdf.cell(pdf.w - 2 * pdf.m - 8, 6, title)
    pdf.ln(6)
    pdf.set_font('S', '', 8.5)
    pdf.set_text_color(0x55, 0x55, 0x55)
    pdf.set_x(pdf.m + 10)
    pdf.multi_cell(pdf.w - 2 * pdf.m - 12, 5.5, desc, align='J')
    pdf.ln(3)

pdf.gold_bar()
pdf.quote_box('方法论的底层逻辑：操作系统升级不是"一个趋势"，而是一个结构的必然。一旦你理解了新OS的架构，投资方向就变得清晰——不是猜测哪个应用会赢，而是押注整个平台的升级。')

# ================================================================
# 四、框架
# ================================================================
pdf.ch_title('四、框架：OS 6.0 的架构')

pdf.body('OS 6.0（智能操作系统）的架构可以理解为四个层次，每一层都创造不同类型的投资机会。理解这个栈的结构，就是在理解未来10年的财富创造逻辑。')

pdf.gold_bar()

pdf.layer_card('Layer 1 — 算力层',
    '物理基础设施。GPU集群、数据中心、能源、光通信。这是新OS的"电力"。\n\n关键特征：前置资本极重，进入壁垒极高，一旦建成很难被替代。在每一轮OS升级中，硬件层的赢家都是最确定、回报最稳健的。',
    'NVIDIA (GPU)、台积电 (制造)、微软Azure/谷歌GCP (云)、数据中心REITs',
    (0xF2, 0xF5, 0xFA), (0x1B, 0x5E, 0x8A))

pdf.layer_card('Layer 2 — 智能层',
    '基础模型与AI平台。大语言模型、多模态模型、推理引擎。这是新OS的"内核"。\n\n关键特征：训练成本极高（数十亿美元），数据飞轮效应显著，自然趋向寡头垄断。智能层的竞争类似于PC时代的CPU竞争——赢家通吃，输家消失。',
    'OpenAI (GPT)、Google DeepMind (Gemini)、Anthropic (Claude)、Meta (Llama)',
    (0xF5, 0xF0, 0xFA), (0x7B, 0x3B, 0x9E))

pdf.layer_card('Layer 3 — 协议层',
    'AI Agent框架、身份验证、信任机制、数据标准。这是新OS的"TCP/IP"。\n\n关键特征：协议层的价值在于"标准"和"网络效应"。一旦某个协议成为事实标准，它的价值会随着整个生态的增长而增长。协议层的赢家在OS升级完成后仍能持续创造价值数十年。',
    'AI Agent框架 (LangChain)、身份协议 (World ID)、验证协议 (数字水印/认证)、API网关',
    (0xF0, 0xFA, 0xF5), (0x1B, 0x6E, 0x5E))

pdf.layer_card('Layer 4 — 应用层',
    '所有被AI重新编译的传统行业 + AI原生新行业。这是新OS的"应用软件"。\n\n关键特征：应用层竞争最激烈，更替最快，但也是创新的主战场。在OS升级的早期（2026-2030），应用层的机会最多但风险也最高。在后期（2030-2036），赢家会逐渐显现。',
    'AI教育 (可汗学院/Khanmigo)、AI医疗 (诊断/药物发现)、AI金融、AI法律、AI编程、AI创意',
    (0xFA, 0xF5, 0xF0), (0x9E, 0x7B, 0x3B))

pdf.gold_bar()
pdf.quote_box('框架的关键理解：这四层不是"四种投资选择"，而是一个栈。每一层都依赖于下面一层。投资决策的核心问题是：你在押注栈的哪一层？你的回报来自该层在OS升级中的"不可替代性"程度。')

# ================================================================
# 五、案例
# ================================================================
pdf.ch_title('五、深度案例')

pdf.sub_title('案例一：NVIDIA — 赌对了OS升级的"芯片层"')

pdf.body('NVIDIA在2010年代将自己从"显卡公司"重塑为"AI计算平台"。这不是一个产品策略，而是对OS升级的预判。')
pdf.bullet('2012年：AlexNet在NVIDIA GPU上训练——OS升级的第一个信号')
pdf.bullet('2016-2022年：CUDA生态成为AI开发的默认平台（协议层）')
pdf.bullet('2023-2026年：GPU供不应求，算力成为最稀缺资源')
pdf.bullet('投资启示：NVIDIA做对的事情不是"卖芯片"，而是"在新OS的算力层建立垄断"。CUDA是软件协议层，GPU是硬件层——两层合一的赢家。')

pdf.sub_title('案例二：教育行业——OS升级中的"应用迁移"')

pdf.body('教育是最典型的"将被OS 6.0重新编译"的行业。传统教育的OS是工业化时代的产物：统一课程、标准化考试、按年龄分班。')
pdf.bullet('旧OS逻辑：教师是知识传递者，课堂是学习场所，考试是评估标准')
pdf.bullet('OS 6.0逻辑：AI Tutor 是个性化教师，随时随地学习，能力评估代替知识考试')
pdf.bullet('2024-2026：AI辅助教学（可汗学院Khanmigo、Duolingo AI）')
pdf.bullet('2027-2032：AI核心教学（个性化课程、实时适应、虚拟实验）')
pdf.bullet('2033-2036：教育范式迁移完成——"学校"的概念被重塑')
pdf.bullet('投资启示：教育的OS迁移是一个10年进程。早期押注"AI+教育"平台（而非内容），中期关注评估认证体系的重建，后期关注新型教育机构的崛起。')

pdf.sub_title('案例三：金融——OS 6.0的"原生应用"')

pdf.body('金融行业一直是新技术OS的早期采纳者——从电报、电话到计算机、互联网。AI带来的升级可能是最彻底的一次。')
pdf.bullet('旧OS逻辑：人工风控、标准产品、固定利率、周期性波动')
pdf.bullet('OS 6.0逻辑：AI实时风控、个性化产品、动态定价、预测性管理')
pdf.bullet('银行业：AI信用评估覆盖央行征信盲区（如科技企业、自由职业者）')
pdf.bullet('投资端：AI辅助投研覆盖传统分析无法触及的领域（如早期科技估值）')
pdf.bullet('保险业：AI精算 + 可穿戴数据 → 个性化定价')
pdf.bullet('投资启示：在OS升级中，金融业最大的机会不是"做AI应用"，而是"用AI重写金融基础设施"。分布式账本+AI风控+数字身份=新一代金融OS。')

# ================================================================
# 六、结语
# ================================================================
pdf.ch_title('六、结语：重新编译你的投资思维')

pdf.body('文明操作系统的升级，不是每十年一次的趋势轮动，而是每几百年一次的底层重构。我们这一代人，正处在从OS 5.0（数字）到OS 6.0（智能）的迁移窗口。')

pdf.body('这个窗口的特征是：')

pdf.bullet('初期看起来像"炒作"——因为新OS的应用在旧OS上运行时显得笨拙可笑')
pdf.bullet('中期看起来像"替代"——因为新OS的应用开始超越旧OS的体验')
pdf.bullet('后期看起来像"理所当然"——因为年轻一代从未体验过旧OS')

pdf.body('作为投资者，真正的选择只有一个：你是选择用旧OS的思维去理解新OS的机会，还是切换到这个新的操作系统上？')

pdf.gold_bar()

pdf.set_font('H', '', 11)
pdf.set_text_color(0x1A, 0x1A, 0x2E)
pdf.multi_cell(pdf.w - 2 * pdf.m, 7,
               'Civilization OS 文明操作系统\n'
               '当文明的底层平台升级时，一切都在其上重建',
               align='C')
pdf.ln(1)
pdf.set_font('S', '', 9)
pdf.set_text_color(0x88, 0x99, 0xAA)

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
OUTPUT = os.path.join(OUTPUT_DIR, 'CivilizationOS_文明操作系统投资框架.pdf')
pdf.output(OUTPUT)
print(f'Saved: {OUTPUT} | Pages: {pdf.page_no()}')
