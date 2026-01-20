# Claude Code Skills 분석

> 분석일: 2026-01-20
> 상태: 연구 완료
> 태그: #AI #Claude #Skills #코드리뷰 #자동화

---

## 개요

Claude Code Skills는 Claude Code 환경에서 커뮤니티가 만든 스킬을 설치하고 슬래시 커맨드로 사용할 수 있는 시스템이다.

```
npx skillscokac -i vercel-react-best-practices
                   ↓
/vercel-react-best-practices 슬래시 커맨드 사용 가능
                   ↓
React/Next.js 성능 체크, 코드 리뷰 자동화
```

## 핵심 개념

### 스킬이란?
- 특정 도메인의 규칙/체크리스트를 **실행 가능한 형태**로 패키징
- 슬래시 커맨드로 즉시 호출
- 코드 분석, 리뷰, 개선 제안 자동화

### RLM과의 연결점

| 개념 | Claude Skills | RLM |
|-----|--------------|-----|
| 지식 접근 | 스킬 패키지 로드 | 선택적 컨텍스트 로드 |
| 활성화 방식 | 슬래시 커맨드 | 프로그래밍적 탐색 |
| 효율성 | 필요한 스킬만 로드 | 필요한 문서만 로드 |

---

## Stock Predictor 전용 스킬 제안

### 1. `/sp-backend-rules`

**목적**: FastAPI 백엔드 코드 규칙 검사

**포함 규칙**:
```
- 하드코딩 금지 (API 키, URL 등)
- API 에러 로깅 패턴 준수
- Pydantic 모델 필수
- 캐시 TTL 명시
- 비동기 함수 우선
```

**사용 예시**:
```
/sp-backend-rules 이 엔드포인트 검토해줘
→ "하드코딩된 URL 발견: line 45"
→ "에러 로깅 누락: exception handler 추가 권장"
```

### 2. `/sp-frontend-rules`

**목적**: React 프론트엔드 최적화 검사

**포함 규칙**:
```
- React 18 최적화 (useMemo, useCallback)
- Ant Design 사용 패턴
- SSE 스트리밍 처리
- 타입 정의 필수
```

### 3. `/sp-screening-patterns`

**목적**: 스크리닝 로직 검증

**포함 규칙**:
```
- 토너먼트 스크리닝 4단계 구조
- 섹터별 기준 동적 적용
- YoY 분석 패턴
- 캐시 우선 조회
```

---

## Universal DevKit 스킬 제안

### 1. `/devkit-pre-work`

**목적**: 작업 시작 전 체크리스트

**내용**:
```
[ ] AGENT_CONTEXT.md 확인
[ ] 현재 브랜치 확인
[ ] 관련 케이스 스터디 검색
[ ] CRITICAL 규칙 리마인드
```

### 2. `/devkit-post-work`

**목적**: 작업 완료 후 체크리스트

**내용**:
```
[ ] CHANGELOG 업데이트
[ ] 커밋 메시지 컨벤션 확인
[ ] 케이스 스터디 작성 여부
[ ] experience-db 패턴 추가 여부
```

### 3. `/devkit-case-study`

**목적**: 케이스 스터디 템플릿 제공

**내용**:
```markdown
# [제목]

**날짜**: YYYY-MM-DD
**프로젝트**: 
**태그**: 

## 배경
## 핵심 발견
## 교훈
## 관련 파일
## 다음 단계
```

---

## 기대 효과

| 항목 | 현재 | Skills 적용 후 |
|------|------|----------------|
| 규칙 참조 | 매번 파일 열기 | 슬래시 커맨드로 즉시 |
| 코드 리뷰 | 수동 체크 | 자동 패턴 검사 |
| 새 에이전트 온보딩 | 문서 읽기 | 스킬 실행으로 컨텍스트 로드 |
| 규칙 위반 탐지 | 사후 발견 | 사전 경고 |

---

## 구현 로드맵

```
Phase 1: 커뮤니티 스킬 적용 (즉시)
  - vercel-react-best-practices 설치
  - 프론트엔드 코드 체크

Phase 2: 자체 스킬 개발 (1주)
  - AGENT_CONTEXT.md → sp-context 스킬 변환
  - CODING_GUIDELINES.md → sp-rules 스킬 변환

Phase 3: 스킬 허브 구축 (2주)
  - idea-vault/skills/ 폴더에 스킬 정의
  - 버전 관리 + 배포 자동화
```

---

## 주의사항

1. **Claude Code 의존성**
   - Cursor IDE에서 Claude 사용 시에만 적용
   - 다른 AI (GPT, Gemini)에서는 사용 불가

2. **스킬 유지보수**
   - 규칙 변경 시 스킬도 업데이트 필요
   - 버전 관리 필요

3. **커뮤니티 vs 자체 스킬**
   - 커뮤니티: 검증된 베스트 프랙티스
   - 자체: 프로젝트 특화 규칙

---

## 성공 지표 (KPIs)

- [ ] 코드 리뷰 시간 50% 단축
- [ ] 규칙 위반 사전 탐지율 90%
- [ ] 새 에이전트 온보딩 시간 30분 → 5분

---

## 참고 자료

- [SkillsCokac Platform](https://skillscokac.com)
- Claude Code 공식 문서
