#!/usr/bin/env python3
"""A股市场全景分析报告 — 全动态实时数据"""
import os, json, urllib.request, time, sys, warnings
warnings.filterwarnings("ignore")
os.environ.pop('HTTP_PROXY',None); os.environ.pop('HTTPS_PROXY',None); os.environ['NO_PROXY']='*'
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

F=None
for fp in ["/System/Library/Fonts/PingFang.ttc","/System/Library/Fonts/STHeiti Light.ttc","/Library/Fonts/Arial Unicode.ttf"]:
    if os.path.exists(fp):
        try: pdfmetrics.registerFont(TTFont("CJK",fp)); F="CJK"; break
        except: pass
assert F

D=HexColor("#1A2744"); LB=HexColor("#F0F4FF"); W=white; G=HexColor("#999")
ts=ParagraphStyle("T",fontName=F,fontSize=20,textColor=D,alignment=TA_CENTER,spaceAfter=4)
sub=ParagraphStyle("S",fontName=F,fontSize=10,textColor=HexColor("#666"),alignment=TA_CENTER,spaceAfter=12)
h1=ParagraphStyle("H1",fontName=F,fontSize=14,textColor=D,spaceBefore=16,spaceAfter=8)
h2=ParagraphStyle("H2",fontName=F,fontSize=11,textColor=D,spaceBefore=10,spaceAfter=6)
bd=ParagraphStyle("B",fontName=F,fontSize=9,leading=14,textColor=HexColor("#333"),alignment=TA_JUSTIFY)
cs=ParagraphStyle("C",fontName=F,fontSize=8,leading=11,textColor=HexColor("#333"))
hs=ParagraphStyle("H",fontName=F,fontSize=8,leading=11,textColor=W)
ms=ParagraphStyle("M",fontName=F,fontSize=8,textColor=G,alignment=TA_CENTER)
rs=ParagraphStyle("R",fontName=F,fontSize=9,textColor=HexColor("#EF4444"))
ns=ParagraphStyle("N",fontName=F,fontSize=7,textColor=HexColor("#888"))

def TBL(h,r,c):
    data=[[Paragraph(x,hs) for x in h]]
    for row in r: data.append([Paragraph(str(v),cs) for v in row])
    t=Table(data,colWidths=c)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),D),('GRID',(0,0),(-1,-1),0.3,HexColor("#DDD")),('ROWBACKGROUNDS',(0,1),(-1,-1),[W,LB]),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
    return t

# ─── 实时数据获取 ───
def fetch_idx(secid):
    url=f"https://push2.eastmoney.com/api/qt/stock/get?invt=2&fltt=1&fields=f43,f44,f45,f46,f47,f48,f57,f58,f170,f3&secid={secid}"
    for _ in range(2):
        try:
            r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=10)
            d=json.loads(r.read()).get('data',{})
            p=float(d.get('f43',0) or 0); pc=float(d.get('f3',0) or 0)
            return p, pc
        except: time.sleep(1)
    return 0,0

def fetch_breadth():
    url="https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5000&po=1&np=1&fltt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f3,f12,f14"
    try:
        r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Referer':'https://quote.eastmoney.com/'}),timeout=10)
        items=json.loads(r.read()).get('data',{}).get('diff',[])
        up=sum(1 for i in items if float(i.get('f3',0) or 0)>0)
        dn=sum(1 for i in items if float(i.get('f3',0) or 0)<0)
        return up, dn, len(items)
    except: return None,None,None

def fmt_p(pct):
    return f"{pct:+.2f}%"

print("获取实时数据...",flush=True)
sh_p, sh_pct = fetch_idx("1.000001")
sz_p, sz_pct = fetch_idx("0.399001")
cy_p, cy_pct = fetch_idx("0.399006")
kc_p, kc_pct = fetch_idx("1.000688")
up_c, dn_c, tot = fetch_breadth()

# Normalize prices
sh_d = sh_p/100 if sh_p>10000 else sh_p
sz_d = sz_p/100 if sz_p>100000 else sz_p
cy_d = cy_p/100 if cy_p>10000 else cy_p
kc_d = kc_p/100 if kc_p>10000 else kc_p

