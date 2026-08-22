# Blaque Baux Buyouts

**After the buyout — is the "cash out" a pump-and-dump, and is the exit shortable?**

Buyouts is a member of the Blaque Baux family. The [core repo](https://github.com/blaquebaux/base)
is the **engine and blueprint** — a governed, systematic platform (Julia) with a venue-agnostic
execution controller and a Layer-3 live-money safety gate. Buyouts points that engine at the *targets*
of the buyout machine — and inherits the governance wholesale.

> **Not investment advice.** Educational/research software. Nothing here is validated. See [LICENSE](LICENSE).

```bash
git clone --recursive https://github.com/blaquebaux/buyouts.git
julia --project=engine -e 'using Pkg; Pkg.instantiate()'   # one-time engine setup
```

## The thesis

[blackstone](https://github.com/blaquebaux/blackstone) studies the private-equity *managers*; **Buyouts
studies what happens to the companies they touch.** The sponsor's model is buy → lever → dress up → exit
at a markup, and the exit is where the public gets involved. The question is whether that exit is a
**pump-and-dump** — the sponsor floats or re-floats a business, supports the story through the lockup,
then sells into retail demand and the stock bleeds. If that pattern is real and *timeable*, the honest
trade is not to buy the IPO — it's to **short the post-lockup sponsor exit.**

**Data honesty — the private leg is invisible; the exit is where the tape exists.** A company taken
*private* loses its ticker, so the "prop it up" years are unobservable from price bars — a stated gap,
not faked. The **testable surface is the exit**: PE-sponsor-backed **IPOs and re-IPOs** (the Renaissance
IPO ETF `IPO`, First Trust `FPX`, and named recent sponsor-backed listings), the **post-lockup drift**
(the ~90–180-day window when insiders/sponsors can first sell), and the adjacent **SPAC** pattern (a
notorious "prop it up, cash out" structure). We test the drift causally against `SPY`/`QQQ`, net of cost.

## Research plan (Path A)

- **The IPO/re-IPO tape.** Characterize sponsor-backed IPOs (`IPO`, `FPX`, named listings): beta,
  Jarque-Bera normality (expect fat left tails), Jensen's alpha and M² vs `SPY` — is there *negative*
  risk-adjusted drift after listing?
- **The lockup-expiry event study.** Align names on lockup-expiry dates; measure abnormal return in the
  window around the sponsor's first legal sell. Is the "dump" real, and is it shortable net of borrow?
- **The pump tell.** Where the pattern holds, define the entry/exit rules for a short (or an avoid), and
  keep the null on the record if the "dump" is already priced in.

## Status
**[Concept] — scaffolded, not yet built.** Thesis, data-honesty boundary (private leg invisible; exit is
testable), and the Path-A plan are defined. The distinctive claim is a *short/avoid* on the post-lockup
sponsor exit, tested with the family's fat-tail-aware toolkit (Jarque-Bera + Jensen's alpha + M²). No
research run yet; no live driver.

## About Blaque Baux

**Blaque Baux** is a quantitative research initiative and a subsidiary of **[Carter Warrens](https://carterwarrens.com)**.
[**BlaqueBaux.com**](https://blaquebaux.com) is the home for the work; the code lives here on GitHub — open to
study, test, and build bespoke strategies on top of.

Anyone can point an AI at a market. The edge is **understanding what the data actually says — and turning it
into something you can act on.** We test relentlessly and put most of it *on the record as rejected, with the
reason*; what survives is built, governed, and validated before it is ever called real. That combination —
honest research, reproducible evidence, and execution you can trust — is why Carter Warrens leads on
**strategy and implementation**, not merely uses the tools everyone now has.

## The Blaque Baux family
This repo is one sleeve of the **Blaque Baux** family — a single governed engine steered in
many directions. The [core repo](https://github.com/blaquebaux/base) is the
base/blueprint and holds the [full family roster](https://github.com/blaquebaux/base#the-blaquebaux-family).

## Layout
```
engine/     the Blaque Baux platform (git submodule -> blaquebaux/base)
research/   _buyouts_common.py (loaders + JB/Jensen/M² toolkit) + sketches + scorecard  [to build]
live/       governed live drivers (once a sleeve graduates to paper A/B)
```

## License
[MIT](LICENSE). (c) 2026 Carter Warrens.
