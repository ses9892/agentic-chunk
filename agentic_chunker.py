"""
Agentic Chunking 구현 - 개선된 버전
"""
import uuid
from typing import Dict, List, Optional, Any
from langchain_openai import ChatOpenAI
from models import ChunkID, ChunkSummary, ChunkTitle, PropositionList
import config
import warnings

# 경고 메시지 숨기기
warnings.filterwarnings("ignore", category=UserWarning)

class AgenticChunker:
    """
    Agentic Chunking을 수행하는 클래스
    """
    
    def __init__(self, model_name: str = config.DEFAULT_MODEL):
        """
        AgenticChunker 초기화
        
        Args:
            model_name: 사용할 OpenAI 모델명
        """
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=config.TEMPERATURE,
            api_key=config.OPENAI_API_KEY
        )
        self.chunks: Dict[str, Dict[str, Any]] = {}
        print("✅ AgenticChunker initialized successfully")
    
    def add_propositions(self, propositions: List[str]) -> None:
        """
        명제 리스트를 처리하여 청크에 추가
        
        Args:
            propositions: 처리할 명제들의 리스트
        """
        for proposition in propositions:
            self.add_proposition(proposition)
    
    def add_proposition(self, proposition: str) -> None:
        """
        단일 명제를 처리하여 적절한 청크에 추가
        
        Args:
            proposition: 처리할 명제
        """
        print(f"\n🔄 Adding: '{proposition}'")
        
        if not self.chunks:
            print("📝 No chunks exist, creating a new one")
            chunk_id = self._create_new_chunk(proposition)
            return
        
        # 관련 청크 찾기 (더 엄격한 기준 적용)
        relevant_chunk_id = self._find_relevant_chunk(proposition)
        
        if relevant_chunk_id:
            print(f"✅ Found relevant chunk ({relevant_chunk_id[:5]}), adding proposition")
            self._add_proposition_to_chunk(relevant_chunk_id, proposition)
            self._update_chunk_metadata(relevant_chunk_id)
        else:
            print("❌ No relevant chunks found, creating new chunk")
            self._create_new_chunk(proposition)
    
    def _find_relevant_chunk(self, proposition: str) -> Optional[str]:
        """
        주어진 명제와 관련된 청크를 찾습니다. (더 엄격한 기준)
        
        Args:
            proposition: 검색할 명제
            
        Returns:
            관련 청크의 ID 또는 None
        """
        if not self.chunks:
            return None
        
        # 기존 청크들의 정보를 수집
        chunk_info = ""
        for chunk_id, chunk_data in self.chunks.items():
            chunk_info += f"Chunk ID: {chunk_id}\n"
            chunk_info += f"Summary: {chunk_data['summary']}\n"
            chunk_info += f"Title: {chunk_data['title']}\n"
            # 기존 명제들도 포함하여 더 정확한 판단
            chunk_info += f"Existing propositions: {'; '.join(chunk_data['propositions'][:3])}...\n\n"
        
        # function_calling 방식으로 명시적 설정
        if config.DEFAULT_MODEL == "gpt-3.5-turbo":
            structured_llm = self.llm.with_structured_output(
                ChunkID, 
                method="function_calling"
            )
        else:
            structured_llm = self.llm.with_structured_output(ChunkID)
        
        prompt = f"""
다음 명제와 기존 청크들을 비교하여 관련성을 판단해주세요.

새로운 명제: "{proposition}"

기존 청크들:
{chunk_info}

판단 기준:
1. 주제적 관련성: 같은 주제나 도메인인가?
2. 의미적 연관성: 내용이 논리적으로 연결되는가?
3. 맥락적 일관성: 함께 있을 때 의미가 있는가?

매우 관련성이 높은 경우에만 기존 청크 ID를 반환하고,
조금이라도 다른 주제나 맥락이면 "NONE"을 반환하세요.

예시:
- "10월입니다"와 "2023년입니다" → 관련성 높음 (시간 정보)
- "날씨가 좋습니다"와 "쿠키를 좋아합니다" → 관련성 낮음 (다른 주제)
- "AI는 변화를 가져옵니다"와 "머신러닝은 데이터를 처리합니다" → 관련성 높음 (AI 주제)
"""
        
        try:
            result = structured_llm.invoke(prompt)
            
            if result.chunk_id == "NONE" or result.chunk_id not in self.chunks:
                return None
            return result.chunk_id
            
        except Exception as e:
            print(f"⚠️ 청크 찾기 중 오류 발생: {e}")
            return None
    
    def _create_new_chunk(self, proposition: str) -> str:
        """
        새로운 청크를 생성합니다.
        
        Args:
            proposition: 청크에 추가할 첫 번째 명제
            
        Returns:
            생성된 청크의 ID
        """
        chunk_id = str(uuid.uuid4())[:8]  # 8자리 UUID
        
        # 청크 초기화
        self.chunks[chunk_id] = {
            'propositions': [proposition],
            'summary': '',
            'title': ''
        }
        
        # 메타데이터 생성
        self._update_chunk_metadata(chunk_id)
        
        title = self.chunks[chunk_id]['title']
        print(f"🆕 Created new chunk ({chunk_id}): {title}")
        
        return chunk_id
    
    def _add_proposition_to_chunk(self, chunk_id: str, proposition: str) -> None:
        """
        기존 청크에 명제를 추가합니다.
        
        Args:
            chunk_id: 대상 청크 ID
            proposition: 추가할 명제
        """
        if chunk_id in self.chunks:
            self.chunks[chunk_id]['propositions'].append(proposition)
    
    def _update_chunk_metadata(self, chunk_id: str) -> None:
        """
        청크의 메타데이터(요약, 제목)를 업데이트합니다.
        
        Args:
            chunk_id: 업데이트할 청크 ID
        """
        if chunk_id not in self.chunks:
            return
        
        propositions = self.chunks[chunk_id]['propositions']
        propositions_text = '\n'.join(propositions)
        
        # 요약 생성
        summary = self._generate_summary(propositions_text)
        self.chunks[chunk_id]['summary'] = summary
        
        # 제목 생성
        title = self._generate_title(propositions_text)
        self.chunks[chunk_id]['title'] = title
    
    def _generate_summary(self, text: str) -> str:
        """
        텍스트의 요약을 생성합니다.
        
        Args:
            text: 요약할 텍스트
            
        Returns:
            생성된 요약
        """
        if config.DEFAULT_MODEL == "gpt-3.5-turbo":
            structured_llm = self.llm.with_structured_output(
                ChunkSummary, 
                method="function_calling"
            )
        else:
            structured_llm = self.llm.with_structured_output(ChunkSummary)
        
        prompt = f"""
다음 텍스트의 핵심 내용을 간결하게 요약해주세요.

텍스트:
{text}

지침:
- 1-2문장으로 핵심 내용을 요약하세요
- 주요 개념과 아이디어를 포함하세요
- 명확하고 이해하기 쉽게 작성하세요
"""
        
        try:
            result = structured_llm.invoke(prompt)
            return result.summary
        except Exception as e:
            print(f"⚠️ 요약 생성 중 오류 발생: {e}")
            return "요약 생성 실패"
    
    def _generate_title(self, text: str) -> str:
        """
        텍스트의 제목을 생성합니다.
        
        Args:
            text: 제목을 생성할 텍스트
            
        Returns:
            생성된 제목
        """
        if config.DEFAULT_MODEL == "gpt-3.5-turbo":
            structured_llm = self.llm.with_structured_output(
                ChunkTitle, 
                method="function_calling"
            )
        else:
            structured_llm = self.llm.with_structured_output(ChunkTitle)
        
        prompt = f"""
다음 텍스트의 내용을 나타내는 간결한 제목을 생성해주세요.

텍스트:
{text}

지침:
- 3-5단어로 간결하게 작성하세요
- 텍스트의 주요 주제를 반영하세요
- 명확하고 기억하기 쉽게 작성하세요
"""
        
        try:
            result = structured_llm.invoke(prompt)
            return result.title
        except Exception as e:
            print(f"⚠️ 제목 생성 중 오류 발생: {e}")
            return "제목 생성 실패"
    
    def get_chunks(self) -> Dict[str, Dict[str, Any]]:
        """
        모든 청크를 반환합니다.
        
        Returns:
            청크 딕셔너리
        """
        return self.chunks
    
    def print_chunks(self) -> None:
        """
        모든 청크를 출력합니다.
        """
        print(f"\n📊 Total chunks created: {len(self.chunks)}")
        print("=" * 80)
        
        for chunk_id, chunk_data in self.chunks.items():
            print(f"\n🏷️ Chunk ID: {chunk_id}")
            print(f"📝 Title: {chunk_data['title']}")
            print(f"📄 Summary: {chunk_data['summary']}")
            print(f"📋 Propositions ({len(chunk_data['propositions'])}):")
            for i, prop in enumerate(chunk_data['propositions'], 1):
                print(f"   {i}. {prop}")
            print("-" * 40)
    
    def extract_propositions_from_text(self, text: str) -> List[str]:
        """
        텍스트에서 명제들을 추출합니다.
        
        Args:
            text: 명제를 추출할 텍스트
            
        Returns:
            추출된 명제들의 리스트
        """
        if config.DEFAULT_MODEL == "gpt-3.5-turbo":
            structured_llm = self.llm.with_structured_output(
                PropositionList, 
                method="function_calling"
            )
        else:
            structured_llm = self.llm.with_structured_output(PropositionList)
        
        prompt = f"""
다음 텍스트를 의미있는 명제(proposition)들로 분해해주세요.

텍스트:
{text}

지침:
- 각 명제는 하나의 완전한 아이디어나 사실을 담아야 합니다
- 명제는 독립적으로 이해 가능해야 합니다
- 너무 세분화하지 말고, 의미있는 단위로 분해하세요
- 각 명제는 한 문장으로 표현하세요
"""
        
        try:
            result = structured_llm.invoke(prompt)
            return result.propositions
        except Exception as e:
            print(f"⚠️ 명제 추출 중 오류 발생: {e}")
            return []
