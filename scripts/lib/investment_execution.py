#!/usr/bin/env python3
"""投资执行系统 — 投资飞轮第5层

将"分析"转化为"行动"：实时持仓监控→风险阈值检查→执行信号生成→飞书推送今日操作。

用法:
  python3 scripts/lib/investment_execution.py --daily     # 推送到飞书
  python3 scripts/lib/investment_execution.py --dry-run   # 只打印不推送
  python3 scripts/lib/investment_execution.py --status    # 打印持仓快照
"""

import os, sys, json, time
from datetime import datetime, date
from pathlib import Path

# ─── 项目路径 ───
ROOT = Path(__file__).resolve().parent.parent.parent
STATE_FILE = ROOT / ".bridge" / "execution_state.json"

# ─── 持仓配置（仓位变动时修改此处）───
PORTFOLIO = {
    "300418_普通": {
        "symbol": "300418", "name": "昆仑万维", "market": "A",
        "shares": 10200, "cost": 53.50, "account": "普通",
        "target_shares": 3000,
        "stop_loss": None, "take_profit_start": None,
    },
    "300418_信用": {
        "symbol": "300418", "name": "昆仑万维(信用)", "market": "A",
        "shares": 6800, "cost": 57.25, "account": "信用",
        "target_shares": 0,
        "stop_loss": None, "take_profit_start": None,
    },
    "159715": {
        "symbol": "159715", "name": "稀土ETF", "market": "A",
        "shares": 45300, "cost": 1.47, "account": "普通",
        "target_shares": 45300,
        "stop_loss": None, "take_profit_start": None,
    },
    "300059": {
        "symbol": "300059", "name": "东方财富", "market": "A",
        "shares": 1300, "cost": 5.28, "account": "普通",
        "target_shares": 1300,
        "stop_loss": None, "take_profit_start": None,
    },
    "159206": {
        "symbol": "159206", "name": "卫星ETF", "market": "A",
        "shares": 4700, "cost": 2.11, "account": "普通",
        "target_shares": 4700,
        "stop_loss": None, "take_profit_start": None,
    },
    "09678_HK": {
        "symbol": "09678.HK", "name": "云知声", "market": "HK",
        "shares": 80, "cost": 262.0, "account": "港股",
        "target_shares": 80,
        "stop_loss": 240.0, "take_profit_start": 350.0,
    },
    "06030_HK": {
        "symbol": "06030.HK", "name": "中信证券", "market": "HK",
        "shares": 1000, "cost": 29.91, "account": "港股",
        "target_shares": 0,
        "stop_loss": 23.0, "take_profit_start": None,
    },
}

# ─── 风险参数 ───
CONCENTRATION_LIMIT = 0.40     # 单只股票上限40%
DEBT_TARGET = 600000           # 信用贷本金
DEBT_DUE_DATE = "2026-09-15"
MARGIN_CALL_PRICE = 37.2       # 昆仑万维追保线


# ══════════════════════════════════════════════════
# 状态持久化
# ══════════════════════════════════════════════════

def get_default_state() -> dict:
    return {
        "version": 2,
        "last_update": "",
        "total_assets_cny": 0,
        "debt": {
            "target": DEBT_TARGET,
            "raised_so_far": 0,
            "from_sell_orders": [],
            "from_savings": 0,
            "last_check_date": "",
        },
        "pending_orders": [],
        "executed_orders": [],
        "last_snapshot": {},
    }


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            d = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            if "version" in d:
                return d
        except (json.JSONDecodeError, KeyError):
            pass
    return get_default_state()


def save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


# ══════════════════════════════════════════════════
# 价格获取
# ══════════════════════════════════════════════════

def fetch_a_price(symbol: str):
    """获取A股实时价格"""
    try:
        import akshare as ak
        df = ak.stock_zh_a_spot_em()
        row = df[df["代码"] == symbol]
        if not row.empty:
            return float(row.iloc[0].get("最新价", 0) or 0)
    except Exception:
        pass
    return None


