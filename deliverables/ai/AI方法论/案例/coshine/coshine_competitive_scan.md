---
goal: AI能力
type: AI方法论案例—竞争情报
company: Coshine（开先）
version: v1.1
date: 2026-05-29
last_updated: 2026-05-29
---

# 支付处理器行业AI竞争情报

> 追踪主要竞争对手的AI动态，判断Coshine的战略方向是否需要校准。
>
> 更新节奏：每月至少1次，重大事件即时更新。

---

## 行业全景：2026年是"AI Agent支付元年"

2026年全球支付处理行业的核心主题是 **Agentic Commerce（代理型商务）**——AI Agent代表人类自主搜索、决策和执行支付。McKinsey预测到2030年全球Agentic Commerce交易额可达$3-5万亿。

**协议层格局（两层的标准争夺战）：**

| 层 | 协议 | 主导方 | 特点 |
|:---|:---|:---|:---|
| 意图编排 | ACP | OpenAI+Stripe | 用户委托支付权限给AI Agent（ChatGPT Instant Checkout已关闭，因转化率低） |
| | UCP | Google | 开放标准，30+合作伙伴（Shopify/Stripe/Visa/Mastercard/Walmart） |
| 结算 | SPT | Stripe | 基于现有卡网络的共享支付token |
| | Visa智能商务 | Visa | 升级版token化，含身份元数据绑定 |
| | Mastercard Agentic Token | Mastercard | 首个完整身份Agent交易已完成（2025.09，与CBA合作） |
| | x402 | Coinbase | HTTP 402状态码原生加密支付（USDC），日活约$28K |
| | MPP | Tempo+Stripe | 多轨框架，支持稳定币/法币/卡网络token/Bitcoin Lightning |

**关键趋势：**
- B2C Agentic Commerce进展缓慢（仅24%美国人信任AI代购）
- B2B加速明显——预计2026年底约1/3的B2B支付工作流使用自主AI Agent
- "Know Your Agent"（KYA）成为新的身份验证范式
- 责任归属问题未解决——当消费者争议Agent授权的交易时，"友好欺诈"风险显著增加
- 主要支付处理器一致押注Agentic Commerce，但分歧在协议选择

---

## 主要竞争对手

