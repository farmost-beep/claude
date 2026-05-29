---
goal: AI能力
dimension: 扩展力
type: Python训练
week: 1
date: 2026-05-28
status: in_progress
---

# Python Week 1：基础语法与数据结构

> 目标：能独立写50行以内的数据处理脚本，能看懂AI生成的Python代码每一行在做什么。

## 本周覆盖

- 变量、类型（str, int, float, bool）
- 条件判断（if/elif/else）
- 循环（for/while）
- 函数定义与调用
- 列表、字典、集合的操作
- 文件读取（CSV）

## 不覆盖（后续周）

- 类与面向对象（Week 3）
- 异常处理（Week 3）
- 正则表达式（Week 2）

---

## Day 1：变量、类型、条件、循环

### 练习：写一个脚本统计投资组合数据

创建一个文件 `portfolio_stats.py`，完成以下任务：

1. 定义一个列表，包含你的持仓股票（名称、买入价、当前价、仓位比例）
2. 遍历列表，计算每只股票的盈亏比例
3. 筛选出亏损超过20%的股票（触发投资行为规范§4.3的强制复盘）
4. 打印结果

```python
# portfolio_stats.py
# 你的持仓数据（名称, 买入价, 当前价, 仓位%）
portfolio = [
    ("昆仑万维", 45.0, 32.5, 8.0),
    ("东方财富", 18.0, 22.3, 10.0),
    ("寒武纪", 380.0, 520.0, 12.0),
    ("招商银行", 38.0, 42.0, 15.0),
]

print("=== 持仓盈亏扫描 ===\n")

losers = []  # 亏损超过20%的股票

for name, buy_price, current_price, weight in portfolio:
    pnl_pct = (current_price - buy_price) / buy_price * 100
    status = "📈" if pnl_pct > 0 else "📉"

    print(f"{status} {name}: {pnl_pct:+.1f}% (买入{buy_price} → 当前{current_price}) 仓位{weight}%")

    if pnl_pct < -20:
        losers.append((name, pnl_pct))

if losers:
    print("\n⚠️ 强制复盘清单（亏损>20%）：")
    for name, pnl in losers:
        print(f"  🔴 {name}: {pnl:.1f}% — 检查买入逻辑是否被破坏")
else:
    print("\n✅ 无触发强制复盘")
```

### 自查题

- [ ] `for name, buy_price, current_price, weight in portfolio:` 是什么意思？为什么可以一次取4个值？
- [ ] `pnl_pct:+.1f` 中的 `+.1f` 是什么意思？
- [ ] `losers.append((name, pnl_pct))` 中的双括号是为什么？
- [ ] 如果要把结果保存为CSV文件，需要加什么代码？

---

## Day 2：列表、字典、集合操作

### 练习：重构Day 1的代码，用字典替代元组

```python
# portfolio_stats_v2.py — 用字典存储，更易读
portfolio = [
    {"name": "昆仑万维", "buy": 45.0, "current": 32.5, "weight": 8.0},
    {"name": "东方财富", "buy": 18.0, "current": 22.3, "weight": 10.0},
    {"name": "寒武纪",   "buy": 380.0, "current": 520.0, "weight": 12.0},
    {"name": "招商银行", "buy": 38.0, "current": 42.0, "weight": 15.0},
]

# 计算总仓位
total_weight = sum(stock["weight"] for stock in portfolio)
print(f"总仓位: {total_weight}%")

# 找出盈利的股票
winners = [s for s in portfolio if s["current"] > s["buy"]]
print(f"盈利: {len(winners)}/{len(portfolio)} 只")

# 按盈亏排序
sorted_by_pnl = sorted(portfolio,
    key=lambda s: (s["current"] - s["buy"]) / s["buy"],
    reverse=True)
for s in sorted_by_pnl:
    pnl = (s["current"] - s["buy"]) / s["buy"] * 100
    print(f"  {s['name']}: {pnl:+.1f}%")
```

### 自查题

- [ ] `sum(stock["weight"] for stock in portfolio)` 为什么不用方括号？
- [ ] 列表推导式 `[s for s in portfolio if ...]` 的语法结构是什么？
- [ ] `lambda s: ...` 是什么意思？什么时候用？

---

## Day 3：函数定义

### 练习：把扫描逻辑封装成函数

```python
def scan_portfolio(portfolio, alert_threshold=-20):
    """扫描持仓，返回需要复盘的股票列表"""
    alerts = []
    for stock in portfolio:
        pnl_pct = (stock["current"] - stock["buy"]) / stock["buy"] * 100
        if pnl_pct <= alert_threshold:
            alerts.append({
                "name": stock["name"],
                "pnl": pnl_pct,
                "reason": f"亏损超过{abs(alert_threshold)}%，触发强制复盘"
            })
    return alerts

def check_position_limits(portfolio, max_single=15.0):
    """检查仓位是否超标"""
    over = []
    for stock in portfolio:
        if stock["weight"] > max_single:
            over.append(stock["name"])
    return over

# 使用
alerts = scan_portfolio(portfolio)
print(f"强制复盘: {len(alerts)} 只")
for a in alerts:
    print(f"  {a['name']}: {a['pnl']:.1f}% — {a['reason']}")

over_weight = check_position_limits(portfolio)
if over_weight:
    print(f"仓位超标: {over_weight}")
```

### 自查题

- [ ] 为什么要把代码封装成函数？直接写在外面不行吗？
- [ ] `alert_threshold=-20` 中的 `=-20` 是什么意思？
- [ ] 函数返回的 `alerts` 是什么类型？调用方怎么用它？

---

## Day 4-5：读CSV + 综合练习

### 练习：读取真实的投资数据CSV，做统计分析

假设你有一个 `positions.csv`:

```csv
name,code,market,buy_price,current_price,shares,weight
昆仑万维,300418,SZ,45.0,32.5,5000,8.0
东方财富,300059,SZ,18.0,22.3,15000,10.0
寒武纪,688256,SH,380.0,520.0,1000,12.0
招商银行,600036,SH,38.0,42.0,12000,15.0
```

写脚本读取并分析：

```python
import csv

def load_portfolio(filepath):
    """从CSV加载持仓数据"""
    portfolio = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            portfolio.append({
                "name": row["name"],
                "code": row["code"],
                "buy": float(row["buy_price"]),
                "current": float(row["current_price"]),
                "shares": int(row["shares"]),
                "weight": float(row["weight"]),
            })
    return portfolio

# 使用
portfolio = load_portfolio("positions.csv")

# 计算总市值
total_value = sum(s["current"] * s["shares"] for s in portfolio)
print(f"组合总市值: {total_value:,.0f} 元")

# 计算盈亏
total_cost = sum(s["buy"] * s["shares"] for s in portfolio)
total_pnl = total_value - total_cost
print(f"总盈亏: {total_pnl:+,.0f} 元 ({total_pnl/total_cost*100:+.1f}%)")
```

---

## 本周验证标准

- [ ] 能独立写出 `portfolio_stats.py` 全部代码（不看模板）
- [ ] 能解释每一行代码在做什么
- [ ] 能从报错信息中找到问题所在行
- [ ] 能把代码跑通并输出正确结果