def fetch_hk_price(symbol: str):
    """获取港股实时价格"""
    try:
        import akshare as ak
        df = ak.stock_hk_spot_em()
        row = df[df["代码"] == symbol]
        if not row.empty:
            return float(row.iloc[0].get("最新价", 0) or 0)
    except Exception:
        pass
    return None


def fetch_prices() -> dict:
    """获取所有持仓的最新价格"""
    prices = {}
    for hid, cfg in PORTFOLIO.items():
        try:
            if cfg["market"] == "A":
                p = fetch_a_price(cfg["symbol"])
            elif cfg["market"] == "HK":
                p = fetch_hk_price(cfg["symbol"])
            else:
                p = None
            if p and p > 0:
                prices[hid] = p
        except Exception:
            pass

    # 从state读取上次价格作为fallback
    state = load_state()
    last_snap = state.get("last_snapshot", {})
    for hid in PORTFOLIO:
        if hid not in prices:
            cached = last_snap.get("holdings", {}).get(hid, {}).get("current_price", 0)
            if cached > 0:
                prices[hid] = cached

    return prices


# ══════════════════════════════════════════════════
# 持仓快照
# ══════════════════════════════════════════════════

def calc_snapshot(prices: dict) -> dict:
    """计算完整的持仓快照"""
    holdings = {}
    total = 0.0

    for hid, cfg in PORTFOLIO.items():
        price = prices.get(hid, 0)
        mv = cfg["shares"] * price
        cost_basis = cfg["shares"] * cfg["cost"]
        pnl = mv - cost_basis
        total += mv

        holdings[hid] = {
            "name": cfg["name"],
            "account": cfg["account"],
            "shares": cfg["shares"],
            "cost": cfg["cost"],
            "current_price": price,
            "market_value": round(mv, 2),
            "cost_basis": round(cost_basis, 2),
            "pnl": round(pnl, 2),
            "target_shares": cfg["target_shares"],
        }

    # 计算集中度
    for hid in holdings:
        mv = holdings[hid]["market_value"]
        holdings[hid]["weight_pct"] = round(mv / total * 100, 1) if total > 0 else 0

    # 找最大持仓
    sorted_h = sorted(holdings.values(), key=lambda x: x["market_value"], reverse=True)
    top = sorted_h[0] if sorted_h else {}

    return {
        "holdings": holdings,
        "total_value": round(total, 2),
        "top_holding_name": top.get("name", ""),
        "top_holding_pct": top.get("weight_pct", 0),
        "concentration_breach": top.get("weight_pct", 0) > CONCENTRATION_LIMIT * 100,
        "total_unrealized_pnl": round(sum(h["pnl"] for h in holdings.values()), 2),
    }


# ══════════════════════════════════════════════════
# 风险监控
# ══════════════════════════════════════════════════

def check_concentration(snapshot: dict) -> list[dict]:
    """检查集中度风险"""
    alerts = []
    for hid, h in snapshot["holdings"].items():
        pct = h["weight_pct"]
        if pct > CONCENTRATION_LIMIT * 100:
            to_sell = h["shares"] - h["target_shares"]
            est_value = to_sell * h["current_price"] if to_sell > 0 else 0
            alerts.append({
                "severity": "🔴" if pct > 60 else "⚠️",
                "holding_id": hid,
                "holding_name": h["name"],
                "actual_pct": pct,
                "limit_pct": CONCENTRATION_LIMIT * 100,
                "action": "sell",
                "to_sell_shares": to_sell if to_sell > 0 else 0,
                "est_value": round(est_value, 2),
                "reason": f"集中度{pct}% > {CONCENTRATION_LIMIT*100:.0f}%上限",
            })
    return alerts


