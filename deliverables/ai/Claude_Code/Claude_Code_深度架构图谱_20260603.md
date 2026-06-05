# Claude Code 深度架构图谱

> 整合自：Harness深度解析 / how-claude-code-works（社区逆向）/ Anthropic Engineering Blog / SDK类型声明 / 运行时配置分析 / VILA-Lab论文
>
> 版本 v2.0 | 2026年6月5日 | 补充技能系统/代码编辑/任务系统/UX设计/最小组件/系统提示词等 P0 缺口

---

## 一、整体架构鸟瞰

### 1.1 核心公式

```
Agent = Model + Harness
```

— Mitchell Hashimoto, 2026

Claude Code 约 **51.2 万行 TypeScript**（~1,332 个 .ts + ~552 个 .tsx），基于 **Bun 运行时**。其中仅约 **1.6% 是 AI 决策逻辑**，其余 **98.4% 是确定性基础设施**（权限门控、上下文管理、工具路由、状态恢复）[VILA-Lab, arXiv:2604.14228]。

Harness 完整展开：
```
Harness = Context Engineering + Tool/Permission Protocol 
          + Agent Loop + State Recovery + Verification Feedback + Sub-agent Orchestration
```

### 1.2 核心技术栈

| 层次 | 技术选型 | 说明 |
|:----|:--------|:-----|
| 运行时 | **Bun** | 高性能 JS/TS 运行时，支持编译时 Feature Flag 消除 |
| 语言 | **TypeScript** | 全量严格类型检查 |
| UI 框架 | **React + Ink（自研）** | `src/ink/` ~1.0MB 定制渲染器，非上游 Ink |
| 布局引擎 | **Yoga** | Facebook Flexbox 布局引擎，适配终端 |
| Schema 验证 | **Zod** | 运行时类型校验，用于工具输入/Hook输出/配置验证 |
| CLI 框架 | **Commander.js** | 命令行参数解析，分发到 REPL/Headless/SDK 模式 |
| API 协议 | **Anthropic SDK** | 官方 TypeScript SDK，支持流式响应 |

核心技术选型的影响：Bun 的 `feature()` 宏允许**编译时物理消除**未公开功能的代码（而非运行时隐藏）；自研 Ink 渲染器支持组件化状态管理（权限对话框、流式代码高亮、嵌套工具进度指示器）。

### 1.3 六条核心设计原则

来自源码逆向分析，与 v1.0 的五条原则互补：

| # | 原则 | 一句话 | 体现位置 |
|:---:|:----|:------|:--------|
| 1 | **Generator-based 流式架构** | 从API到UI全链路使用 `async function*`，每个token/工具结果实时流向UI | query() 返回值类型 `AsyncGenerator<StreamEvent>` |
| 2 | **分层防御安全** | 7层独立防御，每层假设上一层可能被突破 | see Ch.4 |
| 3 | **编译时特性门控** | 通过Bun的 `feature()` 宏在构建时物理删除条件代码 | query.ts 头部6个 `feature()` |
| 4 | **集中式状态与不可变更新** | Zustand式不可变状态更新，单向数据流 | AppState / setAppState |
| 5 | **渐进式压缩** | 最便宜的压缩策略最先执行，类似CPU多级缓存 | 5阶段压缩管线 |
| 6 | **工具作为扩展点** | 统一 `Tool<Input,Output,P>` 泛型接口，新工具只需实现接口无需修改执行流水线 | src/Tool.ts |

### 1.4 四层架构模型

来自《Claude Code 实战：Harness 工程之道》（黄佳，人民邮电出版社，2026-05）：

| 层级 | 组件 | 职责 |
|:----|:----|:----|
| **记忆层** | CLAUDE.md / MEMORY.md / Auto Memory | 四层封闭记忆体系（user/feedback/project/reference） |
| **扩展层** | Skills / SubAgents / Hooks / MCP | 可热插拔的行为与工具扩展 |
| **集成层** | MCP 服务器 / LSP / OS Shell | 连接外部世界 |
| **编程层** | Agent SDK / Workflow Engine | 可编程的 Agent 框架 |

### 1.5 五层子系统

| 层级 | 名称 | 职责 | 关键文件 | 代码量参考 |
|:---:|:----|:----|:--------|:---------:|
| 1 | **Surface**（表层） | CLI、Headless、SDK、IDE | React + Ink 终端渲染器 | ~1.0MB (src/ink/) |
| 2 | **Core**（核心） | QueryEngine + query() 双层生成器 | QueryEngine.ts (1,295行) + query.ts (1,729行) + REPL.tsx (875KB) | ~3K+行 |
| 3 | **Safety/Action**（安全/行动） | 7层纵深防御、权限规则系统、分层Hook引擎、工具池 | tools.ts / bashSecurity.ts / hooks/ | 大量 |
| 4 | **State**（状态） | Append-only JSONL、CLAUDE.md四层、Auto Memory | context.ts (190行) / 记忆系统 | — |
| 5 | **Backend**（后端） | Shell执行、MCP连接、66+工具目录 | src/tools/ 每个工具独立目录 | — |

### 1.6 6 + 1 关键术语表

| 术语 | 定义 | 源码位置 |
|:----|:----|:--------|
| **State（状态）** | 不可变的消息列表，每次迭代重新创建新对象 | query() 循环内 |
| **Tool（工具）** | Agent 执行副作用操作的单位（读文件/写文件/执行命令） | src/Tool.ts |
| **Message（消息）** | API 请求中的消息数组，包含 user/assistant/tool_result/thinking | Anthropic SDK |
| **StreamEvent（流事件）** | 流式响应的中间事件，涵盖 token 增量、工具调用开始/完成、信号量 | query() 输出 |
| **Terminal/Continue（终止/继续）** | query() 返回 `Terminal` 表示循环结束，`Continue` 表示需要更多轮次 | query.ts:307 |
| **QueryEngine（查询引擎）** | 管理会话全生命周期（持久化、预算、恢复策略） | src/QueryEngine.ts |
| **query()** | 单次查询循环（压缩→API→工具执行→继续/终止决策） | src/query.ts |

