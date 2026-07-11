from pathlib import Path
from langchain_core.documents import Document
from ingestion.loader import DocumentLoader

class DocumentSplitter:
    def __init__(self):
        # Disabling character splitting entirely to keep visual pages intact
        pass

    def split_documents(self, documents: list[Document]) -> list[Document]:
        """
        Keeps each loaded PDF page completely intact as its own semantic chunk.
        This ensures text descriptions and OCR-extracted image content from 
        the same page stay glued together.
        """
        chunks = documents # Each document page naturally becomes one chunk
        
        print(f"\nOriginal Document Pages : {len(documents)}")
        print(f"Total Page Chunks       : {len(chunks)}")
        return chunks

if __name__ == "__main__":
    # Robust path setup to match your project root structure
    current_script_dir = Path(__file__).resolve().parent
    project_root = current_script_dir.parent 
    target_data_dir = project_root / "data" / "downloads"
    
    print(f"Testing splitter on data from: {target_data_dir}")
    
    loader = DocumentLoader(str(target_data_dir))
    documents = loader.load_documents()
    
    splitter = DocumentSplitter()
    chunks = splitter.split_documents(documents)
    
    if len(chunks) > 0:
        print("\n" + "=" * 60)
        print("Sample Chunk (Page 1)")
        print("=" * 60)
        print(chunks[0].page_content[:1000]) # Print first 1000 chars of page 1
        print("\nMetadata")
        print(chunks[0].metadata)
    else:
        print("\n⚠️ No chunks created. Please make sure PDFs are loaded first.")