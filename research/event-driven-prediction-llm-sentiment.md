# Event-Driven Prediction + LLM Sentiment Analysis Deep Dive

**Status**: researching  
**Created**: 2026-02-16  
**Category**: research  

---

## Overview

Deep dive into event-driven stock prediction (earnings surprises, EPS trends, analyst revisions) vs LLM-based news sentiment analysis. Key finding: structured event data has significantly higher predictive power than sentiment alone. This research informs the "WHEN to buy" axis of the product vision.

---

## Event Prediction Hierarchy

### Tier 1: High Predictive Power (60~70% directional accuracy)

**Earnings Surprise**
- Negative surprise: **68.7% directional accuracy** (SSRN 2024)
- Positive surprise: **59.2% accuracy** (lower due to earnings management)
- ML-based strategy: **Sharpe 1.39, 11.63% annualized** (S&P 1500, Random Forest)
- **PEAD confirmed in Korean market** — especially for growth stocks & low-attention stocks (KAIST, Korean Finance Journal)
- Korean market: value stocks respond promptly, growth stocks show delayed drift → exploitable anomaly

**EPS Estimate Trend (epsTrend)**
- 7/30/60 day changes in consensus → leading indicator for earnings surprise
- Upward estimate momentum → higher surprise probability
- Available via yfinance `eps_trend` for some Korean large-caps

**Ex-Dividend Date**
- Mechanical price adjustment → near-certain short-term prediction
- Currently NOT in our system (only div_yield exists)

### Tier 2: Medium Predictive Power

**Analyst Revisions**
- epsRevisionsUp/Down trends → short-term momentum signal
- yfinance `eps_revisions` for limited Korean coverage
- FnGuide API for full Korean market coverage (paid)

**Economic Calendar**
- FOMC, BOK rate decisions, CPI → sector-specific impact patterns
- Partially implemented: `fomc_calendar.py` (hardcoded schedules)
- ECOS API (Bank of Korea) available for real-time data (free)

### Tier 3: Low Predictive Power (54~61%)

**News Sentiment Alone**: 54~61% accuracy — barely above coin flip
**Social Media Sentiment**: Even noisier

### Key Insight

> **News sentiment should NOT be the primary signal. Use event-based signals as main, sentiment as confirming overlay.**
> Sentiment alone = 54-61%. But earnings surprise + sentiment direction alignment → prediction power amplifies significantly.

---

## LLM Sentiment Analysis — Current State of Research

### LLM vs Traditional NLP

| Method | Directional Accuracy | Sharpe Ratio | Source |
|--------|---------------------|--------------|--------|
| Dictionary-based (Loughran-McDonald) | ~54% | 1.23 | UCL 2024 |
| OPT (GPT-3 based) | 74.4% | 3.05 | ACL WASSA 2024 |
| FinBERT + FF5 | Significant alpha | 2.80 | arXiv 2025 |
| BERT news sentiment portfolio | — | 3.96 | SSRN 2023 |

### Best Prompt Engineering Practices

- **FinCoT (Structured Chain-of-Thought)**: Boosts accuracy from 63.2% to 80.5% for general LLMs (ACL FinNLP 2025)
- **AD-FCoT (Analogy-Driven)**: Compare new events to historical scenarios → improved sentiment classification + market return correlation (arXiv 2025)
- **Meta-prompting**: LLM assumes multiple analyst roles → reduces hallucination
- **Structured JSON output**: 90% ticker extraction accuracy, outperforms data providers

### Gemini-Specific Findings

- Thai market study: Gemini captures financial nuance well, but less consistent than GPT-4
- FinBen benchmark (NeurIPS 2024): GPT-4 overall #1, Gemini "variable but strong in specific tasks"
- Gemini 2.0 Flash: 1M token context, 2x speed of 1.5 Pro — ideal for batch sentiment

---

## Our Current System — What We Already Have

### News Collection
- Naver Search API (primary), Google News RSS, Hankyung RSS
- `RSSParser` class with 3-source fallback

