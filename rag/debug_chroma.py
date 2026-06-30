from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

db = Chroma(
    persist_directory="./vectorstore/chroma_db",
    embedding_function=OllamaEmbeddings(
        model="nomic-embed-text"
    ),
)

collection = db._collection

print("Number of documents:", collection.count())