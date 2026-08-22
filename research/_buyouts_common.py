#!/usr/bin/python3
# =============================================================================
# _buyouts_common.py — shared helpers for the Blaque Baux Buyouts sketches.
# Alpaca SIP daily bars; reads ALPACA_KEY_ID / ALPACA_SECRET_KEY from env. Read-only.
#
# Buyouts studies the TARGETS of the PE machine (cf. blackstone = the managers). The private "prop it up"
# years are invisible (no ticker); the testable surface is the EXIT — sponsor-backed IPOs/re-IPOs and the
# post-lockup drift. IPO/FPX are the liquid IPO-basket proxies; add named sponsor-backed listings as history
# allows. Benchmarks SPY/QQQ. Verdicts use the family fat-tail toolkit below (Jarque-Bera + Jensen's alpha
# + M-squared) because IPO returns are especially skewed/kurtotic — Sharpe alone would mislead.
# =============================================================================
IPO_BASKET = ["IPO", "FPX"]                 # Renaissance IPO / First Trust US IPO — sponsor-heavy new listings
BENCH = ["SPY", "QQQ"]
# named recent PE/sponsor-backed listings to add as SIP history allows (edit per study):
NAMED = []  # e.g. ["OWL", "CG", ...] target-side names; keep honest about survivorship

import os, json, urllib.request, math
import numpy as np

H = {"APCA-API-KEY-ID": os.environ["ALPACA_KEY_ID"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"]}
START, END = "2016-01-01", "2026-08-01"
_cache = {}

def bars(s):
    if s in _cache: return _cache[s]
    u = (f"https://data.alpaca.markets/v2/stocks/bars?symbols={s}&timeframe=1Day"
         f"&start={START}&end={END}&adjustment=all&feed=sip&limit=10000")
    try:
        d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=40))
        _cache[s] = {b["t"][:10]: b for b in d.get("bars", {}).get(s, [])}
    except Exception:
        _cache[s] = {}
    return _cache[s]

def panel(syms):
    """Aligned close-price panel over the symbols with >250 bars; returns ({sym: prices}, dates)."""
    D = {s: bars(s) for s in syms}; D = {s: v for s, v in D.items() if len(v) > 250}
    if not D: return {}, []
    u = list(D); dates = sorted(set.intersection(*[set(D[s]) for s in u]))
    M = np.array([[D[s][d]["c"] for s in u] for d in dates], float)
    return {s: M[:, i] for i, s in enumerate(u)}, dates

def rets(px): return px[1:] / px[:-1] - 1

def stats(r):
    r = np.asarray(r, float); r = r[np.isfinite(r)]
    if len(r) < 30 or r.std() == 0: return dict(sh=float('nan'), cagr=float('nan'), dd=float('nan'), vol=float('nan'))
    cum = np.cumprod(1 + r)
    return dict(sh=r.mean()/r.std()*math.sqrt(252), cagr=cum[-1]**(252/len(r))-1,
                dd=(cum/np.maximum.accumulate(cum)-1).min(), vol=r.std()*math.sqrt(252))

def corr(y, x):
    y = np.asarray(y, float); x = np.asarray(x, float); m = np.isfinite(y) & np.isfinite(x)
    return np.corrcoef(y[m], x[m])[0, 1] if m.sum() > 2 else float('nan')

def beta(y, x):
    y = np.asarray(y, float); x = np.asarray(x, float); m = np.isfinite(y) & np.isfinite(x)
    return float(np.cov(y[m], x[m])[0, 1] / np.var(x[m])) if m.sum() > 2 and np.var(x[m]) > 0 else float('nan')

# --- Blaque Baux shared risk-stats (canonical; numpy-only, no scipy) -----------------------------
# Adopted family-wide 2026-08: returns are fat-tailed, so we (1) TEST normality with Jarque-Bera before
# leaning on any mean-variance metric, and (2) report risk-adjusted performance with Jensen's alpha
# (return beyond what beta earns) and M-squared (return re-scaled to the benchmark's own volatility),
# not Sharpe alone. Sharpe assumes normality; JB usually rejects it for daily bars, which is exactly why
# alpha/M2 (benchmark-relative) and downside measures carry the verdict.
def jarque_bera(r):
    """Jarque-Bera normality test. H0 = returns are normal; reject (non-normal, fat tails) if p < 0.05.
    JB ~ chi-square(2), whose survival fn is exp(-x/2) — so no scipy needed. Returns skew + excess kurtosis."""
    r = np.asarray(r, float); r = r[np.isfinite(r)]; n = len(r)
    if n < 30: return dict(jb=float('nan'), p=float('nan'), skew=float('nan'), exkurt=float('nan'), normal=None)
    m, s = r.mean(), r.std()
    if s == 0: return dict(jb=0.0, p=1.0, skew=0.0, exkurt=0.0, normal=True)
    z = (r - m) / s
    sk = float(np.mean(z**3)); ku = float(np.mean(z**4) - 3.0)
    jb = n / 6.0 * (sk**2 + ku**2 / 4.0); p = math.exp(-jb / 2.0)
    return dict(jb=jb, p=p, skew=sk, exkurt=ku, normal=(p >= 0.05))

def jensens_alpha(r, rb, rf=0.0):
    """Jensen's alpha (annualized) = (Rp-Rf) - beta*(Rb-Rf) — return beyond what market beta earns.
    r, rb = daily return arrays; rf = ANNUAL risk-free (default 0). Also returns beta."""
    r = np.asarray(r, float); rb = np.asarray(rb, float)
    mk = np.isfinite(r) & np.isfinite(rb); r, rb = r[mk], rb[mk]
    if len(r) < 30 or np.var(rb) == 0: return dict(alpha_ann=float('nan'), beta=float('nan'))
    rf_d = rf / 252.0
    beta = float(np.cov(r, rb)[0, 1] / np.var(rb))
    alpha_d = (r.mean() - rf_d) - beta * (rb.mean() - rf_d)
    return dict(alpha_ann=alpha_d * 252.0, beta=beta)

def m_squared(r, rb, rf=0.0):
    """Modigliani M^2 (annualized, RETURN units): the book levered/de-levered to the benchmark's vol.
    m2_ann = rf + Sharpe_p * sigma_bench.  m2_excess = M^2-alpha = (Sharpe_p - Sharpe_bench) * sigma_bench
    — the Sharpe-DIFFERENCE form, so the benchmark vs itself is exactly 0 (no arithmetic/geometric offset)."""
    r = np.asarray(r, float); rb = np.asarray(rb, float)
    r = r[np.isfinite(r)]; rb = rb[np.isfinite(rb)]
    if len(r) < 30 or r.std() == 0 or rb.std() == 0 or len(rb) < 30: return dict(m2_ann=float('nan'), m2_excess=float('nan'))
    rf_d = rf / 252.0
    sh_p = (r.mean() - rf_d) / r.std() * math.sqrt(252)
    sh_b = (rb.mean() - rf_d) / rb.std() * math.sqrt(252)
    sig_b_ann = rb.std() * math.sqrt(252)
    return dict(m2_ann=rf + sh_p * sig_b_ann, m2_excess=(sh_p - sh_b) * sig_b_ann)

def riskadj(r, rb, rf=0.0):
    """One-call bundle: Sharpe/CAGR/DD/vol (from stats) + JB normality + Jensen's alpha + M^2, all vs a
    benchmark return series rb. This is the family's standard scorecard row for a return stream."""
    out = dict(stats(r)); out.update(jarque_bera(r))
    out.update(jensens_alpha(r, rb, rf)); out.update(m_squared(r, rb, rf))
    return out
# --------------------------------------------------------------------------------------------------
