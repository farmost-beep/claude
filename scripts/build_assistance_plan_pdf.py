#!/usr/bin/env python3
"""Claude 协助能力分析 & 长期协作计划 PDF"""

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
        self.add_page(); self.ln(25)
        self.set_font('H', '', 26); self.set_text_color(0x17, 0x2B, 0x4F)
        self.multi_cell(self.w - 2 * self.m, 12, main, align='C')
        if sub:
            self.ln(6); self.set_font('S', '', 11); self.set_text_color(0x66, 0x66, 0x66)
            self.multi_cell(self.w - 2 * self.m, 7, sub, align='C')
        self.ln(10); self.set_draw_color(0x00, 0x7A, 0x3D); self.set_line_width(0.6)
        cx = self.w / 2; self.line(cx - 25, self.get_y(), cx + 25, self.get_y())
        self.ln(6); self.set_font('S', '', 9); self.set_text_color(0x99, 0x99, 0x99)
        self.multi_cell(self.w - 2 * self.m, 6, '— Claude 系统扫描分析报告 —', align='C')

    def ch_title(self, t):
        self.set_font('H', '', 18); self.set_text_color(0x17, 0x2B, 0x4F)
        self.set_x(self.m); self.cell(self.w - 2 * self.m, 10, t); self.ln(12)
        self.set_draw_color(0x00, 0x7A, 0x3D); self.set_line_width(0.5)
        self.line(self.m, self.get_y() - 6, self.m + 40, self.get_y() - 6); self.ln(6)

    def sub_title(self, t):
        self.set_font('H', '', 13); self.set_text_color(0x00, 0x7A, 0x3D)
        self.set_x(self.m); self.cell(self.w - 2 * self.m, 8, t); self.ln(10)

    def body(self, t):
        self.set_font('S', '', 10.5); self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m); self.multi_cell(self.w - 2 * self.m, 6.2, t, align='J'); self.ln(2)

    def bullet_num(self, num, t):
        self.set_font('H', '', 11); self.set_text_color(0x00, 0x7A, 0x3D)
        self.set_x(self.m); self.cell(8, 6, f'{num}.')
        self.set_font('S', '', 10.5); self.set_text_color(0x33, 0x33, 0x33)
        x0 = self.get_x()
        self.multi_cell(self.w - 2 * self.m - 8, 6.2, t, align='J'); self.set_x(self.m); self.ln(1)

    def bullet(self, t):
        self.set_font('S', '', 10); self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m + 4); self.cell(5, 5.5, '◦')
        self.multi_cell(self.w - 2 * self.m - 9, 5.8, t, align='J'); self.set_x(self.m); self.ln(0.5)

    def green_bar(self):
        self.set_draw_color(0x00, 0x7A, 0x3D); self.set_line_width(0.3)
        y = self.get_y(); self.line(self.m, y, self.w - self.m, y); self.ln(3)

    def tag(self, t):
        self.set_font('S', '', 8); self.set_text_color(0xFF, 0xFF, 0xFF)
        w = self.get_string_width(t) + 4
        self.set_fill_color(0x00, 0x7A, 0x3D)
        self.cell(w, 5, t, fill=True); self.ln(1)

    def page_num(self):
        self.set_font('S', '', 8); self.set_text_color(0xAA, 0xAA, 0xAA)
        self.set_y(-15); self.cell(self.w - 2 * self.m, 5, str(self.page_no()), align='R')


pdf = PDF(); pdf.set_margin(22)

# ===== COVER =====
pdf.title_page('Claude 协助能力分析\n与长期协作计划',
               '基于您的电脑文件扫描，整理出10大可协助领域及长期规划')

# ================================================================
pdf.add_page()
pdf.ch_title('扫描概况')

pdf.body('对您的电脑进行了全面扫描，包括以下关键资源：')

table_data = [
    ['类别', '发现'],
    ['Python PDF脚本', '30+ 个脚本（fpdf + reportlab）'],
    ['已生成PDF', '74+ 份（五年规划/融资图/阅读手册/银行报告等）'],
    ['小说创作', '5个项目（道陨·19章/天阁/灵境/外卖侠影/论语仙侠）'],
    ['金融分析', '邮储银行科技金融、融资路线图、神州信息、投资手册'],
    ['家庭规划', '陈颖芳/张庆芬/陈于东 五年规划'],
    ['产业研究', '十五五产业规划追踪、宽岳医疗分析'],
    ['阅读体系', '哲学/历史/经济/宗教 零散读生阅读手册'],
    ['智能体崛起', '10万字系列文章，多卷未完成'],
]

