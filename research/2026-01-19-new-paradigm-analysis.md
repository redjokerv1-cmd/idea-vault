# 🚀 New Paradigm Analysis: 우리 프로젝트 적용 방안

**작성일**: 2026-01-19  
**분류**: research  
**상태**: 📋 planned  

---

## 1. MIT RLM (Recursive Language Models) 적용

### 1.1 핵심 개념

```
기존 LLM 방식:
User → [10M 토큰 프롬프트] → Transformer → Output
        (Context Rot 발생)

RLM 방식:
User → [프롬프트를 REPL 환경 변수로] ← LLM (코드 생성)
                ↓                           ↑
            재귀 호출 (Sub-LM) ←────────────┘
```

### 1.2 현재 우리 시스템 분석

**현재 Gemini 호출 방식**:
```python
# gemini_analyzer.py
def analyze_stock(ticker, financial_data, news_summary, ...):
    prompt = f"""
    종목: {stock_name}
    재무 데이터: {financial_data}
    뉴스 100개: {news_summary}  # ← 모든 데이터를 한 번에 전달
    ...
    """
    return self.model.generate_content(prompt)
```

**문제점**:
- 뉴스 100개 전체를 프롬프트에 포함 → Context 비효율
- 재무 데이터 양이 증가하면 품질 저하 가능
- 복잡한 비교 분석 (섹터 평균 vs 개별 종목) 어려움

### 1.3 RLM 적용 방안

**적용 아이디어**: Gemini가 Python 코드를 생성하여 데이터 탐색

```python
# 새로운 방식: RLM 기반 Gemini Analyzer
class RLMGeminiAnalyzer:
    def analyze_stock(self, ticker: str):
        # 1. 데이터를 REPL 환경에 로드 (Gemini에게 메타데이터만 전달)
        context = {
            "news_list": self.fetch_news(ticker),  # 100개
            "financial": self.fetch_financial(ticker),
            "technical": self.fetch_technical(ticker),
        }
        
        # 2. Gemini에게 탐색 코드 생성 요청
        code = self.gemini.generate_exploration_code(
            task="이 종목의 투자 적합성을 분석하라",
            context_metadata={
                "news_count": len(context["news_list"]),
                "available_fields": list(context["financial"].keys())
            }
        )
        
        # 3. 코드 실행 (샌드박스)
        # Gemini가 생성한 코드 예시:
        # ```
        # positive_news = [n for n in news_list if "상승" in n or "호재" in n]
        # debt_ratio = financial["debt_ratio"]
        # if debt_ratio > 150:
        #     sub_analysis = llm_query(f"부채비율 {debt_ratio}%인 기업의 리스크 분석")
        # ```
        
        result = self.execute_in_sandbox(code, context)
        return result
```

### 1.4 기대 효과

| 항목 | 현재 | RLM 적용 후 |
|------|------|-------------|
| 뉴스 처리 | 100개 전체 전달 | 필터링 후 10-20개만 |
| Context 효율 | 30-40% | 80-90% |
| 비용 | $0.05/분석 | $0.02-0.03/분석 |
| 복잡 분석 | 어려움 | 가능 (재귀 호출) |

### 1.5 보완점 및 도전 과제

1. **샌드박스 보안**
   - Gemini가 생성한 코드를 안전하게 실행해야 함
   - RestrictedPython 또는 Docker 격리 필요

2. **코드 품질**
   - Gemini가 유효한 Python 코드를 생성하지 않을 수 있음
   - Syntax error 처리, 재시도 로직 필요

3. **레이턴시**
   - 재귀 호출로 인한 응답 시간 증가
   - 비동기 처리로 완화 가능

### 1.6 구현 우선순위

```
Phase 1 (단기): 뉴스 필터링에만 RLM 적용
  - Gemini가 "관련 뉴스 추출 코드" 생성
  - 100개 → 10-20개 필터링 후 본 분석

Phase 2 (중기): 재무 분석에 RLM 적용
  - 섹터 평균 대비 분석
  - 경쟁사 비교 분석

Phase 3 (장기): 전체 분석 파이프라인 RLM화
  - 토너먼트 스크리닝 + AI 분석 통합
```

---

## 2. n8n AI Workflow Builder 적용

### 2.1 핵심 개념

```
기존 n8n:
노드 수동 연결 → 복잡한 설정 → 테스트 → 배포