| 公司 | 类型 | AI已知动态 | 对Coshine的启示 | 最近更新 |
|:---|:---|:---|:---|:---:|
| FIS | 全球最大Processor | **Jan 2026** 推出行业首个"Agentic Commerce"平台，让银行在AI Agent交易中保持核心地位。与Mastercard/Visa合作完成KYA信任框架。同日完成$13.5B收购Global Payments发卡业务(TSYS)。**AI驱动交易平台**：AI作为个人数字助理，可代客搜索、谈判、完成支付（预授权方式）。Q1 2026向所有FIS发卡银行客户开放。 | FIS走"银行中心化"路线——让银行保持在AI Agent交易中的核心地位。Coshine若聚焦银行客户，需提供与FIS兼容的AI支付接口 | 2026-05 |
| Fiserv | 全球第二大Processor | **May 2026** 推出**agentOS**——面向银行的AI操作系统。含Agent Marketplace（4个Fiserv自建Agent+9个第三方Agent），基于Amazon Bedrock AgentCore。首批客户含First Interstate Bank/Bank OZK/SouthState等。**同日**宣布与OpenAI战略合作。**Jan 2026**同时与Microsoft（AI云基础设施）、Mastercard（Agent Pay接入）、Visa（Trusted Agent Protocol）达成合作。计划Aug 2026全面可用。 | Fiserv是Coshine最强劲的AI竞争对手——openAI+Microsoft+Mastercard+Visa全线联动，覆盖银行核心+支付+商户。Coshine需要在细分场景（如中国本地化/ISO8583迁移/合规自动化）建立差异化 | 2026-05 |
| Global Payments | 全球Processor | **May 2026** 推出**AI-first Genius手持POS**——端侧神经网络处理AI工作负载（非云端），支持语音点单、实时上销、自然语言菜单管理。5G+离线支付模式。在NRA Chicago展会上首发。已获CKE Restaurants（Hardee's/Carl's Jr.）2400+门店独家POS合同。**AI转型方向**：从纯支付处理转向"软件嵌入式+AI赋能"商务解决方案。 | 走"硬件+AI"路线，聚焦商户端而非银行端。与Coshine的直接竞争有限——除非Coshine也做POS硬件 | 2026-05 |
| ACI Worldwide | 支付软件/Processor | **Mar 2026** 推出**ACI Connetic**云原生统一支付平台，整合A2A+卡支付+ATM，内置AI风控。处理3000亿+卡交易/年。**Feb 2026** MIT Sloan Fintech Conference发言：Agentic Commerce需要**可验证权限+持久身份+可证明的公平结果**。**年度预测**：AI将成为盈利倍增器，"智能编排"（实时决策平衡成本/速度/风险/合规）是竞争必需品。 | ACI Connetic的"统一平台"思路与Coshine有重叠。Coshine需关注：ACI在中国的布局有限，这是Coshine的本地化优势 | 2026-05 |
| Worldline | 欧洲最大Processor | **Jan 2026** 推出**MCP Server（Model Context Protocol）**——让LLM能通过自然语言调用Worldline支付API（"给交易XXXX退款"）。同时推出**ConnectAI**开发者平台。支持Google AP2、OpenAI ACP、Visa/Mastercard框架。**PAY360 2026**：AI作为多轨支付环境的编排层 + 适应性风控。营收€46亿，服务100万+商户。 | Worldline的MCP Server是行业内最务实的AI接入方案——不追求自主AI，而是做"AI接入层"。Coshine可借鉴此思路，做中国本地支付协议的MCP封装 | 2026-05 |
| Nexi | 欧洲Processor | **Mar 2026** 与**Google Cloud**签订MoU共建Agentic Commerce基础设施。推出MCP让开发者用对话指令连接Nexi支付系统。北欧和意大利已有试点商户。**Jan 2026**加入**Agentic Commerce Alliance(ACA)**。**Feb 2026**推出Nexi Ready（数字发卡方案，内置EU AI Act/PSD3合规）。 | Nexi的Google Cloud合作路线指向"云原生Agentic Commerce"。Coshine需注意：如果商户端的Agent标准最终被Google UCP统一，Coshine需要UCP兼容 | 2026-05 |
| Network International | 中东/非洲Processor | **2026** 全面AI转型——从传统处理转向"洞察驱动型金融科技平台"。AI部署在风控（Mastercard Brighterion AI）、对账、销售、运营全栈。**Agentic Commerce**：正在构建AI Agent-to-Agent支付基础设施。**My Network App**：AI驱动的商户实时数据洞察。**稳定币/CBDC**：首个接入阿联酋央行CBDC的支付平台。覆盖56个市场，处理$4000亿+支付量。 | Network International的"全栈AI+新兴市场"路线表明：AI支付不只在成熟市场——新兴市场（尤其是金融基础设施薄弱的地区）可能是AI支付更快落地的场景 | 2026-05 |

---

## 行业趋势信号

| 信号 | 来源 | 日期 | 对Coshine的影响 |
|:---|:---|:---|:---|
| 所有7家主要Processor在2026年H1全部推出Agentic Commerce相关产品（MCP/Agent平台/协议支持） | 各公司官方发布 | 2026 H1 | Coshine必须有自己的AI Agent支付方案——"我们不急"=3年内出局 |
| B2C Agent信任度仅24%，但B2B Agent支付预计2026年底达1/3 | Forrester | 2026-05 | Coshine应优先聚焦B2B场景（对账/采购/退款自动化），B2C可延后 |
| "Know Your Agent"（KYA）成为新的身份验证范式 | Visa/Mastercard/FIS | 2026 | KYA将是Coshine的下一个合规要求——需在产品路线图中考虑 |
| 协议大战：OpenAI ACP vs Google UCP vs Visa/Mastercard自有框架 | 多方 | 2025-2026 | Coshine做架构决策时的关键因素——押注哪个协议生态风险最低？ |
| 传统ISO8583迁移到云原生API的进程加速（ACI Connetic为代表） | ACI Worldwide | 2026-03 | Coshine的ISO8583经验在下一次协议升级周期中是核心资产 |
| PCI DSS + AI合规框架正在形成（EU AI Act + 各国监管） | EU/监管机构 | 2026 | AI支付产品的合规成本会显著上升——提前准备比追赶好 |

---

## 搜索维度（用于Agent C1定期搜索）

1. "[公司名] AI payment processor" — 各公司AI在支付处理的应用
2. "[公司名] acquires AI" — AI相关收购
3. "[公司名] AI partnership" — AI合作伙伴关系
4. "payment processor AI fraud detection 2026" — 行业AI风控趋势
5. "ISO8583 AI migration" — 支付协议AI迁移
6. "PCI DSS AI compliance" — AI合规自动化
7. "card processor AI copilot" — 竞争对手的AI Copilot动向
8. "Agentic Commerce protocol China" — 中国市场的AI Agent支付协议动态
