# Harness深度解析——当模型能力趋同，什么决定了智能体的上限？

> 2026年，AI行业经历了一场静默的权力转移。从"哪个模型最强"变成了"哪个harness最强"。
>
> 你不是在挑选模型——你是在挑选一个AI的操作系统。

---

## 一、引子：一场9美元的教训

2025年，Anthropic做了一个意味深长的实验。

他们让同一个模型——Opus 4.5——去完成同一个编码任务。唯一的变量是：一个"裸跑"，另一个外面套了一层harness。

结果令人震惊：

- **裸模型**：花费 $9，**成功率 20%**
- **带harness**：花费 $200，**成功率 100%**

10倍的成本，5倍的胜率。**多出来的$191全部花在了验证循环上。**

几乎同一时间，LangChain的团队在做另一组实验。他们在Terminal-Bench 2.0上优化同一个模型（GPT-5.2-Codex）的harness，实现了从**Top 30跃升至Top 5**——25个名次的飞跃，模型一次都没换。

OpenAI的Codex团队则发现了一个更令人玩味的现象：在代码库根目录加一个约100行的`AGENTS.md`文件，所带来的质量提升超过任何一次模型升级。

这些实验指向同一个结论：

> **当三大前沿模型在SWE-bench上的差距缩小到1%以内时（Verified榜单第1名80.9% vs 第4名80.0%，差距0.9个百分点）**，模型的边际优势在消失。真正的差异化因素，是harness。

这不是一个技术趋势的猜测——它已经是事实。2026年，AI工程化的核心命题从"怎么训练更好的模型"变成了"怎么构建更好的harness"。

---

## 二、Harness的本质：AI的操作系统

### 2.1 一个正在被接受的公式

Mitchell Hashimoto在2026年提出的公式已经被行业广泛接受：

```
Agent = Model + Harness
```

模型提供的是原始智能——推理能力、知识储备、语言理解。但一个Agent要在真实世界中稳定运行，还需要太多模型本身不提供的东西：

- 如何组装提示词？
- 如何管理上下文窗口？
- 如何安全地调用工具？
- 如何授权、审计、回滚？
- 如何在长时间运行中保持目标一致性？
- 如何验证自己的产出？

**这些就是harness的职责。**

### 2.2 Harness = AI的操作系统

如果你了解操作系统，会发现harness的架构惊人地熟悉：

| 操作系统概念 | Agent Harness 类比 |
|:---|:---|
| CPU / 调度器 | LLM（推理引擎） |
| 工作内存 | 上下文窗口 |
| syscalls | 工具调用（Tool Call） |
| 内核 | MCP Server（中介访问系统资源） |
| 虚拟文件系统 / 分发表 | 注册表（按资源类型+操作分发） |
| 内存管理 | 上下文压缩管线 |
| 进程隔离 | Sub-agent 隔离上下文 |
| 用户权限管理 | Deny-first 权限系统 |
| 日志系统 | Append-only JSONL transcripts |
| 守护进程 | 后台任务与定时调度 |

这个类比不是牵强附会。**Harness的核心循环——observe→reason→act→observe——本质上就是一个事件驱动的操作系统内核。**

### 2.3 Claude Code的5层子系统

从源码层面看（约51.2万行TypeScript），Claude Code的harness由5层子系统构成：

| 层级 | 名称 | 职责 |
|:---:|:---|:---|
| 1 | **Surface**（表） | CLI、Headless、SDK、IDE（React + Ink 终端UI） |
| 2 | **Core**（核） | queryLoop、5阶段压缩管线、子代理调度 |
| 3 | **Safety/Action**（安全） | 7种权限模式、Auto Mode分类器、27个Hook事件、工具池、Shell沙箱 |
| 4 | **State**（状态） | Append-only JSONL transcripts、CLAUDE.md层级体系、自动记忆、Sidechain文件 |
| 5 | **Backend**（后端） | Shell执行、MCP连接（8种传输类型）、42个工具子目录 |

**关键数据**：在这51.2万行代码中，只有约 **1.6% 是AI决策逻辑**，剩下的 **98.4% 是确定性基础设施**——权限门控、上下文管理、工具路由、状态恢复（数据来源：VILA-Lab论文 arXiv:2604.14228 的源码统计，AI决策逻辑定义为直接与LLM推理交互的调用路径，不含工具实现、UI、通信等层）。

