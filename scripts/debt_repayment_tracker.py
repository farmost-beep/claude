#!/usr/bin/env python3
"""还本追踪器：管理19只死仓位清仓进度 + 还本专户余额

用法:
  python3 debt_repayment_tracker.py status     # 查看当前进度
  python3 debt_repayment_tracker.py sell 代码 数量 单价   # 记录一笔卖出
  python3 debt_repayment_tracker.py transfer 金额   # 记录转入还本专户
  python3 debt_repayment_tracker.py reset      # 重置所有数据（清仓完成后）
"""

import json, os, sys
from datetime import date

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "repayment_tracker.json")

INITIAL_POSITIONS = {
    "普通账户": [
        # 格式: (代码, 名称, 股数, 成本价)
        ("002555", "三七互娱", 800, 26.70),
        ("300418", "昆仑万维(普通)", 10200, 53.50),
        ("159715", "稀土ETF", 45300, 1.47),
        ("300059", "东方财富", 1300, 5.28),
        ("159206", "卫星ETF", 4700, 2.11),
        ("600519", "贵州茅台", 100, 980.00),
        ("000858", "五粮液", 200, 125.00),
        ("002415", "海康威视", 500, 32.00),
    ],
    "信用账户": [
        ("300418", "昆仑万维(信用)", 6800, 57.25),
    ],
    "港币账户": [
        ("09678.HK", "云知声", 80, 262.00),
        ("06030.HK", "中信证券", 1000, 29.91),
        ("00390.HK", "中国中铁", 1000, 9.13),
        ("00700.HK", "腾讯控股", 100, 320.00),
        ("01810.HK", "小米集团", 500, 18.00),
        ("09988.HK", "阿里巴巴", 200, 85.00),
        ("09618.HK", "京东集团", 100, 130.00),
        ("09888.HK", "百度集团", 100, 95.00),
        ("02015.HK", "理想汽车", 200, 110.00),
        ("09866.HK", "蔚来", 300, 45.00),
        ("01024.HK", "快手", 200, 55.00),
    ],
}

TARGET_AMOUNT = 600000  # 60万还本目标

def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return init_data()

def init_data():
    return {
        "target": TARGET_AMOUNT,
        "special_account_balance": 1,  # 测试金1元
        "bank_loan_info": {
            "confirmed": False,
            "due_date": None,
            "repayment_account": None,
            "early_repayment_penalty": None,
            "transfer_limit": None,
            "partial_repayment": None,
            "extension_rate": None,
        },
        "positions": {acct: [
            {"code": c, "name": n, "shares": s, "cost": p,
             "sold": False, "sell_price": None, "sell_date": None}
            for c, n, s, p in items
        ] for acct, items in INITIAL_POSITIONS.items()},
        "transfers": [],  # 转入还本专户记录
        "updated": date.today().isoformat(),
    }

def save(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    data["updated"] = date.today().isoformat()
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def cmd_status(data):
    total_positions = sum(len(positions) for positions in data["positions"].values())
    total_sold = 0
    total_proceeds = 0
    remaining = 0
    all_sold = True

    print("=" * 60)
    print(f"  还本专户余额: {data['special_account_balance']:>10,.0f} 元")
    print(f"  目标金额:     {data['target']:>10,.0f} 元")
    gap = data['target'] - data['special_account_balance']
    print(f"  剩余缺口:     {gap:>10,.0f} 元")
    print()

    for acct, positions in data["positions"].items():
        print(f"  ── {acct} ──")
        for p in positions:
            est = p["shares"] * (p["sell_price"] or p["cost"])
            marker = "✅" if p["sold"] else "○"
            status_str = (f"已清@{p['sell_price']}" if p['sold']
                          else f"待清 预估{est:>8.0f}元")
            print(f"    {marker} {p['code']} {p['name']:　<8} "
                  f"{p['shares']:>6}股 "
                  f"成本{p['cost']:>7.2f} "
                  f"{status_str:>16}")
            if p["sold"]:
                total_sold += 1
                total_proceeds += p["shares"] * p["sell_price"]
            else:
                all_sold = False
                remaining += 1
        print()

    print(f"  已清仓: {total_sold}/{total_positions}  待清: {remaining}/{total_positions}")
    print(f"  回笼资金合计: {total_proceeds:>10,.0f} 元")
    print(f"  还本专户余额: {data['special_account_balance']:>10,.0f} 元")
    print(f"  可还本总额:   {total_proceeds + data['special_account_balance']:>10,.0f} 元")
    print(f"  距目标60万:   {data['target'] - (total_proceeds + data['special_account_balance']):>10,.0f} 元")
    print()

    if data["bank_loan_info"]["confirmed"]:
        i = data["bank_loan_info"]
        print(f"  银行信息已确认:")
        print(f"    到期日: {i['due_date']}")
        print(f"    还款账户: {i['repayment_account']}")
        print(f"    提前还款: {'有违约金 ' + i['early_repayment_penalty'] if i['early_repayment_penalty'] else '无违约金'}")
        print(f"    大额转账限额: {i['transfer_limit']}")
    else:
        print(f"  ⚠️ 银行电话尚未拨打（5/29执行）")
    print("=" * 60)

    if all_sold and data['special_account_balance'] >= data['target']:
        print("\n🎉 全部完成！19个死仓位清空，还本专户余额达标！")

def cmd_sell(data, code, shares, price):
    for acct, positions in data["positions"].items():
        for p in positions:
            if p["code"] == code and not p["sold"]:
                p["sold"] = True
                p["sell_price"] = float(price)
                p["sell_date"] = date.today().isoformat()
                proceeds = int(shares) * float(price)
                save(data)
                print(f"✅ 已记录: {p['name']} {shares}股 × {price} = {proceeds:,.0f} 元")
                return
    print(f"⚠️ 未找到代码 {code} 的未清仓持仓")

def cmd_transfer(data, amount):
    data["special_account_balance"] += float(amount)
    data["transfers"].append({
        "date": date.today().isoformat(),
        "amount": float(amount),
        "balance_after": data["special_account_balance"],
    })
    save(data)
    print(f"✅ 转入还本专户: {float(amount):,.0f} 元")
    print(f"   当前余额: {data['special_account_balance']:,.0f} 元")

def cmd_reset(data):
    data = init_data()
    save(data)
    print("✅ 已重置所有数据")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    data = load()
    cmd = sys.argv[1]

    if cmd == "status":
        cmd_status(data)
    elif cmd == "sell" and len(sys.argv) == 5:
        cmd_sell(data, sys.argv[2], int(sys.argv[3]), float(sys.argv[4]))
    elif cmd == "transfer" and len(sys.argv) == 3:
        cmd_transfer(data, float(sys.argv[2]))
    elif cmd == "reset":
        cmd_reset(data)
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
