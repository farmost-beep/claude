#!/usr/bin/env python3
"""陈于东 2026-2031 五年规划 PDF"""

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
        self.set_font('H', '', 28); self.set_text_color(0x17, 0x2B, 0x4F)
        self.multi_cell(self.w - 2 * self.m, 12, main, align='C')
        if sub:
            self.ln(6); self.set_font('S', '', 12); self.set_text_color(0x66, 0x66, 0x66)
            self.multi_cell(self.w - 2 * self.m, 7, sub, align='C')
        self.ln(12); self.set_draw_color(0x00, 0x96, 0x53); self.set_line_width(0.6)
        cx = self.w / 2; self.line(cx - 25, self.get_y(), cx + 25, self.get_y())
        self.ln(8); self.set_font('S', '', 10); self.set_text_color(0x99, 0x99, 0x99)
        self.multi_cell(self.w - 2 * self.m, 6, '规划周期：2026年5月 — 2031年5月 | 20岁→25岁', align='C')

    def ch_title(self, t):
        self.set_font('H', '', 18); self.set_text_color(0x17, 0x2B, 0x4F)
        self.set_x(self.m); self.cell(self.w - 2 * self.m, 10, t); self.ln(12)
        self.set_draw_color(0x00, 0x96, 0x53); self.set_line_width(0.5)
        self.line(self.m, self.get_y() - 6, self.m + 40, self.get_y() - 6); self.ln(6)

    def sub_title(self, t):
        self.set_font('H', '', 13); self.set_text_color(0x00, 0x96, 0x53)
        self.set_x(self.m); self.cell(self.w - 2 * self.m, 8, t); self.ln(10)

    def body(self, t):
        self.set_font('S', '', 10.5); self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m); self.multi_cell(self.w - 2 * self.m, 6.2, t, align='J'); self.ln(2)

    def bullet(self, t):
        self.set_font('S', '', 10.5); self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m); self.cell(6, 6, '>')
        self.multi_cell(self.w - 2 * self.m - 6, 6.2, t, align='J'); self.set_x(self.m); self.ln(1)

    def green_bar(self):
        self.set_draw_color(0x00, 0x96, 0x53); self.set_line_width(0.3)
        y = self.get_y(); self.line(self.m, y, self.w - self.m, y); self.ln(4)

    def page_num(self):
        self.set_font('S', '', 8); self.set_text_color(0xAA, 0xAA, 0xAA)
        self.set_y(-15); self.cell(self.w - 2 * self.m, 5, str(self.page_no()), align='R')


pdf = PDF(); pdf.set_margin(22)

pdf.title_page('陈于东 五年规划\n2026 — 2031', '考研/保研 · 学业进阶 · 职业起航')

# ================================================================
pdf.add_page()
pdf.ch_title('规划总纲')

pdf.body('规划对象：陈于东，2006年1月出生，2026年5月时20岁。上海大学大二在读（推测理学院相关专业）。性格谦逊随和，善思考、有进取心，文理科均衡。初中阶段获得上海市青少年科技创新大赛一等奖、静安区明日科技之星、古诗文阅读大赛一等奖等多项荣誉。家庭背景：父亲陈颖芳在金融行业（邮储银行科技金融），母亲在科技行业（已退休）。')

pdf.body('规划基准：大学二年级即将结束，进入大三——保研/考研的关键准备期。本规划覆盖20岁→25岁，从大学本科到研究生阶段的核心路径。')

pdf.ln(2)
pdf.sub_title('五年核心目标')
pdf.bullet('2026-2027：大三-大四，成功保研（优先）或考研上岸，锁定研究生去向')
pdf.bullet('2028-2029：研一-研二，深入学术研究，明确职业方向')
pdf.bullet('2030-2031：研三或工作初期，完成从学生到职业人的转变')

pdf.page_num()

# ================================================================
pdf.add_page()
pdf.ch_title('第一篇：保研/考研策略（2026-2027）')

pdf.sub_title('一、现状诊断')
pdf.body('当前优势：(1) 上海大学211平台，理学院有保研名额（62个名额/76名候选人，GPA要求3.00+）；(2) 中学阶段有科创竞赛获奖经历，科研潜力有证明；(3) 文理科均衡，不偏科；(4) 家庭支持——母亲在筹备保研咨询业务，有信息优势。')
pdf.body('当前待提升：(1) GPA排名未知，需要确认是否在保研候选范围内（前30%）；(2) 科研经历不足——大二阶段应有实验室/课题参与；(3) 目标院校和专业方向需要明确。')

pdf.sub_title('二、保研路线图（优先方案）')

pdf.body('大三上（2026年9-12月）：')
pdf.bullet('确认GPA排名：向辅导员/教务处确认是否进入保研候选名单（62名/76人），如不在名单内立即启动考研准备')
pdf.bullet('科研加分：加入导师课题组，争取发表一篇论文或参与一个课题项目（保研加分关键）')
pdf.bullet('学科竞赛：参加数学建模竞赛（全国大学生数学建模竞赛9月）或专业相关学科竞赛')
pdf.bullet('英语准备：通过六级（如未过），六级550+为保研加分项')

pdf.body('大三下（2027年2-6月）：')
pdf.bullet('确定目标院校：优先本校保底（上海大学理学院），冲刺上海更高层次院校（复旦/上交/同济相关专业）')
pdf.bullet('联系目标导师：提前半年通过邮件联系心仪导师，表达研究兴趣')
pdf.bullet('准备保研材料：个人陈述、研究计划、推荐信（至少2封）、成绩单、获奖证书')
pdf.bullet('参加夏令营：5-7月各高校保研夏令营，争取拿到预录取')