> **你花了几千美元订阅的模型能力，实际上只占整个系统不到2%的代码量。剩下的98%，是harness。**

---

## 三、上下文工程：比Prompt Engineering更难的山峰

### 3.1 从Prompt到Context

2022-2023年，AI工程化的核心技能是**Prompt Engineering**——怎么写更好的提示词。

2024-2025年，升级为**Context Engineering**——怎么组装更好的上下文。

2026年，在harness的框架下，它已经演变为**上下文全生命周期管理**：从组装、到压缩、到隔离、到恢复。

Claude Code的上下文组装包含**9个有序来源**：

```
系统提示词 → 环境信息 → CLAUDE.md层级 → 路径作用域规则
→ 自动记忆 → 工具元数据 → 对话历史 → 工具执行结果 → 压缩摘要
```

这不是简单的拼接。每一层的顺序、优先级、缓存策略都经过精心设计。例如，**系统提示词采用分段缓存设计**——动态边界标记将提示词分为静态区（可全量缓存）和动态区（每轮重算）。

### 3.2 5阶段压缩管线：从轻到重的防御

这可能是Claude Code最被低估的工程成就。每次模型调用前，消息队列会依次经过**5道防线**，从最轻量到最重量级：

| 阶段 | 策略 | 触发条件 | 设计意图 |
|:---:|:---|:---:|:---|
| 1 | **预算控制**（Budget Reduction） | 始终激活 | 对工具结果施加每个消息的token上限 |
| 2 | **历史裁剪**（Snip） | 功能开关 | 裁剪较旧的冗余历史 |
| 3 | **微型压缩**（Microcompact） | 始终激活（基于时间） | 移除冗余元数据 |
| 4 | **上下文折叠**（Context Collapse） | 功能开关 | 非破坏性虚拟投影，渐进式折叠 |
| 5 | **自动压缩**（Auto-Compact） | 最终手段（断路器：连续失败3次后停止） | 全量模型生成摘要 |

设计哲学极其清晰：**最便宜的策略最先执行，昂贵的AutoCompact作为最后手段。** 这就像是操作系统的多级缓存——L1/L2/L3逐级递进，绝大多数情况在最轻的几层就完成了。

### 3.3 CLAUDE.md四层体系

CLAUDE.md是整个记忆体系的核心出入口，分为4个级别：

| 级别 | 路径 | 作用域 |
|:---:|:---|:---|
| Managed | `/etc/claude-code/CLAUDE.md` | 企业级（管理端下发） |
| User | `~/.claude/CLAUDE.md` | 用户全局 |
| Project | `CLAUDE.md` + `.claude/rules/*.md` | 项目级（纳入版本控制） |
| Local | `CLAUDE.local.md` | 本地级（gitignored） |

**关键设计抉择**：CLAUDE.md是**用户上下文**（概率性遵从），而**不是系统提示词**（确定性执行）。权限规则提供确定性的强制执行层。

经验表明，CLAUDE.md的可靠容量约**200行以内**。超出范围的内容容易被模型忽略或稀释。

### 3.4 无向量数据库的文件记忆

Claude Code的记忆系统没有使用向量数据库。它基于LLM对记忆文件的头部元数据进行扫描——没有嵌入、没有向量检索、没有RAG。

- 每次从记忆目录中选择最多5个相关文件
- 完全可审计、可编辑、可版本控制
- 设计目标是**可理解性优先于自动化**

这种"反潮流"的选择耐人寻味。当整个行业疯狂涌入向量数据库时，Claude Code选择了一种更简单、更透明的方式——因为对于Agent记忆来说，**可审计性比检索速度更重要**。

### 3.5 Context Rot：上下文窗口的诅咒

Latent Space的研究发现一个令人不安的现象——**Context Rot（上下文腐败）**：

- 随着上下文窗口被填满，模型的准确率和召回率持续下降
- 模型产生"上下文焦虑"——窗口快满时慌慌张张地收尾
- 超越约**5万-20万token**后，性能出现显著下降

