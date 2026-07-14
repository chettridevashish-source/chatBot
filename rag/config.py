from pathlib import Path
import os

from dotenv import load_dotenv

# Absolute path to the root of the project (rag directory)
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Directory definitions
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
DOWNLOADS_DIR = DATA_DIR / "downloads"
VECTORSTORE_DIR = BASE_DIR / "vectorstore" / "chroma_db"

# Ensure directories exist
VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Model settings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen3:8b")
RAG_HOST = os.getenv("RAG_HOST", "127.0.0.1")
RAG_PORT = int(os.getenv("RAG_PORT", "8000"))
RAG_RELOAD = os.getenv("RAG_RELOAD", "false").lower() == "true"

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
    if origin.strip()
]

# Text splitting settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval settings
RETRIEVER_K = 3
FETCH_K = 10