def check_debt_timeline() -> dict:
    """检查还本进度"""
    state = load_state()
    debt = state.get("debt", {})
    raised = debt.get("raised_so_far", 0)
    gap = max(0, DEBT_TARGET - raised)

    try:
        due = datetime.strptime(DEBT_DUE_DATE, "%Y-%m-%d")
        days_left = (due - datetime.now()).days
    except Exception:
        days_left = 97  # fallback

    on_track = gap <= 0
    daily_rate = round(gap / max(days_left, 1)) if days_left > 0 else 0

    return {
        "target": DEBT_TARGET,
        "raised": raised,
        "gap": gap,
        "days_left": max(days_left, 0),
        "on_track": on_track,
        "daily_rate_needed": daily_rate,
        "urgency": "🔴" if days_left < 60 and gap > 0 else "⚠️" if gap > 0 else "✅",
    }


def check_triggers(prices: dict) -> list[dict]:
    """检查价格触发条件"""
    alerts = []
    for hid, cfg in PORTFOLIO.items():
        price = prices.get(hid, 0)
        name = cfg["name"]

        # 止损
        if cfg.get("stop_loss") and price > 0 and price <= cfg["stop_loss"]:
            alerts.append({
                "severity": "🔴",
                "holding_id": hid,
                "holding_name": name,
                "type": "stop_loss",
                "current": price,
                "trigger": cfg["stop_loss"],
                "action": "立即卖出",
                "reason": f"{name}触发止损线{cfg['stop_loss']}",
            })

        # 止盈
        if cfg.get("take_profit_start") and price > 0 and price >= cfg["take_profit_start"]:
            alerts.append({
                "severity": "🟡",
                "holding_id": hid,
                "holding_name": name,
                "type": "take_profit",
                "current": price,
                "trigger": cfg["take_profit_start"],
                "action": "考虑分批止盈",
                "reason": f"{name}达到止盈观察区{cfg['take_profit_start']}",
            })

        # 追保
        if hid == "300418_信用" and price > 0 and price < MARGIN_CALL_PRICE:
            alerts.append({
                "severity": "🔴",
                "holding_id": hid,
                "holding_name": "昆仑万维(信用)",
                "type": "margin_call",
                "current": price,
                "trigger": MARGIN_CALL_PRICE,
                "action": "强制平仓风险",
                "reason": f"昆仑万维{price}跌破追保线{MARGIN_CALL_PRICE}",
            })

    return alerts


# ══════════════════════════════════════════════════
# 执行信号生成
# ══════════════════════════════════════════════════

def generate_signals(snapshot: dict, risk_alerts: list, debt_info: dict) -> list[dict]:
    """生成今日执行信号"""
    orders = []

    # P0: 集中度超标 → 卖出
    for a in risk_alerts:
        if a.get("action") == "sell":
            orders.append({
                "priority": "P0",
                "action": "sell",
                "holding_id": a["holding_id"],
                "holding_name": a["holding_name"],
                "shares": a["to_sell_shares"],
                "order_type": "limit",
                "limit_price": None,
                "estimated_value": a["est_value"],
                "reason": a["reason"],
            })

    # P0: 债务紧急
    if debt_info.get("urgency") == "🔴":
        orders.append({
            "priority": "P0",
            "action": "fund",
            "holding_name": None,
            "reason": f"距还本仅{debt_info['days_left']}天，缺口¥{debt_info['gap']:,.0f}",
            "estimated_value": debt_info["gap"],
        })

    # P1: 止损触发
    for a in risk_alerts:
        if a.get("type") in ("stop_loss", "margin_call"):
            orders.append({
                "priority": "P1",
                "action": "sell_urgent",
                "holding_id": a["holding_id"],
                "holding_name": a["holding_name"],
                "reason": a["reason"],
            })

    # P1: 价格信号检查
    for hid, cfg in PORTFOLIO.items():
        if cfg["market"] == "HK" and cfg.get("stop_loss"):
            price = snapshot["holdings"].get(hid, {}).get("current_price", 0)
            if price > 0:
                dist = (price - cfg["stop_loss"]) / cfg["stop_loss"]
                if dist < 0.1:  # 距离止损线不到10%
                    orders.append({
                        "priority": "P1",
                        "action": "monitor",
                        "holding_id": hid,
                        "holding_name": cfg["name"],
                        "reason": f"距止损仅{dist*100:.0f}%（现价{price}，止损{cfg['stop_loss']}）",
                    })

    # 排序：P0在前
    orders.sort(key=lambda o: (0 if o["priority"] == "P0" else 1))
    return orders


