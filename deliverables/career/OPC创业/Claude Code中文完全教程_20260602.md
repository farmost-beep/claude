# Claude Code 中文完全教程

> 从入门到精通 | 2026-06-02 | v1.0
> 作者：陈颖芳 | 基于6个月深度使用实战经验
> 
> **适合读者**：有编程基础的开发者/技术管理者/AI工具重度用户
> **学习目标**：把Claude Code从"聊天工具"变成你的"个人AI操作系统"

---

## 第一篇：认识Claude Code

### 1.1 Claude Code是什么

**一句话**：驻留在你项目目录中的AI编程伙伴，而不是网页端的问答机器人。

它与ChatGPT/claude.ai/其他AI工具的核心区别：

| 维度 | Claude Code | ChatGPT/网页Claude | GitHub Copilot |
|:-----|:-----------|:------------------|:---------------|
| **感知范围** | 你的整个项目目录 | 只有你粘贴的内容 | 当前打开的文件 |
| **能做的事** | 读写文件、执行命令、运行脚本 | 只能聊天 | 代码补全 |
| **多任务** | 同时跑多个子Agent | 单线程对话 | 单文件 |
| **记忆** | CLAUDE.md持久化记住你 | 每次从零开始 | 无 |
| **自动化** | cron定时任务、hooks钩子 | 无 | 无 |

**适用场景**：软件开发、文档编写、数据分析、投资研究、知识管理、自动化运维、项目管理

**不适用场景**：纯聊天、图片生成、视频处理（这些用网页版Claude）

### 1.2 安装

**前提**：
- macOS或Linux（Windows可通过WSL）
- Node.js 18+（`node --version` 检查）
- 一个Anthropic账号（claude.ai）

**安装**：
```bash
npm install -g @anthropic-ai/claude-code
```

**验证**：
```bash
claude --version
```

**配置API密钥**：
```bash
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxx"
```
建议写入 `~/.zshrc` 或 `~/.bashrc` 避免每次设置。

### 1.3 启动

```bash
cd your-project-directory
claude
```

第一次启动会在当前目录创建 `.claude/` 目录，存放配置和会话记录。

---

## 第二篇：核心操作

### 2.1 基础命令

| 命令 | 作用 | 示例 |
|:-----|:-----|:------|
| `/help` | 查看所有命令 | `/help` |
| `/status` | 查看当前会话的token使用量 | `/status` |
| `/compact` | 压缩长对话上下文 | `/compact` |
| `/clear` | 清空当前对话 | `/clear` |
| `/exit` | 退出 | `/exit` |

### 2.2 自然语言指令（最常用）

不需要记命令，直接说你想做的事：

```bash
# 文件操作
"读取 investment_report.md 的第三章"
"修改 config.json 中的数据库连接字符串"
"在当前目录下创建一个新文件夹 analysis/，并生成README"

# 代码操作
"给这个Python脚本加注释"
"解释一下这个函数的逻辑"
"把我的Flask应用改成FastAPI"
"帮我调试这个报错"

# 多步骤任务
"先统计项目中的文件数，然后列出最大的5个文件"
"帮我搜索所有包含'TODO'的文件，汇总成清单"
```

### 2.3 关键技巧：思维链

Claude Code最强大的能力不是一次回答，而是**逐步推理**：

```bash
# 好的写法（明确说明要做什么）
"帮我分析一下这个项目的代码质量"

# 更好的写法（让AI展示思考过程）
"逐步分析这个项目的代码质量：
 步骤1：统计代码行数、文件数、语言分布
 步骤2：检查是否有明显的问题模式
 步骤3：给优化建议
 步骤4：输出格式化的分析报告"
```
核心原则：**先说目标，再说步骤，最后要输出格式**。

---

## 第三篇：文件与项目操作

### 3.1 文件读写

Claude Code可以直接读写你的文件——这是它与网页版最本质的区别。

```bash
"读取 src/main.py"                    # 读文件
"把下面这段JSON写入 config.json"      # 写文件
"把README.md的第二节改为以下内容..."  # 编辑文件
"重命名 report_v1.md 为 report_v2.md" # 重命名
```

