from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from loader import DocumentLoader


class DocumentSplitter:

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ],
        )

    def split_documents(
        self,
        documents: list[Document],
    ) -> list[Document]:

        chunks = self.splitter.split_documents(documents)

        print(f"\nOriginal Documents : {len(documents)}")
        print(f"Total Chunks       : {len(chunks)}")

        return chunks


if __name__ == "__main__":

    loader = DocumentLoader("../data/raw")

    documents = loader.load_documents()

    splitter = DocumentSplitter()

    chunks = splitter.split_documents(documents)

    print("\n" + "=" * 60)
    print("Sample Chunk")
    print("=" * 60)

    print(chunks[0].page_content)

    print("\nMetadata")

    print(chunks[0].metadata)