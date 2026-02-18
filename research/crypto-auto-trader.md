# AI 코인 자동매매 트레이더

**상태**: 🔬 researching  
**생성일**: 2026-02-18  
**분류**: research  

---

## 개요

기존 주식 스크리닝 시스템(stock-predictor)의 인프라와 노하우를 활용하여, 업비트 기반 AI 코인 자동매매 도구를 구축하는 프로젝트.

---

## 프로젝트 전제

- 사용자: 한국(서울) 거주 개인 트레이더
- 용도: 본인 계정 + 본인 자금 + 개인용 도구 (서비스화는 별도)
- 거래소: 업비트 (현물 전용, 선물/레버리지 없음)
- 방향: 독립 리포로 분리 (projects-hub 서브모듈), universal-devkit 통해 지식 공유

---

## 시스템 3단계 구조

### 1. 시그널 생성
- 입력: 가격/거래량, 오더북, 체결, 온체인, 뉴스/소셜
- 출력: 매수/매도/대기, 방향/강도, 기대 수익/위험 추정
- 방식: 규칙 기반 전략(기술지표, 오더북 패턴) + ML/AI 모델 혼합

### 2. 리스크/포지션 결정
- 계좌 % 베팅 규칙, 손절/익절, 일/주 손실 한도, MDD 한도
- 코인별 익스포저 제한

### 3. 실행(Execution)
- 거래소 API로 주문 전송, 체결/잔고/포지션 실시간 관리
- 슬리피지/수수료/레이트리밋 대응

---

## 기존 자산 재활용 분석

### 직접 재활용 가능 (70%+)
| 기존 자산 | 활용 |
|---|---|
| FastAPI + async 아키텍처 | 봇 백엔드 서버 |
| Rate Limiter + Circuit Breaker | 업비트 API 보호 (KIS 429 경험 적용) |
| CacheManager + EventBus | 시세 캐싱 + 이벤트 무효화 |
| Debug API + 로그 버퍼 | 24/7 모니터링 |
| PostgreSQL 중앙 DB (sv2 패턴) | OHLCV + 주문/체결 이력 |
| APScheduler 배치 | 데이터 수집 스케줄러 |
| DevKit 전체 | 개발 프로세스 |

### 적응/확장 필요
| 기존 자산 | 변경 |
|---|---|
| Technical Indicators 엔진 | 입력 소스를 Upbit로 변경 |
| Composite Score | 코인용 스코어링 재설계 |
| Signal Tracker | 크립토 시그널 추적 |
| Market Radar | 코인 패턴 스캔 |
| React 모니터링 UI | 실시간 PnL/포지션 뷰 추가 |

### 완전히 새로 구축 필요
| 컴포넌트 | 중요도 | 설명 |
|---|---|---|
| 주문 실행 엔진 | CRITICAL | 시장가/지정가, 부분체결, 취소, 리트라이 |
| 포지션 매니저 | CRITICAL | 실시간 잔고/포지션 동기화 |
| WebSocket 수신기 | HIGH | 업비트 실시간 체결/호가 24/7 |
| 리스크 엔진 | HIGH | 계좌 % 베팅, MDD 한도, 연속손실 정지 |
| 백테스팅 프레임워크 | HIGH | 이벤트 기반, 수수료/슬리피지 반영 |
| Paper Trading | MEDIUM | 실제 주문 없이 시뮬레이션 |
| AI/ML 파이프라인 | MEDIUM | 모델 학습/추론/드리프트 모니터링 |

---

## 업비트 API 스펙

| 항목 | 상세 |
|---|---|
| 인증 | JWT + HMAC-SHA256, 매 요청 nonce |
| Rate Limit (시세) | 초당 10회/IP (캔들, 체결, 호가 각각) |
| Rate Limit (Origin) | Origin 헤더 시 10초당 1회 |
| 초과 시 | 429 → 반복 위반 시 418 + 차단 |
| WebSocket | 시세 공개 스트림, 120초 idle, ping 30초 |
| 최소 주문 | KRW 마켓 5,000원+ |
| 거래 유형 | 현물(spot)만 — 선물/레버리지/공매도 없음 |