**实际案例**：写一份投资报告
```bash
"帮我生成一份投资分析报告，内容包含：
 - 当前持仓清单
 - 各品种的盈亏情况
 - 风险集中度分析
 保存为 investment/持仓分析_20260601.md"
```

### 3.2 Git操作

```bash
"查看当前git状态"
"帮我提交刚才的改动，commit信息写'feat: 新增投资分析报告'"
"查看这个文件的历史版本"
"创建一个新分支 feature-analysis，并切换到它"
```

### 3.3 搜索

```bash
"在所有.md文件中搜索'昆仑万维'"
"在 investment/ 目录下找包含'PE'的文件"
"帮我统计一下项目中有多少个Python文件"
```

---

## 第四篇：多Agent并行（核心能力）

这是Claude Code最难被替代的功能。**一个Claude可以同时分身成多个子Agent，分别处理不同任务。**

### 4.1 基础并行

```bash
"同时做三件事：
 1. 帮我统计deliverables/下有多少个文件
 2. 搜索所有含'TODO'的文件
 3. 检查git状态
 三个任务独立运行，互不等待"
```

### 4.2 研究型并行

```bash
"同时开3个Agent，分别研究：
 Agent A：昆仑万维(300418)的最新财报
 Agent B：稀土ETF(159715)的近期走势
 Agent C：A股市场的整体资金流向
 完成后汇总成一份报告"
```

### 4.3 多Agent协作模式

```
大Claude（主控）→ 分配任务 → 子Agent A（数据收集）
                        → 子Agent B（分析计算）
                        → 子Agent C（报告撰写）
完成后 → 汇总 → 输出
```

实操指令：
```bash
"启动Agent组研究昆仑万维：
 第一步（并行启动）：
   Agent A：提取Q1财报的9项核心指标
   Agent B：对比行业75分位数
   Agent C：扫描9条风险信号
 第二步（A/B/C完成后）：
   Agent D：基于前三者的输出做一句话总结
 第三步（所有完成后）：
   Agent E：汇总审查，检查一致性"
```

---

## 第五篇：记忆系统

Claude Code通过 `CLAUDE.md` 文件记住你的偏好。

### 5.1 项目级记忆

在每个项目根目录创建 `CLAUDE.md`，写入项目相关的背景信息。每次启动Claude Code时，它自动读取这些规则。

示例 `CLAUDE.md`：
```markdown
# 项目规则

## 代码风格
- 使用Python 3.9+
- 遵循PEP8规范
- 使用type hints

## 约定
- 修改文件后必须验证文件是否存在
- 提交信息格式：feat/fix/refactor + 中文描述
```

### 5.2 全局级记忆

`~/.claude/CLAUDE.md` 中的规则对**所有项目**生效。适合存放：
- 你个人的工作习惯
- 常用的工具链
- 通用偏好设置

### 5.3 内存文件系统（进阶）

对于复杂项目，可以建立记忆文件索引：
```bash
~/.claude/projects/<project-name>/memory/
  ├── MEMORY.md          # 索引
  ├── personal.md        # 个人偏好
  └── project_state.md   # 项目状态
```

CLAUDE.md 的第一行可以写：
```markdown
开始会话前，先加载 .claude/projects/当前项目/memory/ 目录下的所有.m d文件
```

---

## 第六篇：自动化（定时任务 + Hooks）

### 6.1 定时任务（Cron）

Claude Code支持自然语言设定定时任务：

```bash
/loop 每天8:00 检查待发布文章
/loop 每30分钟 检查邮件回复
/loop 每周六 运行系统健康检查
```

这些任务在Claude Code空闲时自动触发，支持持久化（重启后继续）。

### 6.2 Hooks（生命周期钩子）

在 `.claude/settings.json` 中配置：
```json
{
  "hooks": {
    "beforeCommand": ["echo '开始执行命令'"],
    "afterCommand": ["echo '命令执行完成'"],
    "afterToolUse": ["python3 scripts/validate_output.py"]
  }
}
```

常用场景：
- 每次写文件后自动验证文件存在
- 每次执行命令前后记录日志
- 每次输出结果后检查格式

### 6.3 后台任务

长时间运行的脚本可以放在后台：
```bash
"在后台运行 python3 build_goal_pdfs.py"
"在后台运行测试脚本，完成后通知我"
```

