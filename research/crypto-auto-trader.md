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

### 업비트 API 실전 이슈 (2025-2026 리서치)

| 이슈 | 상세 | 대응 |
|---|---|---|
| **PyJWT 2.0+ 호환성** | `jwt.encode()` 반환 타입 변경 (bytes→str) | 버전별 분기 또는 `.decode('utf-8')` 처리 |
| **Rate Limit 정정** | 공식: Public 30 req/sec, Private 8 req/sec | CCXT의 기본 rate limiter + 자체 버퍼 |
| **Query Hash** | SHA-512, URL 파라미터 알파벳 정렬 필수 | CCXT가 처리하지만 직접 호출 시 주의 |
| **Nonce** | UUID 기반, replay attack 방지 | 매 요청 새 UUID 생성 |
| **API 안정성** | 2019년 이후 인증 스킴 변경 없음 | 장기 프로젝트에 적합 (바이낸스 대비 안정) |
| **라이브러리** | `upbit-client` (2026.01 최신, 36 releases) | CCXT 우선, 필요 시 upbit-client 보조 |

> CCXT가 대부분 처리하지만, 직접 REST 호출이 필요한 경우(WebSocket 인증 등) 위 이슈를 알아야 한다.

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
- **AI/ML**: scikit-learn, XGBoost, LightGBM, PyTorch (향후 LSTM)
- **모델 해석**: SHAP (피처 중요도 투명 공개, CatBoost/XGBoost와 호환)
- **레짐 감지**: hmmlearn (HMM), arch (GARCH-MIDAS)
- **알림**: python-telegram-bot (텔레그램 알림 체계)
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
- **레짐 감지 모듈** (변동성/추세/횡보 구분):
  - 1차: BBW + ATR 기반 규칙 (빠른 구현, 해석 가능)
  - 2차: Hidden Markov Model (hmmlearn 또는 hidden-regime 패키지)
    - 입력: log returns → HMM 2~4 상태 분류
    - 상태 수 결정: AIC/BIC 기준 모델 선택
    - Baum-Welch(파라미터 추정) + Viterbi(레짐 추론)
    - GARCH-MIDAS + HMM 조합으로 단기/장기 변동성 분리 (2025 연구)
  - 레짐 결과를 ML 피처로 투입 + 메타 컨트롤러 입력으로 사용

### Phase 3: ML 파이프라인 (3~4주)
- **모델 출력 제한**: 수익률 값이 아닌 "방향(Up/Down/Flat) + 확신도(0~1)"만 출력
  - 근거: 수익률 크기 R²≈0 (Mohtashami Zadeh 2026), 방향 정확도만 유의미
- **멀티 모델 앙상블**: 단일 LSTM 올인 금지
  - XGBoost/LightGBM (빠른 실험, 해석 가능)
  - 단순 모멘텀/MA 규칙 전략
  - 얕은 NN (선택)
  - LSTM은 후보 중 하나일 뿐, 자동 우승자 아님
- **메타 컨트롤러**: 최근 OOS 성과 + 레짐 기반으로 각 모델 가중치 동적 조정
  - 특정 레짐에서 한 모델 성능 하락 → 자동으로 weight 감소/off
  - 근거: "보편적 우등생 모델 없음" (Boozary 2025, Qureshi 2025)
- 시간 기반 train/validation/test, 롤링 워크포워드
- 규칙 기반 전략은 ML fallback으로 유지
- Signal Tracker 연동 (시그널 정확도 자동 추적)

### Phase 4: 실행 엔진 + 리스크 (3~4주)
- Paper Trading 먼저 (ML 모델 시그널로 시뮬레이션)
- CCXT 통한 주문 실행 (시장가/지정가)
- **SmartTrade 스타일 조건부 주문**: 복합 TP/SL + 트레일링 (3Commas 벤치마킹)
- **리스크 기반 포지션 사이징** (3계층):
  - Layer 1: Fixed-Fractional (계좌의 0.5~2% 리스크/트레이드)
  - Layer 2: ATR-based 조정 (Units = Account × Risk% / ATR × multiplier)
    - 변동성 높으면 자동 축소, 낮으면 확대 → 리스크 정규화
  - Layer 3: Kelly-Lite (Dynamic Kelly + 드로우다운 스케일링)
    - 순수 Kelly는 드로우다운 과대 → Half-Kelly 또는 드로우다운 비례 축소
  - 전략 로직(진입/청산)과 사이징 로직 완전 분리 (모듈 교체 가능)