### Sentiment Analysis
- Keyword-based: ~60 Korean financial keywords with weights (NewsCorrelator)
- Hybrid: keyword first → Gemini fallback when confidence < 0.5
- Multi-source aggregation: News(30%) + Community(20%) + Expert(50%)
- Time weighting: 24h = 2.0x, 1wk = 1.5x

### Gemini Integration
- Model: `gemini-3-pro-preview` (with Grounding enabled)
- GCI (Gemini Comprehensive Intelligence): 100 news + financials + technicals
- WHY-MOVED: price change cause analysis
- Structured JSON output already in use
- Prediction verification: sv2_analysis_history tracks 1d/1w accuracy

### Data Gaps (What We DON'T Have)
- EPS consensus/estimates → cannot calculate earnings surprise
- Earnings announcement dates
- EPS estimate trend changes (epsTrend)
- Ex-dividend dates
- Analyst revision history (stored transiently, not in DB)
- FRED/ECOS API real-time economic calendar integration

### Available Data Sources

| Source | Data | Cost | Korean Coverage |
|--------|------|------|----------------|
| yfinance | earnings_estimate, eps_trend, eps_revisions, earnings_dates | Free | Limited (large-caps only) |
| FnGuide/FnSpace API | Full consensus EPS, target prices, analyst opinions | Paid (coin-based) | Full |
| ECOS API (BOK) | Interest rates, CPI, GDP, 100+ indicators | Free | Full |
| FRED | US economic data | Free | US only |
| pykrx | No dividend ex-dates | Free | No |

---

## Improvement Proposals

### 1. Per-News Individual Sentiment Scoring (from InsightBig article)

Current: analyze news batch as whole → single overall_sentiment
Improved: score each news title individually via Gemini → distribution analysis

```
[Current] 20 news → keyword sum → "positive"
[Improved] 20 news → Gemini batch → [{title, score: +7, reason}, ...] → distribution
```

Cost: Gemini Flash, 500 stocks × 1/day = ~$0.20/day

### 2. Chain-of-Thought Prompt Upgrade

Apply FinCoT/AD-FCoT style structured reasoning:
1. Classify event impact area (earnings, regulation, market, product, management)
2. Analogize to historical similar events
3. Consider current market context (rates, FX, sector trends)
4. Distinguish short-term (1d) vs medium-term (1w) impact
5. Score -10 to +10

### 3. Sentiment DB Storage + Trend Analysis

New table: `sv2_news_sentiment` — per-news scores stored as time series
Enables: sentiment trend, reversal detection, prediction verification

### 4. Integration with Screening (Separate Signal)

Keep sentiment SEPARATE from composite score (academic evidence supports separation).

```
UI display: "Value 82 | Sentiment +6 | Momentum Neutral"
```

---

## InsightBig Article Analysis

