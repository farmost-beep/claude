#!/usr/bin/env python3
"""融资路线图 2025-2026 更新专题 PDF — 补充最新案例与机构信息"""

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
        self.set_font('H', '', 24); self.set_text_color(0x0D, 0x23, 0x4B)
        self.multi_cell(self.w - 2 * self.m, 12, main, align='C')
        if sub:
            self.ln(6); self.set_font('S', '', 11); self.set_text_color(0x55, 0x66, 0x77)
            self.multi_cell(self.w - 2 * self.m, 7, sub, align='C')
        self.ln(10); self.set_draw_color(0x00, 0x6D, 0xBA); self.set_line_width(0.6)
        cx = self.w / 2; self.line(cx - 25, self.get_y(), cx + 25, self.get_y())
        self.ln(6); self.set_font('S', '', 9); self.set_text_color(0x99, 0x99, 0x99)
        self.multi_cell(self.w - 2 * self.m, 6, '2026年5月 更新 | 内部参考', align='C')

    def ch_title(self, t):
        self.set_font('H', '', 16); self.set_text_color(0x0D, 0x23, 0x4B)
        self.set_x(self.m); self.cell(self.w - 2 * self.m, 10, t); self.ln(11)
        self.set_draw_color(0x00, 0x6D, 0xBA); self.set_line_width(0.5)
        self.line(self.m, self.get_y() - 5, self.m + 40, self.get_y() - 5); self.ln(5)

    def sub_title(self, t):
        self.set_font('H', '', 12); self.set_text_color(0x00, 0x6D, 0xBA)
        self.set_x(self.m); self.cell(self.w - 2 * self.m, 8, t); self.ln(9)

    def body(self, t):
        self.set_font('S', '', 9.5); self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m); self.multi_cell(self.w - 2 * self.m, 5.8, t, align='J'); self.ln(1.5)

    def bullet(self, t):
        self.set_font('S', '', 9.5); self.set_text_color(0x33, 0x33, 0x33)
        self.set_x(self.m); self.cell(6, 5.5, '>')
        self.multi_cell(self.w - 2 * self.m - 6, 5.8, t, align='J'); self.set_x(self.m); self.ln(0.5)

    def blue_bar(self):
        self.set_draw_color(0x00, 0x6D, 0xBA); self.set_line_width(0.3)
        y = self.get_y(); self.line(self.m, y, self.w - self.m, y); self.ln(3)

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

# ===== TITLE =====
pdf.title_page(
    '融资路线图 2025-2026 更新专题',
    '最新退出案例 · 机构动态 · 市场趋势 · 附原37页主文档')

# ================================================================
pdf.add_page()
pdf.ch_title('一、一级市场总览（2025-2026）')

pdf.sub_title('募资端')
pdf.bullet('2026年Q1新成立基金1,904支，同比+95.88%，几乎翻番')
pdf.bullet('参与机构1,266家，同比+89.81%，市场全面回暖')
pdf.bullet('新LP结构：企业投资者46%(最活跃) | 国资20% (出资占比34%) | 银行AIC出资+930% | 险资+387%')
pdf.bullet('国资从"绝对主导"转向"重要支撑"，产业LP崛起推动财务投资向产业投资转型')

pdf.sub_title('投资端')
pdf.bullet('2026年Q1投资案例3,195起，同比+33.24%')
pdf.bullet('投资规模4,071.8亿元，同比+35.66%')
pdf.bullet('连续半年月度投资规模破千亿，A轮主导市场')
pdf.bullet('热点赛道TOP5：半导体(1,068起/1,415亿) > AI(347起) > 医疗健康(449起) > 人形机器人(193起/465亿) > 低空经济')

pdf.sub_title('退出端')
pdf.bullet('2025年前三季度退出案例2,029笔，其中IPO退出1,002笔(+37.8%)')
pdf.bullet('2025年并购交易2,963笔(+12.58%)，交易金额1,786亿美元(+51.64%)')
pdf.bullet('2025年港股IPO融资约2,863亿港元，全球第一')
pdf.bullet('S基金2025年交易规模约784亿元(上半年)，国资成为S交易主力')