- 리스크 엔진: max %, 일일 한도, MDD 정지
- 가장매매 방지 로직
- 모델 드리프트 모니터링 (성능 하락 시 자동 fallback)

### Phase 5: 내부 벤치마크 + 모델 승급 체계 (2~3주)
- **벤치마크 프레임워크**: 모든 모델/전략 버전을 동일 기준으로 자동 비교
  - 평가 지표: PnL, Sharpe, Sortino, MDD, 승률, 비용 포함 turnover
  - RMSE/Accuracy는 참고만 (논문식 지표 ≠ 실전 성과)
  - 근거: 대부분 연구가 실전 PnL 평가 부족 (Qureshi 2025)
- **모델 승급 프로세스**: 새 모델은 소액 샌드박스 → 일정 기간 OOS 성과 → 메인 승급
- 표준 피처 세트 + 실험 로그/코드 버전 관리 (내부 재현성 확보)

### Phase 6: 운영 + 대시보드 + 확장 (장기)
- 소액 Live → 단계적 확대
- **실시간 대시보드** (상용 봇 UX 벤치마킹):
  - PnL 트래커 (일별/누적, 코인별 breakdown)
  - 포지션 뷰 (현재 보유, 진입가, 손익, 청산 조건)
  - 주문 히스토리 + 실행 상태
  - 모델별 시그널 투명 공개 (확신도, 피처 중요도)
  - 전략 모드 전환 UI (백테스트 / 페이퍼 / 실전)
- **알림 체계**: 텔레그램/푸시 (손실 한도 접근, 오류, 주문 실패, MDD 경고)
- 온체인 데이터 통합 (축 3 확장)
- 멀티 코인/멀티 전략 확장
- 전략 템플릿 라이브러리 (DCA, 그리드, 모멘텀 등 모듈화)

---

## 아키텍처 원칙

1. **독립 프로젝트, 지식은 공유** — stock-predictor와 별도 리포, universal-devkit 경유 패턴/경험 공유
2. **KIRA 교훈의 올바른 적용** — KIRA는 "같은 도메인 내 사일로"라서 실패, 코인은 다른 도메인이므로 독립이 정답
3. **계산과 해석의 분리** — 지표 수학 공식은 참고 가능, 파라미터/해석/전략은 코인 전용으로 독립 구현
4. **리스크 엔진 우선** — 시그널보다 리스크 관리가 상위 레이어, 포지션 크기는 리스크 모델이 결정
5. **방향 예측만, 크기 예측은 과신 금지** — 모델 output은 방향+확신도, 수익률 크기 예측 R²≈0 (실증 근거)
6. **단일 모델 올인 금지** — 멀티 모델 앙상블 + 메타 컨트롤러로 레짐 변화 대응
7. **실전 PnL 기준 평가** — RMSE/Accuracy가 아닌 Sharpe/MDD/비용 포함 성과로 모델 평가
8. **모델 승급 프로세스** — 새 모델은 샌드박스 → OOS 검증 → 메인 승급 (바로 라이브 금지)
9. **Paper Trading 필수** — 실거래 전 반드시 시뮬레이션 검증
10. **백테스트 없이 라이브 없다** — 코인 데이터로 재보정하지 않은 전략은 실거래 금지
11. **상용 봇 UX 벤치마킹** — AI/ML은 직접, 운영 안정성/UX 패턴은 상용 봇(3Commas, Cryptohopper) 적극 참고
12. **투명성 > 블랙박스** — 모든 시그널에 피처 중요도·확신도 공개, "왜 이 판단인지" 사용자가 볼 수 있어야 함

---

## 오픈소스 & 상용 봇 비교 결론

### 오픈소스 프레임워크

| 옵션 | 판단 |
|---|---|
| Freqtrade (46K stars) | 기존 시스템과 통합 어려움 |
| Jesse (7K stars) | 깔끔하지만 별도 생태계 |
| Hummingbot (오픈소스) | 마켓메이킹 특화, 범용 봇으로는 과잉 |
| **CCXT + 자체 구축** | 기존 인프라 활용 + 확장성 최적 |

### 상용 봇 벤치마킹 (2026 기준)

