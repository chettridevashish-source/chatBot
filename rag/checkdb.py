import chromadb
from pathlib import Path

def view_all_chunks():
    # Safely resolve the path to your ChromaDB folder
    current_dir = Path(__file__).resolve().parent
    db_path = current_dir / "data" / "chroma_db"
    
    # Fallback to the old path if it's in vectorstore/
    if not db_path.exists():
        db_path = current_dir / "vectorstore" / "chroma_db"

    if not db_path.exists():
        print(f" Could not find database at {db_path.resolve()}")
        return

    print(f"Connected to Database: {db_path.resolve()}")
    
    client = chromadb.PersistentClient(path=str(db_path))
    collections = client.list_collections()
    
    if not collections:
        print(" No collections found. Your database is completely empty.")
        return
        
    for collection in collections:
        # .get() with no arguments fetches 100% of the stored data
        all_data = collection.get()
        total_chunks = len(all_data['ids'])
        
        print(f"\n Fetching {total_chunks} chunks from collection: '{collection.name}'...\n")
        
        if total_chunks == 0:
            continue
            
        # Loop through every single chunk and print its contents
        for i in range(total_chunks):
            chunk_id = all_data['ids'][i]
            metadata = all_data['metadatas'][i]
            content = all_data['documents'][i]
            
            file_name = metadata.get('file_name', 'Unknown')
            page_num = metadata.get('page_label', 'N/A')
            
            print("=" * 80)
            print(f" CHUNK INDEX : {i + 1} / {total_chunks}")
            print(f" SOURCE FILE : {file_name}")
            print(f" PAGE NUMBER : {page_num}")
            print(f" TEXT LENGTH : {len(content)} characters")
            print("-" * 80)
            print(f"{content}") 
            print("=" * 80 + "\n")

if __name__ == "__main__":
    print("Initiating full database text dump...")
    view_all_chunks()