# Foliage Debug Tool

> 선택한 폴리지 액터를 상세 분석하는 디버깅 도구 (v2.0)

## 개요

Foliage_Tools에서 발견된 문제 데이터와 함께 선택한 폴리지 액터를 상세 분석.
개별 인스턴스 레벨까지 디버깅 정보를 제공.

## 주요 기능

### 1. 선택 기반 분석
```python
# 선택한 폴리지 액터만 분석
selected_actors = unreal.EditorLevelLibrary.get_selected_level_actors()
foliage_actors = [a for a in selected_actors 
                  if a.get_components_by_class(HierarchicalInstancedStaticMeshComponent)]
```

### 2. 인스턴스별 상세 정보
- 각 인스턴스의 Transform
- 액터 위치로부터의 거리
- 샘플링 (최대 50개) 표시

### 3. 문제 데이터 연계
```python
def analyze_problems(problem_data):
    """Foliage_Tools 결과와 연계 분석"""
    problems_by_type = Counter()
    problems_by_actor = defaultdict(list)
    problems_by_mesh = defaultdict(list)
    coordinate_ranges = calculate_ranges(problem_data)
```

### 4. 통합 분석
| 분석 항목 | 설명 |
|-----------|------|
| 기본 통계 | 액터 수, 인스턴스 수, 컴포넌트 수 |
| 메시 분포 | 메시 타입별 인스턴스 비율 |
| 문제 분석 | 문제 유형별 개수 및 비율 |
| 액터별 상태 | 정상/문제 상태 표시 |

## 기술 스택

```python
import unreal
import time
import math
from collections import defaultdict, Counter
```

## HTML 리포트 기능

### 시각적 요소
- 통계 카드 (글래스모피즘 스타일)
- 문제 유형별 배지 (색상 코딩)
- 좌표 복사 버튼
- 스크롤 가능한 테이블

### 색상 시스템
```python
debug_colors = {
    'FLOATING': '#ef4444',           # 빨강
    'PARTIAL_OVERLAP': '#f97316',    # 주황
    'TOUCHING': '#eab308',           # 노랑
    'CLOSE': '#3b82f6',              # 파랑
    'NORMAL': '#22c55e',             # 초록
    'NO_MESH': '#64748b'             # 회색
}
```

## 사용 방법

1. 레벨 에디터에서 폴리지 액터 선택
2. Python 스크립트 실행
3. HTML 리포트 자동 열림

```python
# 버튼용 메인 함수
debug_selected_foliage_with_problems(problem_data)
```

## StaticMesh Overlap Detector 통합

이 도구는 StaticMesh 겹침 검사 기능도 포함:

```python
class StaticMeshOverlapDetector:
    """폴리지가 아닌 StaticMesh 액터의 겹침 검사"""
    - 바운딩 박스 기반 겹침 계산
    - 겹침 비율에 따른 타입 분류
    - 거리 계산
```

## 향후 개선 아이디어

1. **실시간 하이라이트**: 문제 인스턴스 에디터에서 선택
2. **비교 분석**: 수정 전/후 비교
3. **배치 수정**: 문제 인스턴스 일괄 수정/삭제
4. **필터 저장**: 자주 쓰는 필터 프리셋

## 원본 파일

`f:\workspace_3rd\client\NP\Content\_EditorOnly\World_Test\Shin\ToolTEST\Foliage_Debug_Tool.py`