pdf.blue_bar()
pdf.note_box('核心趋势："两端扩容、中间收窄"——早期项目与头部大额融资活跃，腰部企业承压。退出渠道从IPO单一依赖转向IPO+并购+S交易+询价转让多元化。')

# ================================================================
pdf.add_page()
pdf.ch_title('二、2025-2026年标志性退出案例')

pdf.sub_title('1. 摩尔线程 — 科创板IPO（2025年12月）')
pdf.body('GPU芯片独角兽，2025年12月5日登陆科创板，首日暴涨425%，市值突破2,800亿元。早期投资者回报超5,000倍（190万元投资→市值超百亿）。背后超80家早期股东，包括红杉中国、深创投、腾讯等。是国产GPU赛道最标志性的退出案例，印证了硬科技IPO的造富效应。')
pdf.bullet('退出路径：科创板IPO')
pdf.bullet('投资回报：早期投资5,000倍+')
pdf.bullet('阶段覆盖：种子→天使→B→C→Pre-IPO')
pdf.bullet('关键机构：红杉中国、深创投、腾讯、中关村发展等')

pdf.sub_title('2. 沐曦股份 — 科创板IPO')
pdf.body('GPU芯片企业，上市为多家机构带来超额回报：葛卫东账面回报超165亿元，经纬创投超113亿元，和利资本超107亿元，红杉中国超92亿元。是2025年硬科技退出的又一标杆。')
pdf.bullet('退出路径：科创板IPO')
pdf.bullet('关键机构：经纬创投、红杉中国、和利资本')

pdf.sub_title('3. 英矽智能 — 港股IPO（2025年12月）')
pdf.body('AI制药龙头，2025年12月30日港股上市，募资22.77亿港元，为当年最高港股生物医药IPO。华平投资自2021年持续注资，成为最大单一股东。')
pdf.bullet('退出路径：港股IPO')
pdf.bullet('关键机构：华平投资')

pdf.sub_title('4. 壁仞科技 — 港股IPO（2026年1月）')
pdf.body('GPU企业，2026年1月2日登陆港股，首日收涨75.82%。')
pdf.bullet('退出路径：港股IPO')

pdf.sub_title('5. 启明创投"先拿壳再装资产" — 新模式里程碑（2025-2026）')
pdf.body('启明创投以5.42亿元收购天迈科技26.10%股权入主上市公司，随后启动向上市公司注入被投项目芬能自动化。这是"并购六条"后首单市场化创投机构入主上市公司的实践，被视为VC/PE退出模式的里程碑。')
pdf.bullet('退出路径：并购重组（控股上市公司→注入资产退出）')
pdf.bullet('关键人物：启明创投创始主管合伙人邝子平')
pdf.bullet('行业意义：VC/PE从"财务投资者"进化到"产业整合者"，退出逻辑从"等IPO"转向"造平台"')

# ================================================================
pdf.add_page()
pdf.ch_title('三、2025-2026年重大募资事件')

pdf.sub_title('国际PE/VC大额募资')
pdf.bullet('EQT BPEA IX基金：156亿美元(约1,000亿人民币)，超募，聚焦科技/医疗/工业')
pdf.bullet('贝恩资本亚洲基金VI：105亿美元(超额完成原70亿目标)，聚焦科技/工业/消费/医疗')
pdf.bullet('Paradigm：15亿美元，押注AI与机器人（加密VC跨界）')
pdf.bullet('康桥资本+GHO Capital合并：组建AUM超210亿美元的全球最大医疗健康投资平台')

pdf.sub_title('中国本土重要募资')
pdf.bullet('蓝池资本Riverside Fund：10亿美元，蔡崇信家族办公室首支PE基金，聚焦高端零售/金融科技/AI')
pdf.bullet('BAI资本美元基金：目标8亿美元(首关6亿)，龙宇主导，聚焦科技AI/金融服务/消费')
pdf.bullet('湖北社保科创基金：首期200亿元，光电子信息/汽车制造/生命健康/高端装备')
pdf.bullet('江苏省战新产业基金：100亿元，生物医药/新能源/集成电路/AI/机器人/低空经济')
pdf.bullet('东方嘉富中小企业基金：目标20亿元(首关16亿)，先进制造/新材料/前沿科技')