상용 봇의 "AI"는 실제로는 규칙+자동화+약간의 추천 수준. ML 트레이더가 아님.

**벤치마킹 대상 (운영 안정성/UX):**
- 전략 템플릿 모듈화 (DCA, 그리드, 모멘텀 — 3Commas/Cryptohopper 수준)
- 백테스트 → 페이퍼 → 실전 3단계 모드
- 실시간 대시보드 (PnL, 포지션, 주문, 레버리지)
- 알림 체계 (텔레그램/푸시 — 손실 한도 접근, 오류, 주문 실패)
- 리스크 관리 UI (TP/SL, 트레일링, 일일 한도)
- SmartTrade 스타일 조건부 주문 (3Commas 참고)

**상용 봇 대비 차별점:**

| 상용 봇 | 우리 설계 |
|---|---|
| 프리셋 전략 추천, IF-THEN 규칙 | 3축 피처 기반 ML 앙상블 |
| 단일 전략 고정 실행 | 메타 컨트롤러: 레짐별 가중치 동적 조정 |
| "AI가 추천" (블랙박스) | 모델별 확신도 + 피처 중요도 투명 공개 |
| 모델 성능 하락 시 수동 대응 | 자동 fallback + 모델 승급 프로세스 |
| RMSE/백테스트 수익률 표시 | 실전 PnL/Sharpe/MDD 벤치마크 프레임워크 |

**자체 개발 근거:**
1. 업비트 전용 — 상용 봇들의 업비트 지원 제한적
2. AI 깊이 — 상용 "AI"는 우리 설계 수준의 ML이 아님
3. 완전한 통제 — 전략/모델/리스크 소스코드 레벨 관리
4. 기존 인프라 — FastAPI, PostgreSQL, 모니터링 체계 보유

CCXT 라이브러리만 활용하고 나머지는 자체 구축. 상용 봇의 UX/운영 패턴은 적극 벤치마킹.

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

### 시그널 엔진 설계 (연구 기반, v2 — 메타 컨트롤러 포함)

```
[피처 엔진 (3축)]
├── 기술지표 (SMA_50/200, RSI_14, MACD, BBW, ATR, OBV)
├── 센티먼트 (Fear&Greed, 뉴스 감성 점수)
└── 시장구조 (오더북 imbalance, 거래량 구조)
         │
         ↓
[레짐 감지] → 현재 시장 상태 (추세/횡보/고변동성)
         │
         ↓
[멀티 모델 레이어]
├── 모델 A: XGBoost (방향 + 확신도)
├── 모델 B: LightGBM (방향 + 확신도)
├── 모델 C: 규칙 기반 모멘텀 (방향 + 확신도)
└── 모델 D: LSTM (선택, 방향 + 확신도)
         │
         ↓
[메타 컨트롤러] → 최근 OOS 성과 + 레짐에 따라 각 모델 가중치 동적 조정
         │         성능 나쁜 모델은 weight↓ 또는 off
         ↓
[최종 시그널] → 방향(Up/Down/Flat) + 가중 확신도
         │
         ↓
[리스크 엔진] → 포지션 크기 결정 (ATR/변동성/계좌% 기반)
         │       모델은 방향만, 크기는 리스크가 결정
         │       일일/주간 손실 한도, MDD 체크
         ↓
[실행 엔진] → 주문 전송 또는 대기
```

### ML 모델 후보 (연구 결과 기반)

| 모델 | 용도 | 주의 | 근거 |
|---|---|---|---|
| XGBoost/LightGBM | 방향 예측 (빠른 실험, 해석 가능) | 첫 번째 시도 추천 | RSIS 2025: 90.4% |
| 규칙 기반 (MA/모멘텀) | fallback + 앙상블 멤버 | 항상 유지 | 레짐에 따라 ML보다 우수할 수 있음 |
| 앙상블 (LR+XGBoost) | 안정성 확보 | 단일 모델보다 안정 | RSIS 2025 |
| LSTM/GRU | 시계열 패턴 | **항상 이기지 않음** | 단기에서 SVR에 밀리기도 (2026 연구) |

---

## 온체인 데이터: 현실적 평가 (2025-2026 리서치)

### 핵심 결론
온체인 데이터는 **보조 피처**로 활용하되, 단독 시그널로는 신뢰도 부족.

