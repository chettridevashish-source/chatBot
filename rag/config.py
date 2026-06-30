import os
from pathlib import Path

# Absolute path to the root of the project (rag directory)
BASE_DIR = Path(__file__).resolve().parent

# Directory definitions
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
VECTORSTORE_DIR = BASE_DIR / "vectorstore" / "chroma_db"

# Ensure directories exist
VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Model settings
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "qwen3:8b" 

# Text splitting settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval settings
RETRIEVER_K = 3
FETCH_K = 10