pdf.sub_title('LP结构新变化')
pdf.bullet('银行AIC出资同比+930%：工银AIC、建信AIC成为增量核心来源')
pdf.bullet('险资同比+387%：新华保险、中汇人寿等加速入场')
pdf.bullet('产业资本(企业投资者)占比46%，从财务投资向产业投资转型')

pdf.sub_title('合伙人/机构重要变动')
pdf.bullet('红杉中国(HongShan)：2026年AI赛道项目占比超53%，领投它石智航刷新融资纪录')
pdf.bullet('厚朴投资获澳门首家投资基金牌照，布局科技/消费/物流')
pdf.bullet('康桥资本CEO傅唯+GHO管理合伙人Mike Mortimer任联席CEO')

# ================================================================
pdf.add_page()
pdf.ch_title('四、2025-2026年投资热点赛道')

pdf.sub_title('1. 人形机器人/具身智能 — 最强风口')
pdf.body('从2024年初62起/35亿元跃升至2026年Q1的193起/465亿元，爆发式增长。驱动力：春晚破圈效应+国家战略扶持+核心零部件国产化突破+量产能力提升。资本结构：国家队+头部VC+产业资本全覆盖。')
pdf.bullet('银河通用：B轮25亿元')
pdf.bullet('它石智航：Pre-A轮4.55亿美元（刷新融资纪录），红杉中国领投')
pdf.bullet('千寻智能：近20亿元')
pdf.bullet('破壳机器人：种子轮4亿美元')
pdf.bullet('RoboParty：小米+顺为联合投资')

pdf.sub_title('2. AI大模型/Agent — 持续高热')
pdf.bullet('阶跃星辰：B+轮50亿元（印奇出任董事长）')
pdf.bullet('月之暗面：C轮+共超120亿元')
pdf.bullet('爱诗科技：C轮3亿美元')
pdf.bullet('核心趋势：从"模型层"竞争转向"应用层/AI Agent"落地')

pdf.sub_title('3. 半导体 — 绝对领跑')
pdf.body('2026年Q1交易1,068起，规模1,415亿元，是投资规模最大的赛道。GPU、AI芯片、先进制造为核心方向。')
pdf.bullet('神玑技术：22.57亿元')
pdf.bullet('摩尔线程/沐曦/壁仞：科创板/港股上市退出')

pdf.sub_title('4. 医疗健康 — 稳健增长')
pdf.bullet('2026年Q1交易449起')
pdf.bullet('箕星药业：D1轮2.87亿美元')
pdf.bullet('英矽智能：港股IPO 22.77亿港元')

pdf.blue_bar()
pdf.note_box('赛道判断：未来12-18个月，人形机器人和AI Agent将成为一级市场最活跃的两大赛道，半导体继续领跑规模。建议重点关注具身智能供应链和AI行业应用层机会。')

# ================================================================
pdf.add_page()
pdf.ch_title('五、退出渠道多元化趋势')

pdf.sub_title('1. IPO仍是核心，但不再唯一')
pdf.bullet('A股IPO持续回暖，科创板成硬科技主要退出通道')
pdf.bullet('港股保持活跃，2025年融资额全球第一')
pdf.bullet('科创板成为半导体/AI企业首选')

pdf.sub_title('2. 并购退出全面崛起')
pdf.bullet('2025年1-11月并购交易2,963笔(+12.58%)，金额1,786亿美元(+51.64%)')
pdf.bullet('"并购六条"(2024.9)+新重组办法(2025.5)扫清制度障碍')
pdf.bullet('私募基金收购上市公司控制权成为新策略')
pdf.bullet('梅花创投吴世春三次出手购买上市公司股权')
pdf.bullet('初芯集团入主皮阿诺')
pdf.bullet('奇瑞瑞丞基金15.75亿元收购鸿合科技25%股权')

pdf.sub_title('3. S基金交易快速增长')
pdf.bullet('2024年国内S基金交易规模1,078亿元(+46%)')
pdf.bullet('2025年上半年交易笔数已超2024全年，规模约784亿元')
pdf.bullet('国资成为S交易主力，粤科母基金积极策划S基金')

