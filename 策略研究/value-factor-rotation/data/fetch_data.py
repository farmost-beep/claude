"""真实数据获取模块 - 使用 akshare 获取 A 股行情和基本面数据"""
import akshare as ak
import pandas as pd
from datetime import datetime


def _add_sina_prefix(code: str) -> str:
    """6位代码转 Sina 格式（sh600xxx / sz000xxx / sz300xxx / sz688xxx）"""
    if code.startswith("6"):
        return f"sh{code}"
    return f"sz{code}"


def get_stock_list():
    """获取沪深300 + 科创50 成分股列表"""
    hs300 = ak.index_stock_cons_csindex("000300")
    kc50 = ak.index_stock_cons_csindex("000688")
    codes = list(set(hs300["成分券代码"].tolist() + kc50["成分券代码"].tolist()))
    return codes


def get_daily_data(symbols, start_date, end_date):
    """获取日线行情数据（Sina API，格式匹配 backtest 期望）"""
    frames = {}
    for sym in symbols:
        try:
            df = ak.stock_zh_a_daily(
                symbol=_add_sina_prefix(sym), adjust="qfq")
            if df is None or df.empty:
                continue
            df = df.rename(columns={"date": "date"})
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index("date")
            df = df.sort_index()
            if start_date:
                df = df[df.index >= start_date]
            if end_date:
                df = df[df.index <= end_date]
            if not df.empty:
                frames[sym] = df
        except Exception:
            continue
    return frames


def get_fundamentals(symbols):
    """获取基本面数据：通过 stock_financial_abstract_new_ths 获取最新年报数据（ROE/EPS/BVPS/营收增速）

    返回 DataFrame，字段：
      - symbol: 股票代码
      - ROE_TTM: 加权平均净资产收益率（年报值，单位 %, 如 9.15）
      - EPS: 基本每股收益（年报值）
      - BVPS: 每股净资产（年报值）
      - revenue_growth_yoy: 营业总收入同比增长率（年报值，单位 %, 如 -10.40）
    """
    METRIC_MAP = {
        "ROE_TTM": "index_weighted_avg_roe",
        "EPS": "basic_eps",
        "BVPS": "calc_per_net_assets",
        "revenue_growth_yoy": "calculate_operating_income_total_yoy_growth_ratio",
    }
    records = []
    for sym in symbols:
        try:
            df = ak.stock_financial_abstract_new_ths(symbol=sym)
            if df.empty:
                continue
            # 取最新年报数据（report_name 包含 '年报'）
            annual = df[df['report_name'].str.contains('年报', na=False)]
            if annual.empty:
                continue
            latest = annual.sort_values('report_date').iloc[-1]
            row = {"symbol": sym}
            for our_key, metric_name in METRIC_MAP.items():
                match = df[(df['metric_name'] == metric_name) & (df['report_name'] == latest['report_name'])]
                if not match.empty:
                    val = match.iloc[0]['value']
                    row[our_key] = float(val) if pd.notna(val) else None
                else:
                    row[our_key] = None
            records.append(row)
        except Exception:
            continue
    return pd.DataFrame(records)


def get_real_data(start_date="20200101", end_date=None):
    """主入口：获取完整数据集，格式匹配 strategy.run_backtest() 期望的 stocks_data"""
    if end_date is None:
        end_date = datetime.now().strftime("%Y%m%d")

    print(f"获取成分股列表...")
    symbols = get_stock_list()
    print(f"共 {len(symbols)} 只股票")

    print(f"获取行情数据 {start_date} ~ {end_date}...")
    stocks_data = get_daily_data(symbols, start_date, end_date)
    print(f"获取到 {len(stocks_data)} 只股票行情")

    print(f"获取基本面数据...")
    fundamentals = get_fundamentals(symbols)
    print(f"获取到 {len(fundamentals)} 条基本面记录")

    return stocks_data, fundamentals


if __name__ == "__main__":
    data, fund = get_real_data("20240101", "20260101")
    print(f"行情: {len(data)} 只, 基本面: {len(fund)} 条")
    if not fund.empty:
        print(fund.describe())