**업비트 = 현물 전용**: 롱만 가능, 공매도/헤지 불가, 펀딩비 없음, 레버리지 없음.
→ 리스크 엔진이 단순해지는 장점.

---

## 법적/규제 분석 (2025-2026 기준)

### 개인 자동매매는 합법
업비트 공식 API를 사용한 본인 계정 매매는 정상 트레이딩.

### 금지 행위 (형사처벌 대상)
| 행위 | 위험도 | 자동매매 관련성 |
|---|---|---|
| 가장매매(워시 트레이딩) | 높음 | 봇이 실수로 자기 주문끼리 체결 가능 |
| 스푸핑 | 중간 | 공격적 주문 전략 시 의도 없이 의심 가능 |
| 펌프앤덤프 | 중간 | 소형 코인 전략 주의 |
| 다계정 통정매매 | 낮음 | 1계정만 쓰면 해당 없음 |

### 감시 현황
- 금감원 2025년 10월부터 **분 단위 감시** 도입
- 2024.7~2025.9: 21건 적발, 16건 검찰 고발
- 가상자산이용자보호법: 부당이득 3~5배 벌금

### 방어 설계 (필수)
1. 가장매매 방지: 미체결 주문과 반대 방향 자동 체크
2. 주문 빈도 제한: 분당 최대 주문 캡
3. 저유동성 코인 자동 제외: 일정 거래량 미만 블랙리스트
4. 전 주문/체결 로그 영구 보존 (감사 대비)
5. 타인 자금 운용 절대 금지 (투자일임업 규제)

---

## 기술 스택 (안)

- **언어**: Python 3.11+
- **프레임워크**: FastAPI + uvicorn (기존 아키텍처)
- **거래소 연동**: CCXT (업비트 공식 지원, 멀티거래소 확장 가능)
- **실시간 데이터**: websocket-client + asyncio
- **DB**: PostgreSQL (기존 Railway 인스턴스, ct_ prefix 테이블)
- **기술지표**: pandas, numpy, ta (기존 코드 재활용)
- **AI/ML**: scikit-learn, PyTorch (향후)
- **모니터링**: React UI (기존 확장) + Debug API
- **배포**: Railway (기존) 또는 별도 VPS (24/7 안정성)

---

## 로드맵 (기존 자산 기반)

### Phase 0: 기반 세팅 (1~2주)
- 업비트 API 키 발급 (조회+주문, 출금 제외)
- CCXT 연동 테스트 (잔고/시세 조회)
- 프로젝트 구조 결정

### Phase 1: 데이터 수집 (2~3주)
- REST: 캔들(분/시/일봉) → ct_ohlcv
- WebSocket: 실시간 체결/호가 → 인메모리 + DB
- Rate Limiter/Circuit Breaker 적용
- APScheduler 확장

### Phase 2: 피처 엔진 + 백테스트 인프라 (4~6주)
- 3축 피처 엔진 구축:
  - 축 1 (기술지표): SMA 50/200, EMA 21, RSI, MACD, BB Width, ATR, OBV, VWAP
  - 축 2 (센티먼트): Fear & Greed Index, 뉴스/SNS 감성 (초기는 외부 API)
  - 축 3 (시장구조): 오더북 imbalance, 거래량 구조 (온체인은 후순위)
- 이벤트 기반 백테스터 구축 (수수료 0.05%, 슬리피지)
- 파라미터 코인 환경 튜닝 (RSI 80/20, MA zone 방식, MACD 기간 확대 등)
- 워크포워드 검증, 성과 지표 (샤프, MDD, 승률, PF)
- 레짐 감지 모듈 (변동성/추세/횡보 구분 — BBW, ATR 기반)