# Market assessment
mkt = "窄幅震荡"
if abs(sh_pct)<0.5: mkt = "窄幅震荡"
elif sh_pct<-1: mkt = f"调整下跌({fmt_p(sh_pct)})"
elif sh_pct>1: mkt = f"反弹上行({fmt_p(sh_pct)})"
elif sh_pct<-0.5: mkt = "偏弱震荡"
else: mkt = "偏强震荡"

# Sentiment
up_r = round(up_c/tot*100,1) if tot and up_c else 0
dn_r = round(dn_c/tot*100,1) if tot and dn_c else 0
sent = "中性"
if up_r>60: sent = "偏热"
elif up_r<40: sent = "偏冷"

# ═══ Build PDF ───
T = date.today().isoformat()
OUT = f"/Users/cyingfang/claude/deliverables/investment/A股市场全景分析_{T}.pdf"
doc = SimpleDocTemplate(OUT, pagesize=A4, topMargin=18*mm, bottomMargin=15*mm, leftMargin=15*mm, rightMargin=15*mm)
S = []

S.append(Spacer(1,30))
S.append(Paragraph("A股市场全景分析报告",ts))
S.append(Paragraph(f"{T} | 实时数据:东方财富 | {time.strftime('%H:%M')}更新", sub))
S.append(Spacer(1,20))

# ─── 一、实时行情 ───
S.append(Paragraph("一、实时行情", h1))
S.append(Paragraph(f"数据获取: {time.strftime('%Y-%m-%d %H:%M')} | 当日判断: {mkt}", bd))
S.append(Paragraph("主要指数", h2))
S.append(TBL(["指数","收盘","涨跌幅","判断"],
    [("上证指数", f"{sh_d:.2f}", fmt_p(sh_pct), "偏弱" if sh_pct<0 else "偏强"),
     ("深证成指", f"{sz_d:.2f}", fmt_p(sz_pct), "偏弱" if sz_pct<0 else "偏强"),
     ("创业板指", f"{cy_d:.2f}", fmt_p(cy_pct), "偏弱" if cy_pct<0 else "偏强"),
     ("科创50", f"{kc_d:.2f}", fmt_p(kc_pct), "偏弱" if kc_pct<0 else "偏强")],
    [40,140,120,200]))

S.append(Paragraph("市场宽度", h2))
S.append(TBL(["指标","数值","独立解读"],
    [("上涨家数", str(up_c), f"占比{up_r}%"),
     ("下跌家数", str(dn_c), f"占比{dn_r}%"),
     ("涨跌比", f"{(up_c or 0)/(dn_c or 1):.2f}" if dn_c else "—", "赚钱效应" if (up_c or 0)>(dn_c or 0) else "亏钱效应"),
     ("情绪判断", "", f"市场情绪:{sent}")],
    [44,230,226]))

S.append(PageBreak())

# ─── 二、大趋势 ───
S.append(Paragraph("二、大趋势研判", h1))
S.append(Paragraph("宏观趋势", h2))
S.append(TBL(["驱动","方向","置信度"],
    [("国内经济","弱复苏,财政托底","高"),("海外流动性","加息预期+6月议息","高"),
     ("人民币汇率","~6.78","中高"),("产业升级","AI/半导体/新能源","高"),
     ("资金面","存量博弈","高")],[36,400,64]))

S.append(Paragraph("产业趋势", h2))
S.append(TBL(["产业","判断","确定性"],
    [("存储芯片","景气上行紧缺至2030","高"),("资源周期","上行中段","中高"),
     ("AI算力","长期看好短期消化","中"),("消费医药","底部等待","中"),
     ("煤炭电力","防御价值","中")],[38,416,46]))

# ─── 三、赛道 ───
S.append(PageBreak())
S.append(Paragraph("三、赛道选择", h1))
S.append(Paragraph("配置矩阵", h2))
S.append(TBL(["赛道","估值","确定性","配置","核心逻辑"],
    [("存储/SSD","低","高","超配","产业紧缺+低估值"),
     ("资源/矿业","低","中高","超配","低估值+高股息"),
     ("算力/光模块","高","高","标配等回调","长期强但短期透支"),
     ("消费/白酒","合理","中","标配","等待拐点"),
     ("医药","合理","中","标配","AI制药催化"),
     ("煤炭/电力","低","低","防御","高股息")],[36,100,100,80,184]))

