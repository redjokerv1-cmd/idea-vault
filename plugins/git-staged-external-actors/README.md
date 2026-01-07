# Git Staged External Actors

> Git 스테이징된 External Actor 파일을 분석하는 도구

## 개요

External Actor 시스템(One File Per Actor)을 사용하는 프로젝트에서 
Git에 스테이징된 변경사항을 분석하여 어떤 액터가 변경/삭제되었는지 파악.

## 주요 기능

### 1. Git 스테이징 파일 분석
```python
def get_git_staged_files():
    """git diff --staged --name-status로 변경 파일 목록 획득"""
    # M: 수정, A: 추가, D: 삭제, R: 이름 변경
    return staged_files
```

### 2. External Actor GUID 매핑
```python
def get_external_actor_guid(actor):
    """액터의 External Actor GUID 추출"""
    outermost = actor.get_outermost()
    outermost_path = outermost.get_path_name()
    
    if "/__ExternalActors__/" in outermost_path:
        return os.path.basename(outermost_path)  # GUID
    return ""
```

### 3. 삭제된 External Actor 파싱
```python
def parse_deleted_external_actor_enhanced(file_path, git_root, guid_to_actor_map):
    """삭제된 uasset 파일에서 액터 정보 복원"""
    # Git show로 삭제 전 파일 내용 획득
    # 바이너리 파싱으로 액터 정보 추출
```

### 4. LandscapeStreamingProxy 연결
```python
def get_landscape_streaming_proxy_optimized(actor, landscape_proxies_cache):
    """액터가 속한 Landscape Proxy 찾기 (캐시 사용)"""
```

## 기술 스택

```python
import unreal
import subprocess  # Git 명령 실행
import os
from collections import defaultdict, Counter
```

## 데이터 흐름

```
Git Repository
    ↓
git diff --staged --name-status
    ↓
External Actor 파일 목록 (.uasset)
    ↓
GUID 추출 (파일 경로에서)
    ↓
레벨 내 액터와 매핑
    ↓
CSV 리포트 생성
```

## CSV 출력 정보

| 컬럼 | 설명 |
|------|------|
| Status | M (수정), A (추가), D (삭제) |
| Actor Label | 월드 아웃라이너 이름 |
| Mesh Name | StaticMesh 이름 |
| Level Package | 레벨 패키지 이름 |
| Proxy Name | 소속 LandscapeStreamingProxy |
| GUID | External Actor GUID |
| File Path | uasset 파일 경로 |

## 활용 사례

1. **커밋 전 검토**: 어떤 액터가 변경되었는지 확인
2. **충돌 해결**: 같은 영역 변경 시 영향 범위 파악
3. **변경 추적**: 특정 액터의 변경 이력 분석
4. **삭제 복원**: 실수로 삭제된 액터 정보 복원

## 향후 개선 아이디어

1. **시각화**: 레벨 뷰에서 변경된 액터 하이라이트
2. **Diff 뷰어**: 변경 전/후 Transform 비교
3. **자동 분류**: 변경 유형별 자동 태깅
4. **Slack/Teams 연동**: 커밋 알림에 변경 액터 정보 포함

## 원본 파일

`f:\workspace_3rd\client\NP\Content\_EditorOnly\World_Test\Shin\ToolTEST\GitStagedExternalActors.py`
