"""
后端配置文件
用于管理环境变量和配置参数
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 项目根目录
BASE_DIR = Path(__file__).parent

# 加载 .env 文件（本地开发环境）
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"✓ 已加载本地环境配置: {env_path}")

# 数据目录
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"

# 问卷知识库文件路径
SURVEY_DATA_FILE = DATA_DIR / "ques0313.txt"

# OpenAI API 配置（使用环境变量，避免硬编码）
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.v3.cm/v1/')

# 检查必需的环境变量
if not OPENAI_API_KEY:
    raise ValueError('OPENAI_API_KEY 环境变量未设置，请在 .env 文件或环境变量中配置')

# AI 模型配置
AI_MODEL = "cc-sonnet-4-5-20250929"
MAX_TOKENS = 4000
TEMPERATURE = 0.7

# RAG 配置
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
SIMILARITY_TOP_K = 3

# Flask 配置
FLASK_HOST = '0.0.0.0'
FLASK_PORT = int(os.getenv('PORT', 5001))  # Zeabur 会提供 PORT 环境变量
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# CORS 配置
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',')