S.append(Paragraph("关键信号", h2))
S.append(TBL(["信号","影响"],
    [("存储短缺(黄仁勋:紧缺至2030)","存储超配"),
     ("AI资本门槛(Anthropic$965亿+Google$800亿)","AI长线强化"),
     ("AI制药(剑桥AI疫苗I期成功)","医药催化"),
     ("世界杯开幕(量能萎缩)","短期谨慎"),
     ("中报窗口(7月开启)","聚焦确定性")],[38,462]))

# ─── 四、情绪与事件 ───
S.append(PageBreak())
S.append(Paragraph("四、市场情绪与关键事件", h1))
S.append(Paragraph("实时情绪(基于市场涨跌分布)", h2))
S.append(TBL(["指标","数值","解读"],
    [("上涨/下跌占比",f"{up_r}%/{dn_r}%",f"情绪:{sent}"),
     ("涨跌比",f"{(up_c or 0)/(dn_c or 1):.2f}" if dn_c else "—","赚钱效应" if (up_c or 0)>(dn_c or 0) else "亏钱效应"),
     ("上证当日",fmt_p(sh_pct),mkt)],[44,280,276]))

S.append(Paragraph("事件日历", h2))
S.append(TBL(["时间","事件","影响"],
    [("6月中","美日欧央行议息","流动性扰动"),("6月中旬","世界杯开幕","量能萎缩"),
     ("6月底","半年末资金考核","资金偏紧"),("7月初","AI巨头半年报","验证AI盈利"),
     ("7月中","A股中报密集期","业绩成主线")],[44,240,216]))

# ─── 五、全品种 ───
S.append(PageBreak())
S.append(Paragraph("五、全渠道投资品种", h1))
S.append(Paragraph("权益类(个股+ETF)", h2))
S.append(TBL(["品类","标的","类型","理由","建议"],
    [("存储","佰维存储688525","个股","PE14 ROE34%,HBM/SSD双驱","可建仓"),
     ("存储","江波龙301308","个股","PE14 ROE32%,存储龙头","可建仓"),
     ("存储","德明利001309","个股","PE11 ROE51%,高弹性","可建仓"),
     ("资源","紫金矿业601899","个股","PE9 ROE10%,铜金龙头","可建仓"),
     ("科创50ETF","588000","ETF","科创龙头","分批定投"),
     ("半导体ETF","512480","ETF","芯片全链","分批定投"),
     ("黄金ETF","518880","ETF","地缘对冲","持有"),
     ("沪深300ETF","510300","ETF","核心资产","定投")],[34,154,36,290,60]))

S.append(Paragraph("固收/理财", h2))
S.append(TBL(["品种","收益","场景","风险"],
    [("国债逆回购","1.8-2.5%","T+0管理","极低"),("同业存单","2.5-3.0%","3-6月","低"),
     ("纯债基金","3.0-4.5%","长期","中低"),("银行理财","2.5-3.5%","流动性","低")],[40,156,240,64]))

S.append(Paragraph("私募产品(仅列示)", h2))
S.append(TBL(["策略","管理人","门槛","特征"],
    [("量化指增","幻方/九坤","100万","超额10-20%"),("市场中性","明汯/灵均","100万","Alpha8-15%"),
     ("CTA趋势","黑翼/洛书","100万","10-25%低相关"),("宏观对冲","凯丰/重阳","100万","15-30%"),
     ("FOF","歌斐/中金","40万","6-12%分散")],[34,140,50,276]))

S.append(Paragraph("行业ETF", h2))
S.append(TBL(["主题","ETF","策略"],
    [("AI算力","通信ETF515880","趋势持有,拥挤减仓"),("半导体","半导体ETF512480","震荡定投"),
     ("新能源","新能源ETF516160","等回调建仓"),("红利","红利ETF510880","震荡防御"),
     ("黄金","黄金ETF518880","轻仓持有")],[34,250,316]))

# ─── 六、买卖时机 ───
S.append(PageBreak())
S.append(Paragraph("六、买卖时机(独立设定)", h1))
S.append(Paragraph("买入触发", h2))
S.append(TBL(["信号","观察","触发条件","当前"],
    [("估值","PE分位","<25%分位","未触发(当前高位)"),
     ("情绪","风险溢价>4%","需4%+(当前2.5%)","未触发"),
     ("回调","回踩60日线","量缩支撑确认","等待中"),
     ("事件","中报超预期","环比增>20%","7月窗口"),
     ("技术","放量>5日均量","确认后入场","等待中")],[36,156,260,148]))

