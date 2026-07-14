import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

class DocumentLoader:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)

    def find_pdf_files(self) -> list[Path]:
        return list(self.data_dir.rglob("*.pdf"))

    def load_pdf(self, pdf_path: Path) -> list[Document]:
        # Enabling extract_images=True activates OCR scanning over screenshots
        loader = PyPDFLoader(str(pdf_path), extract_images=True)
        documents = loader.load()

        for document in documents:
            document.metadata["file_name"] = pdf_path.name
            document.metadata["file_path"] = str(pdf_path)

        return documents

    def load_documents(self) -> list[Document]:
        pdf_files = self.find_pdf_files()
        all_documents = []

        print(f"\nFound {len(pdf_files)} PDF(s) to process.")

        for pdf in pdf_files:
            print(f"📖 Loading and OCR-scanning: {pdf.name}...")
            try:
                all_documents.extend(self.load_pdf(pdf))
            except Exception as e:
                print(f"Error parsing {pdf.name}: {str(e)}")

        print(f"\n Successfully loaded {len(all_documents)} raw text/image pages.")
        return all_documents


if __name__ == "__main__":
    current_script_dir = Path(__file__).resolve().parent
    project_root = current_script_dir.parent 
    target_data_dir = project_root / "data" / "downloads"
    
    loader = DocumentLoader(str(target_data_dir))
    documents = loader.load_documents()

    if len(documents) > 0:
        print("\n--- Document Loaded Successfully ---")
        print(f"Sample Content:\n{documents[0].page_content[:500]}")