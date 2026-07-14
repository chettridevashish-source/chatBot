from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_OVERLAP, CHUNK_SIZE

class DocumentSplitter:
    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def split_documents(self, documents: list[Document]) -> list[Document]:
        """
        Splits pages into bounded, overlapping chunks while retaining the
        source metadata assigned by the loader.
        """
        chunks = self.splitter.split_documents(documents)

        for index, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = index
        
        print(f"\nOriginal Document Pages : {len(documents)}")
        print(f"Total Page Chunks       : {len(chunks)}")
        return chunks
