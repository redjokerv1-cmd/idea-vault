# OmniTab (구 PDF to GP5)

**상태**: 🔴 MVP 실패 - 핵심 기능 미완성  
**생성일**: 2026-01-13  
**분류**: apps  
**GitHub**: https://github.com/redjokerv1-cmd/OmniTab  

---

## 개요

PDF/이미지 악보를 분석하여 Guitar Pro 5 (.gp5) 형식의 TAB 악보로 변환하는 도구

---

## 🔴 현재 상태 (2026-01-13)

### MVP 실패 - 핵심 기능 미완성

| 기능 | 상태 | 설명 |
|------|------|------|
| **숫자 OCR** | ✅ | 148개, 80% 정확도 |
| **카포 감지** | ✅ | 100% |
| **가로줄 제거** | ✅ | 작동 |
| **TAB 6줄 감지** | ❌ | 1/3만 성공 |
| **줄 번호 매핑** | ❌ | ~20% 정확도 |
| **마디 구분** | ❌ | 노이즈 문제 |
| **GP5 생성** | ❌ | 사용 불가 |

### 핵심 실패 원인

```
TAB 구조 파싱 실패:
- 6줄의 Y 좌표를 정확히 감지 못함
- 숫자가 어느 줄에 있는지 알 수 없음
- 마디 경계 구분 안 됨

결과: 모든 음표가 1마디에 배치, 줄 번호 틀림
```

### 교훈

1. **TAB 구조 파싱은 단순 OCR로 불가능**
2. **6줄 감지가 핵심** - 이게 없으면 모든 게 틀림
3. **반자동 접근이 현실적** - 완전 자동화는 어려움

### 작동하는 코드

```python
# 숫자 OCR (작동)
from omnitab.tab_ocr.recognizer.enhanced_ocr import EnhancedTabOCR
ocr = EnhancedTabOCR()
result = ocr.process_file("tab.png")  # 148 digits

# GP5 Writer (MIDI 기반, 작동)
from omnitab.gp5.writer import GP5Writer
writer = GP5Writer(title="Song", tempo=120)
writer.write(notes_data, "output.gp5")
```

---

## 핵심 파이프라인

```
┌─────────────────────────────────────────────────────────────────┐
│                    PDF → GP5 변환 파이프라인                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [PDF 악보]                                                      │
│      ↓                                                          │
│  ┌──────────────────────────────────────┐                       │
│  │  1️⃣ OMR (Optical Music Recognition)   │                       │
│  │  • Audiveris (Java, 오픈소스)          │                       │
│  │  • oemer (Python, 딥러닝)             │                       │
│  └──────────────────────────────────────┘                       │
│      ↓                                                          │
│  [MusicXML]                                                     │
│      ↓                                                          │
│  ┌──────────────────────────────────────┐                       │
│  │  2️⃣ 표기법 정규화 (Notation Mapping)   │                       │
│  │  • NotationDetector: 표기법 감지       │                       │
│  │  • NotationNormalizer: 정규화         │                       │
│  │  • 자동 학습 DB                       │                       │
│  └──────────────────────────────────────┘                       │
│      ↓                                                          │
│  [정규화된 음표/코드 데이터]                                     │
│      ↓                                                          │
│  ┌──────────────────────────────────────┐                       │
│  │  3️⃣ GP5 파일 생성                     │                       │
│  │  • PyGuitarPro                        │                       │
│  └──────────────────────────────────────┘                       │
│      ↓                                                          │
│  [.gp5 파일]                                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 핵심 도구

| 도구 | 역할 | 비용 |
|------|------|------|
| **Audiveris** | PDF → MusicXML (OMR) | 무료 (AGPL v3) |
| **oemer** | Python 기반 OMR (대안) | 무료 |
| **music21** | MusicXML 파싱 | 무료 (LGPL) |
| **PyGuitarPro** | GP5 파일 생성 | 무료 (MIT) |
| **FastAPI** | 웹 API | 무료 |

---

## GP5 특수 주법 매핑

### NoteEffect (음표 단위)

| 이펙트 | 속성명 | 설명 |
|--------|--------|------|
| Ghost Note | `ghostNote` | 약하게 연주 (괄호 음표) |
| Palm Mute | `palmMute` | 팜뮤트 (P.M.) |
| Hammer-on/Pull-off | `hammer` | 해머온/풀오프 |
| Let Ring | `letRing` | 울려두기 |
| Staccato | `staccato` | 스타카토 |
| Vibrato | `vibrato` | 비브라토 |
| Bend | `bend` | 벤딩 |
| Slide | `slides` | 슬라이드 |
| Harmonic | `harmonic` | 하모닉스 |

### NoteType

| 타입 | 설명 |
|------|------|
| `normal` | 일반 음표 |
| `dead` | 데드 노트 (X 표시) |
| `rest` | 쉼표 |
| `tie` | 타이 |

### BeatEffect (비트 단위)

| 이펙트 | 값 |
|--------|-----|
| Slap | `SlapEffect.slapping` |
| Pop | `SlapEffect.popping` |
| Tap | `SlapEffect.tapping` |

---

## Notation Mapping System

### 구성 요소

1. **NotationDetector**: 표기법 자동 감지 + 신뢰도 계산
2. **NotationNormalizer**: 표준 형식으로 변환
3. **Mapping DB**: 50+ 표기법 매핑 + 자동 학습

### 신뢰도 기반 처리

| 신뢰도 | 처리 방식 |
|--------|-----------|
| 0.85+ | 자동 처리 |
| 0.7-0.85 | AI 보조 (Gemini) |
| <0.7 | 사용자 수동 선택 |

### DB 스키마

```sql
-- 코드 표기법 매핑
CREATE TABLE chord_notation_mapping (
    id SERIAL PRIMARY KEY,
    standard_kind VARCHAR(50),  -- MusicXML 표준
    alias VARCHAR(50),          -- 다양한 표기법
    confidence FLOAT DEFAULT 0.9
);

