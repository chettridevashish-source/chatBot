from langchain_ollama import OllamaEmbeddings

from loader import DocumentLoader
from splitter import DocumentSplitter


class Embedder:

    def __init__(
        self,
        model="nomic-embed-text:latest",
    ):

        self.embeddings = OllamaEmbeddings(
            model=model
        )

    def embed_documents(self, documents):

        texts = [
            doc.page_content
            for doc in documents
        ]

        return self.embeddings.embed_documents(texts)

    def embed_query(self, query):

        return self.embeddings.embed_query(query)


if __name__ == "__main__":

    loader = DocumentLoader("../data/raw")

    documents = loader.load_documents()

    splitter = DocumentSplitter()

    chunks = splitter.split_documents(documents)

    embedder = Embedder()

    embeddings = embedder.embed_documents(chunks)

    print("=" * 60)
    print("Embedding Test")
    print("=" * 60)

    print(f"Chunks: {len(chunks)}")
    print(f"Embeddings: {len(embeddings)}")
    print(f"Embedding Dimension: {len(embeddings[0])}")