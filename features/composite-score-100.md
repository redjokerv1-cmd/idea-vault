# Composite Score 100 — Screening Score System Upgrade

**Status**: researching  
**Created**: 2026-02-16  
**Category**: features  

---

## Overview

Convert the current binary 7-point Value Score (pass/fail per criterion) into a continuous 100-point Composite Score with category-weighted percentile ranking. Enables finer stock differentiation and proper ranking among top-scoring stocks.

---

## Problem

- Current 7/7 stocks are indistinguishable — no way to rank them
- "ROE barely above sector median" and "ROE 50% above" both get 1 point
- No category weighting — all 7 criteria have equal importance despite PBR/ROE being academically proven stronger factors

---

## Proposed Architecture

```
Composite Score (100) = Value(35) + Quality(25) + Growth(20) + Stability(20)
```

### Value — 35 pts
- PBR vs sector (14): sector-relative percentile, lower = better
- PER vs sector (14): same approach, negative PER = 0
- Dividend yield (7): universe-wide percentile, higher = better

### Quality — 25 pts
- ROE vs sector (10): sector-relative percentile, higher = better
- Operating margin (8): universe-wide percentile
- Cash flow quality (7): operating_cashflow > 0 base + cashflow/net_income ratio

### Growth — 20 pts
- Revenue YoY (8): bracket scoring (0%/5%/15%/30%+ thresholds)
- Operating profit YoY (8): same brackets
- Earnings trend stability (4): 2yr consecutive decrease = 0, stable = 4

### Stability — 20 pts
- Debt ratio (7): universe-wide percentile, lower = better
- Debt trend (4): 2yr consecutive increase = 0, stable = 4
- Dividend consistency (5): 0yr = 0, 1yr = 2, 2yr+ = 5
- Volatility (4): from sv2_technical_indicators, lower = better

### Why These Weights

- **Value 35**: Fama-French Korea research confirms PBR(Book-to-Price) is the strongest return predictor. Korea Value-up Index also uses PBR as primary filter.
- **Quality 25**: Alpha Architect research — Quality filter is key to avoiding "Value Traps". ROE is the most direct quality metric.
- **Growth 20**: Korean market revenue/operating_profit growth rate correlates with short-term returns. Korea Value-up excludes 2yr consecutive losses.
- **Stability 20**: Debt ratio + volatility for risk defense.

### Momentum — Separate Score (NOT included in 100)

Academic evidence (Alpha Architect 2021): separating Value and Momentum yields higher returns in concentrated portfolios. Our screening (top 20~50 stocks) is concentrated.

---

## Scoring Methodology

**Recommended: Sector-Relative Percentile + Universe Fallback (Method A+C Hybrid)**

- Sector-sensitive metrics (PBR, PER, ROE) → percentile within sector
- Universal metrics (debt ratio, div yield, growth) → universe-wide percentile
- Sectors with < 10 stocks → fall back to universe percentile
- Winsorization at 5th/95th percentile for outlier defense
- Aligns with Korea Value-up Index "industry-relative evaluation" philosophy

### Outlier & NULL Handling

- Winsorize: clip at 5th/95th percentile per metric
- PER: 0 < PER < 200 hard cap; negative PER = 0 points
- NULL: 0 points for that item (conservative, Alpha Architect style)
- Auxiliary metrics (volatility, tech indicators): NULL = neutral midpoint

---

## Academic References

- **Piotroski F-Score Continuous Transformation** (Univ. of Pretoria, 2017): Ranked-scale maintains winner/loser separation + improves discrimination
- **MSCI Quality Score**: Z-score based + Winsorization, industry standard
- **SVI Score**: Weighted sum (PER 35% + PBR 10% + Earnings Yield 35% + EPS Growth 20%)
- **Fama-French Korea**: Size + Book-to-Price are key return predictors
- **Korea Value-up Index** (KRX 2024.09): 5-stage screening with sector-relative PBR + ROE ranking
- **Alpha Architect QV Index**: Value + Quality dual screen, equal weight
- **Missing Values in ML Portfolios** (arXiv 2022): Cross-sectional mean imputation works as well as complex EM methods

---

## Industry Benchmarks

| System | Method | Key Feature |
|--------|--------|-------------|
| MSCI Quality Score | Z-score + Winsorization | Industry standard |
| Korea Value-up Index | 5-stage funnel, sector-relative | Korean market official |
| Alpha Architect QV | Value → Quality dual screen | Value trap defense |
| SVI Score | Weighted sum | Market-specific weights |
| Morningstar | DCF fair value + moat rating | Cash-flow based |

---

## DB Changes Required

- `sv2_screening_results` table: add `composite_score DECIMAL(5,2)`, category sub-scores
- OR extend existing `sv2_relative_scores` table (already exists, unused)
- Keep `value_score` (7-point) for backward compatibility

---

## Open Questions (To Decide)

1. Include momentum in 100 or separate? → **Recommended: separate**
2. User-customizable weights? → **Recommended: fixed (avoid overfitting)**
3. Negative PER handling? → **Recommended: 0 points (conservative)**
4. Use value_score as gate? → **Recommended: independent calculation**
5. UI display? → **Recommended: number + letter grade + radar chart**

---

## Tech Stack

- Language: Python
- Framework: FastAPI (backend), React + TypeScript (frontend)
- Libraries: NumPy/Pandas for percentile calculations
- Database: PostgreSQL (existing sv2_* tables)

---

## Estimated Effort

- **Difficulty**: Hard
- **Estimated Time**: 2-3 weeks (engine + API + frontend)

---

## References

- [Piotroski F-Score Continuous Transformation (Univ. of Pretoria)](https://repository.up.ac.za/items/5175ab1f-5718-4a99-86f2-30cbff5cbfd3)
- [MSCI Quality Indexes Methodology](https://www.scribd.com/document/906362113/MSCI-Quality-Indexes-Methodology-20250520-1)
- [Korea Value-up Index Analysis (Samsung)](https://www.samsungpop.com/common.do?cmd=down)
- [Alpha Architect: Quality Factor](https://alphaarchitect.com/the-quality-factor-what-exactly-is-it/)
- [Fama-French Korea: Evaluating Asset Pricing Models](https://www.sciencedirect.com/science/article/abs/pii/S0927538X1100059X)
- [Missing Values in ML Portfolios (arXiv 2022)](https://arxiv.org/html/2207.13071v6)
- [Value Investing and Size Effect in Korean Market](https://www.mdpi.com/2227-7072/6/1/31)
- [Value and Momentum: Combine or Separate? (Alpha Architect)](https://alphaarchitect.com/value-and-momentum-investing-combine-or-separate/)

---

*Last updated: 2026-02-16*