-- 이펙트 표기법 매핑
CREATE TABLE effect_notation_mapping (
    id SERIAL PRIMARY KEY,
    standard VARCHAR(50),
    text_repr VARCHAR(20),
    confidence FLOAT DEFAULT 0.9
);

-- 사용자 수정 기록 (자동 학습)
CREATE TABLE user_corrections (
    id SERIAL PRIMARY KEY,
    original VARCHAR(50),
    corrected VARCHAR(50),
    improvement FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 기술 스택

- **언어**: Python 3.11+
- **OMR**: Audiveris (Java) / oemer (Python)
- **음악 처리**: music21
- **GP5 생성**: PyGuitarPro
- **웹 API**: FastAPI
- **DB**: PostgreSQL (매핑 + 학습)
- **AI**: Gemini API (낮은 신뢰도 처리)

---

## 예상 작업량

| Phase | 기간 | 내용 |
|-------|------|------|
| Week 1 | 7일 | 기본 파이프라인 (OMR → MusicXML → GP5) |
| Week 2 | 7일 | Notation Mapping System |
| Week 3 | 7일 | 웹 UI + API |
| Week 4 | 7일 | 테스트 & 배포 |

**총 예상**: 4주

---

## 테스트 악보

- Yellow Jacket - Shaun Martin (Kent Nishimura 커버)
  - 6페이지 PDF
  - 특수 주법: Body Hit, Full Mute, X (Left Hand Mute)

---

## 경쟁 우위

| 항목 | 기존 OMR 도구 | 이 프로젝트 |
|------|--------------|------------|
| 표준 표기법 | ✅ 지원 | ✅ 지원 |
| 비표준 표기법 | ❌ 미지원 | ✅ 자동 정규화 |
| 자동 학습 | ❌ | ✅ 사용자 피드백 반영 |
| 정확도 | 75% | 92% (목표) |

---

## 참고 자료

- [Audiveris GitHub](https://github.com/Audiveris/audiveris)
- [PyGuitarPro 문서](https://pyguitarpro.readthedocs.io/)
- [music21 문서](https://web.mit.edu/music21/)
- [MusicXML 튜토리얼](https://www.musicxml.com/)

---

*마지막 업데이트: 2026-01-13*
