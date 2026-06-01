#!/usr/bin/env python3
"""免费金融数据源（akshare）——替代Wind/同花顺，供Agent A/B使用。

依赖: pip3 install akshare
数据来源：东方财富/新浪财经/同花顺（免费接口）
"""

from datetime import datetime
from pathlib import Path
import json

CACHE_DIR = Path(__file__).resolve().parent.parent.parent / ".bridge" / "fin_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _cache_get(key: str):
    """读取缓存（1小时内有效）"""
    fp = CACHE_DIR / f"{key}.json"
    if fp.exists():
        age = (datetime.now() - datetime.fromtimestamp(fp.stat().st_mtime)).total_seconds()
        if age < 3600:
            return json.loads(fp.read_text())


def _cache_set(key: str, data):
    fp = CACHE_DIR / f"{key}.json"
    fp.write_text(json.dumps(data, ensure_ascii=False, default=str))


def get_financial_indicators(symbol: str) -> dict:
    """获取核心财务指标（ROE/毛利率/净利率/营收增速等）

    Args:
        symbol: 股票代码，如 "300418"
    Returns:
        {指标名: {最新值, 上季度值, 趋势}}
    """
    cache_key = f"fin_indicator_{symbol}"
    cached = _cache_get(cache_key)
    if cached:
        return cached

    try:
        import akshare as ak
        df = ak.stock_financial_analysis_indicator(symbol=symbol, start_year="2024")
        if df.empty:
            return {"error": "无数据"}

        # 提取关键指标
        result = {}
        latest = df.iloc[-1]  # 最近一期
        prev = df.iloc[-2] if len(df) > 1 else latest

        # 定义需要提取的指标
        mapping = {
            "主营业务利润率": ["主营业务利润率(%)"],
            "毛利率": ["主营业务利润率(%)", "销售毛利率(%)"],
            "净利率": ["销售净利率(%)"],
            "ROE": ["净资产收益率(%)"],
            "每股经营现金流": ["每股经营性现金流(元)"],
            "营收增速": ["主营业务收入增长率(%)"],
            "净利润增速": ["净利润增长率(%)"],
            "营业利润率": ["营业利润率(%)"],
            "资产负债率": ["资产负债率(%)"],
            "每股净资产": ["每股净资产_调整前(元)"],
            "每股收益": ["摊薄每股收益(元)"],
        }

        for name, cols in mapping.items():
            for col in cols:
                if col in df.columns:
                    try:
                        cur_val = float(latest.get(col, 0) or 0)
                        prev_val = float(prev.get(col, 0) or 0)
                    except (ValueError, TypeError):
                        cur_val = prev_val = 0

                    # 判断趋势
                    if cur_val > prev_val * 1.02:
                        trend = "↑"
                    elif cur_val < prev_val * 0.98:
                        trend = "↓"
                    else:
                        trend = "→"

                    # 跳过全是nan的值
                    if cur_val is not None and not (isinstance(cur_val, float) and str(cur_val) == 'nan'):
                        result[name] = {
                            "最新值": round(cur_val, 2),
                            "上期值": round(prev_val, 2),
                            "趋势": trend,
                        }
                    break

        result["报告期"] = str(latest.get("日期", ""))
        result["_source"] = "akshare(东方财富免费接口)"

        _cache_set(cache_key, result)
        return result
    except Exception as e:
        return {"error": str(e)}


def get_industry_peers(symbol: str, industry: str = "") -> list:
    """获取同行业公司的估值和基本数据

    Returns:
        [{代码, 名称, PE, PB, 营收, 市值}]
    """
    # 行业对标数据较复杂，先用简单的行业板块数据
    cache_key = f"peers_{symbol}"
    cached = _cache_get(cache_key)
    if cached:
        return cached

    try:
        import akshare as ak
        # 获取沪深A股行业板块
        df = ak.stock_board_industry_name_em()
        if df.empty:
            return [{"error": "行业数据获取失败"}]

        # 找对应行业
        target_board = None
        for _, row in df.iterrows():
            if industry and industry in str(row.get("板块名称", "")):
                target_board = row["板块名称"]
                break

        if target_board:
            board_df = ak.stock_board_industry_cons_em(symbol=target_board)
            if not board_df.empty:
                peers = []
                for _, row in board_df.head(20).iterrows():
                    peers.append({
                        "代码": row.get("代码", ""),
                        "名称": row.get("名称", ""),
                        "现价": float(row.get("现价", 0) or 0),
                    })
                _cache_set(cache_key, peers)
                return peers

        return [{"error": f"行业'{industry}'未找到"}]
    except Exception as e:
        return [{"error": str(e)}]


def get_stock_valuation(symbol: str) -> dict:
    """获取估值数据（PE/PB/市值）"""
    cache_key = f"valuation_{symbol}"
    cached = _cache_get(cache_key)
    if cached:
        return cached

    try:
        import akshare as ak

        # 获取A股实时行情
        df = ak.stock_zh_a_spot_em()
        stock_row = df[df["代码"] == symbol]
        if stock_row.empty:
            return {"error": "股票未找到"}

        row = stock_row.iloc[0]
        result = {
            "名称": row.get("名称", ""),
            "最新价": float(row.get("最新价", 0) or 0),
            "涨跌幅": f"{row.get('涨跌幅', 0)}%",
            "PE(动态)": float(row.get("市盈率-动态", 0) or 0),
            "总市值": float(row.get("总市值", 0) or 0),
            "流通市值": float(row.get("流通市值", 0) or 0),
            "_source": "akshare(东方财富免费接口)",
        }
        _cache_set(cache_key, result)
        return result
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import sys
    symbol = sys.argv[1] if len(sys.argv) > 1 else "300418"

    print(f"=== {symbol} 财务指标 ===")
    indicators = get_financial_indicators(symbol)
    for k, v in indicators.items():
        if isinstance(v, dict):
            print(f"  {k}: {v.get('最新值')} ({v.get('趋势')}) 上期:{v.get('上期值')}")
        else:
            print(f"  {k}: {v}")

    print(f"\n=== {symbol} 估值 ===")
    val = get_stock_valuation(symbol)
    for k, v in val.items():
        print(f"  {k}: {v}")
