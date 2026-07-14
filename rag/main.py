import sys
import uvicorn
from pathlib import Path

# 1. Safely resolve the root 'rag' directory
root_dir = Path(__file__).resolve().parent

# 2. INSERT at index 0 to guarantee Python prioritizes your local folders
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

if __name__ == "__main__":
    from config import RAG_HOST, RAG_PORT, RAG_RELOAD

    print("🚀 Starting Uvicorn Server for Sikkim SSO API...")
    uvicorn.run("api.main:app", host=RAG_HOST, port=RAG_PORT, reload=RAG_RELOAD)
