# Blaque Baux Buyouts — research

Does the buyout *exit* dump on the public? The private "prop it up" years are invisible (no ticker); the
testable surface is the exit — sponsor-backed IPOs/re-IPOs (`IPO`, `FPX`, named listings) and the
post-lockup drift, vs `SPY`/`QQQ`. Read-only Alpaca SIP bars. Verdicts use the family fat-tail toolkit
([`_buyouts_common.py`](_buyouts_common.py): Jarque-Bera normality + Jensen's alpha + M²) because IPO
returns are heavily skewed/kurtotic and Sharpe alone would mislead.

```bash
export $(grep -v '^#' ~/.config/blaquebaux/alpaca.env | xargs)   # or source it
# python research/buyouts_1_ipo_tape.py        # [to build] IPO-basket beta / JB / Jensen alpha / M2 vs SPY
# python research/buyouts_2_lockup_event.py     # [to build] abnormal return around lockup expiry (the "dump")
```

## Planned scorecard

| # | Question | Metric | Status |
|---|----------|--------|--------|
| 1 | Do sponsor-backed IPOs earn negative risk-adjusted drift? | Jensen's α, M², JB on `IPO`/`FPX` vs SPY | ☐ to build |
| 2 | Is the post-lockup "dump" real and shortable? | event-study abnormal return, net of borrow | ☐ to build |

**The prior (to be tested, not assumed):** the "cash out" leg leaves retail holding — expect flat-to-negative
risk-adjusted drift after listing and measurable weakness around lockup expiry. If it's already priced in,
that's an honest null and goes on the record.

## Status
**[Concept] — plan defined, no sketches run.** Data-honesty boundary set (private leg invisible; exit is the
tape). Next: build sketch #1 (IPO-basket characterization) and #2 (lockup event study).