### Phase 3: ML 파이프라인 (3~4주) ← AI를 앞당김
- ML 모델 구축: XGBoost/LightGBM 앙상블 (빠른 실험) + LSTM (시계열 패턴)
- 피처: 축 1~3 지표를 모델 입력으로 사용 (단일 지표 규칙 X)
- 시간 기반 train/validation/test, 롤링 워크포워드
- 레짐별 모델 성능 분석 (추세장 vs 횡보장 vs 폭락장)
- 규칙 기반 전략은 ML 모델 fallback으로 유지
- Signal Tracker 연동 (시그널 정확도 자동 추적)

### Phase 4: 실행 엔진 + 리스크 (3~4주)
- Paper Trading 먼저 (ML 모델 시그널로 시뮬레이션)
- CCXT 통한 주문 실행 (시장가/지정가)
- 리스크 엔진: max %, 일일 한도, MDD 정지
- 가장매매 방지 로직
- 모델 드리프트 모니터링 (성능 하락 시 자동 fallback)

### Phase 5: 운영 + 확장 (장기)
- 소액 Live → 단계적 확대
- 실시간 대시보드 (모니터링 UI)
- 온체인 데이터 통합 (축 3 확장)
- 멀티 코인/멀티 전략 확장

---

## 아키텍처 원칙

1. **독립 프로젝트, 지식은 공유** — stock-predictor와 별도 리포, universal-devkit 경유 패턴/경험 공유
2. **KIRA 교훈의 올바른 적용** — KIRA는 "같은 도메인 내 사일로"라서 실패, 코인은 다른 도메인이므로 독립이 정답
3. **계산과 해석의 분리** — 지표 수학 공식은 참고 가능, 파라미터/해석/전략은 코인 전용으로 독립 구현
4. **리스크 엔진 우선** — 시그널보다 리스크 관리가 상위 레이어
5. **Paper Trading 필수** — 실거래 전 반드시 시뮬레이션 검증
6. **백테스트 없이 라이브 없다** — 코인 데이터로 재보정하지 않은 전략은 실거래 금지

---

## 오픈소스 비교 결론

| 옵션 | 판단 |
|---|---|
| Freqtrade (46K stars) | 기존 시스템과 통합 어려움 |
| Jesse (7K stars) | 깔끔하지만 별도 생태계 |
| **CCXT + 자체 구축** | 기존 인프라 활용 + 확장성 최적 |

CCXT 라이브러리만 활용하고 나머지는 기존 아키텍처 위에 자체 구축.

---

## 핵심 리스크 요약

| 카테고리 | 리스크 | 대응 |
|---|---|---|
| **규제** | 시세조종 혐의 (형사처벌) | 가장매매 방지, 로그 보존, 저유동성 회피 |
| **재무** | 실제 자금 손실 | Paper Trading 필수, 소액 시작, MDD 자동 정지 |
| **기술** | 24/7 가동 안정성 | 장애 시 자동 정지, 모니터링 알림 |
| **시장** | 코인 변동성/레짐 전환 | 레짐 감지, fallback 전략, 포지션 사이징 |

---

## 주식 vs 코인: 기술지표 차이 분석

### 핵심 결론
계산 공식은 동일하지만, 시장 구조 차이 때문에 해석과 파라미터가 완전히 달라진다.
"같은 지표"를 그대로 옮기면 안 되고, 코인 데이터로 재보정 백테스트가 필수.

### 4대 구조 차이

| 차이 | 주식 | 코인 | 설계 영향 |
|---|---|---|---|
| **시간** | 장 시간(09:00~15:30) | 24/7 연속 | 타임프레임 기준 재설계 필요 |
| **변동성** | 서킷브레이커, 공시 의무 | 고변동성, 유동성 얇음, whale/봇 조작 | RSI 임계값 상향 (70→80, 30→25) |
| **밸류에이션** | PER/PBR/실적 앵커 존재 | 앵커 없음, 가격 자체가 유일 정보 | 역추세보다 모멘텀/추세추종 우세 |
| **참여자** | 기관/연기금 비중 높음 | 리테일/고위험 선호, 소셜 영향 큼 | 패턴 실패율 높음, 확인 신호 엄격 |

### 지표별 튜닝 포인트 (실증 연구 근거 포함)

