# Claude Code 金融插件使用场景手册

> 作者：陈颖芳 | 日期：2026-05-27 | 版本：v2.0（19插件全量覆盖）
> 插件来源：Anthropic Financial Services Plugins（官方市场）
> 安装命令：`claude plugin marketplace add anthropics/financial-services-plugins`

---

## 一、已安装的19大金融插件（全量）

### A区：投资研究线（10个，首次安装）

| # | 插件 | 版本 | 类型 | 一句话定位 |
|---|------|------|------|-----------|
| 1 | `financial-analysis` | 0.1.1 | 垂直 | 核心财务建模：DCF/LBO/Comps/三表模型 |
| 2 | `equity-research` | 0.1.2 | 垂直 | 股票研究：财报分析/覆盖报告/晨报/选题 |
| 3 | `investment-banking` | 0.2.1 | 垂直 | 投行：CIM/Teaser/并购模型/买家名单 |
| 4 | `private-equity` | 0.1.2 | 垂直 | PE：投委会备忘录/尽调/交易筛选/价值创造 |
| 5 | `wealth-management` | 0.1.2 | 垂直 | 财富管理：客户报告/再平衡/税务优化 |
| 6 | `market-researcher` | 0.1.1 | 代理 | 市场研究：竞品分析/行业概览/选题生成 |
| 7 | `valuation-reviewer` | 0.1.1 | 代理 | 估值审查：IC备忘录/组合监控/回报分析 |
| 8 | `model-builder` | 0.1.0 | 代理 | 模型构建：三表/DCF/LBO/审计Excel |
| 9 | `pitch-agent` | 0.1.1 | 代理 | 路演资料：Pitch Deck/行业概览/QC审查 |
| 10 | `earnings-reviewer` | 0.1.1 | 代理 | 财报审查：财报预览/模型更新/晨报 |

### B区：对公信贷线（9个，5/27新增）

| # | 插件 | 版本 | 类型 | 一句话定位 |
|---|------|------|------|-----------|
| 11 | `operations` | 0.1.0 | 垂直 | 银行运营：KYC文档解析+规则网格评估 |
| 12 | `kyc-screener` | 0.1.0 | 代理 | 客户准入：解析尽调文档→跑合规引擎→标记缺口 |
| 13 | `statement-auditor` | 0.1.0 | 代理 | 财报审核：财务报表准确性/完整性/审计就绪度 |
| 14 | `meeting-prep-agent` | 0.1.1 | 代理 | 客户拜访：自动生成拜访简报 |
| 15 | `fund-admin` | 0.1.0 | 垂直 | 贷后管理：GL对账/应计/滚动/NAV验证 |
| 16 | `gl-reconciler` | 0.1.0 | 代理 | 账务核对：差异追踪+根因分析+签批路由 |
| 17 | `month-end-closer` | 0.1.0 | 代理 | 月末关账：应计/滚动/差异说明/关账报告 |
| 18 | `lseg` | 1.0.0 | 合作 | LSEG数据：债券定价/收益率曲线/利率分析 |
| 19 | `sp-global` | 1.0.1 | 合作 | S&P数据：公司快览/财报预览/交易摘要 |

**总计：100+技能，35+斜杠命令，11个MCP数据源**（FactSet, Moody's, S&P Global, Morningstar, PitchBook, LSEG等）

> 注：MCP数据源需企业订阅账号才能使用。斜杠命令和技能开箱即用，无需额外配置。

---

## 二-A：投资研究线（原10插件场景）

### 目标一：投资成功 — 持仓分析

**核心插件：`equity-research` + `financial-analysis` + `market-researcher`**

```
/earnings         昆仑万维    → 分析最新财报，提取管理层指引、风险提示
/thesis           昆仑万维    → 跟踪投资论点是否成立
/morning-note                 → 每日晨报：自选股异动+宏观事件
/screen                        → 按PE/ROE/行业筛选标的
/catalysts                     → 未来30天的催化剂日历
/dcf               昆仑万维    → 自由现金流折现估值
/comps             昆仑万维    → 可比公司分析，看昆仑vs同行的PE/PS/EV-EBITDA
/sector            互联网      → AI/互联网行业概览
/competitive-analysis 昆仑万维 → 昆仑vs竞品的竞争力雷达图
/model-update      昆仑万维    → 财报后自动更新三表模型
```

