import os
import sys
import json
import hashlib
from pathlib import Path

# 1. Force Python to recognize the root 'rag' directory FIRST
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# 2. Safely import local modules
from ingestion.loader import DocumentLoader
from ingestion.splitter import DocumentSplitter
from vectorstore.vectorstore import get_vectorstore

# Path to our new ledger file that tracks what we've already processed
STATE_FILE = BASE_DIR / "data" / "ingested_state.json"

def get_file_hash(filepath):
    """Generates an MD5 fingerprint of the file's exact contents."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def load_state():
    """Loads the ledger of previously ingested files."""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_state(state):
    """Saves the updated ledger."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)

def run_ingestion_pipeline(folder_path="data/downloads/"):
    print("🚀 Starting Smart Ingestion Pipeline...")
    
    vectorstore = get_vectorstore()
    loader = DocumentLoader(folder_path)
    splitter = DocumentSplitter()
    
    state = load_state()
    new_ingestions = 0
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = Path(folder_path) / filename
            
            # Check the file's unique fingerprint
            current_hash = get_file_hash(file_path)
            
            # If we have seen this exact file content before, skip it
            if state.get(filename) == current_hash:
                print(f"⏭️  Skipped (Already up to date): {filename}")
                continue
            
            print(f"📄 Processing new/updated file: {filename}")
            docs = loader.load_pdf(file_path)
            splits = splitter.split_documents(docs)
            
            # Upsert the chunks into ChromaDB
            vectorstore.add_documents(splits)
            
            # Record the new fingerprint in our ledger
            state[filename] = current_hash
            new_ingestions += 1
            print(f"✅ Ingested into VectorDB: {filename}")
            
    # Save our updated ledger
    if new_ingestions > 0:
        save_state(state)
        print(f"🎉 Smart Ingestion Complete! Processed {new_ingestions} new/updated documents.")
    else:
        print("👍 No new changes detected. Database is perfectly synced.")

if __name__ == "__main__":
    run_ingestion_pipeline()