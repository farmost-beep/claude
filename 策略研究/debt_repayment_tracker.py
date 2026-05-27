#!/usr/bin/env python3
"""
还本资金追踪计算器 — 追踪僵尸持仓清仓+昆仑万维减仓进度，计算距60万还本目标的缺口

用法:
  python3 debt_repayment_tracker.py status                  # 显示当前还本进度
  python3 debt_repayment_tracker.py scenario <昆仑万维价格>   # 昆仑万维减仓情景分析
  python3 debt_repayment_tracker.py sell <代码> <成交价>      # 录入僵尸持仓实际卖出
  python3 debt_repayment_tracker.py unsell <代码>             # 撤销某笔卖出记录
  python3 debt_repayment_tracker.py reset                    # 重置所有卖出记录
"""

from __future__ import annotations

import json
import os
import sys
from datetime import date

# ============================================================
# 配置常量
# ============================================================

TARGET = 600_000          # 还本目标 60万元
HKD_RATE = 0.92           # 港币→人民币汇率
COMMISSION_RATE = 0.00025  # 佣金费率 万2.5
COMMISSION_MIN = 5.0       # 佣金最低 5元
STAMP_TAX_RATE = 0.001     # 印花税率 千1 (仅卖出收取)

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".debt_sales.json")

# ============================================================
# 僵尸持仓数据 (19个)
# ============================================================

# 数据结构: (代码, 名称, 股数, 预期单价, 预期总值(CNY), 账户, 市场)
# 市场: "A"=A股(单价为CNY), "H"=港股(单价为HKD, 预期总值已按0.92折算为CNY)

DEAD_POSITIONS = [
    # ===== 普通账户 (8个) =====
    ("300142", "沃森生物",     100,   13.93,  1393,   "普通账户", "A"),
    ("600126", "杭钢股份",     100,    8.07,   807,   "普通账户", "A"),
    ("002570", "贝因美",       100,    4.85,   485,   "普通账户", "A"),
    ("600050", "中国联通",     100,    4.45,   445,   "普通账户", "A"),
    ("688525", "佰维存储",      21,  307.71,  6462,   "普通账户", "A"),
    ("588460", "科创50增强ETF", 100,   2.28,   228,   "普通账户", "A"),
    ("512070", "证券保险ETF",   300,   0.77,   231,   "普通账户", "A"),
    ("512000", "券商ETF",      3200,   0.504, 1613,   "普通账户", "A"),

    # ===== 港币账户 (2个, 单价为HKD, 预期总值已折算CNY) =====
    ("00884",  "旭辉控股集团",  2000,   0.061,  112,   "港币账户", "H"),
    ("00390",  "中国中铁",      1000,   3.57,  3284,   "港币账户", "H"),

    # ===== 信用账户 (9个) =====
    ("600050", "中国联通",     100,    4.45,   445,   "信用账户", "A"),
    ("000002", "万科A",        100,    3.39,   339,   "信用账户", "A"),
    ("600995", "南网储能",     100,   14.19,  1419,   "信用账户", "A"),
    ("601788", "光大证券",     100,   14.67,  1467,   "信用账户", "A"),
    ("601377", "兴业证券",     100,    5.86,   586,   "信用账户", "A"),
    ("002458", "益生股份",     130,    8.40,  1092,   "信用账户", "A"),
    ("512000", "券商ETF",      100,    0.50,    50,   "信用账户", "A"),
    ("512070", "证券保险ETF",  100,    0.77,    77,   "信用账户", "A"),
    ("600549", "厦门钨业",     100,   53.95,  5395,   "信用账户", "A"),
]

# 昆仑万维代码 (用于情景分析)
KUNLUN_SYMBOL = "300418"

# ============================================================
# 费用计算
# ============================================================

def calc_fees(gross: float) -> tuple[float, float, float]:
    """计算交易费用，返回 (总费用, 佣金, 印花税)"""
    commission = max(gross * COMMISSION_RATE, COMMISSION_MIN)
    stamp_tax = gross * STAMP_TAX_RATE
    return commission + stamp_tax, commission, stamp_tax


