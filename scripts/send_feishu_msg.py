#!/usr/bin/env python3
import os
import json
import urllib.request
import sys

APP_ID = os.environ.get("FEISHU_APP_ID")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET")
CHAT_ID = "oc_f1a6804e3b539ea30888fb067e82ac42"

if not APP_ID or not APP_SECRET:
    print("ERROR: FEISHU_APP_ID and FEISHU_APP_SECRET must be set in environment", file=sys.stderr)
    sys.exit(1)

# Step 1: Get tenant access token
token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
token_data = json.dumps({
    "app_id": APP_ID,
    "app_secret": APP_SECRET
}).encode("utf-8")

req = urllib.request.Request(token_url, data=token_data, method="POST")
req.add_header("Content-Type", "application/json")
try:
    resp = urllib.request.urlopen(req)
    token_result = json.loads(resp.read().decode("utf-8"))
except Exception as e:
    print(f"ERROR: Failed to get access token: {e}", file=sys.stderr)
    sys.exit(1)

if token_result.get("code") != 0:
    print(f"ERROR: Token API error: {token_result}", file=sys.stderr)
    sys.exit(1)

access_token = token_result["tenant_access_token"]

# Step 2: Send message
msg_text = """🔬 ultracode 本源量子 综合评估

🎯 核心判断: 本源量子是中国唯一在超导量子计算单芯片比特数（180比特）上达到全球领先、且同时拥有自主芯片产线（6英寸/良率92%）和批量出口能力（稀释制冷机）的量子计算整机企业，其核心竞争力在于"技术指标领先+产业链自主可控+央企背书+科创板预期"的复合优势。

🛡️ 技术壁垒: 高。悟空-180单芯片180计算比特全球超导路线第一；双比特门99.00%触及容错阈值；授权专利超1300项（发明专利>82%），量子计算领域全球第二（仅次于IBM）。短板：单体T1约40μs远低于IBM Nighthawk（350μs）和Google Willow（100-150μs），纠错能力落后Google一个里程碑。
💼 商业化: 中低。2024年营收不足1亿元、净亏损3420万，收入与估值比严重失衡（~1:200）。但营收增速强劲（2025Q1同比+134%）、全球化进展显著（163国/5000万访问/90万任务），且已实现中国自主量子算力首次出口销售。
💡 科技金融启示: 本源量子提供了"含科量"评估的三个新维度：①产业链自主化程度（6英寸芯片线自建、稀释制冷机出口——衡量是否被"卡脖子"的关键指标）；②全球化渗透率（163国访问量、海外客户订单——验证技术接受度的市场化检验）；③发明专利占比（>82%）比专利总数更能反映技术质量。这三项指标比单纯的"研发投入占比"更能识别真科技企业。

⚠️ 风险: 行业级风险：距离实用容错量子计算仍需5-10年，收入与投资比约1:18，行业仍靠资本支撑而非自我造血，本源估值200亿+与不足亿元营收存在巨大落差。 / 地缘政治风险：本源已列入美国实体清单，高端测控设备（低温高频电子器件）进口受限，中美科技脱钩加剧可能进一步影响技术获取和国际市场拓展。 / 技术路线不确定性：超导路线虽当前生态最成熟，但离子阱（>99.99%保真度）、中性原子（千原子扩展）、拓扑（微软Majorana 2相干时间千倍提升）等多路线并行竞争，路径收敛前任何单一路线存在被替代风险。 / 股权分散和上市时间不确定性：IPO辅导尚在进行中，与国仪量子竞争A股'量子计算第一股'，科创板对未盈利企业的审核趋严增加上市风险。

📊 vs 国盾量子: 国盾量子与本源量子代表量子科技的两条不同赛道和商业模式。国盾专注量子通信（QKD+QRNG），对标市场为政务/金融/国防的加密通信领域，中国在该领域全球绝对领先，国盾2020年已科创板上市，拥有稳定现金流和盈利能力，但市场天花板相对有限（量子通信整体市场远小于量子计算）。本源专注通用量子计算，对标IBM/Google全球巨头，市场天花板高达数千亿美元级，但距商业化盈利更远（5-10年窗口），风险更高。简言之：国盾是"确定性强但天花板有限"，本源是"天花板极高但不确定性巨大"，两家公司对银行科技金融的评估方法截然不同——国盾适合成熟期信贷模式，本源适合投贷联动+政策性风险分担模式。"""

msg_url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
msg_body = json.dumps({
    "receive_id": CHAT_ID,
    "msg_type": "text",
    "content": json.dumps({"text": msg_text})
}).encode("utf-8")

req2 = urllib.request.Request(msg_url, data=msg_body, method="POST")
req2.add_header("Content-Type", "application/json; charset=utf-8")
req2.add_header("Authorization", f"Bearer {access_token}")

try:
    resp2 = urllib.request.urlopen(req2)
    msg_result = json.loads(resp2.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    err_body = e.read().decode("utf-8")
    print(f"ERROR: Send message HTTP {e.code}: {err_body}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"ERROR: Failed to send message: {e}", file=sys.stderr)
    sys.exit(1)

if msg_result.get("code") == 0:
    print("Message sent successfully.")
    print(json.dumps(msg_result.get("data", {}), ensure_ascii=False))
else:
    print(f"ERROR: Send message API error: {msg_result}", file=sys.stderr)
    sys.exit(1)