pdf.body('大四上（2027年7-9月）：')
pdf.bullet('保研系统填报：9月全国推免系统开放，填报志愿并确认录取')
pdf.bullet('如保研失败，立即启动考研Plan B（见下节）')

pdf.sub_title('三、考研备选方案（Plan B）')
pdf.body('如果大三上确认不在保研名单内，立即切换考研模式：')
pdf.bullet('2026年10月：确定考研目标院校和专业，购买专业课教材和真题')
pdf.bullet('2026年11月-2027年6月：第一轮系统复习（数学+英语+政治+专业课）')
pdf.bullet('2027年7-9月：第二轮强化复习+真题训练')
pdf.bullet('2027年10-12月：冲刺阶段+模拟考试+正式考试')
pdf.bullet('考研目标建议：本校（上海大学）或同城211院校，成功率最高')

pdf.sub_title('四、专业方向建议')
pdf.body('基于陈于东的兴趣（阅读、历史、科创）和能力特征（文理均衡、善于思考、有科研荣誉）：')
pdf.bullet('方向一：数学/应用数学（基础学科，考研选择面广，可转向金融/数据科学/AI）')
pdf.bullet('方向二：物理/应用物理（与科创竞赛经历匹配，可转向半导体/光电/材料）')
pdf.bullet('方向三：计算机/数据科学（与母亲的技术背景互补，就业前景好）')
pdf.bullet('方向四：金融/经济学（转向金融方向，与家庭金融人脉网络协同）')

pdf.page_num()

# ================================================================
pdf.add_page()
pdf.ch_title('第二篇：研究生阶段（2028-2029）')

pdf.sub_title('一、研一：基础夯实（2028）')
pdf.bullet('完成研究生课程学分，GPA保持3.3+')
pdf.bullet('确定研究方向，与导师商定论文选题')
pdf.bullet('参加学术会议，了解学科前沿')
pdf.bullet('如选择金融/CS方向，开始准备CFA一级或编程技能提升')
pdf.bullet('建立师门关系和学术人脉网络')

pdf.sub_title('二、研二：成果产出（2029）')
pdf.bullet('完成核心论文（至少1篇），争取发表')
pdf.bullet('参与导师的横向课题，积累项目经验')
pdf.bullet('确定毕业后方向：读博（学术路线）或就业（业界路线）')
pdf.bullet('如就业方向：开始暑期实习（金融机构/科技企业）')
pdf.bullet('如读博方向：联系博导，准备博士申请材料')

pdf.page_num()

# ================================================================
pdf.add_page()
pdf.ch_title('第三篇：职业起航（2030-2031）')

pdf.sub_title('一、职业方向选择')
pdf.body('基于家庭资源和个人兴趣，建议三个可能的职业方向：')

pdf.body('方向A：金融机构（银行/券商/基金）')
pdf.bullet('利用母亲在邮储银行和金融行业的深厚人脉')
pdf.bullet('研究生阶段考取CFA一级/二级或CPA')
pdf.bullet('目标岗位：研究员/分析师/交易员/风控')
pdf.bullet('路径：暑期实习→留用→2-3年成长为独立分析师')

pdf.body('方向B：科技企业（AI/半导体/金融科技）')
pdf.bullet('利用科大系校友网络（237人覆盖科技/金融各界）')
pdf.bullet('研究生阶段积累编程/数据分析/项目管理能力')
pdf.bullet('目标岗位：产品经理/数据分析师/技术管理')
pdf.bullet('路径：实习→全职→2-3年成为骨干')

pdf.body('方向C：学术科研（读博→高校/研究院）')
pdf.bullet('研究生阶段表现出色的学术能力')
pdf.bullet('发表高水平论文（SCI/SSCI 2篇+）')
pdf.bullet('联系博导，申请博士项目（国内顶尖或海外）')
pdf.bullet('路径：博士→博士后→高校教职/研究员')

pdf.sub_title('二、2030-2031年里程碑')
pdf.bullet('2030年（24岁）：研究生毕业，确定第一份工作或博士入学')
pdf.bullet('2031年（25岁）：在所选赛道上站稳脚跟，形成初步的职业身份认同')

pdf.green_bar()
pdf.sub_title('五年的关键原则')
pdf.bullet('独立思考：选择真正感兴趣的方向，而非单纯追逐热门或家庭期望')
pdf.bullet('提前布局：保研/考研/求职，每一关都比别人提前半年准备')
pdf.bullet('善用资源：家庭金融人脉+科大校友网络+上海大学平台，三重资源叠加')
pdf.bullet('保持谦逊：性格中的"谦逊随和"是长期职业发展的优势，但需学会适时展示自己')
pdf.bullet('终身学习：持续阅读习惯（兴趣：阅读、历史），构建跨领域知识体系')

pdf.ln(4)
pdf.set_font('S', '', 9); pdf.set_text_color(0x99, 0x99, 0x99)
pdf.multi_cell(pdf.w - 2 * pdf.m, 6, '基于家庭资料、学业记录、个人特征分析。\n2026年5月20日 | 规划定期评估和调整。', align='C')
pdf.page_num()

import os
OUTPUT = '/Users/cyingfang/WorkBuddy/20260429082054/陈于东五年规划-2026-2031.pdf'
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
pdf.output(OUTPUT)
print(f'Saved: {OUTPUT} | Pages: {pdf.page_no()}')