### 1.7 9 阶段启动流程（~235ms 关键路径）

1. **模块求值** — Bun 加载模块时执行顶层代码（`src/cli.ts`），注册所有 `feature()` cond 条件 require
2. **模块加载** — 动态 `import()` 实际入口模块
3. **CLI 解析** — Commander.js 解析 `process.argv`，确定 REPL / Headless / SDK 三模式之一
4. **Commander 设置** — 注册 `/compact`、`/memory` 等斜杠命令
5. **preAction** — 执行前置检查（版本更新、配置一致性）
6. **14 步初始化** — 按严格顺序初始化子系统（日志→配置→插件→MCP→Hook→CLAUDE.md→记忆→任务→遥测→文件监听→Shell 快照→会话恢复→REPL→Tool 池）
7. **Action 处理** — 进入对应模式的主循环（REPL: 终端事件循环 / Headless: 单次执行）
8. **延迟预取** — 模型生成第一个 token 的同时预取记忆文件（~250ms 隐藏在生成延迟中）
9. **遥测记录** — 启动完成事件记录

### 1.8 模块依赖规则

- **核心循环（query.ts）永远不依赖 UI 层**
- **UI 层（REPL.tsx）永远不直接依赖 query.ts**——通过事件流解耦
- 工具系统不依赖任何 UI 组件——工具可在 headless 模式中正常工作

### 1.4 数据流全景

```
用户输入 (CLI/IDE)
  → Surface 层解析
    → Core 层组装上下文（9个来源 + 压缩）
      → LLM 推理（Streaming API）
        → Safety 层检查产出（权限 + ML分类器）
          → Action 层执行工具调用
            → State 层记录日志
              → Backend 层执行（Shell / MCP / 文件系统）
                → 结果返回，循环
```

### 1.5 演进路径

```
Prompt Engineering       (2022-2023)  提示词工程
  → Context Engineering  (2024-2025)  上下文工程（CLAUDE.md体系）
    → Harness Engineering (2025-2026)  Harness工程（当前阶段）
      → Agent-native Architecture (?)  代理原生架构（未来方向）
```

---

## 二、上下文工程管线

### 2.1 九个有序上下文来源

系统提示词采用**分段缓存设计**——动态边界标记将提示词分为静态区（可全量缓存）和动态区（每轮重算）。上下文按以下顺序组装：

```
系统提示词 → 环境信息 → CLAUDE.md层级 → 路径作用域规则
→ Auto Memory → 工具元数据 → 对话历史 → 工具执行结果 → 压缩摘要
```

### 2.2 CLAUDE.md 四层体系

| 级别 | 路径 | 作用域 | 可靠性 |
|:---:|:----|:------|:------|
| **Managed** | `/etc/claude-code/CLAUDE.md` | 企业级（管理端下发） | 确定性 |
| **User** | `~/.claude/CLAUDE.md` | 用户全局 | 概率性 |
| **Project** | `CLAUDE.md` + `.claude/rules/*.md` | 项目级（纳入版本控制） | 概率性 |
| **Local** | `CLAUDE.local.md` | 本地级（gitignored） | 概率性 |

关键设计抉择：CLAUDE.md 是**用户上下文（概率性遵从）**，不是**系统提示词（确定性执行）**。权限规则提供确定性的强制执行层。可靠容量约 **200 行以内**。

### 2.3 五阶段压缩管线（从轻到重）

| 阶段 | 策略 | 触发条件 | 设计意图 |
|:---:|:----|:--------:|:--------|
| 1 | **预算控制**（Budget Reduction） | 始终激活 | 对工具结果施加每消息 token 上限 |
| 2 | **历史裁剪**（Snip） | 功能开关 | 裁剪较旧的冗余历史 |
| 3 | **微型压缩**（Microcompact） | 始终激活（基于时间） | 移除冗余元数据 |
| 4 | **上下文折叠**（Context Collapse） | 功能开关 | 非破坏性虚拟投影，渐进式折叠 |
| 5 | **自动压缩**（Auto-Compact） | 最终手段（断路器：失败3次后停止） | 全量模型生成摘要 |

设计哲学：**最便宜的策略最先执行**。类似操作系统的多级缓存——L1/L2/L3 逐级递进。触发阈值：上下文使用量达约 **50%** 时启动自动压缩。

### 2.4 无向量数据库的记忆系统

- 基于 LLM 对记忆文件头部元数据进行扫描——**无嵌入、无向量检索、无 RAG**
- 从记忆目录中每次选择最多 **5 个**相关文件
- 完全可审计、可编辑、可版本控制
- **核心原则**：记忆是指引，不是存储。能从代码库重新推导的信息绝不存储。系统主动重写、去重、剪除矛盾信息。

### 2.5 六层记忆体系

| 层级 | 说明 |
|:----|:----|
| **Managed Policy** | 组织级策略 | 企业统一规范，不可覆盖 |
| **Project CLAUDE.md** | 项目配置 | 当前项目特定指令 |
| **User Preferences** | 用户偏好 | ~/.claude/CLAUDE.md 个人习惯设置 |
| **Auto Memory** | 自动学习 | MEMORY.md 从历史交互学习模式 |
| **Session** | 会话上下文 | 当前会话临时信息 |
| **Sub-Agent Memory** | 子Agent专项记忆 | 独立维护，物理隔离（`user` / `project` 级别） |

### 2.6 Context Rot（上下文腐败）

- 超越约 **5万-20万 token** 后，性能出现显著下降
- 模型产生"上下文焦虑"——窗口快满时慌慌张张地收尾（Sonnet 4.5 更明显，Opus 4.5 较轻）
- **越大窗口 ≠ 越好**：更大窗口（200K → 1M → 2M）是收益递减的道路
- **应对策略**：压缩管线、子代理隔离、Sidechain 分发
- **学术探索**：CMU《Language Models Need Sleep》论文提出"睡梦合并"——将近期上下文转换为持续快速权重后清空 KV 缓存