### Whale Alert의 한계
- 대형 거래소 입금의 가격 예측력: R² = 0.0017~0.0537 (Presto Research 2025)
- 개별 대형 거래는 OTC 데스크, 커스토디 이동, 거래소 내부 재편일 가능성이 높음
- "고래가 움직였다 = 매도 신호"는 과대 해석

### 유효한 온체인 지표 (우선순위)
| 지표 | 유효성 | 적용 방법 |
|---|---|---|
| **거래소 순유입/유출 (7-30일 추세)** | 높음 | 지속적 유출 = 매집 신호, 추세가 중요 (개별 건 아님) |
| **스테이블코인 거래소 유입** | 중간-높음 | 대량 USDT/USDC 유입 = 매수 준비 가능성 |
| **코인 연령별 분석** | 중간 | 3년+ 미이동 코인 이동 vs 최근 이동 코인 — 의미가 다름 |
| **NVT Ratio** | 중간 | 네트워크 가치 대비 거래량 — 과대/과소 평가 판단 |
| **단발성 Whale Alert** | 낮음 | 노이즈 수준, 단독 시그널로 사용 금지 |

### 설계 반영
- Phase 2의 축 3(시장구조)에서 온체인은 **후순위**로 유지 (기존 결정 유효)
- 초기: 오더북 imbalance + 거래량 구조에 집중
- 확장 시: 거래소 순유입/유출 7일 이동평균 + 스테이블코인 유입을 피처로 추가
- Whale Alert 단독 트리거는 절대 금지

---

## 모델 투명성: SHAP 기반 해석 (2025 리서치)

### 왜 필요한가
- 아키텍처 원칙 #12 "투명성 > 블랙박스"의 구체적 구현
- 상용 봇이 "AI가 추천합니다" 블랙박스인 것과의 핵심 차별점
- 규제 대응: "왜 이 시점에 이 매매를 했는지" 설명 가능

### SHAP 적용 계획
| 적용 대상 | 방법 | 용도 |
|---|---|---|
| XGBoost/LightGBM | TreeSHAP (빠름) | 매 시그널별 피처 기여도 실시간 계산 |
| LSTM/NN (향후) | DeepSHAP/KernelSHAP | 비용 높아 배치 처리 |
| 대시보드 표시 | 글로벌 + 로컬 SHAP | 전체 트렌드 + 개별 판단 근거 |

### 실전 활용 (2025 연구 근거)
- CatBoost/XGBoost + SHAP: 코인 마이크로스트럭처 분석에서 피처 랭킹 자산 간 안정적 (arxiv 2025)
- Order flow imbalance, bid-ask spread, depth가 일관되게 중요 피처
- **레짐 진단**: 스트레스 기간에 매크로 변수 중요도가 급등 → 레짐 전환 감지 보조 활용
- **Quant-Safe 프레임워크** (2026): point-in-time 피처 엔지니어링 + walk-forward SHAP → 데이터 누수 방지

### 대시보드 표시 설계
```
시그널 상세 뷰 (예시):
┌─────────────────────────────────────────┐
│ BTC/KRW  방향: UP  확신도: 0.73         │
│                                          │
│ 피처 기여도 (SHAP):                      │
│ ██████████ RSI_14      +0.15            │
│ ████████   SMA_200     +0.12            │
│ ██████     BBW         +0.09            │
│ █████      F&G_Index   +0.07            │
│ ███        OBV_trend   +0.04            │
│ ▓▓         Orderbook   -0.03            │
│                                          │
│ 레짐: 추세 상승 | 모델: XGBoost(w=0.4)  │
│        + LightGBM(w=0.35) + Rules(w=0.25)│
└─────────────────────────────────────────┘
```

---

## 텔레그램 알림 체계 설계

### 기술 스택
- `python-telegram-bot` (비동기 지원, Telegram Bot API)
- BotFather에서 봇 생성 → 토큰 발급
- 환경변수로 토큰/채팅 ID 관리 (하드코딩 금지)

### 알림 유형 (우선순위)

