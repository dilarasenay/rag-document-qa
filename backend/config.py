import os
from dotenv import load_dotenv

load_dotenv()

# Proje ana dizini
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Upload klasörü (HER ZAMAN ROOT ALTINDA)
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

# API Key
OPENAI_API_KEY = os.getenv("APIKEY")

# RAG Ayarları
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K_RESULTS = 5

LLM_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 1000