pdf.sub_title('4. 柔性退出机制兴起')
pdf.bullet('湖南/山东等地鼓励取消强制回购条款')
pdf.bullet('分期回购、债务重组、股权平移等新机制出现')
pdf.bullet('"一轮退"或"隔轮退"：先行回收本金，保留份额寻求增值')

pdf.sub_title('5. 询价转让常态化')
pdf.bullet('2026年以来12家A股上市公司实施询价转让')
pdf.bullet('易方达、华夏、诺德等公募私募积极参与，部分浮盈超30%')

pdf.blue_bar()
pdf.note_box('关键趋势：VC/PE退出模式正从"IPO单一依赖"转向"IPO+并购+S基金+询价转让"多元化。"先拿壳再装资产"的新型退出模式为行业打开全新空间。')

# ================================================================
pdf.add_page()
pdf.ch_title('六、更新总览')

pdf.body('以下为本次更新对主文档各章节的补充内容索引：')

updates = [
    ['主文档章节', '更新内容'],
    ['第一篇：退出TOP5统计', '新增2025年IPO案例验证退出率趋势（摩尔线程/英矽智能/沐曦）'],
    ['第二篇：行业路线图', '新增人形机器人赛道爆发性增长数据(Q1 193起/465亿)'],
    ['第三篇：种子/天使轮', '补充新机构：BAI资本(8亿美元新基金)、蓝池资本(10亿美元)'],
    ['第四篇：A轮', '新增2026年Q1 A轮活跃度数据(3,195起/+33%)'],
    ['第五篇：B/C轮', '新增千寻智能(近20亿)、银河通用(25亿)、阶跃星辰(50亿)等B/C轮案例'],
    ['第六篇：D/Pre-IPO', '新增壁仞科技港股上市、英矽智能港股IPO案例'],
    ['第七篇：IPO退出', '更新A股/港股2025年IPO数据；新增摩尔线程等标杆案例'],
    ['第八篇：并购退出', '大幅更新——新增启明创投"先拿壳再装资产"、梅花创投买壳等新模式'],
    ['第九篇：国资分析', '更新国资投资趋势：从"绝对主导"转向"重要支撑"(出资占比34%)'],
    ['附篇：联系人', '新增贝恩资本、EQT、康桥资本等新进入中国市场的机构信息'],
]

pdf.set_font('S', '', 9)
for i, r in enumerate(updates):
    pdf.set_fill_color(0xE8, 0xF0, 0xF8) if i == 0 else (
        pdf.set_fill_color(0xF5, 0xF8, 0xFC) if i % 2 == 0 else pdf.set_fill_color(0xFF, 0xFF, 0xFF))
    pdf.set_text_color(0x0D, 0x23, 0x4B) if i == 0 else pdf.set_text_color(0x33, 0x33, 0x33)
    pdf.set_font('H', '', 9) if i == 0 else pdf.set_font('S', '', 9)
    pdf.set_x(pdf.m)
    pdf.cell(45, 6, r[0], border=1, fill=True)
    pdf.cell(pdf.w - 2 * pdf.m - 45, 6, r[1], border=1, fill=True)
    pdf.ln()

pdf.ln(4)
pdf.body('建议：本更新专题与主文档《中国企业融资路线图v2.pdf》(37页)配合阅读，可覆盖截至2026年5月的最新市场动态。')

pdf.ln(4)
pdf.set_font('S', '', 8); pdf.set_text_color(0x99, 0x99, 0x99)
pdf.multi_cell(pdf.w - 2 * pdf.m, 5,
    '数据来源：投中嘉川CVSource、清科研究中心、每日经济新闻、证券时报、36氪、普华永道《2025年中国企业并购市场回顾》等。\n2026年5月25日更新。仅供内部参考。', align='C')
pdf.page_num()

import os
OUTPUT = '/Users/cyingfang/WorkBuddy/20260429082054/融资路线图2025-2026更新专题.pdf'
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
pdf.output(OUTPUT)
print(f'Saved: {OUTPUT} | Pages: {pdf.page_no()}')
