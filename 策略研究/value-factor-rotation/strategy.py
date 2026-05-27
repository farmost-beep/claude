"""
低换手价值因子轮动策略
严格翻译自 STRATEGY_DESIGN.md，不可自由发挥。

策略: 季度末对科技标的池多因子评分，选前N只等权配置
因子: E/P(30%), B/P(20%), ROE(25%), RevGrowth(15%), 6M_Momentum(10%)
风控: 单票≤15%, 总仓位≤80%, 回撤熔断20%, 单票止损15%
"""

import numpy as np
import pandas as pd
from pathlib import Path


# ═══════════════════════════════════════════════════════
# 指标计算
# ═══════════════════════════════════════════════════════

def compute_zscore(series: pd.Series) -> pd.Series:
    """截面Z-score标准化（指标6的组件）"""
    mean_val = series.mean()
    std_val = series.std(ddof=1)
    if std_val == 0 or np.isnan(std_val):
        return pd.Series(0.0, index=series.index)
    return (series - mean_val) / std_val


def compute_factor_scores(fundamentals: pd.DataFrame) -> pd.Series:
    """
    计算综合因子评分（指标6）
    Score = 0.30×Z(1/PE) + 0.20×Z(1/PB) + 0.25×Z(ROE) + 0.15×Z(RevGrowth) + 0.10×Z(Momentum)
    """
    df = fundamentals.copy()

    # 指标1: E/P = 1/PE_TTM
    df['ep'] = 1.0 / df['PE_TTM'].replace(0, np.nan)

    # 指标2: B/P = 1/PB_LF
    df['bp'] = 1.0 / df['PB_LF'].replace(0, np.nan)

    # 指标3: ROE
    df['roe'] = df['ROE_TTM']

    # 指标4: 营收增长率
    df['rev_growth'] = df['revenue_growth_yoy']

    # 指标5: 6个月动量
    df['momentum'] = df.get('momentum_6m', 0)

    # Z-score 标准化
    df['Z_ep'] = compute_zscore(df['ep'])
    df['Z_bp'] = compute_zscore(df['bp'])
    df['Z_roe'] = compute_zscore(df['roe'])
    df['Z_rev'] = compute_zscore(df['rev_growth'])
    df['Z_mom'] = compute_zscore(df['momentum'])

    # 加权综合
    df['composite'] = (
        0.30 * df['Z_ep']
        + 0.20 * df['Z_bp']
        + 0.25 * df['Z_roe']
        + 0.15 * df['Z_rev']
        + 0.10 * df['Z_mom']
    )

    return df['composite']


def filter_universe(stock_data: dict, date) -> list:
    """准入过滤（3.1节）：PE>0, PB>0"""
    qualified = []
    for code, df in stock_data.items():
        if date not in df.index:
            continue
        row = df.loc[date]
        if row['PE_TTM'] <= 0:
            continue
        if row['PB_LF'] <= 0:
            continue
        qualified.append(code)
    return qualified


# ═══════════════════════════════════════════════════════
# 主回测入口
# ═══════════════════════════════════════════════════════