def calc_net(gross: float) -> float:
    """计算扣除费用后的净收入"""
    fees, _, _ = calc_fees(gross)
    return gross - fees


# ============================================================
# 数据持久化
# ============================================================

def load_sales() -> list[dict]:
    """加载已保存的卖出记录"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_sales(sales: list[dict]) -> None:
    """保存卖出记录到JSON文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(sales, f, ensure_ascii=False, indent=2)


# ============================================================
# 持仓查询
# ============================================================

def find_positions(symbol: str) -> list[dict]:
    """根据代码查找僵尸持仓（可能多个账户持有同一代码），返回持仓dict列表"""
    results = []
    for pos in DEAD_POSITIONS:
        if pos[0] == symbol:
            results.append({
                "symbol": pos[0],
                "name": pos[1],
                "shares": pos[2],
                "expected_price": pos[3],
                "expected_value": pos[4],
                "account": pos[5],
                "market": pos[6],
            })
    return results


def find_position(symbol: str, account: str | None = None) -> dict | None:
    """查找唯一持仓。若多账户持有同一代码，需指定account；否则返回第一个匹配。"""
    matches = find_positions(symbol)
    if not matches:
        return None
    if account:
        for m in matches:
            if m["account"] == account:
                return m
        return None  # 指定账户不匹配
    return matches[0]


def _position_key(symbol: str, account: str) -> str:
    """生成持仓唯一键"""
    return f"{symbol}@{account}"


def list_positions_by_account() -> dict[str, list[dict]]:
    """按账户分组返回所有持仓"""
    accounts: dict[str, list[dict]] = {}
    for pos in DEAD_POSITIONS:
        d = {
            "symbol": pos[0],
            "name": pos[1],
            "shares": pos[2],
            "expected_price": pos[3],
            "expected_value": pos[4],
            "account": pos[5],
            "market": pos[6],
        }
        accounts.setdefault(pos[5], []).append(d)
    return accounts


# ============================================================
# 核心计算
# ============================================================

def expected_total() -> float:
    """全部19个僵尸持仓的预期总值 (CNY)"""
    return sum(pos[4] for pos in DEAD_POSITIONS)


def _sold_keys(sales: list[dict]) -> set[str]:
    """返回已卖出持仓的唯一键集合 (symbol@account)"""
    return {_position_key(s["symbol"], s["account"]) for s in sales}


def expected_total_by_sold(sales: list[dict]) -> float:
    """未卖出僵尸持仓的预期总值"""
    sold_keys = _sold_keys(sales)
    return sum(pos[4] for pos in DEAD_POSITIONS
               if _position_key(pos[0], pos[5]) not in sold_keys)


def estimated_net_remaining(sales: list[dict]) -> float:
    """未卖出持仓的预估净收入 (扣除预估费用)"""
    sold_keys = _sold_keys(sales)
    total_net = 0.0
    for pos in DEAD_POSITIONS:
        if _position_key(pos[0], pos[5]) not in sold_keys:
            total_net += calc_net(pos[4])
    return round(total_net, 2)


def realized_gross(sales: list[dict]) -> float:
    """已卖出持仓的成交总额"""
    return sum(s["gross"] for s in sales)


def realized_net(sales: list[dict]) -> float:
    """已卖出持仓的净收入总额 (扣除实际费用)"""
    return sum(s["net"] for s in sales)


def total_projected_net(sales: list[dict]) -> float:
    """全部资金预期净收入 = 已回笼净额 + 待清仓预估净额"""
    return round(realized_net(sales) + estimated_net_remaining(sales), 2)


def gap_to_target(sales: list[dict]) -> float:
    """距60万目标的缺口"""
    return round(TARGET - total_projected_net(sales), 2)


def progress_pct(sales: list[dict]) -> float:
    """还本进度百分比"""
    net = total_projected_net(sales)
    return round(min(net / TARGET * 100, 100.0), 1)


# ============================================================
# 格式化工具
# ============================================================