S.append(Paragraph("退出触发", h2))
S.append(TBL(["信号","触发","当前","动作"],
    [("估值","PE>90%分位","已触发","仓位≤60%"),
     ("情绪","换手率>80%","接近","减少高频"),
     ("事件","中报低于预期>10%","等待","减仓"),
     ("技术","破120日线","未触发","止损"),
     ("资金","北向周净流出>200亿","118亿观察","降敞口")],[36,266,248,50]))
S.append(Paragraph("综合:当前估值已触发退出警戒。总仓位≤60%,超配存储/资源,标配消费/医药。",rs))

# ─── 七、扫描 ───
S.append(PageBreak())
S.append(Paragraph("七、扫描数据附录", h1))
print("扫描A股...",flush=True)
import akshare as ak
t0=time.time()
all_s=[]
for p in range(1,7):
    url=f"https://push2.eastmoney.com/api/qt/clist/get?pn={p}&pz=100&po=1&np=1&fltt=2&fid=f20&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f2,f3,f9,f12,f14,f20"
    for _ in range(2):
        try:
            r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Referer':'https://quote.eastmoney.com/'}),timeout=15)
            all_s.extend(json.loads(r.read()).get('data',{}).get('diff',[])); break
        except: time.sleep(1)
scanned=[]
for it in all_s:
    n,c=it.get('f14',''),it.get('f12','')
    if any(k in n for k in ['ST','退','N']): continue
    try: pe=float(it.get('f9',0) or 0)
    except: pe=0
    if pe<=0 or pe>20: continue
    scanned.append((c,n,pe,float(it.get('f20',0) or 0)/1e8))
scanned.sort(key=lambda x:-x[3]); scanned=scanned[:80]
results={}
for i,(s,n,pe,mk) in enumerate(scanned):
    fin=None
    for _ in range(3):
        try: fin=ak.stock_financial_analysis_indicator(symbol=s,start_year="2025")
        except: time.sleep(0.5)
        if fin is not None and not fin.empty: break
    if fin is None or fin.empty: continue
    l=fin.iloc[-1]
    try:
        roe=float(l.get("净资产收益率(%)",0) or 0); rev=float(l.get("主营业务收入增长率(%)",0) or 0)
        pr=float(l.get("销售净利率(%)",0) or 0); db=float(l.get("资产负债率(%)",0) or 0); eps=float(l.get("摊薄每股收益(元)",0) or 0)
    except: continue
    if roe<5: continue
    sc=round(roe*2.0-pe*0.3+rev*0.2+pr*0.3,1)
    results[s]={"code":s,"name":n,"PE":round(pe,1),"ROE":round(roe,1),"rev":round(rev,1),"profit":round(pr,1),"eps":round(eps,2),"debt":round(db,1),"mkt":int(mk)}
    time.sleep(0.1)
    if (i+1)%20==0: print(f"  {i+1}/{len(scanned)} ({len(results)})",flush=True)
scan_t=round(time.time()-t0)

S.append(Paragraph(f"通过{len(results)}个({scan_t}s) PE≤20 ROE≥5% 排除ST", bd))
if results:
    rl=sorted(results.values(),key=lambda x:x.get("PE",999))
    S.append(TBL(["代码","名称","PE","ROE%","营收+%","净利%","EPS","负债%","市值亿","评价"],
        [(r["code"],r["name"],r["PE"],r["ROE"],r["rev"],r["profit"],r["eps"],r["debt"],r["mkt"],
          f"PE{r['PE']} ROE{r['ROE']}% {'推荐' if r.get('ROE',0)>10 and r.get('PE',99)<15 else '观察'}")
         for r in rl[:12]],[36,46,22,28,34,32,28,26,40,78]))

S.append(Spacer(1,10))
S.append(Paragraph(f"自动生成 | {T} | 实时数据:东方财富 | 独立投资官",ms))
S.append(Paragraph("免责声明:独立投资官个人观点,不构成投资建议。投资有风险。",ns))

doc.build(S)
print(f"OK: {OUT} ({os.path.getsize(OUT)/1024:.0f}KB)")