---

## 第七篇：MCP插件（外部工具扩展）

MCP（Model Context Protocol）是Claude Code调用外部工具的协议。

### 7.1 安装MCP插件

```bash
# 添加一个Web搜索能力
claude mcp add web-search -- npx @anthropic/mcp-web-search

# 添加一个数据库查询能力
claude mcp add database -- python3 scripts/mcp_db_server.py
```

### 7.2 常用MCP插件

| 插件 | 能力 | 场景 |
|:-----|:-----|:------|
| Web Search | 实时网络搜索 | AI简报、行业研究 |
| Filesystem | 高级文件操作 | 项目管理 |
| Database | SQL数据库查询 | 数据分析 |
| GitHub | PR/Issue管理 | 开发工作流 |
| Slack | 消息发送与读取 | 团队协作 |
| 自定义 | 你自己写的能力 | 任意场景 |

### 7.3 自定义MCP Server

10行Python就能写一个MCP Server：
```python
# my_mcp_server.py
import json, sys
from datetime import datetime

def handle_request(request):
    if request["method"] == "get_time":
        return {"result": datetime.now().isoformat()}
    return {"error": "unknown method"}

for line in sys.stdin:
    result = handle_request(json.loads(line))
    print(json.dumps(result), flush=True)
```

---

## 第八篇：实战工作流

### 8.1 个人投资分析工作流

```
7:00  AI搜索全球AI前沿 → 筛选3条+1个行动 → 存入简报
8:00  综合简报 → 提取P0行动清单 → 推送到微信
9:30  开盘 → Agent组跑持仓分析 → 检查集中度
每周 飞轮扫描：知识库/AI能力/投资/健康/家庭/事业
每月 记忆文件新鲜度检查 → 修正过期数据
```

### 8.2 内容创作工作流

```
Claude Code → 生成文章初稿 → 你审阅修改 → 发布
                                            ↓
                            自动生成PDF版本 → 归档
                                            ↓
                            自动同步到知识库
```

### 8.3 知识管理工作流

```
日常记录 → 形成碎片笔记 → Claude整理 → 知识卡片
                                            ↓
                                  MOC索引 → 交付文档 → PDF → Git提交
```

---

## 第九篇：常见问题与技巧

### 9.1 上下文太长怎么办？

```bash
/compact   # 压缩上下文（无损）
```

对话超过50轮后建议用 `/compact`，不要等到卡死才做。

### 9.2 API费用太高怎么办？

- 简单任务用默认模型（够用）
- 复杂分析才切换到Opus
- 设定 `/status` 定期检查token消耗
- 使用 `settings.json` 限制最大token：`"maxTokens": 4096`

### 9.3 安全性

- Claude Code有完整的项目访问权限，不要在不信任的项目中使用
- `/settings` 中可以查看和管理权限
- API密钥不要提交到git

### 9.4 退出后回来能继续吗？

可以。Claude Code会保存会话到 `.claude/sessions/`。下次运行 `claude` 时会自动恢复。

---

## 附：命令速查表

| 场景 | 指令 |
|:-----|:------|
| 读文件 | "读取 xxx.md" |
| 写文件 | "写入 xxx.md" |
| 修改文件 | "把第X行改为" |
| 搜索 | "搜索 'xxx'" |
| 找文件 | "找到所有 .py 文件" |
| 统计数据 | "统计 deliverables/ 下的文件数" |
| 分析代码 | "分析这个函数的时间复杂度" |
| 翻译 | "把这个文档翻译成英文" |
| 总结 | "总结这个文件夹的内容" |
| 对比 | "对比 file1.md 和 file2.md" |
| 批量操作 | "把所有 .txt 文件重命名为 .md" |
| 定时任务 | `/loop 每天9点 检查发布计划` |
| 并行任务 | "同时做三件事：1...2...3..." |
| 后台任务 | "在后台运行...." |
| 查看状态 | `/status` |
| 压缩上下文 | `/compact` |
| 查看帮助 | `/help` |

---

> 作者：陈颖芳 | 基于2026年5-6月深度使用经验
> 
> 本教程是"Claude Code从入门到精通"系列的第一版。
> 反馈与建议请联系作者公众号或邮箱。