**이동평균(MA):**
- 주식: 50/200일선이 기관 의식 수준의 대표 지표
- 코인: "정확한 선"보다 "±몇% 범위의 존(zone)" 개념으로 봐야 함
- ML 관점: SMA_50/200이 XGBoost 피처 중요도 1~2위 (RSIS 2025)
- 튜닝: 타임프레임(4H/1D) + 기간 동시 조정, 단기 MA(5/10)는 노이즈 수준

**RSI/오실레이터:**
- 주식: 70/30 기준 역추세 전략이 통계적으로 유효
- 코인: 과매수 구간에 "며칠~몇 주" 체류 관찰 (PMC 2023), 30/70 규칙은 고위험
- 코인 연구 결과: "교과서와 반대로(역-RSI)" 접근해야 하는 경우도 있음
- 튜닝: 80/20 또는 85/25 + 레짐 구분 (상승장 40~80 정상, 하락장 20~60 정상)
- 다이버전스: 실증 연구에서 "복잡한 대비 효과 제한적, 고위험" 평가

**MACD/모멘텀:**
- 코인: 급등/급락으로 크로스 신호 과다 발생, 가짜 신호 빈번
- MACD vs RSI 비교 (ASJP 2023): MACD는 추세 포착, RSI는 과매수/과매도 포착에 강점
- 튜닝: 12-26-9 기본 → 20-50-10 등 기간 확대, 거래량/브레이크아웃과 결합 필터링

**볼린저/변동성:**
- 주식: 밴드 터치 = 역추세 해석이 주류
- 코인: 밴드 상단 돌파가 추세 시작 시그널인 경우 빈번
- ML 관점: BBW(밴드폭)가 레짐 감지 핵심 피처 (추세/횡보/브레이크아웃 구분)
- 튜닝: 밴드 터치보다 밴드폭 축소→확대 "상태 변화"를 주요 피처로 활용

**거래량/오더북/심리:**
- 코인: wash trade 가능성, 거래소 간 분산 → 단일 거래소 거래량 신뢰도 낮음
- 오더북: 코인은 API로 쉽게 접근 가능, bid/ask imbalance가 유효한 피처
- 센티먼트: 기술지표+감성 혼합 시 RMSE/정확도 개선 (Arslan 2025)

### 설계 원칙 (이 분석에서 도출)

1. **계산 엔진과 해석 엔진 분리**: 수학은 공유, 파라미터/해석은 프로젝트별 독립
2. **리스크 엔진 > 시그널 엔진**: 코인은 "맞출 확률"보다 "틀렸을 때 빨리 빠지기"가 생존 핵심
3. **백테스트와 전략 개발 동시 진행**: 전략 만들면서 바로 코인 데이터로 검증, 반복 루프
4. **전략 코드 비공유**: stock-predictor 전략을 "참고"하되, 코인용은 독립 구현 + 독립 백테스트
5. **ML이 메인, 규칙이 fallback**: 단일 지표 규칙은 코인에서 비효율적 (실증 연구 근거)

---

## 실증 연구 기반: ML + 지표 활용 전략

### 핵심 발견 (2024-2026 논문 종합)

**1. 단일 지표 규칙 < ML 피처 조합**
- 전통적 "RSI 70/30 매매"는 코인에서 고위험/비효율 (PMC 2023)
- 기술지표를 ML 분류기 피처로 넣으면 92%+ 방향 예측 정확도 (Hafid 2024, arxiv)
- SMA_50/200 + RSI + MACD + 볼린저를 XGBoost 앙상블로 → 90.4% 정확도 (RSIS 2025)

**2. 3축 피처 구조가 표준화 추세**
- 축 1 (기술지표): SMA, RSI, MACD, BB — ML 모델의 핵심 입력
- 축 2 (센티먼트): 뉴스/SNS 감성 추가 시 RMSE/정확도 유의미 개선 (Arslan 2025)
- 축 3 (온체인/시장구조): 리스크 프리미엄 예측력 추가 향상 (Freitas 2025)
- 기술지표만 < 기술지표+센티먼트 < 기술지표+센티먼트+온체인