**典型工作流**（每日10分钟）：
1. `/morning-note` → 看自选股异动和市场要闻
2. `/catalysts` → 确认未来一周持仓股的事件风险
3. 如有财报：`/earnings 股票名` → 提取关键变化 → `/model-update`
4. 如有操作：`/thesis 股票名` → 确认投资逻辑是否仍然成立

### 目标一：投资成功 — 还本计划执行

**核心插件：`wealth-management`**

```
/rebalance                    → 持仓再平衡方案（昆仑24.5%→现金45%→其他22-28%）
/financial-plan               → 9月60万还本方案现金流模拟
/client-report                → 生成个人资产配置报告
/tlh                          → 税务亏损收割（择机卖出亏损仓位抵税）
/proposal                     → 资产配置建议书
```

### 目标二：事业进阶 — 并购贷款政策研究

**核心插件：`investment-banking` + `private-equity` + `valuation-reviewer`**

```
/merger-model                 → 科创并购贷款的交易结构建模
/buyer-list                   → 生成科创领域潜在战略买家名单
/one-pager                    → 科创并购融资一页纸摘要
/ic-memo                      → 投委会备忘录（评估并购贷款项目可行性）
/dd-checklist                 → 并购贷款尽职调查清单
/dd-prep                      → 尽调准备：数据需求+问题清单
/screen-deal                  → 筛选科创并购标的
/returns                      → 并购贷款的风险调整回报分析
/portfolio                    → 存量并购贷款组合监控
/value-creation               → 并购后整合价值创造评估
```

**典型工作流**（用于民建课题/工作报告）：
1. `/screen-deal` → 设筛选条件（行业=AI/半导体，交易规模=5-50亿）
2. `/merger-model` → 输入标的财务数据，生成并购模型
3. `/dd-checklist` → 输出科创并购尽调清单
4. `/ic-memo` → 汇总成投委会备忘录 → 导出为.docx

### 目标二：事业进阶 — 科技金融方法论

**核心插件：`market-researcher` + `financial-analysis`**

```
/sector-overview    科技金融   → 科技金融行业概览（银行竞品分析）
/competitive-analysis 邮储银行 → 邮储vs工行/建行在科技金融的差异化
/idea-generation                → 生成科技金融创新产品思路
/3-statement-model              → 科技金融业务线的三表预测模型
/debug-model                    → 审查和调试现有财务模型
```

### 目标五：AI能力 — 投行级报告制作

**核心插件：`pitch-agent` + `earnings-reviewer`**

```
/pitch-agent          → 自动生成全套路演资料（含PPT、行业概览、财务模型）
/deck-refresh         → 刷新已有PPT中的数据
/ib-check-deck        → 投行级PPT质量审查（字体/对齐/数字一致性）
/ppt-template         → 创建符合规范的PPT模板
/earnings-preview     → 财报发布前的预览分析模板
```

**典型工作流**（制作一份高质量文档）：
1. `/pitch-agent 主题` → 生成初稿
2. `/ib-check-deck` → 自动审查格式和数字一致性
3. `/deck-refresh` → 刷新数据到最新
4. 导出为.pptx → 手动微调即可

### 目标六：知识库 — 数据驱动的知识卡片

**核心插件：`market-researcher` + `financial-analysis`**

每个大师投资策略卡片可以用插件辅助：
- `/sector-overview` → 生成某行业的背景知识卡片
- `/competitive-analysis` → 对比两个大师的投资方法论
- `/comps` → 用大师的选股标准实际跑一遍当前A股

---

## 二-B：对公信贷线（5/27新增9插件场景）

### 目标二：事业进阶 — 对公信贷全流程

**覆盖：贷前调查→贷中审查→贷后管理→综合支撑**

**贷前调查：客户拜访与准入**

| 技能 | 用法 | 耗时 |
|------|------|------|
| meeting-prep-agent | 说"准备拜访XX公司的简报" → 自动生成包含公司概况/合作历史/谈判策略/风险评估的一页纸 | 5min |
| kyc-screener | 提供客户尽调材料 → 自动解析+跑合规规则引擎+标记缺口 | 3min |
| operations | KYC文档批量解析+规则网格评估 | 视文件量 |

**贷中审查：财报审核与贷款定价**

