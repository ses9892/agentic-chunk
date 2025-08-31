# 🤖 Agentic Chunking

LangChain을 활용한 지능형 텍스트 청킹 시스템

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://www.langchain.com/)

## 📋 개요

**Agentic Chunking**은 LangChain을 사용하여 텍스트를 지능적으로 청킹하는 시스템입니다. 기존의 단순한 길이 기반 청킹과 달리, LLM(대형 언어 모델)을 활용하여 텍스트의 의미적 구조를 분석하고 최적의 청킹 전략을 자동으로 선택합니다.

## ✨ 주요 특징

- **지능형 전략 선택**: 텍스트 분석을 통해 최적의 청킹 전략 자동 선택
- **다양한 청킹 전략**: 의미 기반, 주제 기반, 계층적 청킹 지원
- **품질 평가**: 청킹 결과의 품질을 다양한 메트릭으로 평가
- **유연한 설정**: 청크 크기, 전략 파라미터 등 커스터마이징 가능

## 🏗️ 지원하는 청킹 전략

### 1. **Semantic Chunking (의미 기반 청킹)**
- 텍스트의 의미적 유사도를 분석하여 관련 있는 부분들을 그룹화
- 장점: 의미적으로 일관된 청크 생성
- 적합: 기술 문서, 학술 논문

### 2. **Topic-based Chunking (주제 기반 청킹)**
- 텍스트의 주제 변화를 감지하여 주제별로 청킹
- 장점: 주제별로 자연스러운 분할
- 적합: 뉴스 기사, 블로그 포스트

### 3. **Hierarchical Chunking (계층적 청킹)**
- 텍스트의 계층적 구조(제목, 소제목 등)를 고려한 청킹
- 장점: 문서의 구조적 특성 보존
- 적합: 장편 문서, 구조화된 콘텐츠

## 🚀 설치 및 설정

### 1. 환경 설정

```bash
# 가상환경 생성 (선택사항)
python -m venv agentic_chunking_env
source agentic_chunking_env/bin/activate  # Linux/Mac
# 또는
agentic_chunking_env\Scripts\activate     # Windows

# 의존성 설치
pip install -r requirements.txt
```

### 2. OpenAI API 키 설정

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

또는 `.env` 파일 생성:
```
OPENAI_API_KEY=your-openai-api-key-here
```

## 📖 사용법

### 기본 사용법

```python
from src.agentic_chunking import ChunkingAgent

# 청킹 에이전트 초기화
agent = ChunkingAgent(
    model_name="gpt-4o-mini",  # 사용할 모델
    temperature=0.1,           # 생성 창의성 (0.0-1.0)
    api_key="your-api-key"     # OpenAI API 키
)

# 샘플 텍스트
text = """
머신러닝의 기초부터 심화까지...
[여기에 긴 텍스트 입력]
"""

# 자동 전략 선택으로 청킹
result = agent.chunk_text(text, auto_analyze=True)

print(f"생성된 청크 수: {len(result.chunks)}")
print(f"선택된 전략: {result.strategy_used}")
print(f"신뢰도: {result.confidence_score:.2f}")

# 각 청크 출력
for i, chunk in enumerate(result.chunks, 1):
    print(f"\n청크 {i}:")
    print(chunk)
```

### 특정 전략 사용

```python
# 의미 기반 청킹 명시적 사용
result = agent.chunk_text(
    text,
    strategy="semantic",
    max_chunk_size=1000,
    min_chunk_size=200
)
```

### 청킹 결과 평가

```python
from src.agentic_chunking.utils import ChunkEvaluator

evaluator = ChunkEvaluator()
evaluation = evaluator.evaluate_chunks(result.chunks, text)

print(f"평균 청크 길이: {evaluation['average_chunk_length']:.1f}")
print(f"품질 점수: {evaluation['average_quality_score']:.2f}")
print(f"텍스트 커버리지: {evaluation['text_coverage_ratio']:.2f}")
```

## 🎯 데모 실행

프로젝트에 포함된 데모를 실행해보세요:

```bash
python examples/basic_usage.py
```

데모에서는 머신러닝 관련 샘플 텍스트를 사용하여 각 전략의 동작을 보여줍니다.

## 📊 평가 메트릭

청킹 결과는 다음 메트릭으로 평가됩니다:

- **기본 통계**: 청크 수, 평균/최대/최소 길이
- **품질 점수**: 문장 완성도, 어휘 다양성 기반 점수
- **일관성**: 텍스트 커버리지, 중복도
- **분포 분석**: 길이 및 문장 수 분포

## 🛠️ 고급 설정

### 청킹 전략 파라미터

```python
# 의미 기반 청킹 설정
result = agent.chunk_text(
    text,
    strategy="semantic",
    max_chunk_size=1200,
    min_chunk_size=300,
    overlap=50  # 청크 간 중복 허용
)

# 주제 기반 청킹 설정
result = agent.chunk_text(
    text,
    strategy="topic_based",
    preserve_topics=True,  # 주제 정보 유지
    max_chunk_size=1000
)

# 계층적 청킹 설정
result = agent.chunk_text(
    text,
    strategy="hierarchical",
    preserve_hierarchy=True,  # 계층 구조 유지
    include_headers=True,     # 헤더 포함
    max_hierarchy_depth=3     # 최대 계층 깊이
)
```

### 커스텀 전략 추가

```python
from src.agentic_chunking.strategies import BaseChunkingStrategy

class CustomStrategy(BaseChunkingStrategy):
    def chunk(self, text: str, **kwargs) -> List[str]:
        # 커스텀 청킹 로직 구현
        pass

# 전략 등록
agent.add_strategy("custom", CustomStrategy())
```

## 📁 프로젝트 구조

```
agentic_chunking/
├── src/
│   └── agentic_chunking/
│       ├── __init__.py
│       ├── agents/
│       │   ├── __init__.py
│       │   └── chunking_agent.py       # 메인 청킹 에이전트
│       ├── strategies/
│       │   ├── __init__.py
│       ├── base_strategy.py            # 베이스 전략 클래스
│       ├── semantic_chunking.py        # 의미 기반 전략
│       ├── topic_based_chunking.py     # 주제 기반 전략
│       └── hierarchical_chunking.py    # 계층적 전략
│       └── utils/
│           ├── __init__.py
│           ├── chunk_evaluator.py       # 청킹 평가기
│           ├── text_analyzer.py         # 텍스트 분석기
│           └── result_formatter.py      # 결과 포맷터
├── examples/
│   └── basic_usage.py                   # 기본 사용 예제
├── tests/                               # 테스트 코드
├── requirements.txt                     # 의존성 목록
└── README.md                           # 프로젝트 설명
```

## 🤝 기여하기

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🙋‍♂️ 문의 및 지원

이슈나 질문이 있으시면 GitHub Issues를 통해 알려주세요.

---

**Agentic Chunking**으로 텍스트 청킹 작업을 더욱 지능적이고 효율적으로 수행해보세요! 🚀
