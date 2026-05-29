#!/usr/bin/env python3
"""自动获取持仓股票实时价格，支持--close 收盘模式"""
import urllib.request
import sys
import json
import os
from datetime import datetime

SINA_URL = "http://hq.sinajs.cn/list="
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "策略研究", ".market_prices.json")

# 所有需要追踪的股票
ALL_STOCKS = {
    # 僵尸清仓品种
    "sz300142": ("300142", "沃森生物", "普通"),
    "sh600126": ("600126", "杭钢股份", "普通"),
    "sz002570": ("002570", "贝因美", "普通"),
    "sh600050": ("600050", "中国联通", "普通"),
    "sh688525": ("688525", "佰维存储", "普通"),
    "sh588460": ("588460", "科创50增强ETF", "普通"),
    "sh512070": ("512070", "证券保险ETF", "普通"),
    "sh512000": ("512000", "券商ETF", "普通"),
    "sz000002": ("000002", "万科A", "信用"),
    "sh600995": ("600995", "南网储能", "信用"),
    "sh601788": ("601788", "光大证券", "信用"),
    "sh601377": ("601377", "兴业证券", "信用"),
    "sz002458": ("002458", "益生股份", "信用"),
    "sh600549": ("600549", "厦门钨业", "信用"),
    # 核心持仓
    "sz300418": ("300418", "昆仑万维", "核心"),
}

def fetch_prices():
    """从新浪API获取实时价格"""
    codes = list(ALL_STOCKS.keys())
    url = SINA_URL + ','.join(codes)
    req = urllib.request.Request(url, headers={'Referer': 'https://finance.sina.com.cn'})
    resp = urllib.request.urlopen(req, timeout=10)
    data = resp.read().decode('gbk')

    results = {}
    for line in data.strip().split('\n'):
        if not line.strip():
            continue
        parts = line.split('"')
        if len(parts) < 2:
            continue
        code = line.split('=')[0][-6:]
        fields = parts[1].split(',')
        if len(fields) < 6:
            continue
        results[code] = {
            "name": fields[0],
            "open": float(fields[1]),
            "prev_close": float(fields[2]),
            "price": float(fields[3]),
            "high": float(fields[4]),
            "low": float(fields[5]),
            "change_pct": round((float(fields[3]) - float(fields[2])) / float(fields[2]) * 100, 2),
        }
    return results


def calc_net(gross):
    commission = max(gross * 0.00025, 5.0)
    stamp_tax = gross * 0.001
    return gross - commission - stamp_tax


def print_prices(prices, label="实时"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"╔══════════════════════════════════════════════════════════════╗")
    print(f"║  持仓价格快照 — {now} ({label})")
    print(f"╠══════════════════════════════════════════════════════════════╣")

    # 昆仑万维单独显示
    kl = prices.get("300418")
    if kl:
        direction = "↑" if kl["change_pct"] > 0 else "↓" if kl["change_pct"] < 0 else "→"
        print(f"║  ★ 昆仑万维 300418: ¥{kl['price']:.2f} {direction} {kl['change_pct']:+.1f}%")
        print(f"║    日内: ¥{kl['low']:.2f} - ¥{kl['high']:.2f}  昨收: ¥{kl['prev_close']:.2f}")
        print(f"╠══════════════════════════════════════════════════════════════╣")

    # 清仓品种
    accounts = {"普通": [], "信用": []}
    for sid, (code, name, acct) in ALL_STOCKS.items():
        if code == "300418":
            continue
        p = prices.get(code)
        if p and acct in accounts:
            accounts[acct].append((code, name, p))

    for acct, stocks in accounts.items():
        print(f"║  [{acct}账户]")
        for code, name, p in stocks:
            print(f"║  {code} {name:<10} ¥{p['price']:>8.2f}  {p['change_pct']:>+6.1f}%  "
                  f"昨收¥{p['prev_close']:.2f}")
        if stocks:
            print(f"║")

    print(f"╚══════════════════════════════════════════════════════════════╝")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "show"

    if mode in ("--close", "--save"):
        prices = fetch_prices()
        # 保存到JSON
        record = {
            "timestamp": datetime.now().isoformat(),
            "prices": {k: {"price": v["price"], "change_pct": v["change_pct"],
                           "high": v["high"], "low": v["low"]} for k, v in prices.items()}
        }
        with open(DATA_FILE, "w") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        print_prices(prices, "收盘")
        print(f"价格已保存至 {DATA_FILE}")

        # 输出汇总
        kl = prices.get("300418", {})
        print(f"\n收盘汇总: 昆仑万维 ¥{kl.get('price', 'N/A')} | "
              f"记录{len(prices)}只股票")
    else:
        prices = fetch_prices()
        print_prices(prices, "实时")
        kl = prices.get("300418", {})
        if kl:
            print(f"\n昆仑万维: ¥{kl.get('price', 'N/A')} "
                  f"({kl.get('change_pct', 0):+.1f}%)")


if __name__ == "__main__":
    main()
