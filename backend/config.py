import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# Proje Dizinleri
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

# =========================
# API Key
# =========================
# Öncelik OPENAI_API_KEY; eski kullanım için APIKEY de desteklenir.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("APIKEY")

# =========================
# RAG Ayarları
# =========================
CHUNK_SIZE = 600
CHUNK_OVERLAP = 100

# Türkçe dokümanlar için daha iyi embedding modeli
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

TOP_K_RESULTS = 5
DEFAULT_TOP_K = 5
MAX_TOP_K = 10

# =========================
# LLM Ayarları
# =========================
LLM_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 1000
TEMPERATURE = 0.2

# =========================
# Dosya Ayarları
# =========================
ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt"]
MAX_UPLOAD_MB = 50
MAX_UPLOAD_SIZE = MAX_UPLOAD_MB * 1024 * 1024