这意味着单纯扩大上下文窗口（从200K到1M到2M）是一条收益递减的道路。**更大的窗口只是把问题推迟了，而不是解决了。**

Harness的应对策略是**多层次的**：
1. 压缩管线（让内容更精炼）
2. 子代理隔离（让每个窗口只处理一件事）
3. Sidechain分发（只把摘要带回主上下文）
4. 学术界也在探索新方向：如CMU等机构的《Language Models Need Sleep》论文提出的"睡梦合并"——将近期上下文转换为持续快速权重后清空KV缓存

---

## 四、工具系统：从"写工具"到"定义协议"

### 4.1 MCP：Agent的外设总线

如果说LLM是CPU，那么**MCP（Model Context Protocol）就是Agent的PCIe总线**——它定义了外设如何接入、如何被发现、如何被调用。

Claude Code的MCP实现支持**8种传输类型**：

| 传输方式 | 典型用途 |
|:---|:---|
| `stdio`（标准输入输出） | 本地子进程工具（文件系统、数据库、自定义脚本）——默认，无需网络 |
| `http`（Streamable HTTP） | 远程服务——当前规范推荐 |
| `sse`（Server-Sent Events） | 旧版远程传输 |
| `ws`（WebSocket） | 双向通信 |
| `claudeai-proxy` | 通过 Claude.ai 基础设施路由 |
| `sdk` / `InProcessTransport` | 同进程函数调用 |
| `sse-ide` / `ws-ide` | IDE插件通信 |

配置从**7个作用域**加载并合并去重：`local` → `user` → `project` → `enterprise` → `managed` → `claudeai` → `dynamic`。去重是基于内容的，不是基于名称的——两个不同名称但相同命令的服务器会被识别为同一台。

### 4.2 工具池组装：5步管道

当MCP服务器连接成功后，每个工具定义会经过**4层转换**注入到Claude Code的内部工具接口：

```
原始MCP工具定义
  → 名称规范化（mcp__{serverName}__{toolName}）
  → 描述截断（上限 2,048 字符——防止OpenAPI生成的15-60KB描述消耗15,000 token/轮）
  → Schema透传（不变换，错误在调用时暴露）
  → 注解映射（readOnlyHint → 标记并发安全，destructiveHint → 触发额外权限审查）
```

然后进入**3层装配管道**：

```
Layer 1: getAllBaseTools() — 直接导入核心工具(~20) + 条件导入工具(~46)
Layer 2: getTools() — 运行时过滤（权限上下文、模式限制、拒绝规则）
Layer 3: assembleToolPool() — 内置+MCP合并，分区排序，去重
```

**关于去重**：内置工具优先于MCP工具。分区排序（内置为连续前缀，MCP为后缀）保证API缓存的键值稳定性。

### 4.3 Tool Search Tool：当工具太多的时候

当连接5个MCP服务器时，工具定义本身就能消耗约**5.5万token**——相当于一篇40页论文的token量。

Claude Code的Tool Search Tool将这一消耗降低了约**85%**，将可用上下文从12.2万token增加到19.1万token。Opus 4在大型工具库上的准确率从**49%提升到74%**。

> **你每次"再加一个MCP服务器"，都是在缩减Agent的推理预算。工具的元数据不是免费的。**

### 4.4 一个设计原则：O(1)工具数承载O(n)能力

Harness Engineering社区在2026年提炼出一个优雅的设计原则：

> **工具数量应该维持在O(1)，而能力增长为O(n)。**

不要为每个API端点创建一个工具。而是创建少量**通用动词**，按资源类型分发：

| 系统 | 模式 |
|:---|:---|
| Unix | `read()`、`write()`、`open()`——同一接口，任何文件 |
| REST | GET、POST、PUT、DELETE——同一动词，任何资源 |
| Agent | `list`、`get`、`create`、`execute`——同一语法，任何领域 |

Harness MCP Server用**10个通用工具**分发到**30个工具集**，覆盖**140+资源类型**。工具数O(1)，能力O(n)。

---

## 五、安全与权限：七层独立防御

这是Claude Code harness中设计最严密的子系统。**没有一个单一的安全机制——而是7层独立安全层，任何一层都可以阻断操作。**

