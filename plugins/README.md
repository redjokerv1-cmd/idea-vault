# Unreal Engine Plugins

> 언리얼 엔진용 Python 스크립트/플러그인 모음

## 개요

레벨 디자인, 에셋 관리, QA 자동화를 위한 언리얼 엔진 Python 스크립트 컬렉션.
모두 Unreal Python API 기반으로 작동.

## 플러그인 목록

### 레벨 에디터 도구

| 플러그인 | 설명 | 상태 |
|----------|------|------|
| [export-selected-actors](./export-selected-actors/) | 선택한 액터 정보를 Excel로 내보내기 | ✅ 완료 |
| [loaded-staticmeshes](./loaded-staticmeshes/) | 레벨 내 모든 StaticMesh 정보 CSV 출력 | ✅ 완료 |

### 품질 검사 도구

| 플러그인 | 설명 | 상태 |
|----------|------|------|
| [staticmesh-overlap-detector](./staticmesh-overlap-detector/) | StaticMesh 겹침/중복 배치 검출 | ✅ 완료 |
| [foliage-tools](./foliage-tools/) | 폴리지 배치 문제 검출 (떠있음/묻힘) | ✅ 완료 |
| [foliage-debug-tool](./foliage-debug-tool/) | 선택한 폴리지 상세 디버깅 | ✅ 완료 |

### Git 연동 도구

| 플러그인 | 설명 | 상태 |
|----------|------|------|
| [git-staged-external-actors](./git-staged-external-actors/) | Git 스테이징된 External Actor 분석 | ✅ 완료 |

## 공통 기술 스택

```python
# 핵심 의존성
import unreal                    # Unreal Python API
from collections import Counter  # 집계
import os, time                  # 파일/시간

# 선택적 의존성
import openpyxl                  # Excel 출력
import xlsxwriter                # 고급 Excel 출력
```

## 공통 패턴

### LandscapeStreamingProxy 연결
대부분의 도구에서 액터가 어떤 Landscape Proxy에 속하는지 파악:
```python
for proxy in landscape_proxies:
    if is_inside_bounds(actor_location, proxy.get_bounds()):
        return proxy.get_name()
```

### External Actor GUID 추출
One File Per Actor 시스템에서 GUID 추출:
```python
if "/__ExternalActors__/" in actor.get_outermost().get_path_name():
    guid = actor.get_outermost().get_name()
```

### HTML 대시보드
대부분의 도구에서 결과를 HTML로 출력:
- 글래스모피즘 스타일
- 좌표 복사 버튼
- 필터링 기능
- 진행 상황 저장 (LocalStorage)

## 향후 통합 계획

1. **통합 UI**: 모든 도구를 하나의 Editor Utility Widget으로 통합
2. **공통 라이브러리**: 반복되는 함수 모듈화
3. **설정 관리**: JSON 기반 설정 파일
4. **로깅 시스템**: 공통 로그 포맷
