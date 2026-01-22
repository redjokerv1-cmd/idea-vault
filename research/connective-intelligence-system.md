# Connective Intelligence System (연결 지능 시스템)

> 분석일: 2026-01-23
> 상태: 📋 planned
> 태그: #AI #뇌과학 #지식관리 #메타시스템

## 개요

"지식 + 뇌과학 + AI 도구"를 결합하여 프로젝트 간 학습을 자동으로 연결하는 "외부 뇌(External Brain)" 시스템 구축 아이디어.

## 배경: 현재 생태계

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        🌐 현재 프로젝트 생태계                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐       │
│  │   Idea Vault    │     │ Universal DevKit│     │ Learning Data   │       │
│  │   (아이디어)     │────▶│   (규칙/경험)    │────▶│   Vault (학습)  │       │
│  └────────┬────────┘     └────────┬────────┘     └────────┬────────┘       │
│           │                       │                       │                │
│           ▼                       ▼                       ▼                │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐       │
│  │ Stock Predictor │     │    OmniTab      │     │  (Future)       │       │
│  │   (주식 분석)    │     │  (TAB→GP5)     │     │                 │       │
│  └─────────────────┘     └─────────────────┘     └─────────────────┘       │
│                                                                             │
│  ═══════════════════════════════════════════════════════════════════════   │
│  │                    🤖 AI (Claude) = 연결자                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 뇌과학적 매핑

| 인간의 뇌 | 현재 시스템 | 역할 |
|-----------|------------|------|
| 해마 (장기기억 형성) | Learning Data Vault | 학습 데이터 축적 |
| 전두엽 (계획, 판단) | Universal DevKit (규칙) | 의사결정 기준 |
| 측두엽 (언어, 의미 연결) | Experience DB (패턴) | 맥락 이해 |
| 작업기억 (7±2 청크) | AI 컨텍스트 윈도우 | 현재 작업 처리 |
| 꿈 (기억 통합) | Case Studies | 경험 정리/통합 |
| 시냅스 (연결) | **부족** → 개선 필요 | 지식 간 연결 |

## 핵심 문제

```
현재:
┌─────────────────────────────────────────────────────────────────┐
│  지식들이 "저장"되지만, "연결"이 수동적                          │
│  → 사용자가 직접 "이거랑 저거 연결해봐"라고 해야 연결됨          │
└─────────────────────────────────────────────────────────────────┘

이상적:
┌─────────────────────────────────────────────────────────────────┐
│  AI가 자동으로:                                                 │
│  "어? OmniTab에서 쓴 합성 데이터 생성 방식,                     │
│   Stock Predictor에서 백테스트 데이터 생성할 때도 쓸 수 있겠는데?" │
└─────────────────────────────────────────────────────────────────┘
```

## 제안: 4-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    🧠 Connective Intelligence System                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Layer 1: Storage (저장)                                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Idea Vault  │  │  DevKit     │  │ Learning    │  │ Projects    │        │
│  │ (아이디어)   │  │  (규칙)     │  │ Data Vault  │  │ (실행 코드) │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         └────────────────┼────────────────┼────────────────┘               │
│                          │                │                                │
│  Layer 2: Indexing (색인)│                │                                │
│  ┌───────────────────────▼────────────────▼───────────────────────────┐    │
│  │                    Knowledge Graph                                  │    │
│  │  - 모든 파일/개념을 노드로                                          │    │
│  │  - 관계를 엣지로 (uses, similar_to, evolved_from, solves)          │    │
│  └───────────────────────┬────────────────────────────────────────────┘    │
│                          │                                                 │
│  Layer 3: Connection (연결)                                                │
│  ┌───────────────────────▼───────────────────────────────────────────┐     │
│  │                    RLM + AI Agent                                  │     │
│  │  - 자동 연결 발견                                                  │     │
│  │  - 교차 프로젝트 인사이트                                          │     │
│  │  - 프로액티브 제안                                                 │     │
│  └───────────────────────┬───────────────────────────────────────────┘     │
│                          │                                                 │
│  Layer 4: Action (행동)  │                                                 │
│  ┌───────────────────────▼───────────────────────────────────────────┐     │
│  │  "Stock Predictor에서 발견한 최적화 패턴을                        │     │
│  │   OmniTab API에도 적용하면 30% 성능 향상 예상됩니다."             │     │
│  └───────────────────────────────────────────────────────────────────┘     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 구현 설계

### Layer 2: Knowledge Graph

```python
# universal-devkit/agent-core/knowledge_graph.py

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class NodeType(Enum):
    CONCEPT = "concept"      # 추상적 개념 (예: "합성 데이터")
    FILE = "file"            # 실제 파일
    PATTERN = "pattern"      # 성공/실패 패턴
    ERROR = "error"          # 에러 유형
    SOLUTION = "solution"    # 해결책

class RelationType(Enum):
    USES = "uses"                    # A가 B를 사용
    SIMILAR_TO = "similar_to"        # 유사한 개념
    EVOLVED_FROM = "evolved_from"    # B에서 발전
    SOLVES = "solves"                # 문제 해결 관계
    CONTRADICTS = "contradicts"      # 충돌/모순

@dataclass
class KnowledgeNode:
    id: str
    type: NodeType
    title: str
    content: str
    project: str  # "stock-predictor", "omnitab", "devkit", "global"
    tags: List[str]
    created_at: str
    
@dataclass  
class KnowledgeEdge:
    source_id: str
    target_id: str
    relation: RelationType
    strength: float  # 0.0 ~ 1.0
    evidence: str    # 왜 이 연결인지 설명
```

