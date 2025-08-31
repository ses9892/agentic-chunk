"""
설정 파일
"""
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# OpenAI API 키
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 모델 설정
DEFAULT_MODEL = "gpt-4.1-mini"
TEMPERATURE = 0.1

# 청크 설정
MAX_CHUNK_SIZE = 1000
MIN_CHUNK_SIZE = 100