**3. 레짐 구분이 필수**
- 같은 RSI 70이 상승장에서는 "더 갈 구간", 횡보장에서는 "과열"
- BBW/ATR 기반 레짐 감지로 모델 해석을 전환해야 함
- 레짐별 모델 분할 또는 레짐을 피처로 추가

**4. 딥러닝에서도 지표 피처가 유효**
- LSTM/CNN에 원시 OHLCV만 vs 기술지표 추가: 거의 모든 연구에서 지표 추가 시 성능 향상
- 코인의 높은 변동성/비정상성 때문에 지표 피처의 기여도가 주식보다 더 큼

### 시그널 엔진 설계 (연구 기반)

```
[피처 엔진]
├── 기술지표 (SMA_50/200, RSI_14, MACD, BBW, ATR, OBV)
├── 센티먼트 (Fear&Greed, 뉴스 감성 점수)
└── 시장구조 (오더북 imbalance, 거래량 구조)
         │
         ↓
[레짐 감지] → 현재 시장 상태 (추세/횡보/고변동성)
         │
         ↓
[ML 앙상블] → XGBoost + LSTM 예측 (방향 + 확신도)
         │
         ├── 확신도 높음 → 시그널 생성
         └── 확신도 낮음 → 대기 또는 규칙 기반 fallback
                              │
                              ↓
                    [리스크 엔진] → 최종 주문 승인/거부
```

### ML 모델 후보 (연구 결과 기반)

| 모델 | 용도 | 근거 |
|---|---|---|
| XGBoost/LightGBM | 방향 예측 (빠른 실험, 해석 가능) | RSIS 2025: 90.4% 정확도 |
| LSTM | 시계열 패턴 포착 | 복수 연구에서 기술지표 피처 추가 시 성능 향상 |
| 앙상블 (LR+XGBoost) | 안정성 확보 | RSIS 2025: 단일 모델보다 앙상블이 우수 |

### 참고 논문

- Hafid et al. (2024): "Predicting Market Trends with Enhanced Technical Indicator Integration" — arxiv 2410.06935
- RSIS (2025): "Bitcoin Closing Price Prediction Model using ML" — Ensemble LR+XGBoost
- Freitas (2025): "Market sentiment and crypto risk premium" — ScienceDirect
- Arslan (2025): "Bitcoin Price Prediction Using Sentiment Analysis and Technical Indicators" — Computational Economics
- PMC (2023): "Effectiveness of RSI Signals in Timing Markets" — PMC 9920669
- CFA Bitcoin Prediction (2025): "Combinatorial Fusion Analysis" — arxiv 2602.00037

### 참고 출처
- [FinanceFeeds: Does TA Work Better for Crypto?](https://financefeeds.com/does-technical-analysis-work-better-for-crypto/)
- [Bitsgap: Stocks vs Crypto Trading](https://bitsgap.com/blog/stocks-vs-crypto-trading-the-similarities-and-differences)
- [Cryptohopper: TA Comparison Stocks vs Crypto](https://www.cryptohopper.com/blog/technical-analysis-comparison-stocks-versus-crypto-12173)
- [Alpha Architect: Are Cryptos Different?](https://alphaarchitect.com/are-cryptos-different/)

---

## 참고 자료

- [업비트 개발자 센터](https://docs.upbit.com/)
- [업비트 REST API Best Practice](https://docs.upbit.com/kr/docs/rest-api-best-practice)
- [업비트 WebSocket Best Practice](https://global-docs.upbit.com/docs/websocket-best-practice)
- [CCXT 업비트 연동 가이드](https://global-docs.upbit.com/docs/ccxt-library-integration-guide)
- [가상자산이용자보호법](https://www.law.go.kr/lsInfoP.do?lsId=014474)
- [금감원 분 단위 감시 발표 (2025.10)](https://www.mbn.co.kr/news/economy/5149771)

---

*마지막 업데이트: 2026-02-18 (실증 연구 기반 3축 피처/ML 아키텍처 추가, 독립 리포 구조로 변경)*
