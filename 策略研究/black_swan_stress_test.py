#!/usr/bin/env python3
"""黑天鹅压力测试 - 极端情景下的净资产影响分析

为陈颖芳投资组合建模五种极端情景，评估净资产变化、偿债能力和恢复难度。
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from typing import List

# ── 当前投资组合基线 ────────────────────────────────────────────
# 总资产 ~383万，负债 60万信用贷，净资产 ~323万

@dataclass
class Portfolio:
    """投资组合状态"""
    kunlun: float          # 昆仑万维市值（万）
    other_stocks: float    # 其他持仓市值（万）
    cash: float            # 现金/货币基金（万）
    credit_loan: float     # 信用贷负债（万）

    @property
    def total_assets(self) -> float:
        return self.kunlun + self.other_stocks + self.cash

    @property
    def net_worth(self) -> float:
        return self.total_assets - self.credit_loan

    @property
    def stock_assets(self) -> float:
        return self.kunlun + self.other_stocks

    def can_repay_loan(self) -> bool:
        """现金是否足够偿还信用贷"""
        return self.cash >= self.credit_loan

    def loan_coverage_ratio(self) -> float:
        """现金/负债覆盖率"""
        if self.credit_loan == 0:
            return float("inf")
        return self.cash / self.credit_loan

    def margin_risk(self, margin_ratio: float = 1.3) -> tuple[bool, float]:
        """检查保证金风险（假设股票质押融资，维持担保比例<130%则预警）

        如果 portfolio 并非融资买入，此检查仅作参考——
        信用贷不存在自动平仓机制，但银行可能在净值大幅缩水时要求提前还款。
        """
        if self.credit_loan == 0:
            return False, float("inf")
        ratio = self.stock_assets / self.credit_loan
        return ratio < margin_ratio, ratio


@dataclass
class ScenarioResult:
    """单个情景的压力测试结果"""
    name: str
    description: str
    baseline_net_worth: float
    shocked: Portfolio
    new_net_worth: float
    net_worth_change: float          # 绝对变化（万）
    net_worth_change_pct: float      # 百分比变化
    can_repay: bool
    margin_risk: bool
    margin_ratio: float
    recovery_needed_pct: float       # 恢复到基线净资产需要的涨幅(%)


# ── 测试执行 ────────────────────────────────────────────────────

def stress_test(baseline: Portfolio, scenario_name: str, scenario_desc: str,
                kunlun_shock: float, other_shock: float, cash_shock: float = 0.0,
                loan_change: float = 0.0) -> ScenarioResult:
    """执行单一压力情景

    Args:
        kunlun_shock: 昆仑万维变动比例 (-0.5 = 跌50%)
        other_shock: 其他持仓变动比例
        cash_shock: 现金变动比例 (通常为0)
        loan_change: 信用贷额外变动（万），正值表示需要额外偿还
    """
    shocked = Portfolio(
        kunlun=baseline.kunlun * (1 + kunlun_shock),
        other_stocks=baseline.other_stocks * (1 + other_shock),
        cash=baseline.cash * (1 + cash_shock) - loan_change,
        credit_loan=baseline.credit_loan - loan_change,  # 偿还后负债减少
    )
    new_nw = shocked.net_worth
    change = new_nw - baseline.net_worth
    change_pct = (change / baseline.net_worth) * 100
    margin_risk, margin_ratio = shocked.margin_risk()

    # 恢复到基线需要的涨幅: (baseline_nw / new_nw - 1) * 100
    recovery = ((baseline.net_worth / new_nw - 1) * 100) if new_nw > 0 else float("inf")

    return ScenarioResult(
        name=scenario_name,
        description=scenario_desc,
        baseline_net_worth=baseline.net_worth,
        shocked=shocked,
        new_net_worth=new_nw,
        net_worth_change=change,
        net_worth_change_pct=change_pct,
        can_repay=shocked.can_repay_loan(),
        margin_risk=margin_risk,
        margin_ratio=margin_ratio,
        recovery_needed_pct=recovery,
    )


def run_all_scenarios(baseline: Portfolio) -> List[ScenarioResult]:
    """运行全部五种黑天鹅情景"""
    scenarios_def = [
        ("情景1: 昆仑万维跌50%",
         "昆仑万维 46.45→23.23，单一重仓股腰斩",
         -0.50, 0.0, 0.0, 0.0),

        ("情景2: 昆仑万维跌70%",
         "昆仑万维 46.45→13.94，重仓股近乎归零级别暴跌",
         -0.70, 0.0, 0.0, 0.0),

        ("情景3: A股整体跌30%",
         "系统性风险，股票仓位全面下跌30%，现金不受影响",
         -0.30, -0.30, 0.0, 0.0),

        ("情景4: 科技股崩盘",
         "昆仑万维-60% + 其他科技股-40%，AI赛道遭遇极端估值回归",
         -0.60, -0.40, 0.0, 0.0),

        ("情景5: 组合冲击(市场跌30%+信用贷到期)",
         "A股跌30% + 全额偿还60万信用贷，双杀流动性",
         -0.30, -0.30, 0.0, 60.0),  # loan_change=60 表示额外偿还60万
    ]

    results = []
    for name, desc, kun, oth, cash, loan in scenarios_def:
        results.append(stress_test(baseline, name, desc, kun, oth, cash, loan))
    return results


# ── 格式化输出 ──────────────────────────────────────────────────

def fmt_money(val: float) -> str:
    """格式化金额（万）"""
    return f"{val:,.1f}万"


def fmt_pct(val: float) -> str:
    """格式化百分比"""
    sign = "+" if val > 0 else ""
    return f"{sign}{val:.1f}%"


def severity_label(change_pct: float) -> str:
    """根据净资产跌幅返回严重性标签"""
    if change_pct >= -10:
        return "可承受 🟢"
    elif change_pct >= -20:
        return "需关注 🟡"
    elif change_pct >= -35:
        return "严重 🟠"
    else:
        return "危急 🔴"


def print_header(title: str, width: int = 78):
    print()
    print("=" * width)
    print(f"  {title}")
    print("=" * width)


def print_portfolio(p: Portfolio, label: str):
    """打印投资组合明细"""
    print(f"\n  📊 {label}")
    print(f"     昆仑万维:    {fmt_money(p.kunlun):>12s}  ({p.kunlun/p.total_assets*100:.1f}%)")
    print(f"     其他持仓:    {fmt_money(p.other_stocks):>12s}  ({p.other_stocks/p.total_assets*100:.1f}%)")
    print(f"     现金/货币:   {fmt_money(p.cash):>12s}  ({p.cash/p.total_assets*100:.1f}%)")
    print(f"     ─────────────────────────────")
    print(f"     总资产:      {fmt_money(p.total_assets):>12s}")
    print(f"     信用贷负债:  {fmt_money(p.credit_loan):>12s}")
    print(f"     净资产:      {fmt_money(p.net_worth):>12s}")


def print_scenario_result(r: ScenarioResult, idx: int):
    """打印单个情景结果"""
    print_header(f"情景{idx+1}: {r.name}", 78)
    print(f"  假设: {r.description}")

    # 投资组合变化
    b = r.baseline_net_worth  # baseline from result
    print(f"\n  📉 冲击后投资组合:")
    print(f"     昆仑万维:    {fmt_money(r.shocked.kunlun):>12s}")
    print(f"     其他持仓:    {fmt_money(r.shocked.other_stocks):>12s}")
    print(f"     现金/货币:   {fmt_money(r.shocked.cash):>12s}")
    print(f"     信用贷负债:  {fmt_money(r.shocked.credit_loan):>12s}")
    print(f"     ─────────────────────────────")
    print(f"     冲击后净资产:{fmt_money(r.new_net_worth):>12s}")

    # 关键指标
    print(f"\n  📋 关键指标:")
    print(f"     净资产变化:   {fmt_money(r.net_worth_change):>12s}  ({fmt_pct(r.net_worth_change_pct)})")
    print(f"     严重级别:     {severity_label(r.net_worth_change_pct)}")

    # 偿债能力
    coverage = r.shocked.loan_coverage_ratio()
    print(f"     信用贷偿还:   {'✅ 可全额偿还' if r.can_repay else '❌ 现金不足'}")
    print(f"     现金/负债比:  {coverage:.2f}x")

    # 保证金风险
    if r.shocked.credit_loan > 0:
        print(f"     股票/负债比:  {r.margin_ratio:.2f}x")
        if r.margin_risk:
            print(f"     保证金预警:   ⚠️  股票担保比例跌破130%，若为融资仓位将触发强制平仓")
        else:
            print(f"     保证金预警:   ✅ 维持担保比例充足")

    # 恢复需求
    if r.recovery_needed_pct == float("inf"):
        print(f"     恢复所需涨幅: ∞ (净资产归零，无法恢复)")
    else:
        print(f"     恢复至当前:   需要上涨 {fmt_pct(r.recovery_needed_pct)}")


def print_summary_table(results: List[ScenarioResult], baseline_nw: float):
    """打印汇总对比表"""
    print_header("压力测试汇总", 90)
    print()
    header_fmt = (
        f"  {'情景':<28s} {'冲击后净资产':>10s} {'净资产变化':>10s} {'变化%':>8s} "
        f"{'偿债':>4s} {'担保比':>6s} {'恢复需涨':>8s} {'级别':<8s}"
    )
    print(header_fmt)
    print("  " + "-" * 86)

    for r in results:
        level = severity_label(r.net_worth_change_pct)
        repay = "✅" if r.can_repay else "❌"
        recovery_str = f"{r.recovery_needed_pct:.1f}%" if r.recovery_needed_pct != float("inf") else "∞"
        print(
            f"  {r.name:<28s} {fmt_money(r.new_net_worth):>10s} {fmt_money(r.net_worth_change):>10s} "
            f"{fmt_pct(r.net_worth_change_pct):>8s} {repay:>4s} "
            f"{r.margin_ratio:>5.2f}x {recovery_str:>8s} {level}"
        )


def print_action_recommendations(results: List[ScenarioResult]):
    """根据测试结果打印行动建议"""
    print_header("行动建议", 78)

    # 找出最严重的情景
    worst = min(results, key=lambda r: r.new_net_worth)
    worst_change = min(results, key=lambda r: r.net_worth_change_pct)
    cant_repay = [r for r in results if not r.can_repay]
    margin_call = [r for r in results if r.margin_risk]

    print(f"\n  🔑 核心发现:")
    print(f"     最严重情景: {worst.name} — 净资产降至 {fmt_money(worst.new_net_worth)}")
    print(f"     最大跌幅情景: {worst_change.name} — 跌幅 {fmt_pct(worst_change.net_worth_change_pct)}")

    # 昆仑万维集中度风险
    print(f"\n  🎯 集中度风险 (昆仑万维占40%):")
    print(f"     情景1 (昆仑跌50%): 净资产减少 {fmt_money(results[0].net_worth_change)}")
    print(f"     情景2 (昆仑跌70%): 净资产减少 {fmt_money(results[1].net_worth_change)}")
    print(f"     建议: 将单一持仓逐步降低至不超过总资产20%，分批减持、设置止损线")

    # 偿债能力
    print(f"\n  💰 信用贷 (60万, 2026年9月到期):")
    if cant_repay:
        for r in cant_repay:
            print(f"     {r.name}: 现金不足以偿还信用贷")
        print(f"     建议: 提前预留60万在货币基金中，不要投入股市")
    else:
        print(f"     全部情景下现金均可覆盖信用贷，但情景5偿还后将大幅削弱投资能力")
        print(f"     建议: 到期前3个月将60万转入货币基金锁定，避免被动低位斩仓")

    # 保证金风险
    if margin_call:
        print(f"\n  ⚠️  保证金风险:")
        for r in margin_call:
            print(f"     {r.name}: 股票/负债比仅 {r.margin_ratio:.2f}x (预警线1.30x)")
        print(f"     建议: 如有融资买入，立即降低杠杆；信用贷虽然不触发自动平仓，")
        print(f"           但银行可能在资产大幅缩水时要求补充担保或提前还款")

    # 恢复难度
    print(f"\n  📈 恢复难度分析:")
    for r in results:
        if r.recovery_needed_pct == float("inf"):
            print(f"     {r.name}: 无法恢复（净资产归零）")
        elif r.recovery_needed_pct <= 25:
            print(f"     {r.name}: 需涨{fmt_pct(r.recovery_needed_pct)} — 一轮反弹可恢复")
        elif r.recovery_needed_pct <= 50:
            print(f"     {r.name}: 需涨{fmt_pct(r.recovery_needed_pct)} — 需要一年以上修复期")
        else:
            print(f"     {r.name}: 需涨{fmt_pct(r.recovery_needed_pct)} — 可能需要3-5年才能恢复")

    # 行动优先级
    print(f"\n  🚀 立即行动清单:")
    print(f"     1. [紧急] 设置昆仑万维止损线（建议-15%即止损）")
    print(f"     2. [紧急] 预留60万现金于货币基金，应对9月信用贷到期")
    print(f"     3. [重要] 制定昆仑万维减持计划，目标降至总资产20%以内")
    print(f"     4. [重要] 新投资资金不得再追加单一持仓，分散至3-5个标的")
    print(f"     5. [建议] 每次昆仑万维反弹10%即减持10-20%仓位")
    print()


# ── main ────────────────────────────────────────────────────────

def main():
    # 当前投资组合基线
    baseline = Portfolio(
        kunlun=153.0,        # 昆仑万维 ~153万 (40%)
        other_stocks=76.5,   # 其他持仓 ~76.5万 (20%)
        cash=153.5,          # 现金/货币 ~153.5万 (40%)
        credit_loan=60.0,    # 信用贷 60万 (2026年9月到期)
    )

    print_header("黑天鹅压力测试 — 陈颖芳投资组合", 90)
    print_portfolio(baseline, "当前投资组合基线")
    print(f"\n  当前净资产: {fmt_money(baseline.net_worth)}")
    print(f"  信用贷到期: 2026年9月 (距今约4个月)")
    print(f"  昆仑万维占比: {baseline.kunlun/baseline.total_assets*100:.1f}% (高集中度风险)")

    # 运行全部情景
    results = run_all_scenarios(baseline)

    for i, r in enumerate(results):
        print_scenario_result(r, i)

    # 汇总表
    print_summary_table(results, baseline.net_worth)

    # 行动建议
    print_action_recommendations(results)

    # 最终判断 - 基于实际计算结果
    r1, r2, r3, r4, r5 = results
    print_header("最终判断", 78)

    def survival_label(r: ScenarioResult) -> str:
        if r.net_worth_change_pct >= -15:
            return "可承受"
        elif r.net_worth_change_pct >= -25:
            return "可生存"
        elif r.net_worth_change_pct >= -35:
            return "危险但可生存"
        else:
            return "危急但可生存"

    print(f"""
  情景1 (昆仑-50%):        {survival_label(r1)} — 净资产降至{fmt_money(r1.new_net_worth)}，现金/负债比{r1.shocked.loan_coverage_ratio():.1f}x
  情景2 (昆仑-70%):        {survival_label(r2)} — 净资产降至{fmt_money(r2.new_net_worth)}，现金/负债比{r2.shocked.loan_coverage_ratio():.1f}x
  情景3 (A股-30%):         {survival_label(r3)} — 净资产{fmt_money(r3.new_net_worth)}，最接近真实系统性风险
  情景4 (科技股崩盘):      {survival_label(r4)} — 净资产{fmt_money(r4.new_net_worth)}，跌幅{fmt_pct(r4.net_worth_change_pct)}，需警惕AI赛道估值回调
  情景5 (市场-30%+偿债):   {survival_label(r5)} — 净资产{fmt_money(r5.new_net_worth)}，现金骤降至{fmt_money(r5.shocked.cash)}，偿债后流动性紧张

  ⚠️  当前组合的最大风险不是绝对亏损，而是昆仑万维集中度(40%)过高。
  任何昆仑万维的重大利空都会成倍放大对净资产的冲击。
  建议尽快将集中度降至20%以下。
""")


if __name__ == "__main__":
    main()