rows = []
for r in table_data:
    pdf.set_font('S', '', 9.5)
    if r == table_data[0]:
        pdf.set_fill_color(0x00, 0x7A, 0x3D); pdf.set_text_color(0xFF, 0xFF, 0xFF)
    else:
        pdf.set_fill_color(0xF0, 0xF7, 0xF3); pdf.set_text_color(0x33, 0x33, 0x33)
    pdf.set_x(pdf.m)
    pdf.cell(35, 7, r[0], border=1, fill=True)
    pdf.cell(pdf.w - 2 * pdf.m - 35, 7, r[1], border=1, fill=True)
    pdf.ln()
pdf.ln(4)

pdf.body('基于以上扫描，我整理出了可以协助您的10大核心领域，并制定了分阶段的长期协作计划。')

pdf.page_num()

# ================================================================
pdf.add_page()
pdf.ch_title('十大可协助领域')

pdf.body('以下是基于您电脑上的工作习惯和项目类型，整理出的我可以最大程度协助您的10大领域：')
pdf.ln(2)

areas = [
    ("PDF文档自动化生成",
     "您已生成74份PDF，但每次都是手动编写脚本。我可以帮您建立一套标准化的PDF生成框架，大幅提升生成速度。",
     "主干能力"),
    ("金融行业报告与分析",
     "您在邮储银行科技金融事业部，经常需要做客户分析、融资方案、竞争对手研究。我可以帮您搜集数据、组织报告结构、自动生成PDF输出。",
     "核心需求"),
    ("小说创作助手",
     "您有多个小说项目在进行中（道陨19章、天阁、灵境、外卖侠影）。我可以帮您纳文修改、内容拓展、人物设定整理、情节线协调。",
     "核心需求"),
    ("阅读与知识管理",
     "您的“三问阅读手册”体系覆盖了从古希腊到当代的大量经典，还有系统阅读规划。我可以帮您扩展阅读手册、维护知识图谱。",
     "核心需求"),
    ("家庭规划与教育",
     "您的三份五年规划、孩子教育三问、健康管理三问。我可以帮您定期追踪规划执行、更新内容。",
     "核心需求"),
    ("投资研究与分析",
     "AI投资手册、investment-masters deliverables。我可以帮您做行业分析、财报研究、投资策略整理。",
     "重要工作"),
    ("产业政策追踪",
     "十五五产业规划追踪、宽岳医疗分析。我可以定期扫描政策动态、整理行业报告。",
     "重要工作"),
    ("学习与身份认证",
     "大学学习三问、高等数学三问、考证准备。我可以帮您制定复习计划、整理知识点。",
     "重要工作"),
    ("PPT与可视化汇报",
     "您已经试过python-pptx生成PPT。我可以帮您自动化生成汇报PPT、可视化图表。",
     "增值服务"),
    ("Python脚本优化与自动化",
     "您的脚本可以进一步优化：模块化、参数化、自动化执行。我可以帮您重构代码、建立模板体系。",
     "增值服务"),
]

for i, (title, desc, tag) in enumerate(areas, 1):
    pdf.bullet_num(i, f'')
    pdf.set_fill_color(0x00, 0x7A, 0x3D)
    pdf.set_text_color(0xFF, 0xFF, 0xFF)
    pdf.set_font('H', '', 10.5)
    pdf.cell(12, 5.5, f' ')
    tw = pdf.get_string_width(title) + 8
    # draw tag
    pdf.set_fill_color(0x00, 0x7A, 0x3D) if tag == '核心需求' else (
        pdf.set_fill_color(0xC9, 0xA8, 0x4C) if tag == '主要专长' else (
        pdf.set_fill_color(0x0D, 0x23, 0x4B) if tag == '核心能力' else (
        pdf.set_fill_color(0x66, 0x66, 0x66))))
    pdf.set_text_color(0xFF, 0xFF, 0xFF)
    pdf.set_font('S', '', 7.5)
    pdf.cell(20, 5, tag, fill=True)
    pdf.set_text_color(0x17, 0x2B, 0x4F)
    pdf.set_font('H', '', 11)
    pdf.set_x(pdf.m + 8)
    pdf.cell(0, 6, title)
    pdf.ln(7)
    pdf.set_x(pdf.m + 8)
    pdf.set_text_color(0x33, 0x33, 0x33)
    pdf.set_font('S', '', 10)
    pdf.multi_cell(pdf.w - 2 * pdf.m - 8, 5.8, desc, align='J')
    pdf.ln(2)