# ══════════════════════════════════════════════════
# 格式化与推送
# ══════════════════════════════════════════════════

def build_daily_text(snapshot: dict, alerts: list, debt_info: dict, orders: list[dict]) -> str:
    """生成今日操作订单文本"""
    today = date.today().isoformat()
    lines = []
    lines.append(f"📋 今日操作订单 | {today}")
    lines.append("")

    # P0
    p0 = [o for o in orders if o["priority"] == "P0"]
    if p0:
        lines.append("🔴 P0 — 必须执行:")
        for o in p0:
            if o["action"] == "sell":
                lines.append(f"  ① 卖出 {o['holding_name']} {o['shares']}股")
                lines.append(f"     委托: 限价单 @ 市价附近")
                lines.append(f"     预估回笼: ¥{o['estimated_value']:,.0f}")
                lines.append(f"     理由: {o['reason']}")
            elif o["action"] == "fund":
                lines.append(f"  ① 资金缺口: ¥{o['estimated_value']:,.0f}")
                lines.append(f"     理由: {o['reason']}")
        lines.append("")

    # P1
    p1 = [o for o in orders if o["priority"] == "P1"]
    if p1:
        lines.append("⚠️ P1 — 监控待命:")
        for o in p1:
            lines.append(f"  • {o['holding_name']}: {o['reason']}")
        lines.append("")

    # 持仓快照
    total = snapshot["total_value"]
    top_name = snapshot["top_holding_name"]
    top_pct = snapshot["top_holding_pct"]
    lines.append("📊 持仓快照:")
    lines.append(f"  总市值: ¥{total:,.0f}  |  {top_name}占比: {top_pct}%"
                 f"{'🔴' if snapshot['concentration_breach'] else '✅'}")
    lines.append(f"  未实现盈亏: ¥{snapshot['total_unrealized_pnl']:+,.0f}")
    lines.append(f"  距9月到期: {debt_info['days_left']}天")
    lines.append("")

    # 还本进度
    pct = round(debt_info["raised"] / debt_info["target"] * 100, 1) if debt_info["target"] > 0 else 0
    bar_len = 20
    filled = int(bar_len * pct / 100)
    bar = "█" * filled + "░" * (bar_len - filled)
    lines.append(f"💰 还本进度:")
    lines.append(f"  {bar} ¥{debt_info['raised']:,.0f}/¥{debt_info['target']:,.0f} ({pct}%)")
    lines.append(f"  还差 ¥{debt_info['gap']:,.0f} | 日均需筹 ¥{debt_info['daily_rate_needed']:,}")
    lines.append(f"  状态: {debt_info['urgency']}")
    lines.append("")
    lines.append(f"上次更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    return "\n".join(lines)


def push_to_feishu(title: str, text: str) -> bool:
    """推送到飞书群"""
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        from lib.feishu_push import push
        ok, msg = push(title, text)
        return ok
    except Exception as e:
        print(f"  推送失败: {e}")
        return False


def assess_执行(snapshot: dict = None, orders: list = None) -> dict:
    """第5层评估：执行系统健康度（供飞轮调用）"""
    if not snapshot or not orders:
        # 独立运行
        prices = fetch_prices()
        snapshot = calc_snapshot(prices)
        alerts_conc = check_concentration(snapshot)
        debt_info = check_debt_timeline()
        alerts_trig = check_triggers(prices)
        orders = generate_signals(snapshot, alerts_conc + alerts_trig, debt_info)

    p0_count = len([o for o in orders if o["priority"] == "P0"])
    p1_count = len([o for o in orders if o["priority"] == "P1"])

    signals = [f"✅ 总市值 ¥{snapshot['total_value']:,.0f}"]
    gaps = []

    if snapshot["concentration_breach"]:
        gaps.append(f"🔴 集中度 {snapshot['top_holding_pct']}% > 40%上限")
    if p0_count > 0:
        gaps.append(f"🔴 {p0_count}项P0待执行")
    if p1_count > 0:
        gaps.append(f"⚠️ {p1_count}项P1监控中")

    if not gaps:
        level = "正常"
        gaps.append("一切正常")
    elif p0_count > 0:
        level = "有行动待办"
    else:
        level = "有缺口"

    return {"level": level, "signals": signals, "gaps": gaps, "orders": orders}


# ══════════════════════════════════════════════════
# 主入口
# ══════════════════════════════════════════════════

def run_daily(dry_run: bool = False) -> bool:
    """每日执行主流程"""
    print(f"\n🔍 投资执行系统 | {date.today()}")

    # 1. 获取价格
    print("  获取实时价格...")
    prices = fetch_prices()
    for hid, p in prices.items():
        print(f"    {hid}: ¥{p}")
    if not prices:
        print("  ❌ 无法获取价格数据")

    # 2. 计算快照
    snapshot = calc_snapshot(prices)

    # 3. 风险监控
    alerts_conc = check_concentration(snapshot)
    debt_info = check_debt_timeline()
    alerts_trig = check_triggers(prices)

    # 4. 生成信号
    orders = generate_signals(snapshot, alerts_conc + alerts_trig, debt_info)

    # 5. 保存状态
    state = load_state()
    state["last_update"] = datetime.now().isoformat()
    state["total_assets_cny"] = snapshot["total_value"]
    state["last_snapshot"] = snapshot
    state["pending_orders"] = orders
    save_state(state)

    # 6. 输出
    text = build_daily_text(snapshot, alerts_conc + alerts_trig, debt_info, orders)
    print("\n" + text)

    if dry_run:
        print("\n⚠️ Dry-run模式，未推送")
        return True

    # 7. 推送到飞书
    title = f"📋 投资执行 | {date.today()}"
    ok = push_to_feishu(title, text)
    if ok:
        print(f"\n✅ 已推送到飞书群")
    else:
        print(f"\n❌ 推送失败")
    return ok


def show_status():
    """打印持仓状态"""
    state = load_state()
    prices = fetch_prices()
    snapshot = calc_snapshot(prices)
    alerts_conc = check_concentration(snapshot)
    debt_info = check_debt_timeline()
    print(build_daily_text(snapshot, alerts_conc, debt_info, []))


# ══════════════════════════════════════════════════
# 模块A：新投资机会建议
# ══════════════════════════════════════════════════

OPPORTUNITY_CRITERIA = {
    "PE_max": 20,
    "ROE_min": 10,
    "revenue_growth_min": 5,
    "debt_ratio_max": 60,
}


def scan_opportunities(max_stocks: int = 30) -> list[dict]:
    """扫描A股，筛选符合投资条件的标的

    用法:
      python3 scripts/lib/investment_execution.py --scan
    """
    print(f"\n🔍 扫描投资机会（筛选条件：PE≤{OPPORTUNITY_CRITERIA['PE_max']}，"
          f"ROE≥{OPPORTUNITY_CRITERIA['ROE_min']}%，"
          f"营收增速≥{OPPORTUNITY_CRITERIA['revenue_growth_min']}%...）")
    candidates = []

    try:
        import akshare as ak
        df = ak.stock_zh_a_spot_em()
        df = df[~df["名称"].str.contains("ST|退|N", na=False)]
        df = df.sort_values("总市值", ascending=False).head(max_stocks * 3)

        count = 0
        for _, row in df.iterrows():
            symbol = row["代码"]
            name = row["名称"]
            price = float(row.get("最新价", 0) or 0)
            pe = float(row.get("市盈率-动态", 0) or 0)

            if pe <= 0 or pe > OPPORTUNITY_CRITERIA["PE_max"]:
                continue

            try:
                fin = ak.stock_financial_analysis_indicator(symbol=symbol, start_year="2025")
                if fin.empty:
                    continue
                latest = fin.iloc[-1]
                roe = float(latest.get("净资产收益率(%)", 0) or 0)
                rev_growth = float(latest.get("主营业务收入增长率(%)", 0) or 0)
                debt_ratio = float(latest.get("资产负债率(%)", 0) or 0)
            except Exception:
                continue

            if roe < OPPORTUNITY_CRITERIA["ROE_min"]:
                continue
            if rev_growth < OPPORTUNITY_CRITERIA["revenue_growth_min"]:
                continue
            if debt_ratio > OPPORTUNITY_CRITERIA["debt_ratio_max"]:
                continue

            candidates.append({
                "symbol": symbol, "name": name, "price": price,
                "PE": round(pe, 1), "ROE": round(roe, 1),
                "营收增速": round(rev_growth, 1),
                "资产负债率": round(debt_ratio, 1),
                "score": round(roe * 0.4 + rev_growth * 0.3 + (1 / pe) * 100 * 0.3, 1),
            })
            count += 1
            if count >= max_stocks:
                break
    except Exception as e:
        print(f"  ❌ 扫描失败: {e}")
        return []

    candidates.sort(key=lambda x: x["score"], reverse=True)
    print(f"  ✅ 筛选出 {len(candidates)} 个标的")
    return candidates


def print_opportunities(candidates: list[dict], top_n: int = 10):
    if not candidates:
        print("  ⚠️ 未找到符合条件的标的")
        return
    print(f"\n📈 Top {top_n} 投资机会（综合评分）:")
    h = f"{'排名':>4} {'代码':>8} {'名称':<10} {'PE':>6} {'ROE':>6} {'营收增速':>8} {'负债率':>6} {'评分':>6}"
    print(h)
    print("-" * len(h))
    for i, c in enumerate(candidates[:top_n]):
        print(f"{i+1:>4} {c['symbol']:>8} {c['name']:<10} "
              f"{c['PE']:>6.1f} {c['ROE']:>6.1f}% {c['营收增速']:>7.1f}% "
              f"{c['资产负债率']:>5.1f}% {c['score']:>6.1f}")


# ══════════════════════════════════════════════════
# 模块B：模拟投资（纸上交易）
# ══════════════════════════════════════════════════

SIMULATED_FILE = ROOT / ".bridge" / "simulated_trades.json"


def load_simulated() -> list[dict]:
    if SIMULATED_FILE.exists():
        try:
            return json.loads(SIMULATED_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def save_simulated(trades: list[dict]):
    SIMULATED_FILE.parent.mkdir(parents=True, exist_ok=True)
    SIMULATED_FILE.write_text(json.dumps(trades, ensure_ascii=False, indent=2), encoding="utf-8")


def add_simulated_trade(action: str, symbol: str, name: str,
                        shares: int, price: float, reason: str = ""):
    trades = load_simulated()
    trade = {
        "id": f"SIM-{len(trades)+1:04d}", "date": date.today().isoformat(),
        "action": action, "symbol": symbol, "name": name,
        "shares": shares, "price": price,
        "value": round(shares * price, 2), "reason": reason,
        "status": "open" if action == "buy" else "closed",
    }
    trades.append(trade)
    save_simulated(trades)
    print(f"✅ 模拟{action}：{name} {shares}股 @ ¥{price}")
    return trade


def report_simulated():
    trades = load_simulated()
    if not trades:
        print("📭 无模拟交易记录")
        return
    print(f"\n📊 模拟投资报告（共{len(trades)}笔）")
    h = f"{'ID':>8} {'日期':<12} {'操作':<6} {'名称':<10} {'数量':>6} {'价格':>8} {'金额':>10} {'状态':<8}"
    print(h)
    print("-" * 75)
    total_buy = total_sell = 0
    for t in trades:
        s = f"{t['id']:>8} {t['date']:<12} {t['action']:<6} "
        s += f"{t.get('name','')[:8]:<10} {t['shares']:>6} ¥{t['price']:>6.2f} ¥{t['value']:>8,.0f} {t['status']:<8}"
        print(s)
        total_buy += t['value'] if t['action'] == 'buy' else 0
        total_sell += t['value'] if t['action'] == 'sell' else 0
    net = total_sell - total_buy
    print(f"\n  总买入: ¥{total_buy:,.0f}  总卖出: ¥{total_sell:,.0f}  模拟盈亏: ¥{net:+,.0f}")


# ══════════════════════════════════════════════════
# 模块C：回检模块
# ══════════════════════════════════════════════════

def review_decision(symbol: str, decision_price: float, decision_date: str,
                    action: str, current_price: float = None):
    """回检单个投资决策"""
    if not current_price:
        prices = fetch_prices()
        current_price = next((prices[hid] for hid, cfg in PORTFOLIO.items()
                             if cfg["symbol"] == symbol and prices.get(hid)), 0)
        if not current_price:
            print("  ❌ 无法获取当前价格")
            return

    change = (current_price - decision_price) / decision_price * 100
    verdict = "—"
    if action == "buy":
        verdict = "✅ 正确" if change > 0 else "❌ 错误" if change < -5 else "⏳ 待观察"
    elif action == "sell":
        verdict = "✅ 正确" if change < 0 else "❌ 错误" if change > 5 else "⏳ 待观察"

    print(f"\n📋 决策回检 | {symbol}")
    print(f"  决策日期: {decision_date}")
    print(f"  决策价格: ¥{decision_price}")
    print(f"  决策动作: {action}")
    print(f"  当前价格: ¥{current_price:.2f}")
    print(f"  价格变动: {change:+.1f}%")
    print(f"  判断: {verdict}")


def review_backlog():
    """回检历史待执行决策"""
    state = load_state()
    orders = state.get("pending_orders", [])
    if not orders:
        print("📭 无待回检决策")
        return
    print(f"\n🔍 待执行决策回检（{len(orders)}项）")
    for o in orders:
        hid = o.get("holding_id", "")
        cfg = PORTFOLIO.get(hid, {})
        if cfg and o.get("action") == "sell":
            review_decision(
                symbol=cfg["symbol"],
                decision_price=cfg["cost"],
                decision_date=state.get("last_update", "?"),
                action="sell",
            )


def main():
    if "--daily" in sys.argv:
        run_daily(dry_run="--dry-run" in sys.argv)
    elif "--status" in sys.argv:
        show_status()
    elif "--scan" in sys.argv:
        candidates = scan_opportunities()
        print_opportunities(candidates)
    elif "--sim-report" in sys.argv:
        report_simulated()
    elif "--sim-buy" in sys.argv:
        # usage: --sim-buy SYMBOL SHARES PRICE NAME
        s = sys.argv[2:6] if len(sys.argv) >= 6 else []
        if len(s) >= 4:
            add_simulated_trade("buy", s[0], s[3], int(s[1]), float(s[2]))
    elif "--sim-sell" in sys.argv:
        s = sys.argv[2:6] if len(sys.argv) >= 6 else []
        if len(s) >= 4:
            add_simulated_trade("sell", s[0], s[3], int(s[1]), float(s[2]))
    elif "--review" in sys.argv:
        # usage: --review SYMBOL PRICE DATE action
        s = sys.argv[2:6] if len(sys.argv) >= 6 else []
        if len(s) >= 4:
            review_decision(s[0], float(s[1]), s[2], s[3])
    elif "--review-all" in sys.argv:
        review_backlog()
    elif "--dry-run" in sys.argv:
        run_daily(dry_run=True)
    else:
        assess_执行()


if __name__ == "__main__":
    main()