### 5.1 Deny-First：最简也最强的哲学

```
deny → ask → allow
```

**deny永远优先于allow**，即使allow写得更具体。这不是技术限制，而是安全原则——**fail-closed**。

这种设计贯穿整个权限系统。你可以精确地允许某些操作，但只要有一条deny规则匹配，操作就被阻断。

### 5.2 7种权限模式

从严格到宽松形成**渐进信任谱系**：

| 模式 | 行为 | 适用场景 |
|:---:|:---|:---|
| `plan` | 只读探索 | 只看不动 |
| `default` | 标准交互式审批 | 日常使用 |
| `acceptEdits` | 文件编辑自动通过 | 开发者日常 |
| `auto` | ML分类器评估安全（2026新增） | 高频使用 |
| `dontAsk` | 不弹框，拒绝规则仍生效 | 信任后提速 |
| `bypassPermissions` | 跳过大多数提示 | 紧急调试 |
| `bubble` | 内部：子代理向父级升级 | Agent间通信 |

**Auto Mode**是2026年最关键的权限升级。它引入了一个**双层防御**架构：

1. **输入层**：Prompt注入探针——在工具输出进入Agent上下文前检测可疑内容
2. **输出层**：Transcript分类器（基于Sonnet 4.6）——在每个操作执行前评估安全性

两阶段分类：
- **Stage 1（快速过滤器）**：单token yes/no，假阳性率8.5%，假阴性率6.6%
- **Stage 2（链式思维推理）**：仅Stage 1标记时触发，假阳性率降至0.4%，但假阴性率升至17%

这个17%的假阴性率意味着：**在真实过度积极行为数据集中，17%的危险操作未被阻断。** Auto Mode不是魔法——它是一个有明确边界的工程权衡。

### 5.3 7层独立安全层

一个请求必须通过所有适用层，任何一层都可以阻断：

1. **工具预过滤**（拒绝的工具从模型视野中移除）
2. **Deny-first规则评估**（deny覆盖allow）
3. **权限模式约束**
4. **Auto Mode ML分类器**（独立LLM调用）
5. **Shell沙箱**（文件系统+网络隔离）
6. **会话恢复时权限不恢复**（信任从不跨会话持久化）
7. **Hook拦截**（PreToolUse Hooks）

### 5.4 已知的架构性漏洞

没有任何系统是完美的。Claude Code的harness有两个被确认的**结构性特权攻击窗口**：

- **Hooks和MCP服务器在初始化期间执行**——在信任对话框出现**之前**，它们已经运行了
- **纵深防御在多层级约束共享时可能退化**——超过50个子命令的命令绕过安全分析以防止REPL冻结

这些不是bug——它们是架构层级的设计权衡。知道它们存在，是理性使用harness的前提。

---

## 六、Agent编排：从单打独斗到集团作战

### 6.1 子代理：上下文的防火墙

Claude Code内置了**6种子代理类型**：Explore、Plan、General-purpose、Claude Code Guide、Verification、Statusline Setup。

关键设计特征：

- **Sidechain转录**：每个子代理写入自己的`.jsonl`文件，只有摘要返回父级——保护父级上下文
- **三种隔离模式**：worktree（文件系统隔离）、remote（远程执行）、in-process（共享文件系统+隔离对话）
- **POSIX `flock()` 协调**——零外部依赖
- **硬性限制**：子代理不能派生子代理——防止无限制任务扩散

### 6.2 SkillTool vs AgentTool

| 维度 | SkillTool | AgentTool |
|:---:|:---|:---|
| 上下文 | 注入当前上下文 | 生成新的隔离上下文 |
| 成本 | 低 | 约7倍（但上下文安全） |
| 用途 | 加载指令、知识 | 独立执行子任务 |
| 隔离性 | 无 | 完全 |

### 6.3 动态工作流：Harness的自编程能力

2026年6月，Claude Code获得了一项关键能力——**用JavaScript脚本编排多Agent工作流**。

```
// pipeline: 每个项依次通过所有阶段（无屏障）
const results = await pipeline(items, stageA, stageB, stageC)

// parallel: 并发执行（屏障）
const all = await parallel(thunks)

// agent: 派生独立子Agent
const result = await agent(prompt, {schema, model, isolation})
```

