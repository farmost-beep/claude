---
codebase: goals
status: pending
auto_apply: true
created: 2026-06-08
---

# 健康追踪中断 — 建议补记录

## 发现了什么
⚠️ 近7天无健康相关记录 — 健康追踪可能中断

## 修复后应该是什么样
近7天至少有一条健康相关记录（运动/体重/睡眠任一项）

## AI修复指令（给Claude的Prompt）
提醒用户：健康追踪已中断。建议立即记录：今天的体重、本周运动次数、最近3天的平均睡眠时长。如果用户提供数据，更新到 deliverables/健康/ 对应文件中。

---
> 状态：pending | 批准后运行 `python3 scripts/auto_pr.py --apply 2026-06-08_goals_health_gap.md` 或在Claude中说"执行auto-fix 2026-06-08_goals_health_gap.md"