def run_backtest(config: dict) -> dict:
    """
    主回测入口。按 STRATEGY_DESIGN.md 逐条翻译。
    """
    # ── 参数提取 ──
    initial_cash = float(config.get("initial_cash", 1_000_000))
    start_date = config.get("start_date", "2021-01-01")
    end_date = config.get("end_date", "2025-12-31")

    selection = config.get("selection", {})
    top_n = selection.get("top_n", 10)
    buffer_n = selection.get("buffer_n", 5)
    rebalance_months = selection.get("rebalance_months", [3, 6, 9, 12])

    risk_cfg = config.get("risk", {})
    total_position_pct = risk_cfg.get("total_position_pct", 80) / 100.0
    single_stock_pct = risk_cfg.get("single_stock_pct", 15) / 100.0
    stop_loss_pct = risk_cfg.get("stop_loss_pct", 15) / 100.0
    drawdown_meltdown_pct = risk_cfg.get("drawdown_meltdown_pct", 20) / 100.0
    max_consecutive_stops = risk_cfg.get("max_consecutive_stops", 3)
    extreme_drop_pct = risk_cfg.get("extreme_drop_pct", 8) / 100.0

    commission_rate = config.get("commission", 0.00025)
    stamp_tax = config.get("stamp_tax", 0.001)
    slippage = config.get("slippage", 0.001)

    # ── 生成模拟科技股数据 ──
    np.random.seed(42)
    dates = pd.bdate_range(start_date, end_date)

    # 创建20只模拟A股科技股
    stock_codes = [
        "TECH_A_300750",  # 新能源科技
        "TECH_A_002415",  # 安防科技
        "TECH_A_688981",  # 半导体
        "TECH_A_688111",  # 办公软件
        "TECH_A_002230",  # AI语音
        "TECH_A_688012",  # 半导体设备
        "TECH_A_300124",  # 工业自动化
        "TECH_A_002049",  # 芯片设计
        "TECH_A_688036",  # 手机
        "TECH_A_688008",  # 芯片互联
        "TECH_A_300782",  # 射频芯片
        "TECH_A_688256",  # AI芯片
        "TECH_A_002920",  # 汽车电子
        "TECH_A_603501",  # 芯片设计2
        "TECH_A_688561",  # 网络安全
        "TECH_A_300661",  # 模拟芯片
        "TECH_A_688536",  # 模拟芯片2
        "TECH_A_300474",  # GPU
        "TECH_A_688126",  # 硅片
        "TECH_A_688065",  # 生物合成
    ]

    # 为每只股票生成真实感的价格和因子数据
    stocks_data = {}
    for i, code in enumerate(stock_codes):
        # 随机种子（确保可复现）
        rng = np.random.RandomState(100 + i)

        # 价格路径：带漂移的几何布朗运动
        drift = rng.uniform(0.03, 0.13) / 252  # 年化3%-13%
        vol = rng.uniform(0.20, 0.40) / np.sqrt(252)
        daily_returns = rng.normal(drift, vol, len(dates))

        # 加入一些市场级别的波动（模拟2022年熊市、2024年牛市）
        market_factor = np.zeros(len(dates))
        for j, d in enumerate(dates):
            if d.year == 2022:
                market_factor[j] = -0.0005  # 2022年熊市
            elif d.year == 2024 and d.month >= 9:
                market_factor[j] = 0.0015  # 2024年9月后牛市
            elif d.year == 2025 and d.month <= 3:
                market_factor[j] = 0.0008

        combined_returns = daily_returns + market_factor + rng.normal(0, 0.0003, len(dates))
        prices = 50.0 * np.exp(np.cumsum(combined_returns))

        # 设置PE/PB/ROE等基本面因子（与价格弱相关，模拟真实世界的价值发现过程）
        base_pe = rng.uniform(12, 35)
        base_pb = rng.uniform(1.2, 4.5)
        base_roe = rng.uniform(0.05, 0.25)
        base_rev_growth = rng.uniform(0.02, 0.25)

        df = pd.DataFrame({
            'open': prices * (1 + rng.normal(0, 0.003, len(dates))),
            'high': prices * (1 + abs(rng.normal(0, 0.008, len(dates)))),
            'low': prices * (1 - abs(rng.normal(0, 0.008, len(dates)))),
            'close': prices,
            'volume': rng.randint(5000000, 80000000, len(dates)),
            'PE_TTM': np.clip(base_pe + rng.normal(0, 0.05, len(dates)).cumsum() * 0.1 + rng.normal(0, 2, len(dates)), 3, 80),
            'PB_LF': np.clip(base_pb + rng.normal(0, 0.01, len(dates)).cumsum() * 0.05 + rng.normal(0, 0.3, len(dates)), 0.3, 8),
            'ROE_TTM': np.clip(base_roe + rng.normal(0, 0.001, len(dates)).cumsum() * 0.01 + rng.normal(0, 0.02, len(dates)), 0.01, 0.40),
            'revenue_growth_yoy': np.clip(base_rev_growth + rng.normal(0, 0.001, len(dates)).cumsum() * 0.005 + rng.normal(0, 0.05, len(dates)), -0.15, 0.50),
            'momentum_6m': np.zeros(len(dates)),
            'avg_daily_volume': rng.uniform(15_000_000, 60_000_000),
            'days_listed': rng.randint(400, 2500),
        }, index=dates)

        # 计算6个月动量（滚动126日）
        df['momentum_6m'] = df['close'].pct_change(126).fillna(0)

        stocks_data[code] = df

    # ── 找出季度调仓日期 ──
    rebalance_dates = set()
    for d in dates:
        if d.month in rebalance_months:
            # 找该月最后一个交易日
            month_end_dates = [x for x in dates if x.year == d.year and x.month == d.month]
            if month_end_dates and d == month_end_dates[-1]:
                rebalance_dates.add(d)

    # ── 初始化状态 ──
    cash = initial_cash
    holdings = {}       # {code: {"shares": N, "cost_price": P, "buy_date": D}}
    daily_values = []
    trades = []
    peak_value = initial_cash
    consecutive_stops = 0
    meltdown_active = False
    paused_stocks = set()
    meltdown_recovery_threshold = 0  # 回撤恢复到此百分比以下才解除熔断

    # ── 每日主循环 ──
    for date_idx, date in enumerate(dates):
        # ── 计算当前持仓市值和总资产 ──
        total_position_market_value = 0.0
        for code, h in list(holdings.items()):
            if date in stocks_data[code].index:
                close_p = float(stocks_data[code].loc[date, 'close'])
                total_position_market_value += h['shares'] * close_p

        total_value = cash + total_position_market_value

        # ── 更新峰值 ──
        if total_value > peak_value:
            peak_value = total_value
            if meltdown_active:
                current_dd = (peak_value - total_value) / peak_value
                if current_dd < meltdown_recovery_threshold:
                    meltdown_active = False
                    consecutive_stops = 0

        daily_values.append({
            'date': str(date.date()),
            'value': round(total_value, 2),
        })

        # ── 每日风控：极端行情检测（规则4）──
        if date_idx > 0:
            for code in list(holdings.keys()):
                if code in paused_stocks:
                    continue
                if date not in stocks_data[code].index:
                    continue
                prev_row = stocks_data[code].iloc[date_idx - 1]
                curr_close = float(stocks_data[code].loc[date, 'close'])
                prev_close = float(prev_row['close'])
                if prev_close > 0:
                    day_drop = (curr_close - prev_close) / prev_close
                    if day_drop < -extreme_drop_pct:
                        paused_stocks.add(code)

        # ── 每日风控：单票止损（规则1）──
        for code in list(holdings.keys()):
            if code in paused_stocks:
                continue
            if date not in stocks_data[code].index:
                continue
            h = holdings[code]
            current_price = float(stocks_data[code].loc[date, 'close'])
            loss_pct = (current_price - h['cost_price']) / h['cost_price']
            if loss_pct < -stop_loss_pct:
                # 执行止损
                sell_price = current_price * (1 - slippage)
                sell_amount = h['shares'] * sell_price
                comm_cost = sell_amount * commission_rate
                stamp_cost = sell_amount * stamp_tax
                cash += sell_amount - comm_cost - stamp_cost
                pnl = (sell_price - h['cost_price']) * h['shares'] - comm_cost - stamp_cost
                trades.append({
                    'date': str(date.date()), 'symbol': code,
                    'action': 'SELL', 'shares': h['shares'],
                    'price': round(sell_price, 2), 'reason': '止损',
                    'pnl': round(float(pnl), 2),
                })
                if pnl < 0:
                    consecutive_stops += 1
                else:
                    consecutive_stops = 0
                del holdings[code]

        # ── 每日风控：回撤熔断（规则2）──
        if peak_value > 0:
            drawdown = (peak_value - total_value) / peak_value
            if drawdown >= drawdown_meltdown_pct and not meltdown_active:
                meltdown_active = True
                meltdown_recovery_threshold = drawdown_meltdown_pct * 0.5
                # 清仓50%（按持仓数量）
                sorted_holdings = list(holdings.keys())
                to_keep = sorted_holdings[:max(1, len(sorted_holdings) // 2)]
                for code in list(holdings.keys()):
                    if code not in to_keep:
                        h = holdings[code]
                        if date in stocks_data[code].index:
                            current_price = float(stocks_data[code].loc[date, 'close'])
                        else:
                            current_price = h['cost_price']
                        sell_price = current_price * (1 - slippage)
                        sell_amount = h['shares'] * sell_price
                        comm_cost = sell_amount * commission_rate
                        stamp_cost = sell_amount * stamp_tax
                        cash += sell_amount - comm_cost - stamp_cost
                        pnl = (sell_price - h['cost_price']) * h['shares'] - comm_cost - stamp_cost
                        trades.append({
                            'date': str(date.date()), 'symbol': code,
                            'action': 'SELL', 'shares': h['shares'],
                            'price': round(sell_price, 2), 'reason': '熔断',
                            'pnl': round(float(pnl), 2),
                        })
                        del holdings[code]

        # ── 季度调仓（仅调仓日执行）──
        if date in rebalance_dates and not meltdown_active:
            # 连续止损降仓（规则3）
            position_multiplier = 0.5 if consecutive_stops >= max_consecutive_stops else 1.0

            # 准入过滤
            qualified = filter_universe(stocks_data, date)
            if len(qualified) < top_n:
                # 不够N只，全选
                selected = qualified
            else:
                # 构建基本面DataFrame
                fund_data = {}
                for code in qualified:
                    row = stocks_data[code].loc[date]
                    fund_data[code] = {
                        'PE_TTM': float(row['PE_TTM']),
                        'PB_LF': float(row['PB_LF']),
                        'ROE_TTM': float(row['ROE_TTM']),
                        'revenue_growth_yoy': float(row['revenue_growth_yoy']),
                        'momentum_6m': float(row['momentum_6m']),
                    }
                df_fund = pd.DataFrame(fund_data).T

                # 综合评分
                composite_scores = compute_factor_scores(df_fund)

                # 选前N
                selected = composite_scores.nlargest(min(top_n, len(composite_scores))).index.tolist()

            # ── 卖出不在选股范围的持仓（条件1: 调仓退出）──
            sell_threshold = top_n + buffer_n
            for code in list(holdings.keys()):
                if code in paused_stocks:
                    continue
                # 计算当前持有股票的评分排名
                qualified_all = filter_universe(stocks_data, date)
                if len(qualified_all) >= sell_threshold:
                    fund_data_all = {}
                    for c in qualified_all:
                        row = stocks_data[c].loc[date]
                        fund_data_all[c] = {
                            'PE_TTM': float(row['PE_TTM']),
                            'PB_LF': float(row['PB_LF']),
                            'ROE_TTM': float(row['ROE_TTM']),
                            'revenue_growth_yoy': float(row['revenue_growth_yoy']),
                            'momentum_6m': float(row['momentum_6m']),
                        }
                    df_fund_all = pd.DataFrame(fund_data_all).T
                    scores_all = compute_factor_scores(df_fund_all)
                    rank = scores_all.rank(ascending=False)
                    stock_rank = rank.get(code, 0)
                    if stock_rank > sell_threshold:
                        # 评分跌出前(top_n+buffer_n)，卖出
                        h = holdings[code]
                        current_price = float(stocks_data[code].loc[date, 'close'])
                        sell_price = current_price * (1 - slippage)
                        sell_amount = h['shares'] * sell_price
                        comm_cost = sell_amount * commission_rate
                        stamp_cost = sell_amount * stamp_tax
                        cash += sell_amount - comm_cost - stamp_cost
                        pnl = (sell_price - h['cost_price']) * h['shares'] - comm_cost - stamp_cost
                        trades.append({
                            'date': str(date.date()), 'symbol': code,
                            'action': 'SELL', 'shares': h['shares'],
                            'price': round(sell_price, 2), 'reason': '调仓退出',
                            'pnl': round(float(pnl), 2),
                        })
                        if pnl < 0:
                            consecutive_stops += 1
                        else:
                            consecutive_stops = 0
                        del holdings[code]

            # ── 买入/调仓：等权配置 ──
            # 重新计算总资产
            pos_val = sum(
                holdings[c]['shares'] * float(stocks_data[c].loc[date, 'close'])
                for c in holdings if date in stocks_data[c].index
            )
            current_total_value = cash + pos_val

            target_total_position = current_total_value * total_position_pct * position_multiplier
            target_per_stock_value = min(
                target_total_position / len(selected),
                current_total_value * single_stock_pct
            )

            for code in selected:
                if code in paused_stocks:
                    continue
                if date not in stocks_data[code].index:
                    continue

                current_price = float(stocks_data[code].loc[date, 'close'])

                # 当前持有
                current_shares = holdings.get(code, {}).get('shares', 0)
                current_value = current_shares * current_price

                # 需要调整的金额
                diff_value = target_per_stock_value - current_value

                if diff_value > 0 and cash > 0:
                    # 买入
                    buy_price = current_price * (1 + slippage)
                    shares_to_buy = int(min(diff_value, cash) / buy_price / 100) * 100
                    if shares_to_buy <= 0:
                        continue
                    cost = shares_to_buy * buy_price
                    comm_cost = cost * commission_rate
                    total_cost = cost + comm_cost
                    if total_cost > cash:
                        # 不够钱了，按可用现金调整
                        shares_to_buy = int(cash * 0.99 / buy_price / 100) * 100
                        if shares_to_buy <= 0:
                            continue
                        cost = shares_to_buy * buy_price
                        comm_cost = cost * commission_rate
                        total_cost = cost + comm_cost

                    cash -= total_cost
                    if code in holdings:
                        # 增持：更新平均成本
                        old_shares = holdings[code]['shares']
                        old_cost = holdings[code]['cost_price']
                        total_shares = old_shares + shares_to_buy
                        avg_cost = (old_shares * old_cost + total_cost) / total_shares
                        holdings[code]['shares'] = total_shares
                        holdings[code]['cost_price'] = avg_cost
                    else:
                        holdings[code] = {
                            'shares': shares_to_buy,
                            'cost_price': buy_price,
                            'buy_date': date,
                        }
                    trades.append({
                        'date': str(date.date()), 'symbol': code,
                        'action': 'BUY', 'shares': shares_to_buy,
                        'price': round(buy_price, 2), 'reason': '调入',
                        'pnl': 0,
                    })

                elif diff_value < 0:
                    # 减持（超出目标仓位）
                    shares_to_sell = int(abs(diff_value) / current_price / 100) * 100
                    if shares_to_sell <= 0 or shares_to_sell > current_shares:
                        continue
                    sell_price = current_price * (1 - slippage)
                    sell_amount = shares_to_sell * sell_price
                    comm_cost = sell_amount * commission_rate
                    stamp_cost = sell_amount * stamp_tax
                    cash += sell_amount - comm_cost - stamp_cost
                    holdings[code]['shares'] -= shares_to_sell
                    if holdings[code]['shares'] <= 0:
                        pnl = (sell_price - holdings[code]['cost_price']) * shares_to_sell - comm_cost - stamp_cost
                        trades.append({
                            'date': str(date.date()), 'symbol': code,
                            'action': 'SELL', 'shares': shares_to_sell,
                            'price': round(sell_price, 2), 'reason': '减仓',
                            'pnl': round(float(pnl), 2),
                        })
                        del holdings[code]
                    else:
                        trades.append({
                            'date': str(date.date()), 'symbol': code,
                            'action': 'SELL', 'shares': shares_to_sell,
                            'price': round(sell_price, 2), 'reason': '减仓',
                            'pnl': 0,
                        })

            # 调仓日清理暂停标记（新季度开始）
            paused_stocks.clear()

    # ── 计算最终回测指标 ──
    return _compute_metrics(daily_values, trades, initial_cash)


# ═══════════════════════════════════════════════════════
# 指标计算
# ═══════════════════════════════════════════════════════

def _compute_metrics(daily_values: list, trades: list, initial_cash: float) -> dict:
    """计算回测指标"""
    if not daily_values:
        return _empty_result()

    values = [d['value'] for d in daily_values]
    final_value = values[-1]
    total_return = (final_value - initial_cash) / initial_cash * 100

    # 年化收益率
    days = len(values)
    years = max(days / 252, 0.5)
    annual_return = ((1 + total_return / 100) ** (1 / years) - 1) * 100

    # 最大回撤
    peak = values[0]
    max_dd = 0.0
    for v in values:
        if v > peak:
            peak = v
        dd = (peak - v) / peak * 100
        if dd > max_dd:
            max_dd = dd

    # 夏普比率（日收益率年化）
    daily_rets = []
    for i in range(1, len(values)):
        if values[i-1] > 0:
            daily_rets.append((values[i] - values[i-1]) / values[i-1])
    if daily_rets and len(daily_rets) > 1:
        avg_daily = np.mean(daily_rets)
        std_daily = np.std(daily_rets, ddof=1)
        sharpe = (avg_daily / std_daily) * np.sqrt(252) if std_daily > 0 else 0
    else:
        sharpe = 0

    # 胜率 & 盈亏比
    sells = [t for t in trades if t['action'] == 'SELL' and t.get('pnl') is not None]
    wins = [t for t in sells if t['pnl'] > 0]
    losses = [t for t in sells if t['pnl'] <= 0]
    win_rate = len(wins) / max(len(sells), 1) * 100

    avg_win = float(np.mean([t['pnl'] for t in wins])) if wins else 0.0
    avg_loss = abs(float(np.mean([t['pnl'] for t in losses]))) if losses else 1.0
    pl_ratio = avg_win / avg_loss if avg_loss > 0 else 0

    # 前后半段收益
    mid = len(values) // 2
    first_half = (values[mid] - values[0]) / values[0] * 100 if values[0] > 0 else 0
    second_half = (values[-1] - values[mid]) / values[mid] * 100 if values[mid] > 0 else 0

    # 换手率（年化）
    total_buy_value = sum(
        t['shares'] * t['price'] for t in trades if t['action'] == 'BUY'
    )
    avg_equity = (initial_cash + final_value) / 2
    annual_turnover = (total_buy_value / avg_equity) / years * 100 if avg_equity > 0 else 0

    return {
        'annual_return': round(annual_return, 2),
        'max_drawdown': round(max_dd, 2),
        'sharpe': round(sharpe, 2),
        'win_rate': round(win_rate, 1),
        'profit_loss_ratio': round(pl_ratio, 2),
        'total_trades': len(trades),
        'initial_cash': initial_cash,
        'final_value': round(final_value, 2),
        'total_return': round(total_return, 2),
        'sell_trades': len(sells),
        'win_trades': len(wins),
        'loss_trades': len(losses),
        'first_half_return': round(first_half, 2),
        'second_half_return': round(second_half, 2),
        'annual_turnover_pct': round(annual_turnover, 1),
        'daily_values': daily_values,
        'period_returns': [round(r * 100, 2) for r in daily_rets[::max(1, len(daily_rets)//10)]],
    }


def _empty_result() -> dict:
    return {
        'annual_return': 0, 'max_drawdown': 0, 'sharpe': 0,
        'win_rate': 0, 'profit_loss_ratio': 0, 'total_trades': 0,
        'error': '无可用数据',
    }
