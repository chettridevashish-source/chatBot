from pathlib import Path
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from config import EMBEDDING_MODEL, VECTORSTORE_DIR

# Target the directory where chroma.sqlite3 is stored
CHROMA_PATH = VECTORSTORE_DIR

def get_vectorstore():
    # Configure Ollama embeddings 
    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        keep_alive=-1
    )
    
    vectorstore = Chroma(
        persist_directory=str(CHROMA_PATH),
        embedding_function=embeddings
    )
    return vectorstore


def delete_documents_by_source(vectorstore: Chroma, file_name: str, source_hash: str | None = None) -> None:
    """Delete chunks for a source, optionally limited to one ingested version."""
    where: dict = {"file_name": file_name}
    if source_hash:
        where = {"$and": [{"file_name": file_name}, {"source_hash": source_hash}]}
    vectorstore.delete(where=where)
