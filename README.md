# Sikkim SSO Assistant

A retrieval-augmented chatbot for Sikkim SSO service manuals. PDFs are ingested into ChromaDB, retrieved per question, and answered through a local Ollama model.

## Architecture

`frontend → Express (/api/chat) → FastAPI (/chat) → ChromaDB + Ollama`

The ingestion job downloads or reads PDF manuals, splits their pages into overlapping chunks, and tracks source hashes. Re-ingesting a changed PDF replaces only its old chunks; removing a PDF removes its indexed chunks.

## Prerequisites

- Python 3.11+
- Node.js 20+
- [Ollama](https://ollama.com/) running locally
- Ollama models: `ollama pull nomic-embed-text` and `ollama pull qwen3:8b`

## Run locally

1. Start the RAG API:

   ```bash
   cd rag
   uv sync
   cp .env.example .env
   uv run python main.py
   ```

2. In another terminal, start the Express API:

   ```bash
   cd backend
   npm install
   cp .env.example .env
   npm start
   ```

3. Serve the frontend on port 5500 and open it in your browser:

   ```bash
   cd frontend
   python3 -m http.server 5500
   ```

   If you use a different frontend origin, update `CLIENT_ORIGINS` to match it.

   The backend defaults to not starting Python automatically. To use one
   command for both services after the RAG environment is set up, set
   `AUTO_START_RAG=true` in `backend/.env`.

## Ingestion

Put source PDFs in `rag/data/downloads/`, then run:

```bash
cd rag
uv run python sync_all.py
```

Use `uv run python ingestion/orchestrator.py` when PDFs already exist locally and only indexing is needed.

## Tests

```bash
cd rag
uv run python -m unittest discover -s tests -v

cd ../backend
npm test
```

## Environment and security

Never commit `.env` files or API keys. The repository provides `.env.example` files with only non-secret configuration. If a key was ever committed, shared, or exposed, revoke and replace it in its provider dashboard.