def fmt_cny(val: float) -> str:
    """格式化人民币金额"""
    if abs(val) >= 10000:
        return f"¥{val/10000:,.1f}万"
    elif abs(val) >= 100:
        return f"¥{val:,.0f}"
    else:
        return f"¥{val:,.2f}"


def fmt_hkd(val: float) -> str:
    """格式化港币金额 (val为HKD)"""
    if abs(val) >= 10000:
        return f"HK${val/10000:,.1f}万"
    elif abs(val) >= 100:
        return f"HK${val:,.0f}"
    elif abs(val) >= 1:
        return f"HK${val:,.2f}"
    else:
        return f"HK${val:,.3f}"


def fmt_price(val: float, currency: str = "¥") -> str:
    """格式化单价，保留适当小数位"""
    if val >= 100:
        return f"{currency}{val:,.2f}"
    elif val >= 1:
        return f"{currency}{val:,.3f}".rstrip("0").rstrip(".")
    else:
        return f"{currency}{val:.4f}".rstrip("0").rstrip(".")


def fmt_pct(val: float, decimals: int = 1) -> str:
    """格式化百分比"""
    return f"{val:.{decimals}f}%"


def progress_bar(pct: float, width: int = 30) -> str:
    """生成ASCII进度条"""
    filled = int(width * pct / 100)
    empty = width - filled
    bar = "█" * filled + "░" * empty
    return f"[{bar}] {pct:.1f}%"


def table(headers: list[str], rows: list[list[str]], align: list[str] | None = None) -> str:
    """生成对齐的ASCII表格文本"""
    if not rows:
        return "(无数据)"

    # 计算每列宽度
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(cell))

    if align is None:
        align = ["<"] * len(headers)

    def fmt_row(cells: list[str]) -> str:
        parts = []
        for i, cell in enumerate(cells):
            a = align[i] if i < len(align) else "<"
            parts.append(f"{cell:{a}{col_widths[i]}}")
        return "  " + "  │  ".join(parts)

    sep = "  " + "──┼──".join("─" * w for w in col_widths)

    lines = [fmt_row(headers), sep]
    for row in rows:
        lines.append(fmt_row(row))
    return "\n".join(lines)


# ============================================================
# 显示函数
# ============================================================

def print_header(title: str) -> None:
    """打印区块标题"""
    print()
    print("═" * 72)
    print(f"  {title}")
    print("═" * 72)


def print_overview(sales: list[dict]) -> None:
    """打印还本进度概览"""
    r_net = realized_net(sales)
    e_net = estimated_net_remaining(sales)
    t_net = total_projected_net(sales)
    gap = gap_to_target(sales)
    pct = progress_pct(sales)

    print_header(f"还本资金追踪 — {date.today()}")
    print(f"  目标金额:     {fmt_cny(TARGET)}")
    print(f"  已回笼净额:   {fmt_cny(r_net)}  ({len(sales)}/19 个僵尸持仓已清)")
    print(f"  待清仓预估:   {fmt_cny(e_net)}  ({19-len(sales)} 个待清)")
    print(f"  预期总回笼:   {fmt_cny(t_net)}")
    print(f"  距目标缺口:   {fmt_cny(gap)}")
    print(f"  完成进度:     {progress_bar(pct)}")
    print(f"  {'(已超额完成!)' if gap <= 0 else ''}")


def print_positions(sales: list[dict]) -> None:
    """按账户打印持仓清仓状态表"""
    sold_map = {_position_key(s["symbol"], s["account"]): s for s in sales}
    accounts = list_positions_by_account()

    account_order = ["普通账户", "港币账户", "信用账户"]
    for acct in account_order:
        if acct not in accounts:
            continue
        positions = accounts[acct]

        headers = ["代码", "名称", "股数", "预估价", "预期值", "状态", "成交价", "净收入"]
        row_align = [">", "<", ">", ">", ">", "<", ">", ">"]
        rows = []
        for p in positions:
            pkey = _position_key(p["symbol"], p["account"])
            if pkey in sold_map:
                s = sold_map[pkey]
                status = "✓ 已清"
                actual_price = fmt_cny(s["price"])
                net_str = fmt_cny(s["net"])
            else:
                status = "○ 待清"
                actual_price = "—"
                net_str = fmt_cny(calc_net(p["expected_value"]))

            if p["market"] == "H":
                exp_price_str = fmt_hkd(p["expected_price"])
            else:
                exp_price_str = fmt_price(p["expected_price"], "¥")

            rows.append([
                p["symbol"],
                p["name"],
                str(p["shares"]),
                exp_price_str,
                fmt_cny(p["expected_value"]),
                status,
                actual_price,
                net_str,
            ])

        print(f"\n  ── {acct} ({len(positions)}个) ──")
        print(table(headers, rows, row_align))

        # 小计
        subtotal_exp = sum(p["expected_value"] for p in positions)
        subtotal_net = sum(
            sold_map[_position_key(p["symbol"], p["account"])]["net"]
            if _position_key(p["symbol"], p["account"]) in sold_map
            else calc_net(p["expected_value"])
            for p in positions
        )
        sold_count = sum(1 for p in positions
                         if _position_key(p["symbol"], p["account"]) in sold_map)
        print(f"  小计: 预期 {fmt_cny(subtotal_exp)} | 净收入 {fmt_cny(subtotal_net)} | {sold_count}/{len(positions)} 已清")


def print_scenario(sales: list[dict], user_price: float) -> None:
    """打印昆仑万维减仓情景分析"""
    gap = gap_to_target(sales)
    r_net = realized_net(sales)
    e_net = estimated_net_remaining(sales)

    print_header(f"昆仑万维 [{KUNLUN_SYMBOL}] 减仓情景分析")
    print(f"  已回笼净额:   {fmt_cny(r_net)}")
    print(f"  待清仓预估:   {fmt_cny(e_net)}")
    print(f"  当前缺口:     {fmt_cny(gap)}")

    if gap <= 0:
        print("\n  ✓ 缺口已为0或负值，无需减仓昆仑万维。")
        return
    print()

    # 情景价格列表 (去重排序)
    scenario_prices = sorted(set([40.0, 45.0, 50.0, user_price]))

    headers = ["情景", "昆仑股价", "需减仓股数", "成交总额", "费用合计", "净收入", "剩余缺口"]
    row_align = ["<", ">", ">", ">", ">", ">", ">"]
    rows = []

    for price in scenario_prices:
        # 计算需卖出多少股才能覆盖缺口 (向上取整到100股/手)
        net_per_share = calc_net(price)
        shares_exact = gap / net_per_share
        # 向上取整到100股
        shares_round = int((shares_exact + 99) / 100) * 100

        gross = shares_round * price
        fees, comm, stamp = calc_fees(gross)
        net = gross - fees
        remaining_gap = round(gap - net, 2)

        marker = " ← 当前" if price == user_price else ""
        label = f"情景{scenario_prices.index(price)+1}{marker}"

        rows.append([
            label,
            f"¥{price:.2f}",
            f"{shares_round:,}股",
            fmt_cny(gross),
            fmt_cny(fees),
            fmt_cny(net),
            fmt_cny(remaining_gap) if remaining_gap > 0 else "✓ 已覆盖",
        ])

    print(table(headers, rows, row_align))
    print()
    print("  费用明细: 佣金万2.5(最低5元) + 印花税千1")
    print("  需减仓股数: 向上取整到整手(100股)，含费用")
    print("  注: 若缺口为0或负值，说明僵尸清仓已足够覆盖还本目标")


def print_sale_summary(sale: dict) -> None:
    """打印单笔卖出摘要"""
    print_header("卖出记录已保存")
    print(f"  代码:     {sale['symbol']} {sale['name']}")
    print(f"  账户:     {sale['account']}")
    print(f"  股数:     {sale['shurns']:,}")
    print(f"  成交价:   {fmt_price(sale['price'], '¥')}")
    print(f"  成交额:   {fmt_cny(sale['gross'])}")
    print(f"  佣金:     {fmt_cny(sale['commission'])}")
    print(f"  印花税:   {fmt_cny(sale['stamp_tax'])}")
    print(f"  费用合计: {fmt_cny(sale['fees'])}")
    print(f"  净收入:   {fmt_cny(sale['net'])}")
    print(f"  日期:     {sale['date']}")
    print()


# ============================================================
# 命令处理
# ============================================================

def cmd_status(sales: list[dict]) -> None:
    """status命令: 显示还本进度概览 + 持仓清仓状态"""
    print_overview(sales)
    print_positions(sales)
    print()

    # 提示下一步
    gap = gap_to_target(sales)
    if gap > 0:
        print(f"  → 缺口 {fmt_cny(gap)}，运行 scenario <价格> 查看昆仑万维减仓方案")
    else:
        print(f"  → 已超额完成! 缺口 {fmt_cny(abs(gap))}")


def cmd_scenario(sales: list[dict], price_str: str) -> None:
    """scenario命令: 昆仑万维减仓情景分析"""
    try:
        price = float(price_str)
    except ValueError:
        print(f"错误: 价格参数无效 '{price_str}'，请输入数字")
        sys.exit(1)

    if price <= 0:
        print(f"错误: 价格必须大于0，当前值 {price}")
        sys.exit(1)

    print_overview(sales)
    print_scenario(sales, price)
    print()


def cmd_sell(sales: list[dict], symbol: str, price_str: str,
             account: str | None = None) -> list[dict]:
    """sell命令: 录入僵尸持仓实际卖出"""
    try:
        price = float(price_str)
    except ValueError:
        print(f"错误: 成交价参数无效 '{price_str}'，请输入数字")
        sys.exit(1)

    if price <= 0:
        print(f"错误: 成交价必须大于0，当前值 {price}")
        sys.exit(1)

    matches = find_positions(symbol)
    if not matches:
        print(f"错误: 代码 '{symbol}' 不在19个僵尸持仓中")
        known = sorted(set(p[0] for p in DEAD_POSITIONS))
        print(f"已知代码: {', '.join(known)}")
        sys.exit(1)

    # 处理多账户持有同一代码的情况
    if len(matches) > 1 and account is None:
        print(f"错误: 代码 '{symbol}' 存在于多个账户，请指定账户:")
        for m in matches:
            print(f"  sell {symbol} <价格> {m['account']}")
        sys.exit(1)

    pos = find_position(symbol, account)
    if pos is None:
        if account:
            print(f"错误: 代码 '{symbol}' 未在账户 '{account}' 中找到")
        sys.exit(1)

    # 检查是否已卖出 (使用复合键)
    pkey = _position_key(pos["symbol"], pos["account"])
    for s in sales:
        if _position_key(s["symbol"], s["account"]) == pkey:
            print(f"错误: {symbol} {pos['name']} ({pos['account']}) 已记录卖出")
            print(f"  成交价 ¥{s['price']:.2f}，净收入 {fmt_cny(s['net'])}")
            print(f"  先用 unsell {symbol} {pos['account']} 撤销后再重新录入")
            sys.exit(1)

    gross = price * pos["shares"]
    fees, commission, stamp_tax = calc_fees(gross)
    net = round(gross - fees, 2)

    sale = {
        "symbol": symbol,
        "name": pos["name"],
        "account": pos["account"],
        "market": pos["market"],
        "shurns": pos["shares"],
        "price": round(price, 4),
        "gross": round(gross, 2),
        "commission": round(commission, 2),
        "stamp_tax": round(stamp_tax, 2),
        "fees": round(fees, 2),
        "net": net,
        "date": str(date.today()),
    }

    sales.append(sale)
    save_sales(sales)

    print_sale_summary(sale)
    print_overview(sales)
    print()
    return sales