| 技能 | 用法 | 耗时 |
|------|------|------|
| statement-auditor | 上传标的公司财报 → 自动审查准确性/完整性/审计就绪度 | 10min |
| sp-global | 说"拉XX公司的S&P快览" → 公司信用评级+财务摘要+交易记录 | 2min |
| lseg | 说"测算这笔贷款基于当前LPR的定价" → 收益率曲线+信用利差+定价区间 | 5min |
| model-builder | 自动构建标的公司三表模型/DCF/偿债能力分析 | 15min |
| valuation-reviewer | 说"审查这个标的的估值" → 对照可比交易+方法论+内控标准 | 10min |

**贷后管理：台账核对与报告**

| 技能 | 用法 | 耗时 |
|------|------|------|
| fund-admin | 贷款台账核对+利息计提验证+NAV验算 | 视数据量 |
| gl-reconciler | 账务差异自动追踪+根因分析 | 5min |
| month-end-closer | 月末关账：自动生成应计/滚动/差异说明/关账报告 | 10min |

### 典型工作流：科创并购贷款全流程（60分钟）

```
1. meeting-prep-agent "并购标的公司"  → 生成拜访简报（5min）
2. kyc-screener + operations           → 客户准入+合规筛查（10min）  
3. screen-deal "并购标的描述"          → 12维度筛查矩阵+判定（5min）
4. statement-auditor                   → 审核标的三张报表（10min）
5. sp-global + lseg                    → 信用评级+定价基准（5min）
6. model-builder                       → 三表预测+偿债能力模型（15min）
7. ic-memo (private-equity)            → 汇总为投委会备忘录（10min）
最终输出：筛查备忘录+尽调清单+内部授信报告
```

### 今日实战验证（2026-05-27）

| 时间 | 操作的插件 | 输入 | 产出 |
|------|-----------|------|------|
| 上午 | morning-note | — | A股晨报（持仓股异动/宏观事件） |
| 上午 | catalysts | — | 30天催化剂日历（FOMC/MLF/解禁） |
| 中午 | screen-deal | "AI芯片公司/10x估值/参股25%" | 12维度筛查备忘录（7PASS/5待补充/6亿贷款方案） |
| 下午 | meeting-prep-agent | "神州信息 000555" | 客户拜访简报（7章/谈判策略/会后行动清单） |
| 下午 | market-researcher | "中国科技金融市场全景" | 行业研究笔记（30万亿赛道/万亿俱乐部全量排名/邮储突围战略） |
| 下午 | pitch-agent | "科技金融方法论" | 13页Pitch Deck PPTX（49KB） |

---

## 三、斜杠命令速查表（按使用频率）

### 每天使用（日频）

| 命令 | 插件 | 用途 | 耗时 |
|------|------|------|------|
| `/morning-note` | equity-research | 自选股异动+宏观事件晨报 | 2min |
| `/catalysts` | equity-research | 未来30天催化剂日历 | 1min |
| `/thesis 标的` | equity-research | 检查投资论点是否成立 | 3min |

### 每次操作前使用（周频）

| 命令 | 插件 | 用途 | 耗时 |
|------|------|------|------|
| `/earnings 标的` | equity-research | 最新财报分析 | 10min |
| `/screen` | equity-research | 按条件筛选标的 | 5min |
| `/dcf 标的` | financial-analysis | 自由现金流折现估值 | 15min |
| `/comps 标的` | financial-analysis | 可比公司分析 | 10min |
| `/rebalance` | wealth-management | 组合再平衡方案 | 10min |
| `/sector 行业` | equity-research | 行业概览 | 5min |

### 按需使用（月频/项目制）

| 命令 | 插件 | 用途 |
|------|------|------|
| `/merger-model` | investment-banking | 并购交易模型 |
| `/cim` | investment-banking | 保密信息备忘录 |
| `/teaser` | investment-banking | 交易摘要（Teaser） |
| `/buyer-list` | investment-banking | 潜在买家名单 |
| `/ic-memo` | private-equity | 投委会备忘录 |
| `/dd-checklist` | private-equity | 尽调清单 |
| `/screen-deal` | private-equity | 筛选交易标的 |
| `/returns` | private-equity | 基金回报分析 |
| `/financial-plan` | wealth-management | 财务规划 |
| `/client-report` | wealth-management | 客户报告 |
| `/tlh` | wealth-management | 税务亏损收割 |
| `/initiate` | equity-research | 首次覆盖报告 |
| `/model-update 标的` | equity-research | 财报后更新模型 |
| `/deck-refresh` | pitch-agent | 刷新PPT数据 |
| `/ib-check-deck` | pitch-agent | PPT质量审查 |
| `/lbo` | financial-analysis | LBO杠杆收购模型 |
| `/3-statement-model` | financial-analysis | 三表预测模型 |
| `/debug-model` | financial-analysis | 审查财务模型错误 |
| `/earnings-preview` | earnings-reviewer | 财报预览模板 |

