from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


class DocumentLoader:

    def __init__(self, data_dir: str):

        self.data_dir = Path(data_dir)

    def find_pdf_files(self) -> list[Path]:

        return list(self.data_dir.rglob("*.pdf"))

    def load_pdf(self, pdf_path: Path) -> list[Document]:

        loader = PyPDFLoader(str(pdf_path))

        documents = loader.load()

        for document in documents:

            document.metadata["file_name"] = pdf_path.name

            document.metadata["file_path"] = str(pdf_path)

        return documents

    def load_documents(self) -> list[Document]:

        pdf_files = self.find_pdf_files()

        all_documents = []

        print(f"\nFound {len(pdf_files)} PDF(s).\n")

        for pdf in pdf_files:

            print(f"Loading {pdf.name}")

            all_documents.extend(self.load_pdf(pdf))

        print(f"\nLoaded {len(all_documents)} document pages.\n")

        return all_documents


if __name__ == "__main__":

    loader = DocumentLoader("../data/raw")

    documents = loader.load_documents()

    print(documents[0].page_content[:500])