def cmd_unsell(sales: list[dict], symbol: str,
               account: str | None = None) -> list[dict]:
    """unsell命令: 撤销某笔卖出记录"""
    # 检查是否有多个账户的卖出记录
    matching = [s for s in sales if s["symbol"] == symbol]
    if not matching:
        print(f"错误: 未找到 '{symbol}' 的卖出记录")
        sys.exit(1)

    if len(matching) > 1 and account is None:
        print(f"错误: '{symbol}' 有多个账户的卖出记录，请指定账户:")
        for m in matching:
            print(f"  unsell {symbol} {m['account']}")
        sys.exit(1)

    pkey = _position_key(symbol, account) if account else _position_key(symbol, matching[0]["account"])
    for i, s in enumerate(sales):
        if _position_key(s["symbol"], s["account"]) == pkey:
            removed = sales.pop(i)
            save_sales(sales)
            print(f"已撤销 {removed['symbol']} {removed['name']} ({removed['account']}) 的卖出记录")
            print_overview(sales)
            print()
            return sales

    print(f"错误: 未找到 '{symbol}' 的卖出记录")
    sys.exit(1)


def cmd_reset() -> None:
    """reset命令: 清除所有卖出记录"""
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
        print("已清除所有卖出记录。")
    else:
        print("没有卖出记录，无需重置。")


# ============================================================
# 帮助信息
# ============================================================

HELP_TEXT = """
还本资金追踪计算器

命令:
  status                      显示当前还本进度 (概览 + 19个持仓清仓状态)
  scenario <昆仑万维价格>      昆仑万维减仓情景分析 (同时对比40/45/50三个价位)
  sell <代码> <成交价> [账户]  录入一笔僵尸持仓的实际卖出
  unsell <代码> [账户]         撤销某笔卖出记录
  reset                       清除所有卖出记录

示例:
  python3 debt_repayment_tracker.py status
  python3 debt_repayment_tracker.py scenario 42.5
  python3 debt_repayment_tracker.py sell 300142 14.0
  python3 debt_repayment_tracker.py sell 600050 4.50 信用账户
  python3 debt_repayment_tracker.py sell 00884 0.065
  python3 debt_repayment_tracker.py unsell 300142
  python3 debt_repayment_tracker.py unsell 600050 信用账户
  python3 debt_repayment_tracker.py reset

说明:
  - 19个僵尸持仓已预置，预期值按用户提供的~估算价格
  - 港币持仓(00884, 00390)单价为港币，预期总值已按0.92折算为人民币
  - 交易费用: 佣金万2.5(最低5元) + 印花税千1 (卖出单向)
  - 卖出记录保存在同目录 .debt_sales.json
  - 昆仑万维情景分析自动对比 40/45/50 三个价位
  - 若同一代码出现在多个账户(如600050)，需在sell/unsell时指定账户名
"""


def print_help() -> None:
    print(HELP_TEXT.strip())


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    cmd = sys.argv[1].lower()
    sales = load_sales()

    if cmd == "status":
        cmd_status(sales)

    elif cmd == "scenario":
        if len(sys.argv) < 3:
            print("用法: python3 debt_repayment_tracker.py scenario <昆仑万维价格>")
            print("示例: python3 debt_repayment_tracker.py scenario 42.5")
            sys.exit(1)
        cmd_scenario(sales, sys.argv[2])

    elif cmd == "sell":
        if len(sys.argv) < 4:
            print("用法: python3 debt_repayment_tracker.py sell <代码> <成交价> [账户]")
            print("示例: python3 debt_repayment_tracker.py sell 300142 14.0")
            print("      python3 debt_repayment_tracker.py sell 600050 4.50 信用账户")
            sys.exit(1)
        account = sys.argv[4] if len(sys.argv) >= 5 else None
        cmd_sell(sales, sys.argv[2], sys.argv[3], account)

    elif cmd == "unsell":
        if len(sys.argv) < 3:
            print("用法: python3 debt_repayment_tracker.py unsell <代码> [账户]")
            sys.exit(1)
        account = sys.argv[3] if len(sys.argv) >= 4 else None
        cmd_unsell(sales, sys.argv[2], account)

    elif cmd == "reset":
        cmd_reset()

    elif cmd in ("help", "-h", "--help"):
        print_help()

    else:
        print(f"未知命令: {cmd}")
        print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
