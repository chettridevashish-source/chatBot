from langchain_core.vectorstores import VectorStoreRetriever
from ingestion.vectorstore import ChromaManager
from config import RETRIEVER_K, FETCH_K

class SSORetriever:
    def __init__(self):
        self.vectorstore = ChromaManager().get_vectorstore()

    def get_retriever(self, search_type: str = "mmr") -> VectorStoreRetriever:
        """
        Returns a configured retriever using Maximal Marginal Relevance.
        """
        return self.vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs={
                "k": RETRIEVER_K,
                "fetch_k": FETCH_K 
            }
        )