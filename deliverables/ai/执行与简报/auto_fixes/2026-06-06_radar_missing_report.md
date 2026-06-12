---
codebase: radar
status: pending
auto_apply: true
created: 2026-06-06
---

# AI能力雷达周报中断 — 自动起草补报提示

## 发现了什么
🟡 雷达周报超过7天未更新 — 建议本周补上

## 修复后应该是什么样
补上缺失的雷达周报，恢复每周一次的节奏

## AI修复指令（给Claude的Prompt）
按 /deliverables/记忆规范/AI能力雷达周报模板.md 的格式，扫描本周AI领域最新动态（四源：基准/产品/实战/反向），生成一份补报的雷达周报初稿，保存到 deliverables/ai/AI能力雷达周报_[周次].md。

---
> 状态：pending | 批准后运行 `python3 scripts/auto_pr.py --apply 2026-06-06_radar_missing_report.md` 或在Claude中说"执行auto-fix 2026-06-06_radar_missing_report.md"
