#!/usr/bin/python3
# =============================================================================
# buyouts_1_ipo_drift.py — the sponsor-exit / post-listing drift thesis: is the new-issue complex a DRAG to avoid?
# Blackstone is the manager (a levered pro-cyclical factor); buyouts is the TARGET side — and the visible,
# priceable surface of "the sponsor cashes out on you" is the IPO complex: IPO (Renaissance) / FPX (First Trust),
# both sponsor-heavy new listings. Thesis = negative alpha / worse tail vs the market (a short/avoid, not a buy).
# =============================================================================
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _buyouts_common import panel, rets, riskadj
import numpy as np

P,dates=panel(["IPO","FPX","SPY","QQQ"])
R={s:rets(P[s]) for s in P}; spy=R["SPY"]; qqq=R.get("QQQ")
print("="*90); print(f"BUYOUTS — sponsor-exit / post-IPO drift: a drag to avoid?  ({dates[0]} → {dates[-1]}, {len(dates)} days)"); print("="*90)
print(f"\n  {'':8}{'Sharpe':>8}{'CAGR':>8}{'maxDD':>8}{'skew':>7}{'β/SPY':>7}{'α/SPY':>9}{'M²exc':>8}")
res={}
for s in ["IPO","FPX","SPY","QQQ"]:
    if s not in R: continue
    a=riskadj(R[s],spy); res[s]=a
    print(f"  {s:8}{a['sh']:>+8.2f}{a['cagr']*100:>+7.0f}%{a['dd']*100:>+7.0f}%{a['skew']:>+7.2f}{a['beta']:>+7.2f}{a['alpha_ann']*100:>+8.1f}%{a['m2_excess']*100:>+7.1f}%")
# verdict from the IPO-complex alpha + tail vs SPY
drag=[s for s in ["IPO","FPX"] if s in res and res[s]["alpha_ann"]<-0.01 and res[s]["m2_excess"]<0]
hi_beta_worse=[s for s in ["IPO","FPX"] if s in res and res[s]["beta"]>1.05 and res[s]["dd"]<res["SPY"]["dd"]-0.05]
if drag: verdict=f"CONFIRMED (avoid/short-bias): {', '.join(drag)} deliver NEGATIVE alpha and worse M² than SPY — the sponsor-exit drag is real; the new-issue complex transfers the premium to the seller, not the buyer."
elif hi_beta_worse: verdict=f"CONDITIONAL: {', '.join(hi_beta_worse)} ≈ high-beta SPY with a deeper drawdown — not negative-alpha, but a worse risk-adjusted deal than just owning the index (no reason to pay up for new issues)."
else: verdict="MIXED/NULL: the IPO complex didn't clearly underperform risk-adjusted in this sample — the drift thesis isn't confirmed on these broad ETFs (per-name post-lockup timing would be the sharper, survivorship-careful test)."
print(f"\n  VERDICT: {verdict}")
print("  (Broad IPO ETFs blunt the per-name lockup-expiry drift; the v2 is a sponsor-backed-name, lockup-dated,")
print("   survivorship-careful event study — NAMED=[] is the honest placeholder for that.)")
