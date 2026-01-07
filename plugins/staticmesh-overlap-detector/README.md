# StaticMesh Overlap Detector

> StaticMesh 겹침/중복 배치를 검출하는 도구

## 개요

레벨에 배치된 StaticMesh 액터들 중 겹치거나 파묻힌 메시를 자동으로 검출.
특히 **같은 이름의 메시가 95% 이상 겹친 경우**를 중복 배치로 판단.

## 주요 기능

### 1. 스마트 필터링
- **SM_ 접두사 메시만** 검사 (에셋 네이밍 컨벤션 기반)
- **제외 대상**: Blueprint, Landscape, Foliage, 게임 오브젝트
- 효율적인 검사 범위 축소

### 2. 다중 정밀도 겹침 검사
```
1단계: AABB 바운딩 박스 (빠른 필터링)
2단계: 거리 기반 (구형 근사)
3단계: 볼륨 기반 (채움 비율 보정)
4단계: 다면체 (8개 꼭짓점 Convex Hull)
5단계: 표면 (10x10x10 격자 샘플링)
```

### 3. 겹침 타입 분류
| 타입 | 조건 | 색상 |
|------|------|------|
| OVERLAP | 95%+ 겹침, 크기 비율 < 3배 | 🔴 빨강 |
| BURIED | 95%+ 겹침, 크기 비율 >= 3배 | 🟣 보라 |
| PARTIAL_OVERLAP | 30-95% 겹침 | 🟠 주황 |
| TOUCHING | 1-30% 겹침 | 🟡 노랑 |

### 4. 공간 분할 최적화
```python
# 1km 그리드로 공간 분할
grid_size = 1000.0
spatial_grid = create_spatial_grid(mesh_actors_info, grid_size)

# 인접 그리드만 검사 (3x3x3 = 27개 셀)
nearby_meshes = get_nearby_meshes(target_mesh, spatial_grid, grid_size)
```

## 기술 스택

```python
import unreal
import math
from collections import defaultdict, Counter
```

## 핵심 알고리즘

### 정밀 볼륨 계산
```python
def calculate_mesh_volume_accurate(static_mesh, world_bounds):
    """바운딩 박스가 아닌 실제 메시 볼륨 추정"""
    mesh_bounds = static_mesh.get_bounding_box()
    mesh_volume = calculate_box_volume(mesh_bounds)
    world_volume = calculate_box_volume(world_bounds)
    
    # 스케일 비율로 실제 볼륨 추정
    scale_ratio = world_volume / mesh_volume if mesh_volume > 0 else 1.0
    return mesh_volume * scale_ratio
```

### Z축 파묻힘 검출
```python
def analyze_vertical_relationship(mesh1, mesh2):
    """한 메시가 다른 메시 안에 완전히 포함되어 있는지 검사"""
    if mesh1_bottom >= mesh2_bottom and mesh1_top <= mesh2_top:
        return "MESH1_INSIDE_MESH2"
    # ...
```

## HTML 대시보드 기능

- 문제 타입별 필터링 버튼
- 좌표 복사 버튼 (언리얼 에디터 Go To 형식)
- 실시간 필터링 (겹침/파묻힘 분류)
- 통계 카드 (총 메시, 겹침 수, 겹침 비율)

## 성능 최적화

1. **공간 분할**: O(n²) → O(n * k) (k = 평균 인접 메시 수)
2. **캐시**: 바운딩 박스, 볼륨 계산 결과 캐시
3. **배치 처리**: 500개 단위로 GC 호출
4. **조기 종료**: AABB 비겹침 시 상세 검사 스킵

## 향후 개선 아이디어

1. **실제 메시 지오메트리 검사**: 삼각형 레벨 충돌 검사
2. **자동 수정**: 중복 메시 자동 삭제/이동
3. **히트맵 시각화**: 레벨 뷰에서 겹침 영역 표시
4. **배치 규칙 검사**: 최소 간격 위반 검출

## 원본 파일

`f:\workspace_3rd\client\NP\Content\_EditorOnly\World_Test\Shin\ToolTEST\StaticMesh_Overlap_Detector.py`