| 유형 | 트리거 | 긴급도 |
|---|---|---|
| **MDD 경고** | MDD가 설정 한도의 80% 도달 | CRITICAL |
| **자동 정지** | MDD 한도 초과, 일일 손실 한도 초과 | CRITICAL |
| **주문 실패** | API 에러, 잔고 부족, 체결 실패 | HIGH |
| **시스템 에러** | WebSocket 끊김, DB 연결 실패, 프로세스 크래시 | HIGH |
| **시그널 발생** | 확신도 임계값 이상의 매수/매도 시그널 | MEDIUM |
| **체결 알림** | 주문 체결 완료 (가격, 수량, 수수료) | MEDIUM |
| **일일 리포트** | 일일 PnL, 거래 횟수, 승률 요약 | LOW |
| **모델 드리프트** | 모델 성능 하락 감지 (fallback 전환) | MEDIUM |

### 구현 주의사항
- 텔레그램 메시지 4000자 제한 → 긴 리포트는 분할 전송
- 중복 알림 방지 (동시 요청 플래그 관리)
- 알림 빈도 제한 (분당 최대 N건) — 시그널 폭주 시 요약 모드

---

## 2026 연구 기반: 한계 인식 & 대응 설계

### 공통 한계 (2024-2026 논문 종합)

| 한계 | 근거 | 현실적 의미 |
|---|---|---|
| 수익률 크기 예측 R²≈0 | Mohtashami Zadeh 2026 (bmfopen) | "내일 5% 오른다"는 예측은 의미 없음 |
| 복잡한 딥러닝 ≠ 항상 우수 | 같은 연구: LSTM이 SVR에 밀리는 경우 존재 | LSTM 올인은 위험 |
| 레짐 변화 시 모델 일반화 실패 | Boozary 2025 (ScienceDirect), Qureshi 2025 (PeerJ) | 한 장세에서 좋은 모델이 다른 장세에서 깨짐 |
| 피처 선택이 주관적/비교 불가 | Qureshi 2025 | 표준 피처 세트 미확립 |
| 평가가 RMSE/Accuracy 편향 | Qureshi 2025, Boozary 2025 | 실전 PnL/리스크 평가 부족 |
| 짧은 기간/소수 코인/재현성 부족 | 복수 리뷰 논문 | 일반화 어려움 |
| 시장조작/규제/이벤트 리스크 미반영 | Qureshi 2025 | 모델이 예측 못하는 외생 충격 |

### 한계-대응 매핑 (우리 설계)

| 한계 | 대응 |
|---|---|
| 수익률 크기 예측 불가 | 모델 출력을 방향+확신도로 제한, 크기는 리스크 모델이 결정 |
| 모델마다 레짐마다 성능 요동 | 멀티 모델 앙상블 + 메타 컨트롤러 (레짐별 가중치 동적 조정) |
| 피처 선택 주관적 | 표준 피처 세트 정의 + 내부 벤치마크 프레임워크 |
| 기술지표만으로 부족 | 3축 피처 통합 (TA + 센티먼트 + 시장구조) |
| RMSE/Accuracy 편향 평가 | PnL, Sharpe, MDD, 비용 포함 실전 성과로 모든 모델 평가 |
| 재현성 부족 | 실험 로그/코드 버전/데이터 기간 문서화, 내부 벤치마크 |
| 이벤트 리스크 미반영 | 리스크 엔진에 유동성/스프레드/규제뉴스 변수 포함 |

### 현실적 기대치

- "정확한 수익률 예측"은 포기. "방향 + 리스크 제어"에 집중
- 논문 92% 정확도는 특정 기간/코인/조건에서의 결과. 일반화 보장 아님
- 학술 수준에서 "모든 한계를 해결한 실거래 검증 AI 봇" 사례는 아직 없음
- 우리가 할 일: 논문이 제안하는 개선 방향을 설계에 녹여서 **한계를 "극복"이 아닌 "우회"**

### 참고 논문 (추가)

- Mohtashami Zadeh (2026): "Short-term crypto prediction comparison" — BMF Open
- Boozary (2025): "Bitcoin prediction ML systems review" — ScienceDirect
- Qureshi (2025): "Cryptocurrency prediction models comparison" — PeerJ CS
- Dubey (2025): "Bitcoin direction prediction using on-chain data" — ScienceDirect
- Visharad (2025): "Stablecoin prediction with TA+ML" — ScienceDirect
- Trade Pilot (2025): "AI Crypto Trading Bot" — IJRPR