**Source**: [Stock Market Sentiment Prediction with OpenAI and Python](https://www.insightbig.com/post/stock-market-sentiment-prediction-with-openai-and-python)

### What They Do
- EODHD News API → 100 news articles
- GPT-3.5-turbo via LangChain → per-article -10 to +10 score
- Pie chart visualization of sentiment distribution

### What They Do Well
- Per-news individual scoring (we should adopt)
- Quantitative -10 to +10 scale
- LangChain template standardization

### What They Do Poorly
- Zero-shot only (no CoT, no few-shot)
- No Korean language support
- No validation against actual price movements
- Full article body (token waste — titles are usually enough)
- Output parsing fragile ("GIVE ANSWER IN ONLY ONE WORD")

### What We Already Do Better
- Korean financial keyword dictionary
- Multi-source aggregation (news + community + expert)
- Structured JSON output via Gemini
- Prediction verification (1d/1w accuracy tracking)
- Google Search Grounding

---

## References

- [Earnings Surprise Directional Accuracy (SSRN 2024)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5056301)
- [Enhanced Financial Sentiment + Trading (ACL WASSA 2024)](https://aclanthology.org/2024.wassa-1.1/)
- [FinBERT + Fama-French 5-Factor (arXiv 2025)](https://arxiv.org/abs/2505.01432)
- [Portfolio Construction with News Sentiment (SSRN 2023)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4454949)
- [AD-FCoT: Analogy-Driven Financial CoT (arXiv 2025)](https://arxiv.org/abs/2509.12611)
- [FinCoT: Structured Domain CoT (ACL FinNLP 2025)](https://aclanthology.org/2025.finnlp-2.8.pdf)
- [Thai Market: NLP vs GPT vs Gemini (SSRN 2024)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4921837)
- [FinBen: 42 Datasets, 21 LLMs Benchmark (NeurIPS 2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/adb1d9fa8be4576d28703b396b82ba1b-Paper-Datasets_and_Benchmarks_Track.pdf)
- [PEAD in Korean Stock Market (Korean Finance Journal)](https://www.e-kjfs.org/journal/view.php?viewtype=pubreader&number=941)
- [ML Earnings Announcement Trading (SSRN 2020)](https://ideas.repec.org/p/zbw/iwqwdp/042020.html)
- [InsightBig: OpenAI Sentiment Analysis](https://www.insightbig.com/post/stock-market-sentiment-prediction-with-openai-and-python)

---

## Appendix: Data Source Gap-Fill Strategy (Cost Analysis)

### Price Reality Check (Verified 2026-02-16)

| Provider | Free Tier | Cheapest Paid | KRX Coverage | Notes |
|----------|-----------|---------------|--------------|-------|
| **yfinance** | Full (rate-limited) | $0 | Uncertain — needs testing | Already in our stack. Has earnings_estimate, eps_trend, eps_revisions, earnings_dates, earnings_history methods |
| **FMP** | 250 calls/day (US only) | $22/mo Starter (US only) | Needs Ultimate $149/mo (Global) — KRX not explicitly confirmed | Good for US, expensive for KRX |
| **Finnhub** | 60 calls/min (US fundamentals) | $3,000/mo All-in-One | Only at $3K tier | Free economic calendar useful; fundamentals too expensive |
| **EODHD** | 1yr history (request needed) | Paid for 30yr+ | Supports KRX for dividends/splits | Good for dividend ex-dates specifically |
| **FnGuide/FnSpace** | None | Coin-based (contact for pricing) | Full Korean coverage | The "gold standard" for Korean consensus but expensive |
| **ECOS (BOK)** | Full | $0 | Korean economic indicators | 100+ metrics, free API, good for macro |
| **FRED** | Full | $0 | US economic data | Good for US macro, no Korean data |

### Recommended Strategy: "Test Free First, Pay Later"

**Phase 0 ($0/mo — Immediate)**
- Test yfinance Korean stock earnings data (005930.KS, 000660.KS, etc.)
- Methods: get_earnings_estimate(), get_eps_trend(), get_eps_revisions(), get_earnings_dates(), get_earnings_history()
- If major KOSPI 50 stocks work → covers core event signal gaps for free

**Phase 1 ($0/mo — Build Over Time)**
- Daily snapshot: yfinance consensus EPS/revenue estimates → DB append
- After 2-3 months: self-built analyst revision history
- Earnings surprise = actual EPS - estimated EPS (auto-calculated)
- Connect ECOS API for Korean economic calendar (free)
- Keep fomc_calendar.py hardcoded schedule as fallback

**Phase 2 (If Needed — $22~149/mo)**
- If yfinance Korean coverage is insufficient:
  - FMP Ultimate ($149/mo) for global consensus
  - OR FnGuide for definitive Korean coverage (contact for pricing)
- EODHD for dividend ex-dates (low cost)
- Finnhub free tier for economic calendar supplement

### Key Insight: "Snapshot → Self-Built History"

The smartest low-cost approach: instead of paying for historical revision data, take daily snapshots of current consensus and build your own revision history over time. This costs $0 and after 2-3 months provides the same data that expensive providers sell.

```
Daily batch job:
1. yfinance.get_earnings_estimate() → sv2_consensus_snapshots
2. yfinance.get_eps_trend() → same table
3. yfinance.get_earnings_dates() → sv2_earnings_calendar
→ After 60-90 days: full self-built EPS revision history
```

---

*Last updated: 2026-02-16*