### Layer 3: Connection Discovery

```python
# universal-devkit/agent-core/connection_engine.py

class ConnectionEngine:
    def __init__(self, graph: KnowledgeGraph):
        self.graph = graph
        
    def discover_new_connections(self, new_node: KnowledgeNode) -> List[KnowledgeEdge]:
        """
        새 지식이 추가될 때 기존 지식과의 연결 발견
        """
        potential_connections = []
        
        # 1. 키워드 기반 유사도
        similar_nodes = self.graph.find_similar_by_keywords(new_node.tags)
        
        # 2. 프로젝트 간 패턴 매칭
        cross_project_matches = self.graph.find_cross_project_patterns(
            new_node.content,
            exclude_project=new_node.project
        )
        
        # 3. 문제-해결 매핑
        if new_node.type == NodeType.SOLUTION:
            related_errors = self.graph.find_related_errors(new_node)
            
        # 4. 연결 강도 계산 및 필터링
        for match in similar_nodes + cross_project_matches:
            edge = self._create_edge(new_node, match)
            if edge.strength > 0.5:  # 임계값
                potential_connections.append(edge)
                
        return potential_connections
        
    def generate_proactive_insights(self) -> List[str]:
        """
        주기적으로 실행: 미발견된 연결 찾기
        """
        insights = []
        
        # 1. 약한 연결 강화 가능성
        weak_edges = self.graph.get_weak_edges(threshold=0.3)
        
        # 2. 고립된 노드 (연결 없음)
        isolated_nodes = self.graph.get_isolated_nodes()
        
        # 3. 패턴 일반화 가능성
        # "OmniTab과 Stock Predictor 모두에서 '비동기 처리' 패턴 사용"
        common_patterns = self.graph.find_common_patterns_across_projects()
        
        return insights
```

### Layer 4: Proactive Suggestions

```python
# universal-devkit/agent-core/insight_generator.py

class InsightGenerator:
    def generate_session_brief(self, current_project: str) -> str:
        """
        세션 시작 시 관련 인사이트 제공
        """
        return f"""
        [AI 인사이트 - {current_project}]
        
        🔗 교차 프로젝트 연결:
        - OmniTab의 "합성 데이터 생성" 패턴이 이 프로젝트의 
          "테스트 데이터 부족" 문제에 적용 가능합니다.
          
        ⚠️ 주의할 패턴:
        - 이전에 Stock Predictor에서 "yfinance 타임아웃" 문제가 있었습니다.
          같은 라이브러리 사용 시 주의하세요.
          
        💡 최근 발견:
        - "아이디어 중심 설계" 패턴이 N8N 분석에서 발견되었습니다.
          이 프로젝트 UX에 적용 가능할 수 있습니다.
        """
```

## 구현 로드맵

### Phase 1: 기반 구축 (1-2주)
- [ ] `KnowledgeNode`, `KnowledgeEdge` 데이터 모델 정의
- [ ] 기존 파일들을 노드로 변환하는 스크립트
- [ ] 수동 연결 태그 시스템 (`related: [file1, file2]`)

### Phase 2: 자동화 (3-4주)
- [ ] 키워드 기반 유사도 계산
- [ ] 새 파일 추가 시 자동 연결 제안
- [ ] 교차 프로젝트 패턴 매칭

### Phase 3: 프로액티브 (5-8주)
- [ ] 세션 시작 시 인사이트 브리핑
- [ ] 주기적 미발견 연결 탐색
- [ ] 학습 효과 측정 지표

## 예상 효과

### 정량적
- 프로젝트 간 지식 재사용률: 현재 ~10% → 목표 50%+
- 동일 실수 반복: 현재 빈번 → 목표 0
- 새 프로젝트 시작 속도: 현재 1주 → 목표 2-3일

### 정성적
- "이거 전에 어디서 봤는데..." → 즉시 연결
- 암묵지 → 형식지 변환 가속
- 프로젝트 복잡도 증가에도 관리 가능

## 위험 요소

| 위험 | 대응 |
|------|------|
| 오버엔지니어링 | MVP 먼저, 점진적 확장 |
| AI 세션 리셋 | Memory 시스템 활용, 핵심 연결은 파일로 |
| 유지보수 비용 | 자동화 우선, 수동 작업 최소화 |
| 노이즈 연결 | 강도 임계값 적용, 사용자 피드백 |

## 관련 개념

- **Second Brain** (Tiago Forte)
- **Zettelkasten** (Niklas Luhmann)
- **RLM** (MIT Recursive Language Models)
- **Knowledge Graph** (Google)
- **Memex** (Vannevar Bush, 1945)

## 참고 자료

- `case-studies/2026-01-20-rlm-integration-analysis.md`
- `case-studies/2026-01-20-idea-centric-design-pattern.md`
- `patterns/success/rlm-selective-context-loading.md`
- `research/n8n-ai-workflow-builder.md`
