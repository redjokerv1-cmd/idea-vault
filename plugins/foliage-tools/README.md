# Foliage Tools

> 폴리지 배치 문제를 검출하는 종합 도구 (v28.5)

## 개요

Instanced Foliage Actor의 모든 인스턴스를 분석하여 떠있거나 묻힌 폴리지를 검출.
대용량 오픈월드 맵에서도 빠르게 동작하도록 최적화됨.

## 주요 기능

### 1. 문제 유형 검출

| 문제 유형 | 조건 | 아이콘 |
|-----------|------|--------|
| FLOATING | 피벗이 30m 이상 떠있음 | 🔴 |
| MESH_FLOATING | 메시 바닥이 8m 이상 떠있음 | 🟠 |
| DEEP_SUNKEN | 피벗이 10m 이상 묻힘 | 🟣 |
| MESH_BURIED | 메시 상단이 6m 이상 묻힘 | 🟤 |
| FLOATING_NO_GROUND | 지면 감지 안 됨 | ❌ |
| OUTSIDE_BOUNDS | 랜드스케이프 범위 밖 | 🚫 |
| EMPTY_FOLIAGE_ACTOR | 인스턴스 0개인 폴리지 액터 | 📭 |

### 2. 지형 트레이스 시스템
```python
class WorkingTracer:
    """Line Trace로 지면 높이 감지"""
    def trace_ground(self, location):
        start_loc = location + Vector(0, 0, 500)  # 시작점
        end_loc = location - Vector(0, 0, 3000)   # 끝점 (30m 아래)
        
        hit_result = line_trace_single(...)
        return hit_result.z, hit_result.actor_name
```

### 3. 지형 높이 캐시
```python
class GroundHeightCache:
    """그리드 기반 높이 캐시 (5m 그리드)"""
    grid_size = 500.0  # cm
    max_entries = 5000
    
    # 캐시 히트율 90%+ 달성
```

### 4. 지형 에셋 인식
- SM_ 접두사 메시 중 지형 관련 폴더에 속한 에셋 인식
- Cliff, Rock, Mountain, Hill 등 지형 에셋 위 폴리지는 정상으로 처리

## 기술 스택

```python
import unreal
import openpyxl
from collections import Counter
```

## 설정값

```python
# 허용 오차 (자연스러운 배치 고려)
FLOATING_TOLERANCE_CM = 3000.0      # 30m 이상 떠있으면 문제
DEEP_BURIAL_TOLERANCE_CM = 1000.0   # 10m 이상 묻히면 문제
MESH_BOTTOM_FLOATING_CM = 800.0     # 메시 바닥 8m 이상 떠있음
MESH_TOP_BURIAL_CM = 600.0          # 메시 상단 6m 이상 묻힘

# 성능 설정
BATCH_SIZE = 1000
CACHE_GRID_SIZE = 500.0
MAX_CACHE_ENTRIES = 5000
```

## 출력 형식

### HTML 대시보드
- 진행 상황 추적 (체크박스로 처리 완료 표시)
- LocalStorage에 진행 상황 자동 저장
- 문제 타입별 필터링
- 좌표 복사 버튼

### Excel 리포트
- 문제 유형별 정렬
- 좌표 형식: `(X=...,Y=...,Z=...)`
- 헤더 스타일링

## 성능 최적화

1. **ScopedSlowTask**: 진행 상황 UI + 취소 가능
2. **배치 처리**: 1000개 단위 처리
3. **캐시 시스템**: 지형 높이 캐시 (히트율 90%+)
4. **메시 바운드 캐시**: 같은 메시는 한 번만 계산

## 처리 속도

- 약 **10,000+ 인스턴스/초** (최적화된 환경)
- 100만 폴리지 인스턴스도 2분 내 처리

## 향후 개선 아이디어

1. **자동 수정**: 문제 폴리지 자동 높이 조정
2. **선별 검사**: 특정 메시 타입만 검사
3. **실시간 모니터링**: 폴리지 페인트 중 실시간 검사
4. **배치 규칙**: 최소 간격, 경사 제한 검사

## 원본 파일

`f:\workspace_3rd\client\NP\Content\_EditorOnly\World_Test\Shin\ToolTEST\Foliage_Tools.py`
