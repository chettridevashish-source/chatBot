from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from ingestion.loader import DocumentLoader
from ingestion.splitter import DocumentSplitter


class VectorStore:

    def __init__(
        self,
        persist_directory: str | None = None,
        embedding_model: str = "nomic-embed-text:latest",
    ):

        if persist_directory is None:
            BASE_DIR = Path(__file__).resolve().parent.parent
            persist_directory = BASE_DIR / "vectorstore" / "chroma_db"

        self.persist_directory = str(persist_directory)

        self.embeddings = OllamaEmbeddings(
            model=embedding_model
        )

        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
        )

    def add_documents(
        self,
        documents: list[Document],
    ):

        self.vectorstore.add_documents(documents)

        print(f"✅ Added {len(documents)} chunks to ChromaDB.")

    def reset_database(self):

        try:
            self.vectorstore.delete_collection()

            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
            )

            print("✅ Existing Chroma collection deleted.")

        except Exception:
            print("ℹ️ No previous collection found.")

    def get_vectorstore(self):

        return self.vectorstore


if __name__ == "__main__":

    print("=" * 60)
    print("Loading Documents")
    print("=" * 60)

    loader = DocumentLoader("../data/raw")

    documents = loader.load_documents()

    print("=" * 60)
    print("Splitting Documents")
    print("=" * 60)

    splitter = DocumentSplitter()

    chunks = splitter.split_documents(documents)

    print("=" * 60)
    print("Creating Vector Store")
    print("=" * 60)

    vectorstore = VectorStore()

    # Delete old embeddings
    vectorstore.reset_database()

    # Add new chunks
    vectorstore.add_documents(chunks)

    print("=" * 60)
    print("Vector Store Ready")
    print("=" * 60)