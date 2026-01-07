# Export Selected Actors

> 언리얼 엔진에서 선택한 액터 정보를 Excel로 내보내는 도구

## 개요

레벨 에디터에서 선택한 액터들의 상세 정보를 분석하여 Excel 파일로 내보내는 Python 스크립트.

## 주요 기능

### 1. 액터 정보 추출
- **Transform 정보**: Location, Rotation, Scale, Mobility
- **메시 정보**: StaticMesh 이름, 사용 횟수 집계
- **External Actor**: GUID, uasset 경로, 파일 크기, 수정 시간
- **레벨 정보**: Level Package, LandscapeStreamingProxy 연결

### 2. LandscapeStreamingProxy 기반 그룹화
- 액터 위치 기반으로 어떤 Landscape Proxy에 속하는지 자동 감지
- 캐시 시스템으로 대용량 맵에서도 빠른 처리

### 3. Excel 출력 (두 가지 방식)
- **xlsxwriter** (권장): 조건부 서식, 차트, 데이터 바, 셀 병합
- **XML 방식** (폴백): xlsxwriter 없을 때 기본 스타일로 생성

### 4. 시각적 개선
- 액터 타입별 이모티콘 (🏗️ StaticMesh, 📘 Blueprint, 🌿 Foliage 등)
- 메시 사용량별 색상 (고사용: 빨강, 중간: 주황, 저사용: 노랑)
- 자동 필터, 틀 고정, 차트 생성

## 기술 스택

```python
# 핵심 의존성
import unreal
import xlsxwriter  # 선택적 (없으면 XML 폴백)
from collections import defaultdict, Counter
```

## 핵심 알고리즘

### LandscapeStreamingProxy 매칭
```python
def get_landscape_streaming_proxy_optimized(actor, landscape_proxies_cache):
    """캐시된 프록시 정보로 빠른 위치 기반 매칭"""
    actor_location = actor.get_actor_location()
    
    for proxy_info in landscape_proxies_cache:
        # 바운딩 박스 + 마진으로 포함 여부 체크
        if is_inside_bounds(actor_location, proxy_info):
            return proxy_info['label']
    
    # 가장 가까운 프록시 반환 (5km 이내)
    return find_nearest_proxy(actor_location, landscape_proxies_cache)
```

### 메시 사용량 집계
```python
mesh_name_counts = Counter(mesh_name_list)
# 결과: {"SM_Rock_01": 150, "SM_Tree_02": 85, ...}
```

## 출력 예시

| STATICMESH_NAME | WORLD_OUTLINER | LEVEL_PACKAGE | TRANSFORM_INFO |
|-----------------|----------------|---------------|----------------|
| SM_Rock_01 (150) | 🏗️ Rock_Instance_001 | Level_Terrain | Location=(X=...) |
| | 🏗️ Rock_Instance_002 | Level_Terrain | Location=(X=...) |

## 향후 개선 아이디어

1. **필터링 옵션**: 특정 메시 타입만 내보내기
2. **비교 기능**: 두 레벨 간 액터 비교
3. **실시간 업데이트**: 레벨 변경 시 자동 갱신
4. **JSON/CSV 출력**: Excel 외 포맷 지원

## 원본 파일

`f:\workspace_3rd\client\NP\Content\_EditorOnly\World_Test\Shin\ToolTEST\ExportSelectedActors.py`