AI Workflow Builder:
"슬랙에 이슈 오면 노션에 정리해줘" → 워크플로 자동 생성
```

### 2.2 현재 우리 시스템에서 자동화 가능한 작업

**1. 데이터 수집 자동화**
```
현재 수동:
- yfinance 데이터 수집 (스크리닝 시)
- KIS API 토큰 갱신 (9시간마다)
- 뉴스 API 호출

n8n으로:
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Cron 트리거  │ ──→ │  데이터 수집  │ ──→ │  PostgreSQL  │
│  (매일 6시)   │     │  (yfinance)  │     │   저장       │
└─────────────┘     └─────────────┘     └─────────────┘
```

**2. 신호 검증 자동화**
```
현재 수동:
- 5일 후 신호 정확도 평가 (스케줄러)
- 결과를 DB에 저장

n8n으로:
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Cron (5일)  │ ──→ │  가격 조회   │ ──→ │  정확도 계산  │
└─────────────┘     │  (yfinance)  │     │  + DB 저장   │
                    └─────────────┘     └─────────────┘
                           ↓
                    ┌─────────────┐
                    │  Slack 알림  │
                    │  (정확도 리포트)│
                    └─────────────┘
```

**3. 배포 파이프라인 자동화**
```
현재:
git push → Railway/Vercel 자동 배포 → (수동 확인)

n8n으로:
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ GitHub Push │ ──→ │  빌드 체크   │ ──→ │  Slack 알림  │
│  Webhook    │     │  (API 호출)  │     │  (성공/실패) │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 2.3 기대 효과

| 항목 | 현재 | n8n 적용 후 |
|------|------|-------------|
| 데이터 수집 | Python 스케줄러 | n8n 워크플로 |
| 모니터링 | Railway 로그 확인 | Slack 알림 |
| 배포 확인 | 수동 브라우저 | 자동 헬스체크 |
| 에러 대응 | 로그 발견 시 | 즉시 알림 |

### 2.4 보완점

1. **n8n 호스팅**
   - n8n Cloud (유료) 또는 Self-hosted (Railway/Docker)
   - 비용: Cloud $20/월, Self-hosted 무료

2. **기존 스케줄러와 중복**
   - APScheduler (백엔드)와 n8n 역할 정리 필요
   - 점진적 마이그레이션

3. **Slack 워크스페이스 필요**
   - 현재 없음 → 개설 필요
   - 대안: Discord, Telegram

### 2.5 구현 계획

```
Phase 1: 배포 알림 워크플로
  - GitHub Webhook → n8n → Slack
  - 1일 작업

Phase 2: 신호 검증 워크플로
  - Cron → 가격 조회 → 정확도 계산 → 알림
  - 3일 작업

Phase 3: 전체 모니터링 대시보드
  - API 헬스체크, 에러 알림, 일일 리포트
  - 1주 작업
```

---

## 3. Claude Code Skills 적용

### 3.1 핵심 개념

```
Claude Code 환경에서:
npx skillscokac -i vercel-react-best-practices
                   ↓
/vercel-react-best-practices 슬래시 커맨드 사용 가능
                   ↓
React/Next.js 성능 체크, 코드 리뷰 자동화
```

### 3.2 우리 프로젝트에 필요한 Skills

**1. Stock Predictor 전용 스킬**
```
/sp-backend-rules
  - FastAPI 규칙 (CODING_GUIDELINES.md 기반)
  - 하드코딩 금지 검사
  - API 에러 로깅 패턴

/sp-frontend-rules
  - React 18 최적화
  - Ant Design 사용 패턴
  - SSE 스트리밍 처리

/sp-screening-patterns
  - 토너먼트 스크리닝 로직
  - 섹터별 기준 적용
  - YoY 분석 패턴
```

**2. Universal DevKit 스킬**
```
/devkit-pre-work
  - 작업 시작 전 체크리스트
  - CRITICAL 규칙 리마인드

/devkit-post-work
  - CHANGELOG 업데이트
  - 커밋 메시지 포맷

/devkit-case-study
  - 케이스 스터디 템플릿
  - 경험 기록 가이드
```

### 3.3 기대 효과

| 항목 | 현재 | Skills 적용 후 |
|------|------|----------------|
| 규칙 참조 | 매번 파일 열기 | 슬래시 커맨드로 즉시 |
| 코드 리뷰 | 수동 체크 | 자동 패턴 검사 |
| 새 에이전트 온보딩 | 문서 읽기 | 스킬 실행으로 컨텍스트 로드 |