---

## 四、典型工作流

### 工作流1：快速晨间投资检查（5分钟）

```
1. /morning-note          → 昆仑/稀土ETF/东方财富有无异动
2. /catalysts             → 未来一周有无重大事件（美联储/财报/解禁）
3. 如有异动 → /thesis 标的 → 判断是否需要操作
```

### 工作流2：深度分析一只股票（30分钟）

```
1. /earnings 昆仑万维     → 提取最新季报关键数据
2. /comps 昆仑万维        → 可比公司PE/PS对比
3. /dcf 昆仑万维          → DCF估值
4. /sector 互联网AI       → 行业整体判断
5. /competitive-analysis  → 竞争地位
6. 汇总 → /initiate       → 生成首次覆盖报告
```

### 工作流3：并购贷款政策研究 → 民建社情民意（60分钟）

```
1. /screen-deal                       → 设定条件筛科创并购案例
2. /merger-model 案例                 → 构建并购融资模型
3. /dd-checklist                      → 生成科创并购尽调清单
4. /ic-memo                           → 汇总为投委会备忘录
5. /pitch-agent 主题                   → 生成社情民意配套PPT
6. /ib-check-deck                     → 质量审查
最终输出：.doc社情民意 + .pptx汇报材料
```

### 工作流4：9月还本60万方案推演（15分钟）

```
1. /financial-plan                    → 输入：现有持仓、每月现金流、9月需60万
                                      → 插件计算：最优减持路径+时间表
2. /rebalance                         → 再平衡到目标结构
3. /client-report                     → 生成个人资产报告（可作家庭沟通材料）
```

### 工作流5：科技金融方法论课件（用于内部培训/竞聘）

```
1. /sector-overview 科技金融          → 行业全景图
2. /competitive-analysis 邮储银行     → 邮储vs竞品雷达图
3. /idea-generation                   → 创新产品点子
4. /pitch-agent 科技金融方法论        → 自动生成全套路演材料
5. /deck-refresh                      → 更新最新数据
最终输出：.pptx竞聘课件 + .doc方法论文档
```

---

## 五、快捷入口

### 方式一：斜杠命令（推荐）

在 Claude Code 对话中直接输入 `/命令名`，例如：
```
/earnings 昆仑万维
```

### 方式二：自然语言

直接用中文描述需求，Claude 会自动调用对应技能：
```
"用可比公司法给昆仑万维做个估值，和百度、阿里对比"
"帮我生成一份科技金融行业概览的PPT"
"检查一下我的投资组合是否偏离目标配置"
```

### 方式三：查看插件所有能力

```bash
claude plugin details financial-analysis@claude-for-financial-services
```

---

## 六、注意事项

1. **MCP数据源需企业订阅**：FactSet、Moody's、S&P Global、PitchBook 等需企业账号。无订阅时，Claude 会用公开数据源（新浪财经、Wind公开数据等）替代
2. **输出格式**：所有报告/模型可直接导出为 .xlsx / .pptx / .docx
3. **中文友好**：所有斜杠命令支持中文输入（标的名称、行业名称、公司名称）
4. **插件更新**：每月运行 `claude plugin update` 保持最新
5. **Token消耗**：always-on部分每个插件约900-1,200 tokens。全部10个插件共约10,000 tokens 常驻开销，相当于每个新对话多消耗约1分钟上下文。大任务调用单个技能（如DCF/merger-model）约额外5k-10k tokens

---

## 七、插件分类速记

```
投资研究三件套：equity-research  financial-analysis  market-researcher
投行交易三件套：investment-banking  private-equity  valuation-reviewer
产出自动化三件套：pitch-agent  model-builder  earnings-reviewer
个人财富一套：wealth-management
```

---

> 更新记录：2026-05-27 初版，随插件使用经验持续更新