### 참고 출처
- [FinanceFeeds: Does TA Work Better for Crypto?](https://financefeeds.com/does-technical-analysis-work-better-for-crypto/)
- [Bitsgap: Stocks vs Crypto Trading](https://bitsgap.com/blog/stocks-vs-crypto-trading-the-similarities-and-differences)
- [Cryptohopper: TA Comparison Stocks vs Crypto](https://www.cryptohopper.com/blog/technical-analysis-comparison-stocks-versus-crypto-12173)
- [Alpha Architect: Are Cryptos Different?](https://alphaarchitect.com/are-cryptos-different/)

---

## 참고 자료

### 업비트 & 규제
- [업비트 개발자 센터](https://docs.upbit.com/)
- [업비트 REST API Best Practice](https://global-docs.upbit.com/docs/rest-api-best-practice)
- [업비트 WebSocket Best Practice](https://global-docs.upbit.com/docs/websocket-best-practice)
- [CCXT 업비트 연동 가이드](https://global-docs.upbit.com/docs/ccxt-library-integration-guide)
- [python-upbit-client (GitHub)](https://github.com/uJhin/python-upbit-client)
- [TildAlice: Upbit Trading Bot Setup](https://tildalice.io/upbit-trading-bot-setup-auth/)
- [가상자산이용자보호법](https://www.law.go.kr/lsInfoP.do?lsId=014474)
- [금감원 분 단위 감시 발표 (2025.10)](https://www.mbn.co.kr/news/economy/5149771)

### 상용 봇 & 벤치마킹
- [altfins: Best Crypto Trading Bots 2025](https://altfins.com/knowledge-base/best-crypto-tradings-bots-2025/)
- [WestAfricaTradeHub: Best AI Crypto Trading Bots](https://westafricatradehub.com/crypto/best-ai-crypto-trading-bots/)
- [Growlonix: Top 11 Crypto Trading Bots](https://www.growlonix.com/support/article/top-11-crypto-trading-bots-features-and-reviews)
- [CoinLaunch: Best Crypto Trading Bots](https://coinlaunch.space/blog/best-crypto-trading-bots/)

### 레짐 감지 & HMM
- [crypto_vol_regimes (GitHub)](https://github.com/jonatansator/crypto_vol_regimes)
- [hidden-regime PyPI](https://pypi.org/project/hidden-regime/2.0.0/)
- [QuantStart: HMM Market Regime Detection](https://www.quantstart.com/articles/market-regime-detection-using-hidden-markov-models-in-qstrader/)
- [Springer: Regime Switching Forecasting for Cryptocurrencies (2024)](https://link.springer.com/article/10.1007/s42521-024-00123-2)

### 온체인 데이터
- [Nansen: Onchain Data for Token Flow Research](https://www.nansen.ai/post/how-to-effectively-use-onchain-data-for-token-flow-research-a-comprehensive-guide)
- [Presto Research: Whale Alerts - Are They Tradable?](https://www.prestolabs.io/research/whale-alerts-are-they-tradable)
- [Katoshi: On-Chain Indicators for Algorithmic Strategy](https://katoshi.ai/blog/on-chain-indicators-for-algorithmic-strategy-development-using-blockchain-analytics-as-trading-signals)

### SHAP & 모델 해석
- [MarketCalls: SHAP for Traders](https://marketcalls.in/machine-learning/demystifying-shap-for-traders-how-to-trust-your-machine-learning-forecast.html)
- [Quant-Safe XAI Framework (2026 preprint)](https://www.preprints.org/manuscript/202601.1636)
- [arxiv: Explainable Patterns in Cryptocurrency Microstructure (2025)](https://arxiv.org/html/2602.00776v1)

### 포지션 사이징 & 리스크
- [PyQuantLab: Dynamic Kelly Sizing for Crypto](https://pyquantlab.medium.com/dual-momentum-selection-with-dynamic-kelly-sizing-for-crypto-portfolio-08b3822cfa29)
- [Ildi Veliu: Position Sizing Frameworks](https://medium.com/@ildiveliu/risk-before-returns-position-sizing-frameworks-fixed-fractional-atr-based-kelly-lite-4513f770a82a)
- [TradingTechAI: ATR Risk Management Bot](https://tradingtechai.medium.com/build-an-advanced-python-trading-bot-with-atr-risk-management-da9354899a58)

---

*마지막 업데이트: 2026-02-18 (상용 봇 벤치마킹 + 레짐 감지 HMM + 온체인 현실 평가 + SHAP 투명성 + 포지션 사이징 3계층 + 업비트 실전 이슈 + 텔레그램 알림 설계)*
