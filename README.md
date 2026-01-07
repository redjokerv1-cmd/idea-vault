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
| plugins | [Export Selected Actors](plugins/export-selected-actors/README.md) | ✅ completed | 선택한 액터 Excel 내보내기 |
| plugins | [StaticMesh Overlap Detector](plugins/staticmesh-overlap-detector/README.md) | ✅ completed | 메시 겹침/중복 검출 |
| plugins | [Foliage Tools](plugins/foliage-tools/README.md) | ✅ completed | 폴리지 배치 문제 검출 |
| plugins | [Foliage Debug Tool](plugins/foliage-debug-tool/README.md) | ✅ completed | 폴리지 상세 디버깅 |
| plugins | [Git Staged External Actors](plugins/git-staged-external-actors/README.md) | ✅ completed | Git External Actor 분석 |
| plugins | [Loaded StaticMeshes](plugins/loaded-staticmeshes/README.md) | ✅ completed | StaticMesh 정보 CSV 출력 |

---

*마지막 업데이트: 2026-01-07*