### 2.7 缓存经济

系统追踪 **14 种缓存失效向量**。分区排序（内置工具为连续前缀 + MCP 工具为后缀）保证 API Prompt Cache 键值稳定性。

---

## 三、工具系统

### 3.1 统一 Tool 接口

所有工具（内置 / MCP / REPL）通过统一泛型接口契约层：

```typescript
export type Tool<Input, Output, P extends ToolProgressData> = {
  name: string
  aliases?: string[]
  maxResultSizeChars: number
  call(args, context, canUseTool, parentMessage, onProgress?): Promise<ToolResult<Output>>
  description(input, options): Promise<string>
  prompt(options): Promise<string>
  inputSchema: Input                    // Zod schema
  isConcurrencySafe(input): boolean     // 默认 false（fail-closed）
  isReadOnly(input): boolean            // 默认 false（需权限检查）
  isDestructive?(input): boolean
  checkPermissions(input, context): Promise<PermissionResult>
  renderToolUseMessage(input, options): React.ReactNode
}
```

安全默认值：新工具默认 **需权限检查、不允许并发、不自动批准**。

### 3.2 三层工具池装配管道

```
Layer 1: getAllBaseTools()
  → 编译期工具裁剪。核心工具(~20) 直接 import；特性门控工具(~46) 通过 Bun 编译宏按条件移除
  
Layer 2: getTools()
  → 运行时上下文过滤。SIMPLE模式 / REPL模式 / 拒绝规则 / isEnabled() 四层过滤
  
Layer 3: assembleToolPool()
  → 内置工具 + MCP 工具合并，分区排序（内置前缀块 + MCP 后缀块）保证缓存命中率
```

去重策略：内置工具优先于 MCP 工具。

### 3.3 66+ 内置工具分类清单

| 类别 | 工具 | 输入类型 |
|:----|:----|:--------:|
| **文件操作** | Bash, FileRead, FileEdit, FileWrite, Glob, Grep, NotebookEdit | 7个 |
| **网络** | WebFetch, WebSearch | 2个 |
| **Agent管理** | Agent, TaskCreate/Get/Update/List/Stop/Output, SendMessage, TeamCreate/Delete, ListPeers | 10+个 |
| **用户交互** | AskUserQuestion, TodoWrite | 2个 |
| **系统** | EnterPlanMode, ExitPlanMode, EnterWorktree, ExitWorktree, Brief, Config, REPL | 7个 |
| **工具扩展** | Skill, ToolSearch, MCP, LSP, ListMcpResources, ReadMcpResource | 6个 |
| **编排** | Workflow, CronCreate/Delete/List, ScheduleWakeup, Monitor | 6个 |
| **通知** | PushNotification | 1个 |
| **其他** | RemoteTrigger | 1个 |

**SDK类型声明共36种输入类型**，其中部分（如Agent）有多个子模式。

### 3.4 MCP（Model Context Protocol）——Agent 的 PCIe 总线

#### 传输类型（8种）

| 传输方式 | 典型用途 |
|:--------|:--------|
| `stdio` | 本地子进程工具——默认，无需网络 |
| `http` (Streamable HTTP) | 远程服务——当前规范推荐 |
| `sse` (Server-Sent Events) | 旧版远程传输 |
| `ws` (WebSocket) | 双向通信 |
| `claudeai-proxy` | 通过 Claude.ai 基础设施路由 |
| `sdk` / `InProcessTransport` | 同进程函数调用 |
| `sse-ide` / `ws-ide` | IDE 插件通信 |

#### 配置作用域（7个，按优先级从低到高）

```
local → user → project → enterprise → managed → claudeai → dynamic
```

去重基于内容而非名称。MCP 配置可通过 CLI 参数或 `.mcp.json` 文件管理。

#### 三层纵深安全

```
工具声明约束 → 权限系统校验 → 用户确认拦截
```

当 MCP 工具定义总 token 数超过上下文窗口的 **10%** 时，自动启用 **MCP Tool Search**（延迟加载）。

#### MCP + Skills 协作模式

| 组件 | 回答的问题 |
|:----|:----------|
| **MCP** | "我能连接到什么？"——能力供应 |
| **Skills** | "我应该如何操作？"——编排指引 |

组合为 **「厨房与菜谱」模式**：MCP 提供能力，Skills 提供编排指引。

### 3.5 Harness MCP Server v2 重构（行业案例）

Harness 团队将 MCP 服务器从 **130+ 工具压缩至 11 个**：

| 指标 | v1 (130+工具) | v2 (11工具) |
|:----|:------------:|:----------:|
| 上下文消耗（200K窗口） | ~26%（约52,000 token） | ~1.6%（约3,150 token） |
| 架构模式 | 一接口一工具 | 注册表分发模型 |
| 支持资源类型 | 逐个硬编码 | 125+ 类型声明式注册 |