工作流引擎本质上是一个**微型运行时**——它有自己的agent调用、并行控制、阶段管理、进度日志和token预算监控。

常见模式：
- **Classify-and-act**：按任务类型路由到不同Agent
- **Fan-out-and-synthesize**：并行子Agent + 合并结果
- **Adversarial verification**：独立的对抗性验证Agent
- **Generate-and-filter**：生成 → 按标准过滤
- **Tournament**：Agent在相同任务上竞争，成对评判
- **Loop-until-done**：持续派生Agent直到满足停止条件

> **动态工作流实际上是把harness的构建从编译时推迟到了运行时。Agent不再只是使用harness——它可以自己编写和优化harness。**

### 6.4 企业级：Managed Agents三层结构

2026年，Anthropic推出了企业级的多Agent管理体系：

| 层级 | 描述 |
|:---|:---|
| **Subagent** | 最小执行单元，独立上下文窗口、专属系统提示词、受限工具集 |
| **Agent Teams** ⚠️ | 多个Claude Code实例并行工作，通过共享任务列表自协调、通过Mailbox互发消息（2026年2月推出的实验性功能） |
| **Managed Settings** | 企业控制平面，下发不可被用户覆盖的策略（MDM/管理后台） |

**跨项目隔离**：`memory: user` 和 `memory: project` 物理隔离——防止一个项目的信息泄露到另一个项目。

---

## 七、验证循环：为什么Harness的大部分成本花在这里

### 7.1 那个$191的教训

回到文章开头的那组数字：$200 vs $9——多出的$191几乎全部**花在了验证循环上**。

验证不是锦上添花——它是harness和裸模型之间最本质的差距。

LangChain的失败模式分析发现，Agent最常见的失败方式是：**写了一个解决方案，读了一遍自己的代码，觉得"看起来没问题"，然后就停了。** 没有测试、没有验证、没有检查边界条件。

### 7.2 做事与评判的分离

核心原则：**做事的人和评判的人必须分开。**

```
User Request → Planner → Generator → Code Reviewer → Security Reviewer → QA Engineer → Delivery
```

每个Agent：
- **独立的认知边界**——角色之间没有上下文污染
- **隔离的工具权限**——审查者只有只读访问
- **独立的模型选择**——规划/审查用更强模型，生成用更快模型

### 7.3 Fresh-Context Evaluator

这是Anthropic在cwc-long-running-agents项目中定义的核心Primitive：

> 一个**没有Write/Edit工具**的独立Agent，从**从未见过构建过程的上下文窗口**中审视工作成果。

返回 `PASS` 或 `NEEDS_WORK`（附带具体发现）。

**关键设计**：Evaluator的上下文从未接触过构建过程——这防止了"确认偏误"。

### 7.4 质量保证的三驾马车

Anthropic的经验总结出三个核心模式：

| 模式 | 解决的问题 | 实现机制 |
|:---|:---|:---|
| **Default-FAIL合约** | 成果宣告偏误（Agent声称完成但实际未完成） | 每个标准从false开始，Agent必须打开证据才能标记通过 |
| **Fresh-Context Evaluator** | 自我审查偏误（Agent偏袒自己的成果） | 独立的、只读的、上下文中从未接触过构建过程的审查Agent |
| **Agent-Maintained Handoff** | 上下文压缩后的目标漂移 | Agent写入结构化的PROGRESS.md并提交到Git |

### 7.5 验证的成本结构

据Harness Engineering社区的测算（基于Terminal-Bench 2.0 benchmark）：

| 方法 | 平均成本/任务 | 排名 |
|:---|:---:|:---:|
| 单会话Agent（无验证） | ~$22 | 5.00 |
| Plan + 基础验证 | ~$162 | 4.00 |
| **自适应Harness**（如Zenith） | **~$176** | **1.38** |
| 全量审查循环 | ~$408 | 1.75 |

关键发现：**不是验证越多越好。** 最贵的全量审查循环（$408）并没有取得最好的排名。自适应harness（$176）用不到一半的成本取得了更好的结果。

