# Product Synopsis — "Should I Buy This Stock Now?"

**Status**: researching  
**Created**: 2026-02-16  
**Category**: business  

---

## Overview

Product positioning for RedJoker as an AI-powered investment decision tool that answers the single most important question every retail investor asks: **"Should I buy this stock NOW?"** — synthesizing fundamentals, event timing, and risk into a clear, actionable answer.

---

## The Core Question

> **"이 종목, 지금 사도 되는가?"**
> "Is this stock worth buying right now?"

Every retail investor asks this. No Korean tool answers it comprehensively.

---

## The 3-Axis Decision Framework

```
"이 종목, 지금 사도 되는가?"

├── WHAT: 뭘 살까? → Composite Score (100점)
│   "Is this a GOOD stock?"
│
├── WHEN: 지금이 맞아? → Event Signal (Tiered)
│   "Is NOW the right time?"
│
└── RISK: 뭘 조심해? → Risk Monitor
    "What should I watch out for?"
```

### Axis 1: WHAT — Is It a Good Stock? (Composite Score 100)

Filters fundamentally strong stocks:

- Value (35pts): PBR + PER sector-relative + dividend yield
- Quality (25pts): ROE + operating margin + cash flow quality
- Growth (20pts): Revenue/profit YoY + earnings stability
- Stability (20pts): Debt ratio + debt trend + dividend consistency + volatility

**Differentiator**: Not just raw data — a synthesized, ranked score that answers "how good is this stock compared to peers?"

### Axis 2: WHEN — Is Now the Right Time? (Event Signal)

This is THE biggest differentiator. Tiered by prediction accuracy:

**Tier 1 — Action Signals (High Accuracy, 60~70%)**
- Earnings surprise direction → "Buy/Avoid within 3 days of announcement"
- EPS estimate uptrend → "Leading indicator → enter before announcement"
- Ex-dividend D-3 → "Dividend capture strategy"

**Tier 2 — Context Signals (Medium Accuracy)**
- Analyst target price upgrade → "Momentum confirmation"
- FOMC/BOK rate decision D-day → "Consider sector rebalancing"

**Tier 3 — Sentiment Overlay (Low Accuracy, 54~61%)**
- News sentiment (Gemini-analyzed) → "Market mood check"
- Community sentiment → "Retail investor psychology reference"

**Differentiator**: Naver Finance doesn't even show earnings announcement dates. We tell you "earnings in 3 days, consensus trending up, surprise probability HIGH" → a **timing signal**.

### Axis 3: RISK — What to Watch Out For? (Risk Monitor)

- Debt ratio 2yr consecutive increase warning (already implemented)
- Operating profit 2yr consecutive decline warning (already implemented)
- News sentiment reversal detection (positive → negative flip)
- Volatility spike (Bollinger Band breakout)
- Macro risk (rate hike → growth stock headwind)

---

## Competitive Positioning

```
[Naver Finance]  Lots of data → but "So what?" (no synthesis)
[Broker HTS]     Chart-centric → no fundamental + event integration
[Overseas Tools]  AI analysis exists → but not Korea-market specialized
[RedJoker]       Fundamentals + Events + AI → Korea-specialized synthesis
```

### Why This Wins

1. **No Korean tool does 3-axis synthesis**: They show data, we show answers
2. **Event signals are the moat**: Earnings surprise + PEAD is academically proven in Korean market
3. **AI-powered but grounded**: Gemini analysis backed by quantitative scores, not hallucination
4. **"Buy decision tool" positioning**: Clear, emotionally resonant — every investor's core need

---

## Evidence Base

### Event-Driven Prediction Accuracy

| Signal | Accuracy | Source |
|--------|----------|--------|
| Earnings Surprise (negative) | 68.7% | SSRN 2024 |
| Earnings Surprise (positive) | 59.2% | SSRN 2024 |
| ML Earnings Strategy | Sharpe 1.39, 11.63% annual | SSRN 2020 |
| PEAD in Korea | Confirmed for growth stocks | Korean Finance Journal |
| News Sentiment Alone | 54~61% | Multiple studies |

### PEAD in Korean Market

- Growth stocks: overreact to positive, underreact to negative → drift
- Low-attention stocks: delayed price response → exploitable
- Value stocks: respond promptly → less drift
- Market sentiment amplifies effects for small/mid caps

### LLM Enhancement

- GPT-based sentiment: 74.4% accuracy, Sharpe 3.05 (vs dictionary 1.23)
- FinBERT + FF5: Sharpe 2.80, 471% improvement over CAPM
- Key: LLM is most powerful as **confirming overlay** on event signals, not standalone

---

## Implementation Roadmap

### Phase 1: Foundation (1-2 weeks)
- Fix data health warning (sector benchmarks tolerance)
- Add yfinance earnings_estimate/eps_trend/eps_revisions collection
- Add yfinance earnings_dates (announcement calendar)
- Store analyst target price/rating in DB (currently real-time only)
- Connect ECOS API (economic calendar real-time)

### Phase 2: Core Engines (2-4 weeks)
- Build Event Signal engine: earnings surprise calculation, EPS trend analysis
- Build 100-point Composite Score engine
- Add per-news Gemini sentiment scoring (Flash model)
- Create sv2_news_sentiment table + sentiment trend storage

### Phase 3: Integration Dashboard (4-6 weeks)
- 3-axis integrated UI: Composite Score + Event Signal + Risk Monitor
- Per-stock "Investment Decision Card" — comprehensive at-a-glance view
- Event alerts: "Earnings in 3 days", "EPS trending up", "Ex-dividend D-3"
- Sentiment trend chart + event timeline

### Phase 4: Advanced (Long-term)
- FnGuide API integration (full Korean consensus coverage)
- Earnings surprise backtesting → prediction model accuracy verification
- AI comprehensive judgment (Gemini): 3-axis data → "Buy/Hold/Sell" + reasoning
- PEAD strategy auto-signal

---

## Data Source Strategy

### Free (Immediate)
- yfinance: earnings estimates, eps_trend, eps_revisions, earnings_dates (limited Korean coverage)
- ECOS API: Korean economic indicators (100+ metrics, free)
- pykrx: existing daily metrics (no ex-dividend dates)

### Paid (Future)
- FnGuide/FnSpace: full Korean consensus EPS, analyst opinions, target prices
- Decision: start with free yfinance → validate value → invest in FnGuide if justified

---

## Marketing Angle

### Tagline Options

- **"이 종목, 지금 사도 되는가? — AI가 답합니다"**
- **"데이터를 보여주는 도구는 많다. 답을 주는 도구는 하나."**
- **"좋은 종목 × 적기 × 리스크 = 투자 판단"**

### Key Selling Points

1. **100점 스코어**: 복잡한 재무제표를 한 숫자로 — "이 종목 몇 점?"
2. **이벤트 타이밍**: "3일 후 실적 발표, 컨센서스 상향 중" — 다른 데 없는 정보
3. **AI 종합 분석**: Gemini 기반 증권사급 리포트 — 초보자도 읽을 수 있게
4. **리스크 경고**: "부채 2년 연속 증가, 주의!" — 잃지 않는 투자

---

*Last updated: 2026-02-16*
