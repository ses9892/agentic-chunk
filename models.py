"""
Pydantic 모델 정의
"""
from pydantic import BaseModel, Field
from typing import List, Optional

class ChunkID(BaseModel):
    """청크 ID를 추출하기 위한 스키마"""
    chunk_id: str = Field(description="관련 청크의 ID, 관련성이 없으면 'NONE'")

class ChunkSummary(BaseModel):
    """청크 요약을 생성하기 위한 스키마"""
    summary: str = Field(description="청크 내용의 간결한 요약")

class ChunkTitle(BaseModel):
    """청크 제목을 생성하기 위한 스키마"""
    title: str = Field(description="청크 내용을 나타내는 간결한 제목")

class PropositionList(BaseModel):
    """명제 리스트를 추출하기 위한 스키마"""
    propositions: List[str] = Field(description="텍스트에서 추출된 명제들의 리스트")
