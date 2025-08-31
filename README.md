# Agentic Chunking

LangChain을 활용한 지능형 텍스트 청킹 시스템

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://www.langchain.com/)

## 개요

**Agentic Chunking**은 텍스트를 의미적 단위로 분할하는 지능형 시스템입니다. 기존의 단순한 길이 기반 청킹과 달리, LLM을 활용하여 텍스트의 의미적 구조를 분석하고 관련 있는 내용들을 그룹화합니다.

## 시스템 아키텍처

### 전체 시스템 구성도

```mermaid
graph TB
    A[사용자 입력 텍스트] --> B[AgenticChunker]
    B --> C[명제 추출]
    C --> D[청킹 프로세스]
    D --> E[청크 생성 및 관리]

    subgraph "AgenticChunker 클래스"
        F[add_proposition]
        G[_find_relevant_chunk]
        H[_create_new_chunk]
        I[_update_chunk_metadata]
        J[extract_propositions_from_text]
    end

    subgraph "외부 의존성"
        K[OpenAI GPT 모델]
        L[환경 설정]
        M[Pydantic 모델]
    end

    B --> F
    F --> G
    G --> K
    F --> H
    H --> I
    I --> K
    C --> J
    J --> K

    L --> B
    M --> B
```

### 데이터 흐름

```mermaid
sequenceDiagram
    participant User
    participant Main
    participant Chunker
    participant LLM
    participant Models

    User->>Main: 텍스트 입력
    Main->>Chunker: AgenticChunker 초기화
    Chunker->>Models: Pydantic 모델 로드

    Main->>Chunker: extract_propositions_from_text()
    Chunker->>LLM: 명제 추출 요청
    LLM-->>Chunker: 추출된 명제 리스트
    Chunker-->>Main: 명제 리스트 반환

    Main->>Chunker: add_propositions()
    loop 각 명제에 대해
        Chunker->>Chunker: _find_relevant_chunk()
        Chunker->>LLM: 관련 청크 검색
        LLM-->>Chunker: 청크 ID 또는 NONE
        alt 관련 청크 발견
            Chunker->>Chunker: _add_proposition_to_chunk()
        else 관련 청크 없음
            Chunker->>Chunker: _create_new_chunk()
        end
        Chunker->>Chunker: _update_chunk_metadata()
        Chunker->>LLM: 요약/제목 생성
        LLM-->>Chunker: 메타데이터
    end

    Main->>Chunker: print_chunks()
    Chunker-->>Main: 청크 결과 출력
```

## 코드 설명

### AgenticChunker 클래스
텍스트를 의미있는 단위로 분할하는 메인 클래스

- `extract_propositions_from_text()` - 텍스트를 명제로 분해
- `add_propositions()` - 명제들을 청크로 그룹화
- `print_chunks()` - 결과 출력

### 데이터 모델
Pydantic을 사용한 구조화된 데이터

- `ChunkID` - 청크 식별자
- `ChunkSummary` - 요약 텍스트
- `ChunkTitle` - 청크 제목
- `PropositionList` - 명제 리스트

## 핵심 다이어그램

### 시스템 구조도
```mermaid
graph TB
    A[텍스트 입력] --> B[AgenticChunker]
    B --> C[명제 추출]
    C --> D[청크 생성]
    D --> E[요약/제목 생성]
```

### 작업 흐름도
```mermaid
flowchart TD
    A[텍스트 입력] --> B[명제 추출]
    B --> C[청크 검색/생성]
    C --> D[메타데이터 추가]
    D --> E[결과 출력]
```

## 사용법

```python
from agentic_chunker import AgenticChunker

# 1. 초기화
chunker = AgenticChunker()

# 2. 텍스트에서 명제 추출
text = "여기에 긴 텍스트 입력..."
propositions = chunker.extract_propositions_from_text(text)

# 3. 청킹 실행
chunker.add_propositions(propositions)

# 4. 결과 출력
chunker.print_chunks()
```

## 테스트 결과

### 샘플 텍스트 청킹 결과

```
📊 전체 통계:
   • 총 청크 수: 8개
   • 총 명제 수: 35개
   • 평균 청크당 명제 수: 4.4개

📈 각 청크별 명제 수:
   청크 1: 4개 명제 - "인공지능 핵심 기술"
   청크 2: 1개 명제 - "자연어 처리 기술"
   청크 3: 5개 명제 - "기후 변화와 재생 에너지"
   청크 4: 7개 명제 - "한국 전통 음식과 건강"
   청크 5: 5개 명제 - "우주 탐사와 미래 목표"
   청크 6: 5개 명제 - "디지털 교육 혁신"
   청크 7: 3개 명제 - "건강한 생활 습관"
   청크 8: 5개 명제 - "경제 원리와 변화"
```

### 생성된 청크 예시

**청크: 인공지능 핵심 기술**
- 인공지능은 현재 우리 사회의 모든 분야에서 혁신을 이끌고 있다.
- 머신러닝 알고리즘은 대량의 데이터를 처리하고 인간이 놓칠 수 있는 패턴을 찾아낸다.
- 딥러닝은 머신러닝의 한 분야로, 다층 신경망을 사용하여 복잡한 문제를 해결한다.
- 컴퓨터 비전은 기계가 시각적 정보를 해석하고 분석할 수 있도록 한다.

**청크: 기후 변화와 재생 에너지**
- 기후 변화는 21세기 인류가 직면한 가장 심각한 문제 중 하나이다.
- 지구 온난화로 인해 빙하가 녹고 해수면이 상승하고 있다.
- 태양광과 풍력 같은 재생 에너지가 점점 더 경제적이 되고 있다.
- 전 세계가 탄소 중립을 위해 노력하고 있다.

## 파일 구조

- `agentic_chunker.py` - 메인 청킹 클래스
- `config.py` - 설정 파일
- `main.py` - 실행 파일
- `models.py` - 데이터 모델
- `requirements.txt` - 의존성

## 라이선스

MIT License