验证策略的效率比验证强度更重要。**聪明的验证比暴力的验证更便宜，也更有效。**

---

## 八、Harness的五大设计原则

从Claude Code和整个Harness Engineering社区的实践中，可以提炼出五条核心设计原则：

### 原则一：Fail-closed > Fail-open

默认说"不"。拒绝永远覆盖允许。工具默认为非并发、非只读、需要权限。

这是一个安全原则，也是一个质量原则。**在不确定的时候，往保守的方向犯错。**

### 原则二：Context是RAM

每一条被工具定义消耗的token，都是Agent不能用于推理的token。

每个MCP服务器消耗的上下文、每条工具描述的长度、每个系统提示词的冗余——所有这些都有机会成本。**Harness的第一要务是保持上下文的清洁。**

### 原则三：隔离比共享更安全

- Sub-agent的Sidechain隔离
- 验证Agent的Fresh-Context隔离
- Worktree的文件系统隔离
- Managed Agents的项目记忆物理隔离

**上下文共享是性能优化，上下文隔离是正确性保证。**

### 原则四：Append-only

每一件事都是可审计的：JSONL transcripts、Git历史、Sidechain文件。

**可追溯性不是功能——它是信任的前提。**

### 原则五：每个组件都是假设

Claude Code的一个核心洞察：

> 每个harness组件都编码了一个关于模型不能独立完成什么的假设。当模型升级时，这些假设会过期。

这就是为什么他们在每个模型发布后做一个"反向实验"：**逐一注释掉harness组件，看看哪些仍然必要。** 随着模型变强，有些曾经必须的harness逻辑不再需要了。

---

## 九、结语：从Model Scaling到System Scaling

2026年，AI行业正在经历一场静默的范式转换。

过去的两年属于**Model Scaling**——更大的模型、更多的数据、更长的训练。这是一场关于"原始算力"的竞赛。

2026年属于**System Scaling**——更好的harness、更聪明的验证、更高效的编排。这是一场关于"系统工程"的竞赛。

这不是说模型不再重要。而是说：**当三大基础模型的能力差距缩小到1%时，竞争优势的来源从一个物理常数（浮点运算），变成了一个工程变量（系统设计）。**

从Claude Code的harness中，我们看到了一条清晰的路：

```
Prompt Engineering（2022-2023）
  → Context Engineering（2024-2025）
    → Harness Engineering（2025-2026）
      → 下一步：Agent-native Architecture？
```

Harness Engineering的核心公式是：

```
Harness = Context Engineering + Tool/Permission协议 + Agent Loop + 状态恢复 + 验证反馈 + 子智能体编排
```

这六个要素的任何一个缺失，都会成为Agent能力的天花板。而它们的联合优化，正在定义AI工程化的下一个十年。

最后，回到那$9和$200的差距：

> **不是模型不够聪明——是还不够认真。**
>
> 裸模型像是一个天才少年——聪明但不可靠。Harness像是一个成熟的团队——流程、检查、备份、复盘。天才少年的成功依赖于个人状态，团队的可靠性来自系统工程。
>
> 2026年的答案已经很清楚了：我们不再需要更聪明的天才。**我们需要更好的团队。**

---

### 留给你思考的三个问题

1. **关于成本**：当验证循环占据harness 90%以上的成本时，你是否有勇气为了质量多花这10倍的钱？还是你觉得Agent"差不多"就行了？

2. **关于信任**：一个通过了7层安全审查的Agent，和一个通过了1层审查但速度快10倍的Agent——在什么场景下你选后者？

3. **关于架构**：如果你的组织明天要构建自己的Agent harness，你会从Claude Code的哪三个设计决策开始复制？哪三个你决定不复制？

欢迎在评论区写下你的思考。

---

*本文基于2025-2026年公开资料独立研究写作。核心数据来源：Anthropic Engineering Blog、VILA-Lab "Dive into Claude Code" 论文 (arXiv:2604.14228)、LangChain Harness Engineering报告、Faros AI Harness Engineering指南、Harness Blog、Anthropic cwc-long-running-agents仓库。*

*封面图：DALL·E 生成 | 发布日期：2026-06-03*