### 3.4 보완점

1. **Claude Code 의존성**
   - Cursor IDE에서 Claude 사용 시에만 적용
   - 다른 AI (GPT, Gemini)에서는 사용 불가

2. **스킬 유지보수**
   - 규칙 변경 시 스킬도 업데이트 필요
   - 버전 관리 필요

3. **커뮤니티 스킬 vs 자체 스킬**
   - 커뮤니티: vercel-react-best-practices
   - 자체: sp-backend-rules (직접 개발)

### 3.5 구현 계획

```
Phase 1: 커뮤니티 스킬 적용
  - vercel-react-best-practices 설치
  - 프론트엔드 코드 체크

Phase 2: 자체 스킬 개발
  - AGENT_CONTEXT.md → sp-context 스킬 변환
  - CODING_GUIDELINES.md → sp-rules 스킬 변환

Phase 3: 스킬 허브 구축
  - idea-vault/skills/ 폴더에 스킬 정의
  - 버전 관리 + 배포 자동화
```

---

## 4. 종합 로드맵

### 4.1 우선순위 매트릭스

| 개념 | 영향도 | 구현 난이도 | 우선순위 |
|------|--------|------------|----------|
| **n8n 배포 알림** | 높음 | 낮음 | ⭐⭐⭐ 1순위 |
| **Claude Skills 적용** | 중간 | 낮음 | ⭐⭐ 2순위 |
| **RLM 뉴스 필터링** | 높음 | 중간 | ⭐⭐ 2순위 |
| **n8n 신호 검증** | 중간 | 중간 | ⭐ 3순위 |
| **RLM 전체 적용** | 높음 | 높음 | 장기 |

### 4.2 실행 계획

```
Week 1 (즉시):
├── n8n Cloud 가입 또는 Self-hosted 설정
├── GitHub → Slack 배포 알림 워크플로
└── vercel-react-best-practices 스킬 설치

Week 2-3:
├── sp-backend-rules 스킬 개발
├── RLM 뉴스 필터링 POC
└── n8n 신호 검증 워크플로

Month 2:
├── RLM 재무 분석 적용
├── n8n 모니터링 대시보드
└── 전체 스킬 허브 구축
```

---

## 5. 리스크 및 완화 전략

### 5.1 기술적 리스크

| 리스크 | 영향 | 완화 전략 |
|--------|------|-----------|
| RLM 코드 실행 보안 | 높음 | RestrictedPython + Docker 격리 |
| n8n 서버 장애 | 중간 | 기존 APScheduler 폴백 유지 |
| Claude Skills 비호환 | 낮음 | 커뮤니티 스킬만 사용 시 한정 |

### 5.2 비용 리스크

| 항목 | 예상 비용 | 절감 방안 |
|------|----------|-----------|
| n8n Cloud | $20/월 | Self-hosted (Railway) |
| Gemini API (RLM) | +10-20% | 캐싱 강화 |
| Slack Pro | $7/월 | Free tier로 시작 |

---

## 6. 성공 지표 (KPIs)

### 6.1 RLM 적용

- [ ] 뉴스 처리 효율 50% 향상
- [ ] Gemini 비용 30% 절감
- [ ] 복잡 분석 (섹터 비교) 구현

### 6.2 n8n 적용

- [ ] 배포 알림 100% 수신
- [ ] 수동 모니터링 시간 80% 감소
- [ ] 신호 검증 자동화 100%

### 6.3 Claude Skills 적용

- [ ] 코드 리뷰 시간 50% 단축
- [ ] 규칙 위반 사전 탐지율 90%
- [ ] 새 에이전트 온보딩 시간 30분 → 5분

---

## 7. 결론

### 핵심 인사이트

1. **RLM**: "LLM이 탐색 전략을 결정" → Context 효율 혁신
2. **n8n**: "자연어 → 워크플로" → 자동화 진입 장벽 제거
3. **Claude Skills**: "규칙을 실행 가능한 형태로" → 지식 활성화

### 다음 액션

1. **즉시**: n8n 배포 알림 구축 (1일)
2. **이번 주**: RLM 뉴스 필터링 POC (3일)
3. **다음 주**: sp-backend-rules 스킬 개발 (2일)

---

*마지막 업데이트: 2026-01-19*