**注册表分发模型**：暴露 11 个通用动词（`list`/`get`/`create`/`update`/`delete`/`execute`等），每个资源类型在注册表中声明式定义 API 路径和参数映射。新增资源类型只需添加声明式对象，无需新增工具定义。详见 [harness.io/blog](https://www.harness.io/blog/harness-mcp-server-redesign)

### 3.6 Tool Search Tool

- 当连接 5 个 MCP 服务器时，工具定义消耗约 **5.5 万 token**（相当于一篇 40 页论文）
- Tool Search Tool 将这一消耗降低了约 **85%**
- 可用上下文从 12.2 万 token 增加到 19.1 万 token
- 大型工具库上准确率从 **49% 提升到 74%**

### 3.7 O(1) 工具数承载 O(n) 能力

| 系统 | 模式 |
|:----|:----|
| Unix | `read()`、`write()`、`open()`——同一接口，任何文件 |
| REST | GET、POST、PUT、DELETE——同一动词，任何资源 |
| Agent | `list`、`get`、`create`、`execute`——同一语法，任何领域 |

**核心原则**：工具数量维持 `O(1)`，能力增长 `O(n)`。

### 3.8 Skills 三层加载体系

| 级别 | 名称 | 加载方式 |
|:---:|:----|:--------|
| **Level 1** | 规则指令 | `CLAUDE.md` / `.cursor/rules/` 自动加载 |
| **Level 2** | MCP Prompt Templates | 服务器端注册的多步工作流模板 |
| **Level 3** | 斜杠命令 | `SKILL.md` 文件 + YAML frontmatter，/ 触发 |

---

## 四、安全与权限体系

### 4.1 Deny-First 哲学

```
deny → ask → allow
```

**deny 永远优先于 allow**。即使 allow 写得更具体。原则：Fail-closed。

### 4.2 七种权限模式（5外部 + 2内部）

| 模式 | 行为 | 适用场景 |
|:---:|:----|:--------|
| **default** | 无匹配规则时交互确认 | 日常使用 |
| **acceptEdits** | 自动批准 Edit/Write/NotebookEdit | 信任度高的项目 |
| **plan** | 执行前暂停审查，仅只读探索 | 敏感操作审计 |
| **bypassPermissions** | 全部自动批准 | 完全信任（危险） |
| **dontAsk** | 无匹配规则时自动拒绝 | CI/CD 环境 |
| *auto（内部）* | ML 分类器自动决策 | 内部高频使用 |
| *bubble（内部）* | 协调器专用模式，向父级升级权限 | 多 Agent 协调 |

### 4.3 权限规则系统

**三种匹配类型**：精确匹配（`Bash(npm test)`）、前缀通配（`Bash(npm test:*)`）、通配符（`Bash(npm *)`）

**三种行为**：`allow`（允许）、`deny`（拒绝）、`ask`（弹窗询问）。**deny 永远优先于 allow**。

**八层优先级来源**（从高到低）：`policySettings > userSettings > projectSettings > localSettings > flagSettings > cliArg > command > session`

**决策流程**（`hasPermissionsToUseToolInner`）：
1. 检查 bypass-immune 列表
2. 拒绝规则匹配 → 直接拒绝
3. 允许规则匹配 → 自动通过
4. 都未命中 → 交互式对话框 / ML 分类器 / Hook 三路竞速

**拒绝追踪与降级**：`DENIAL_LIMITS = { maxConsecutive: 3, maxTotal: 20 }`

### 4.4 三种权限处理器竞速机制

UI 对话框、Hook 和 ML 分类器**同时启动**，`createResolveOnce` 确保**第一个有效决定生效**：
- **200ms 防误触宽限期**
- **`userInteracted` 标志**：用户操作后自动化结果一律丢弃，人类意图永远优先

### 4.5 Auto Mode 双层 ML 分类器

```
Stage 1: 输入层——单token yes/no，假阳性率8.5%，假阴性率6.6%
Stage 2: 输出层——CoT推理（仅Stage1触发），假阳性率0.4%，假阴性率17%
```

**Tree-sitter 影子测试**：`TREE_SITTER_BASH_SHADOW` 特性门控并行运行 tree-sitter 和旧版解析器，比较结果遥测。最终决策仍用旧版路径。**"我们从不解释我们不理解的 AST 结构"**。

### 4.6 七层纵深防御架构

```
Layer 1: 工作区信任确认 → 不信任则禁用项目级Hook（防恶意预埋）
Layer 2: 权限模式 → 全局策略开关
Layer 3: 权限规则匹配 → allow/deny/ask 精确控制
Layer 4: Bash多层安全 → AST解析 + 23项静态检查
Layer 5: 工具级安全 → validateInput / checkPermissions / 危险文件保护
Layer 6: 沙箱隔离 → macOS Seatbelt / Linux 命名空间 / Git Worktree
Layer 7: 用户确认 → 对话框+Hook+ML分类器三路竞速，人类优先
```

```
1. 工具预过滤       → 拒绝的工具从模型视野中移除
2. Deny-first规则评估 → deny 覆盖 allow
3. 权限模式约束     → 当前模式的权限边界
4. Auto Mode ML分类器 → 独立LLM调用评估安全
5. Shell沙箱        → 文件系统 + 网络隔离
6. 会话恢复时权限不恢复 → 信任从不跨会话持久化
7. Hook拦截         → PreToolUse Hooks
```

### 4.5 Shell 安全检查（bashSecurity.ts 23项）

包括但不限于：
- Zsh 内置命令拦截
- Unicode 零宽字符注入防御
- IFS null-byte 注入防御
- 危险命令模式检测
- 路径遍历攻击检测

### 4.6 API 级认证

请求中包含 `cch=00000` 占位符，Bun 原生 HTTP 栈（Zig 编写，JS 层之下）将其替换为计算哈希，服务端验证请求来源是否为真实的 Claude Code 二进制。

### 4.7 已知架构性漏洞

- **Hooks 和 MCP 服务器在初始化期间执行**——在信任对话框出现之前，它们已经运行了
- **纵深防御退化**：超过 50 个子命令的命令绕过部分安全分析以防止 REPL 冻结
- **Auto Mode 17% 假阴性率**：危险操作未被完全阻断

### 4.8 Hook 事件系统（29 个事件）

源码定义（`src/entrypoints/sdk/coreTypes.ts`）的完整事件列表：

```typescript
HOOK_EVENTS = [
  'PreToolUse', 'PostToolUse', 'PostToolUseFailure',
  'Notification', 'UserPromptSubmit', 'SessionStart', 'SessionEnd',
  'Stop', 'StopFailure', 'SubagentStart', 'SubagentStop',
  'PreCompact', 'PostCompact', 'PermissionRequest', 'PermissionDenied',
  'Setup', 'TeammateIdle', 'TaskCreated', 'TaskCompleted',
  'Elicitation', 'ElicitationResult', 'ConfigChange',
  'WorktreeCreate', 'WorktreeRemove', 'InstructionsLoaded',
  'CwdChanged', 'FileChanged'
]  // 共 29 个事件（含常量中的备用条目）
```

#### 六种 Hook 类型

| 类型 | 实现方式 | 适用场景 |
|:----|:--------|:--------|
| **Command Hook** | Shell 脚本执行 | 最常用，支持 `if`/`shell`/`async`/`asyncRewake` |
| **Prompt Hook** | LLM Prompt 调用 | 需要语义理解的复杂评估 |
| **Agent Hook** | 多轮 Agent 验证 | 长时间的验证流程 |
| **HTTP Hook** | POST 到外部端点 | 集成外部审计/通知系统 |
| **Callback Hook** | 进程内函数（-70% 快速路径） | 轻量级同进程扩展 |
| **Function Hook** | 会话级注册函数 | 编程式 SDK 使用 |

#### 6 阶段执行引擎

```
Phase 0: 快速存在性检查（过度近似）
Phase 1: 信任检查（由历史CVE驱动——SessionEnd/SubagentStop在信任对话框之前执行）
Phase 2: Matcher 匹配（精确 / 管道分隔 OR / 正则表达式三级匹配 + if条件两层过滤）
Phase 3: Hook 去重
Phase 4: 输入构建（惰性 JSON 序列化）+ 并行执行
         → 同步、异步、asyncRewake 三种子模式
Phase 5: 输出解析（退出码语义 0/1/2）+ 结果聚合
```

**asyncRewake 模式**：专为"后台检查 + 按需中断"（如 CI 构建）设计。退出码 2 通过 `enqueuePendingNotification` 注入 `<system-reminder>` 中断模型。

#### 4 种技能/插件层级 Hook

三级线性结构：**全局 Hook（settings.json）> 技能级 Hook（技能 frontmatter）> 插件级 Hook（plugins/*/hooks/）**

#### PermissionRequest Hook 深度分析

4 种能力：**审批决策**（允许/拒绝）、**输入修改**（如强制 `--dry-run`）、**规则注入**（`updatedPermissions` 做持久规则）、**操作中断**（`interrupt: true`）。

与权限系统中 UI 对话框和 ML 分类器的竞速机制共同构成 Layer 7 用户确认防御。

---

## 五、Agent 编排系统

### 5.1 核心引擎：双层生成器架构

Claude Code 的查询系统采用**双层生成器架构**，清晰分离会话管理与查询执行：

| 维度 | QueryEngine（src/QueryEngine.ts, 1,295行） | query()（src/query.ts, 1,729行） |
|:----|:-----------------------------------------|:-------------------------------|
| 作用域 | 对话全生命周期 | 单次查询循环 |
| 状态 | 持久化（mutableMessages, usage） | 循环内 State 对象每次迭代重新赋值 |
| 预算追踪 | USD/轮次检查，结构化输出重试 | Task Budget 跨压缩结转，Token 预算续写 |
| 恢复策略 | 权限拒绝、孤儿权限 | PTL 排水/压缩、max_output_tokens 升级/重试 |

**7 个继续站点（Continue Site）**：query() 循环有 7 种不同的继续原因，每个对应特定恢复策略：
1. `next_turn` — 常规轮次切换
2. `collapse_drain_retry` — 上下文折叠后的排水重试
3. `reactive_compact_retry` — API 返回 PTL 错误的反应式压缩
4. `max_output_tokens_escalate` — 输出 token 超限→升级模型
5. `max_output_tokens_recovery` — 输出 token 超限→恢复
6. `stop_hook_blocking` — Stop Hook 触发强制继续
7. `token_budget_continuation` — Token 预算续写

**错误扣留策略**：query() 不会立即将可恢复错误提示给调用方；它在内部尝试恢复，所有恢复尝试都失败后才暴露。

**熔断器**：`MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3`——数据表明 1,279 个会话有 50+ 次连续自动压缩失败，全球每天浪费约 250K API 调用。

```
Think → Act → Observe → Repeat
```

核心哲学：**Orchestrator 越笨，架构越稳定**。核心循环逻辑仅约 **50 行**：
- 运行时只驱动循环、执行工具调用、感知结果
- 所有推理、决策、何时停止全部交给模型
- 给模型无限操作空间

关键入口：**QueryEngine**（`src/QueryEngine.ts`，约 4.6 万行），管理流式 API 调用、工具分发循环、自动重试和上下文窗口压缩。

### 5.2 六种子代理类型

| 子代理类型 | 职责 | 隔离方式 |
|:---------|:----|:--------|
| **Explore** | 搜索阅读 | 只读工具集 |
| **Plan** | 设计实施方案 | 只读 + 强模型 |
| **General-purpose** | 通用执行 | 全套工具 |
| **Claude Code Guide** | 回答Claude Code使用问题 | 知识库专注 |
| **Verification** | 验证/交叉审查 | 只读 + 独立上下文 |
| **Statusline Setup** | 配置管理 | 有限工具集 |

### 5.3 Sidechain 隔离机制

```
每个子Agent → 独立JSONL日志文件 → 仅摘要返回父级
```

关键设计特征：
- **Sidechain 转录**：保护父级上下文不被子Agent的详细输出污染
- **三种隔离模式**：
  - `worktree`：文件系统隔离（git worktree）
  - `remote`：远程执行
  - `in-process`：共享文件系统 + 隔离对话
- POSIX `flock()` 协调——零外部依赖
- 硬性限制：**子代理不能派生子代理**——防止无限制任务扩散

### 5.4 SkillTool vs AgentTool

| 维度 | SkillTool | AgentTool |
|:---:|:---------|:---------|
| 上下文 | 注入当前上下文 | 生成新的隔离上下文 |
| 成本 | 低 | 约 7 倍（但上下文安全） |
| 用途 | 加载指令、知识 | 独立执行子任务 |
| 隔离性 | 无 | 完全（Sidechain） |

### 5.5 动态工作流引擎（JavaScript 编排）

三个核心原语：
```javascript
pipeline(items, stageA, stageB, stageC) // 每个项依次通过所有阶段（无屏障）
parallel(thunks)                          // 并发执行（屏障）
agent(prompt, {schema, model, isolation}) // 派生独立子Agent
```

工作流引擎本质上是**微型运行时**——拥有自己的 agent 调用、并行控制、阶段管理、进度日志和 token 预算监控。

**六种常见编排模式**：

| 模式 | 用途 | 说明 |
|:----|:----|:----|
| Classify-and-act | 任务路由 | 按任务类型分发到不同Agent |
| Fan-out-and-synthesize | 并行搜索 | 并行子Agent + 合并结果 |
| Adversarial verification | 对抗验证 | 独立反驳性验证Agent |
| Generate-and-filter | 生成过滤 | 生成 → 按标准筛选 |
| Tournament | 锦标赛 | 多个Agent在相同任务上竞争，成对评判 |
| Loop-until-done | 持续迭代 | 持续派生Agent直到满足停止条件 |

### 5.6 Planner-Generator-Evaluator 模式

| 角色 | 职责 | 工具限制 |
|:----|:----|:--------|
| **Planner**（规划者） | 将1-4句话需求展开为完整产品规格 | 不写代码 |
| **Generator**（生成者） | 按Sprint实现功能 | 写代码 |
| **Evaluator**（评估者） | 验收质量（Playwright MCP） | 只读 |

**Sprint Contract 机制**：每个 Sprint 开始前，Generator 和 Evaluator 协商可验证的完成标准。

### 5.7 企业级 Managed Agents 三层结构

| 层级 | 描述 |
|:----|:----|
| **Subagent** | 最小执行单元，独立上下文窗口、专属系统提示词、受限工具集 |
| **Agent Teams** | 多个 Claude Code 实例并行工作，共享任务列表、Mailbox 消息（实验性） |
| **Managed Settings** | 企业控制平面，下发不可覆盖策略（MDM/管理后台） |

跨项目隔离：`memory: user` 和 `memory: project` **物理隔离**——防止一个项目的信息泄露到另一个项目。

### 5.8 KAIROS 实验性功能（源码中发现）

- **Always-On Agent**：后台持续运行的 Agent（`feature('KAIROS')` 门控）
- **/dream 技能**：夜间记忆蒸馏
- GitHub Webhook 订阅，感知代码变更
- 每 5 分钟的 Cron 调度刷新
- 后台 Daemon 工作进程

---

## 六、Session / Harness / Sandbox 三组件

### 6.1 三组件架构（2026 年重构）

从捆绑式 **"pet"（宠物）模式** 到解耦式 **"cattle"（牲畜）模式**：

| 组件 | 类比 | 职责 |
|:----|:----|:----|
| **Session**（大脑） | 只追加的事件日志 | 持久化所有发生事件；支持 `wake(sessionId)` 恢复 |
| **Harness**（躯干） | 调用 Claude 并路由工具的循环 | 将 Sandbox 作为普通工具调用：`execute(name, input) → string` |
| **Sandbox**（手） | 代码执行和文件编辑环境 | 可独立崩溃并优雅重启 |

### 6.2 解耦的关键收益

| 收益 | 说明 |
|:----|:----|
| **故障隔离** | 任何组件可独立崩溃和重启 |
| **凭证安全** | API密钥和数据库密码从不进入 Sandbox |
| **延迟优化** | p50 延迟下降约 60%，p95 延迟下降超过 90% |
| **资源共享** | 多 Harness 可共享 Sandbox，多 Sandbox 可服务于一个 Harness |
| **会话审计** | Session 独立记录，支持回放 |

### 6.3 运行时目录结构（~/.claude/）

```
~/.claude/
├── CLAUDE.md                     用户全局配置（个人身份+行为规则）
├── settings.json                 主设置（模型/环境变量/插件/权限）
├── settings.local.json           本地权限覆盖（31条允许规则）
├── history.jsonl                 对话历史（追加写入）
├── sessions/                     活动会话状态（3个文件）
├── shell-snapshots/              ZSH shell环境快照
├── file-history/                 文件编辑历史（47个UUID子目录）
├── tasks/                        任务存储（25个UUID子目录）
├── projects/                     项目级设置（每个项目一个目录）
├── plugins/                      插件安装和目录数据
├── plans/                        计划文件
├── session-env/                  会话环境变量快照
├── cache/                        缓存（changelog等）
├── backups/                      配置备份（5个历史版本）
├── telemetry/                    遥测数据（75个文件）
├── mcp-needs-auth-cache.json     MCP认证状态缓存
├── stats-cache.json              使用统计
└── .credentials.json             认证凭据（API密钥）
```

### 6.4 状态存储策略

- **Append-only**：JSONL transcripts、Git 历史、Sidechain 文件——每一件事都可审计
- **追加写入**：不修改旧记录，新记录追加到文件末尾
- **版本控制**：所有文件变更通过 Git 管理

---

## 七、验证与成本模型

### 7.1 核心原则：做事与评判分离

```
User Request → Planner → Generator → Code Reviewer → Security Reviewer → QA Engineer → Delivery
```

每个 Agent 的特征：
- 独立的认知边界——角色之间没有上下文污染
- 隔离的工具权限——审查者只有只读访问
- 独立的模型选择——规划/审查用更强模型，生成用更快模型

### 7.2 Fresh-Context Evaluator

- 没有 Write/Edit 工具的独立 Agent
- 从**从未见过构建过程的上下文窗口**中审视工作成果
- 返回 `PASS` 或 `NEEDS_WORK`（附带具体发现）
- 防止"确认偏误"的关键设计：Evaluator 的上下文从未接触过构建过程

### 7.3 质量保证三驾马车

| 模式 | 解决的问题 | 实现机制 |
|:----|:----------|:--------|
| **Default-FAIL 合约** | 成果宣告偏误 | 每个标准从 false 开始，Agent 必须打开证据才能标记通过 |
| **Fresh-Context Evaluator** | 自我审查偏误 | 独立的、只读的、从未接触过构建过程的审查 Agent |
| **Agent-Maintained Handoff** | 上下文压缩后目标漂移 | Agent 写入结构化的 PROGRESS.md 并提交到 Git |

### 7.4 验证成本结构（基于 Terminal-Bench 2.0）

| 方法 | 平均成本/任务 | 排名 |
|:----|:-----------:|:---:|
| 单会话Agent（无验证） | ~$22 | 5.00 |
| Plan + 基础验证 | ~$162 | 4.00 |
| **自适应Harness（如Zenith）** | **~$176** | **1.38** |
| 全量审查循环 | ~$408 | 1.75 |

**关键发现**：最贵的全量审查循环（$408）并未取得最好排名。自适应 Harness（$176）用不到一半的成本取得了更好结果。**验证策略的效率比验证强度更重要。**

### 7.5 基础实验数据

| 实验 | 条件 | 结果 |
|:----|:----|:----|
| Harness vs 裸模型 | Opus 4.5 | 裸模型 $9/20%胜率 → Harness $200/100%胜率 |
| Terminal-Bench 2.0 | 仅优化Harness | Top30 → Top5（25个名次飞跃） |
| AGENTS.md 实验 | ~100行规范文件 | 质量提升 > 任何一次模型升级 |
| C编译器实验 | 16并发Agent | 10万行Rust代码，编译Linux 6.9内核 |

---

## 八、配置参考与实操

### 8.1 settings.json 完整 Schema

```jsonc
{
  "model": "string",                    // 默认模型（如 "deepseek-v4-flash"）
  "env": {},                            // 环境变量（API密钥/端点/模型映射）
  "permissions": {
    "allow": ["Bash(pattern) *"],       // 允许的Bash命令（glob模式）
    "deny": ["Bash(dangerous *)"]       // 拒绝的Bash命令（可选）
  },
  "autoMode": {
    "allow": ["$defaults", "Bash(python3 scripts/*.py *)"]  // Auto模式白名单
  },
  "enabledPlugins": {
    "plugin-name@marketplace": true     // 启用/禁用插件
  },
  "extraKnownMarketplaces": {},         // 额外插件市场源
  "includeCoAuthoredBy": false,         // 是否包含共同作者信息
  "skipWorkflowUsageWarning": true,     // 跳过工作流使用警告
  "theme": {},                          // 主题配置（可选）
  "keybindings": {}                     // 快捷键配置（可选）
}
```

### 8.2 用户配置实战（本项目 settings.json 分析）

你正在运行的配置：

| 配置项 | 值 | 含义 |
|:------|:---|:----|
| 默认模型 | `deepseek-v4-flash` | 通过 DeepSeek 的 Anthropic 兼容端点 |
| Opus映射 | `deepseek-v4-pro[1M]` | 100万token上下文窗口 |
| 已启用插件 | 19 个金融服务插件 | earnings-reviewer, equity-research, lseg 等 |
| 白名单脚本 | `python3 scripts/*.py` | 公众号/简报/PR自动化 |
| 自动模式 | `$defaults` + 4个脚本规则 | Auto模式免确认 |

### 8.3 插件系统架构

- **市场来源**：GitHub 仓库 `anthropics/financial-services-plugins`
- **安装方式**：通过 `plugins/` 目录管理
- **技能清单**：每个插件提供若干 Skill（如 `lseg:macro-rates`、`equity-research:earnings`）
- **认证状态**：OAuth 认证缓存在 `mcp-needs-auth-cache.json`。每次会话检查认证状态
- **已安装**：21 个插件（19 金融服务 + 2 官方）

### 8.4 部署与版本更新

| 安装途径 | 方式 |
|:--------|:----|
| macOS | `npm install -g @anthropic-ai/claude-code` |
| 二进制 | 8个平台架构各有独立二进制包 |
| 更新 | CLI 内置 `claude update` 或 npm update |
| 版本记录 | `~/.claude/.last-update-result.json` 记录更新日志 |

当前版本：**v2.1.161**（npm global，2026-06-03 更新，从 v2.1.160）

### 8.5 MCP 认证流程

```
插件启用 → 检测OAuth需求 → mcp-needs-auth-cache.json 记录
→ 首次调用时弹出认证对话框 → 浏览器OAuth流程
→ token 缓存到 .credentials.json → 后续调用自动使用缓存token
```

认证失败的 MCP 服务器会记录在 `mcp-needs-auth-cache.json` 中，每次会话重试。

### 8.6 日志与调试

| 数据源 | 位置 | 用途 |
|:------|:----|:----|
| 对话历史 | `history.jsonl` (~259KB) | 完整交互记录 |
| 遥测 | `telemetry/` 目录 | 事件失败日志 |
| 备份 | `backups/` 目录 | 配置快照 |
| Shell快照 | `shell-snapshots/` | 环境状态 |
| 文件历史 | `file-history/` (47个UUID) | 编辑追踪 |

---

## 附录

### A. 五大设计原则

1. **Fail-closed > Fail-open**：默认说不。拒绝永远覆盖允许。工具默认为非并发、非只读、需要权限。
2. **Context is RAM**：每一条被工具定义消耗的 token 都是 Agent 不能用于推理的 token。有机会成本。
3. **Isolation over Sharing**：Sub-agent Sidechain、Fresh-Context Evaluator、Worktree、Managed Agents 物理隔离。
4. **Append-only**：JSONL transcripts、Git 历史、Sidechain 文件——每一件事都可审计。
5. **Every component is a hypothesis**：每个 Harness 组件都编码了一个关于模型不能独立完成什么的假设。当模型升级时，这些假设会过期。每个模型发布后做"反向实验"——逐一注释掉 Harness 组件，看看哪些仍然必要。

### B. 引用来源

| 来源 | 类型 | 链接 |
|:----|:----|:----|
| VILA-Lab "Dive into Claude Code" | 学术论文 | arXiv:2604.14228 |
| Anthropic "Managed Agents" | 官方技术文章 | anthropic.com/engineering/managed-agents |
| Anthropic "Harness Design for Long-Running Apps" | 官方技术文章 | anthropic.com/engineering/harness-design-long-running-apps |
| Anthropic "Building a C Compiler" | 官方技术文章 | anthropic.com/engineering/building-c-compiler |
| Harness MCP Server Redesign | 官方博客 | harness.io/blog/harness-mcp-server-redesign |
| 《Claude Code实战：Harness工程之道》 | 技术书籍 | 黄佳，人民邮电出版社，2026-05 |
| how-claude-code-works | 社区逆向工程 | github.com/Windy3f3f3f3f/how-claude-code-works |
| BAAI 深度分析 | 社区分析 | hub.baai.ac.cn/view/53619 |
| LangChain Terminal-Bench 2.0 | 行业基准 | langchain.com |

### C. 新增模块概览（v2.0）

以下五个模块在 v1.0 中完全缺失，来自 how-claude-code-works 社区逆向。每个模块均可扩展为完整章节，此处提供概要索引。

#### C.1 技能系统（Skills System）

技能是 Claude Code 的"AI Shell 脚本"——将验证有效的 prompt 模板化为可复用单元。

**六个来源**（按优先级合并）：内置技能（bundled）> 文件系统（.claude/skills/）> 工作流技能 > 插件技能 > MCP Prompt Template > 外部注册

**双重调用机制**：用户手动（`/review`）或模型自动（SkillTool 识别意图后触发）。两条路径最终汇合到相同执行逻辑。

**SKILL.md 文件格式**：目录格式 `.claude/skills/review/SKILL.md`，YAML frontmatter 定义 name/description/whenToUse/allowedTools/context/model/hooks。

**技能安全模型（5 级信任）**：
| 级别 | 来源 | 权限 |
|:---:|:----|:----|
| L0 | 内置技能 | 完全信任，无额外确认 |
| L1 | 文件系统技能 | 白名单权限（`SAFE_SKILL_PROPERTIES`） |
| L2 | 工作流技能 | 中等信任，fork 执行 |
| L3 | 插件技能 | 低信任，MCP 安全隔离 |
| L4 | 外部注册 | 最低信任，逐操作确认 |

#### C.2 代码编辑策略（Code Editing Strategy）

Claude Code 采用 **search-and-replace** 编辑策略（不采用行号编辑、AST 编辑或统一 diff），经过 14 步验证管道：

1. 唯一性约束 → 2. 引号标准化 → 3. 反消毒 → 4. 防止级联编辑 → ...

**编辑前读取要求**：`readFileState` 缓存强制在编辑前读取文件。`isPartialView` 检查防止在部分视图上编辑。

**原子写入**：`call()` 方法中临界区最小化（步骤 4-8 之间避免 `await`）。编码与换行符完整往返（读→处理→写）。LSP `didChange`/`didSave` 通知。文件历史备份（内容哈希去重）。

**Diff 渲染系统**：`StructuredDiff` 组件，color-diff Rust NAPI 模块（3 层缓存：WeakMap + 参数化键 + 每 hunk 最多 4 条目）。

**NotebookEditTool**：专门 Jupyter Notebook 编辑器。3 种模式（replace/insert/delete），自动降级 insert。

#### C.3 任务系统（Task System）

4 个核心工具：TaskCreate、TaskGet、TaskList、TaskUpdate

- **状态机**：`pending → in_progress → completed` / `deleted`
- **依赖追踪**：`blocks` / `blockedBy` 字段建立任务网络
- **文件级存储**：每个任务独立文件（从 TodoV1 单一 JSON 文件演进）
- **高水位标记**：防止 ID 重用
- **2 种粒度锁**：任务级 / 目录级（原子认领）
- **3 层变更检测**：fs.watch / 进程内信号 / 5 秒轮询兜底
- **上下文注入**：工具调用 + 每 10 轮周期性提醒
- **多 Agent 协调**：共享列表、自动所有权、邮箱通知、忙碌检测
- **Hook 集成**：TaskCreated / TaskCompleted 事件

#### C.4 用户体验设计（UX Design）

- **自研 React 终端渲染器**（251KB 核心）：React → Reconciler → Yoga → Screen Buffer → 差异检测 → ANSI
- **内存优化**：CharPool / StylePool / HyperlinkPool 对象池化
- **StreamingMarkdown**：增量解析，单调边界前进，不回溯
- **Spinner 5 模式状态机**：带停滞颜色插值（主题色 → ERROR_RED）
- **工具透明度**：工具调用透明度和 ToolUseLoader
- **Vim 4 模式状态机**：Normal/Insert/Visual/Replace
- **REPL 虚拟滚动**：`DEFAULT_ESTIMATE=3`，`OVERSCAN_ROWS=80`，`MAX_MOUNTED_ITEMS=300`
- **成本展示**：精度分档显示 token/美元消耗

#### C.5 最小必要组件（Minimal Components）

- **7 个最小必要组件**：查询循环、工具系统、上下文管理、权限检查、错误恢复、文件编辑、状态持久化
- **演进路径**：500行 → 2000行 → 5000行 → 20000行（515行 vs 512K+行对比表）
- claude-code-from-scratch 项目：用 515 行纯 TypeScript 实现最简 Agent 核心

---

### D. 术语对照

| 英文 | 中文 | 说明 |
|:----|:----|:----|
| Harness | 运行时外壳 | 围绕LLM的确定性基础设施层 |
| Session | 会话 | 只追加的事件日志，支持 `wake(sessionId)` |
| Sidechain | 侧链 | 子Agent独立JSONL日志，仅摘要返回父级 |
| MCP | 模型上下文协议 | Agent与工具的标准化通信协议 |
| TAOR | 思考-行动-观察-重复 | 核心执行循环 |
| Fresh-Context | 全新上下文 | 审查Agent从空白上下文重新审视产出 |
| Context Rot | 上下文腐败 | 长上下文窗口中的性能衰减 |
| Knowledge Distillation | 知识蒸馏 | 将大型模型知识迁移到较小模型 |
| Worktree | 工作树 | git worktree隔离，文件系统级隔离 |
