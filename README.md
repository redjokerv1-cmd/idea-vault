# 💡 Idea Vault

미래 프로젝트를 위한 아이디어 창고

---

## 📁 구조

```
idea-vault/
├── apps/                    # 앱/도구 아이디어
│   └── tileable-ai/         # 타일 텍스처 생성기
├── plugins/                 # 언리얼 엔진 플러그인/스크립트
│   ├── export-selected-actors/
│   ├── staticmesh-overlap-detector/
│   ├── foliage-tools/
│   ├── foliage-debug-tool/
│   ├── git-staged-external-actors/
│   └── loaded-staticmeshes/
├── features/                # 기존 프로젝트에 추가할 기능
├── research/                # 기술/논문 조사
├── business/                # 비즈니스/수익화 아이디어
└── archive/                 # 보류/완료된 아이디어
```

## 🏷️ 아이디어 상태

| 상태 | 설명 |
|------|------|
| 💡 `idea` | 초기 아이디어 |
| 📋 `planned` | 계획됨 |
| 🔬 `researching` | 조사 중 |
| 🚧 `in-progress` | 진행 중 |
| ✅ `completed` | 완료됨 |
| 📦 `archived` | 보류됨 |

## 📝 아이디어 템플릿

각 아이디어는 다음 형식으로 작성:

```markdown
# [아이디어 이름]

**상태**: 💡 idea
**생성일**: YYYY-MM-DD
**분류**: apps / features / research / business

## 개요
한 줄 설명

## 상세 내용
...

## 기술 스택
- ...

## 예상 작업량
- 난이도: 쉬움 / 보통 / 어려움
- 예상 시간: N주

## 참고 자료
- [링크1](url)
- [링크2](url)
```

---

## 📚 현재 아이디어 목록

| 분류 | 이름 | 상태 | 설명 |
|------|------|------|------|
| apps | [Tileable AI](apps/tileable-ai/README.md) | 💡 idea | AI 기반 타일 텍스처 생성 도구 |
| features | [Composite Score 100](features/composite-score-100.md) | 🔬 researching | 스크리닝 7점→100점 연속형 복합 스코어 개편 |
| research | [Event-Driven Prediction + LLM Sentiment](research/event-driven-prediction-llm-sentiment.md) | 🔬 researching | 이벤트 기반 예측 + LLM 감성분석 딥다이브 |
| research | [AI 코인 자동매매 트레이더](research/crypto-auto-trader.md) | 🔬 researching | 업비트 기반 AI 코인 자동매매 도구 — 기존 주식 인프라 활용 |
| business | [Product Synopsis: Buy Decision Tool](business/product-synopsis-buy-decision.md) | 🔬 researching | "이 종목, 지금 사도 되는가?" 3축 의사결정 프레임워크 |
| plugins | [Export Selected Actors](plugins/export-selected-actors/README.md) | ✅ completed | 선택한 액터 Excel 내보내기 |
| plugins | [StaticMesh Overlap Detector](plugins/staticmesh-overlap-detector/README.md) | ✅ completed | 메시 겹침/중복 검출 |
| plugins | [Foliage Tools](plugins/foliage-tools/README.md) | ✅ completed | 폴리지 배치 문제 검출 |
| plugins | [Foliage Debug Tool](plugins/foliage-debug-tool/README.md) | ✅ completed | 폴리지 상세 디버깅 |
| plugins | [Git Staged External Actors](plugins/git-staged-external-actors/README.md) | ✅ completed | Git External Actor 분석 |
| plugins | [Loaded StaticMeshes](plugins/loaded-staticmeshes/README.md) | ✅ completed | StaticMesh 정보 CSV 출력 |

---

## 🔄 통합 워크플로우 (3개 저장소 시너지)

이 저장소는 **universal-devkit**, **dev-kit**과 함께 운영됩니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    📋 아이디어 → 완성 워크플로우                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣ 아이디어 발생                                               │
│     └── idea-vault에 기록 (TEMPLATE.md 사용)                    │
│         상태: 💡 idea                                            │
│                                                                 │
│  2️⃣ 개발 시작                                                   │
│     └── dev-kit으로 환경 구성                                    │
│         - scripts/setup.sh 실행                                 │
│         - env-templates/ 참고                                   │
│         상태: 📋 planned → 🚧 in-progress                        │
│                                                                 │
│  3️⃣ 개발 중                                                     │
│     └── universal-devkit 참고                                   │
│         - AGENT_CONTEXT.md 필독                                 │
│         - rules/ 규칙 준수                                       │
│                                                                 │
│  4️⃣ 문제 발생                                                   │
│     └── dev-kit/blackbox/incidents에 기록                       │
│         - 문제-해결 매핑                                         │
│         - 재사용 가능한 해결법 축적                              │
│                                                                 │
│  5️⃣ 완료                                                        │
│     └── universal-devkit/case-studies에 상세 기록               │
│         - "왜" 이렇게 했는지 기록                                │
│         상태: ✅ completed                                       │
│                                                                 │
│  6️⃣ 다음 세션                                                   │
│     └── blackbox + learning-log로 맥락 복원                     │
│         - 이전 작업 이해                                         │
│         - 같은 실수 방지                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 관련 저장소

| 저장소 | 용도 | GitHub |
|--------|------|--------|
| **idea-vault** | 아이디어 저장 | `redjokerv1-cmd/idea-vault` |
| **universal-devkit** | 개발 규칙/케이스스터디 | `redjokerv1-cmd/universal-devkit` |
| **dev-kit** | 환경 구성/디버그 도구 | `redjokerv1-cmd/stock-predictor-dev-kit` |

---

*마지막 업데이트: 2026-02-16*
