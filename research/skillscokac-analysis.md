# SkillsCokac - Claude Code 스킬 공유 플랫폼 분석

**상태**: 📚 research  
**생성일**: 2026-01-20  
**분류**: research  

---

## 개요

Claude Code용 커스텀 스킬(프롬프트/규칙)을 공유하고 발견하는 커뮤니티 플랫폼

---

## 상세 분석

### 플랫폼 특징

| 항목 | 내용 |
|-----|------|
| **URL** | https://skills.cokac.com |
| **목적** | Claude Code 스킬 공유 |
| **설치 방식** | NPX CLI 도구 |
| **커뮤니티** | 공개 (누구나 Fork/Share) |

### 사용 방법

```bash
# 설치
npx skillscokac -i [skill-name]

# 제거
npx skillscokac -r [skill-name]

# Claude Code에서 사용
/[skill-name]
```

### 예시 스킬: vercel-react-best-practices

- Vercel Engineering의 React/Next.js 성능 최적화 가이드라인
- React 컴포넌트, 데이터 페칭, 번들 최적화 작업 시 자동 적용

---

## Universal DevKit과의 비교

| 비교 항목 | Universal DevKit | SkillsCokac |
|----------|------------------|-------------|
| **형태** | Git 리포지토리 | CLI 도구 + 웹 플랫폼 |
| **배포** | 수동 (Git clone) | NPX로 자동 설치 |
| **공유** | Private | Public 커뮤니티 |
| **커스터마이징** | 완전 자유 | 포맷 제한 |
| **버전 관리** | Git 기반 | 플랫폼 관리 |
| **오프라인** | 완전 지원 | 설치 시 인터넷 필요 |

---

## 인사이트 & 아이디어

### 1. DevKit NPX 배포 가능성

```bash
# 아이디어: Universal DevKit을 NPX로 설치 가능하게
npx universal-devkit install stock-predictor
npx universal-devkit install omnitab

# Claude Code에서
/stock-predictor-rules
/omnitab-rules
```

### 2. 스킬 포맷 표준화

SkillsCokac의 스킬 포맷을 분석하면 DevKit 규칙 포맷 표준화에 참고 가능

### 3. 커뮤니티 공유 고려

DevKit의 일부 범용 규칙(예: Python 베스트 프랙티스)을 SkillsCokac에 공개 가능

---

## 다음 단계

- [ ] SkillsCokac 스킬 구조 상세 분석 (파일 포맷)
- [ ] Universal DevKit NPX 배포 가능성 검토
- [ ] vercel-react-best-practices 설치 후 내용 분석

---

## 참고 자료

- [SkillsCokac 플랫폼](https://skills.cokac.com)
- [vercel-react-best-practices](https://skills.cokac.com/p/cmkfhyxcf0002dlpctvvwwgxd)

---

*마지막 업데이트: 2026-01-20*