# Check if we need a page break
for t, d, _ in areas[:2]:
    h = 15 + len(d) // 50 * 5
    pass

pdf.page_num()

# ================================================================
pdf.add_page()
pdf.ch_title('长期协作计划')

pdf.sub_title('第一阶段：基础建设期（当前 - 2026年8月）')
pdf.body('重点建立数字化工作体系，提升日常工作效率。')
pdf.bullet('建立标准化PDF模板体系：金融报告、五年规划、阅读手册三套模板')
pdf.bullet('整理已有小说项目的结构、人物、情节线文档化')
pdf.bullet('完成智能体崛起系列剩余卷节的创作')
pdf.bullet('制定系统阅读计划执行时间表')

pdf.sub_title('第二阶段：深化应用期（2026年9月 - 12月）')
pdf.body('将自动化能力应用到核心工作流程中。')
pdf.bullet('邮储银行科技金融客户分析报告自动化生成')
pdf.bullet('十五五产业规划定期追踪与汇报自动化')
pdf.bullet('家庭规划季度评估与调整报告')
pdf.bullet('小说项目规律性更新（每周章节输出）')

pdf.sub_title('第三阶段：系统化运营期（2027年及以后）')
pdf.body('建立稳定的工作节奏和知识体系。')
pdf.bullet('年度规划与季度评估机制')
pdf.bullet('知识产品化：将研究成果转化为系统性专题报告')
pdf.bullet('可能：建立个人知识数库/文章系统')

pdf.green_bar()

pdf.sub_title('每周协作节奏建议')
pdf.body('建议每周安排1-2次集中协作时间，每次1-2小时，聚焦一个明确的任务。以下是建议的每周节奏：')
pdf.bullet('周一/周二：工作相关（金融报告、产业研究、客户分析）')
pdf.bullet('周三/周四：创作相关（小说写作、阅读笔记、学习计划）')
pdf.bullet('周末：家庭相关（规划评估、教育、健康）')

pdf.green_bar()

pdf.sub_title('当前候选任务（可直接开始）')
pdf.bullet('完成智能体崛起未完卷节（第4-7卷）')
pdf.bullet('道陨剩余章节续写')
pdf.bullet('系统阅读规划下的下一本三问手册生成')
pdf.bullet('邮储银行融资路线图或其他金融报告更新')

pdf.page_num()

# ================================================================
pdf.add_page()
pdf.ch_title('工具与技术叠代')

pdf.sub_title('已掌握的技术栈')
pdf.bullet('fpdf2 — 74+ 份PDF的核心引擎，支持中文字体')
pdf.bullet('reportlab — 高级PDF生成，表格、图表、复杂布局')
pdf.bullet('python-pptx — PPT自动化生成')
pdf.bullet('WebSearch/WebFetch — 实时数据搜集与研究')
pdf.bullet('Bash/Python — 任何可定制的自动化任务')

pdf.sub_title('可拓展的技术能力')
pdf.bullet('Markdown → PDF — 直接将Markdown转换为排版PDF')
pdf.bullet('Web 爬虫 — 定时爬取数据并生成报告')
pdf.bullet('LlamaIndex/LangChain — 建立个人知识数库')
pdf.bullet('Excel/CSV 分析 — 财务数据处理与可视化')
pdf.bullet('Selenium/Playwright — 网页自动化操作')

pdf.sub_title('个人化数据记忆体系')
pdf.body('我的记忆系统会记住您的工作背景、偏好和项目上下文，每次会话都能从上次离开的地方继续，不需要重复介绍。')

pdf.ln(4)
pdf.set_font('S', '', 9); pdf.set_text_color(0x99, 0x99, 0x99)
pdf.multi_cell(pdf.w - 2 * pdf.m, 6,
    '基于对您电脑文件的全面扫描。\n'
    '2026年5月25日 | 随时可根据您的反馈调整计划', align='C')
pdf.page_num()

import os
OUTPUT = '/Users/cyingfang/WorkBuddy/20260429082054/Claude协助能力分析与长期协作计划.pdf'
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
pdf.output(OUTPUT)
print(f'Saved: {OUTPUT} | Pages: {pdf.page_no()}')
