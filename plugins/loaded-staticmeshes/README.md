# Loaded StaticMeshes

> 레벨에 로드된 모든 StaticMesh 정보를 추출하는 도구

## 개요

현재 레벨에 로드된 모든 액터의 StaticMesh 정보를 수집하여 CSV로 내보내기.
External Actor 정보와 LandscapeStreamingProxy 연결 정보 포함.

## 주요 기능

### 1. 액터 정보 수집
```python
for actor in sorted(all_actors, key=lambda a: a.get_actor_label()):
    # Transform 정보
    loc, rot, scale = actor.get_transform()
    mobility = comp.mobility  # Static/Movable/Stationary
    
    # StaticMesh 정보
    for comp in actor.get_components_by_class(StaticMeshComponent):
        mesh_name = comp.static_mesh.get_name()
```

### 2. External Actor 정보
```python
# External Actor 여부 확인
if "/__ExternalActors__/" in outer_path:
    external_guid = outer.get_name()
    asset_path = get_external_asset_path(package_path)
    file_size = os.path.getsize(asset_path)
    last_modified = os.path.getmtime(asset_path)
```

### 3. LandscapeStreamingProxy 매핑
```python
for potential_proxy in all_actors:
    if isinstance(potential_proxy, LandscapeStreamingProxy):
        if is_inside_bounds(actor_loc, proxy_bounds):
            proxy_name = potential_proxy.get_name()
            break
```

### 4. 메시 사용량 집계
```python
mesh_name_counts = Counter(mesh_name_list)
# 출력: "SM_Rock_01 (150)" - 150번 사용됨
```

## 기술 스택

```python
import unreal
import csv
import codecs  # UTF-8 BOM 지원
from collections import defaultdict, Counter
```

## CSV 출력 컬럼

| 컬럼 | 설명 |
|------|------|
| STATICMESH_NAME | 메시 이름 (사용 횟수) |
| WORLD_OUTLINER | 액터 라벨 |
| LEVEL_PACKAGE | 레벨 패키지 이름 |
| PROXY_NAME | 소속 LandscapeStreamingProxy |
| TRANSFORM_INFO | Location, Rotation, Scale, Mobility |
| EXTERNAL_GUID | External Actor GUID |
| EXTERNALIZED? | Yes/No |
| UASSET_EXISTS? | Yes/No |
| UASSET_PATH | 실제 파일 경로 |
| FILE_SIZE | 파일 크기 (bytes) |
| LAST_MODIFIED | 마지막 수정 시간 |
| TAGS | 액터 태그 |

## 출력 예시

```
=== SUMMARY ===
Total Actors,15234
StaticMesh Assigned,12450

★ STATICMESH_NAME,★ WORLD_OUTLINER,★ LEVEL_PACKAGE,...
SM_Rock_01 (150),Rock_001,Level_Terrain,...
,Rock_002,Level_Terrain,...
,Rock_003,Level_Terrain,...
SM_Tree_02 (85),Tree_001,Level_Forest,...
```

## 활용 사례

1. **에셋 최적화**: 과다 사용 메시 식별
2. **레벨 감사**: 모든 배치된 에셋 목록화
3. **External Actor 관리**: GUID-액터 매핑 테이블
4. **파일 크기 분석**: 대용량 External Actor 식별

## 자동 실행

```python
# CSV 저장 후 자동으로 열기
os.startfile(save_path)
```

## 향후 개선 아이디어

1. **Excel 출력**: openpyxl로 스타일링된 Excel
2. **필터링**: 특정 메시 타입만 출력
3. **그룹화**: Proxy별, 레벨별 그룹화
4. **통계 차트**: 메시 사용량 시각화

## 원본 파일

`f:\workspace_3rd\client\NP\Content\_EditorOnly\World_Test\Shin\ToolTEST\LoadedStaticMeshes.py`
