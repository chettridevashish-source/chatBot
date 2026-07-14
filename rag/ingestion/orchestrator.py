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
from config import DOWNLOADS_DIR
from vectorstore.vectorstore import delete_documents_by_source, get_vectorstore

# Path to our new ledger file that tracks what we've already processed
STATE_FILE = BASE_DIR / "data" / "ingested_state.json"

def get_file_hash(filepath: Path) -> str:
    """Generates a SHA-256 fingerprint of the file's exact contents."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()

def load_state():
    """Loads the ledger of previously ingested files."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r', encoding="utf-8") as f:
                state = json.load(f)
            return state if isinstance(state, dict) else {}
        except (OSError, json.JSONDecodeError):
            print("Warning: ignoring unreadable ingestion state file.")
    return {}

def save_state(state):
    """Saves the updated ledger."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w', encoding="utf-8") as f:
        json.dump(state, f, indent=4)

def _state_hash(entry: str | dict | None) -> str | None:
    return entry if isinstance(entry, str) else entry.get("hash") if isinstance(entry, dict) else None


def _chunk_ids(filename: str, source_hash: str, count: int) -> list[str]:
    return [f"{filename}:{source_hash}:{index}" for index in range(count)]


def run_ingestion_pipeline(folder_path: str | Path = DOWNLOADS_DIR):
    print("🚀 Starting Smart Ingestion Pipeline...")
    folder = Path(folder_path).resolve()
    if not folder.exists():
        raise FileNotFoundError(f"PDF folder does not exist: {folder}")

    vectorstore = get_vectorstore()
    loader = DocumentLoader(str(folder))
    splitter = DocumentSplitter()
    state = load_state()
    new_ingestions = 0
    current_files = {path.name for path in folder.glob("*.pdf")}

    for filename in sorted(current_files):
        file_path = folder / filename
        current_hash = get_file_hash(file_path)
        previous_hash = _state_hash(state.get(filename))
        if previous_hash == current_hash:
            print(f"⏭️  Skipped (Already up to date): {filename}")
            continue

        print(f"📄 Processing new/updated file: {filename}")
        docs = loader.load_pdf(file_path)
        splits = splitter.split_documents(docs)
        if not splits:
            print(f"Warning: no text extracted; keeping the previous index: {filename}")
            continue

        for chunk in splits:
            chunk.metadata["source_hash"] = current_hash

        # State files created before version metadata did not tag chunks with
        # source_hash, so they need one one-time replacement migration.
        if isinstance(state.get(filename), str):
            delete_documents_by_source(vectorstore, filename)
        vectorstore.add_documents(splits, ids=_chunk_ids(filename, current_hash, len(splits)))
        if previous_hash and not isinstance(state.get(filename), str):
            delete_documents_by_source(vectorstore, filename, previous_hash)
        state[filename] = {"hash": current_hash, "chunks": len(splits)}
        new_ingestions += 1
        print(f"Ingested into VectorDB: {filename}")

    deleted_files = set(state) - current_files
    for filename in deleted_files:
        delete_documents_by_source(vectorstore, filename)
        del state[filename]
        new_ingestions += 1
        print(f"🗑️ Removed deleted source from VectorDB: {filename}")

    if new_ingestions:
        save_state(state)
        print(f"Smart Ingestion Complete! Processed {new_ingestions} new/updated documents.")
    else:
        print(" No new changes detected. Database is perfectly synced.")

if __name__ == "__main__":
    run_ingestion_pipeline()
