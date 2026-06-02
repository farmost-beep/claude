# Anthropic 把Agent拆成了三部分：大脑、躯干、手

如果你用过任何一个AI Agent产品，你大概遇到过这个问题：Agent跑着跑着卡住了、崩溃了、或者进入了一个死循环。你没法重启它，因为重启意味着丢失上下文。

Anthropic 的工程团队在2026年发表了一篇文章，详细描述了他们如何解决这个问题。方法很简洁：**把Agent拆成三个独立的组件。**

## 三组件架构

```
Session（会话）→ 所有发生的事件的只追加日志
Harness（躯干）→ 调用Claude并路由工具调用的循环
Sandbox（沙箱）→ 代码执行和文件编辑的环境
```

在早期版本的实现中，这三个组件是捆绑在同一个容器里的。作者称之为"pet"（宠物）模式——如果容器死了，你不仅失去了运行环境，还失去了上下文。你不敢重启它。

重构后的架构将三者解耦。

## 关键洞察：容器变成了"cattle"

在解耦后的架构中，Harness 将 Sandbox 当作一个普通工具调用：

```
execute(name, input) → string
```

如果 Sandbox 容器崩溃了，Harness 捕获到的是一个工具调用错误。它可以优雅地启动一个新的 Sandbox 容器，把上下文从 Session 恢复。

**这是"cattle"（牲畜）和"pet"（宠物）的区别**：死了一头牲畜，你换一头。死了一只宠物，你难受半天。

## 三个独立的好处

**Session独立于Harness**意味着：
- 新Harness可以通过 `wake(sessionId)` 恢复
- Fault tolerance——任何组件都可以独立崩溃和重启
- 你可以在Session级别做审计和回放

**Harness独立于Sandbox**意味着：
- **凭证安全**——API密钥和数据库密码永远不需要进入Sandbox
- 响应速度提升——p50延迟下降约60%，p95延迟下降超过90%（不需要为"从不进入Sandbox的会话"预分配容器）
- 多Harness可以共享Sandbox，多Sandbox可以服务于一个Harness

**"很多大脑，很多手"**：
- Harness甚至可以互相传递Sandbox
- Harness不需要知道Sandbox的具体实现——它是一个容器、一台手机、还是一个宝可梦模拟器
- 这为未来Agent互操作打开了可能性

## 与你的关联

这与你用Claude Code的体验直接相关。当你同时启动多个Agent时：
- 每个Agent是一个Harness
- 每个文件系统交互发生在Sandbox中
- Session就是你看到的会话日志

理解这三者的界限，你就理解了为什么Claude Code可以同时处理多个任务而不互相干扰——以及未来Agent系统应该怎么设计。

## 更长远的含义

Anthropic 的文章没有明说，但从架构中可以推断出一条路线：

当 Session（大脑）可以和 Harness（躯干）解耦，你就可以在Session级别做持久化、搜索、跨会话分析。当 Sandbox（手）可以跨Harness共享，Agent就可以接力工作——一个Agent做不完的复杂任务，另一个Agent可以接着做。

这不是一次性会话，这是**分布式Agent操作系统**的雏形。

**来源**：[anthropic.com/engineering/managed-agents](https://www.anthropic.com/engineering/managed-agents)
