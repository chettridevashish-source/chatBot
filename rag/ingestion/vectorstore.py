from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from config import VECTORSTORE_DIR, EMBEDDING_MODEL

class ChromaManager:
    def __init__(self):
        """
        Initializes the Vector Store manager using absolute paths from config.
        """
        self.persist_directory = str(VECTORSTORE_DIR)
        self.embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

    def get_vectorstore(self) -> Chroma:
        """
        Returns the Chroma vector store instance. 
        """
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )