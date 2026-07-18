# Sikkim SSO Assistant: User Manual

Use this guide to run the chatbot on a laptop for development or a demo. The app has three services that must run at the same time:

`React frontend (5173) → Express API (3000) → RAG API (8000) → Ollama`

## 1. What You Need

Install these before starting:

- Git
- Node.js 20 or newer
- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/) for the Python environment
- [Ollama](https://ollama.com/) for the local AI model

Check that the tools are available:

```bash
git --version
node --version
python3 --version
uv --version
ollama --version
```

## 2. Get the Project

Clone the project and open its folder:

```bash
git clone https://github.com/chettridevashish-source/chatBot.git
cd chatBot
```

If you already have the project, update it instead:

```bash
git pull origin main
```

## 3. Download the AI Models

Open Ollama, or start it in a terminal if it is not already running:

```bash
ollama serve
```

In a second terminal, download the models:

```bash
ollama pull nomic-embed-text
ollama pull qwen3:8b
```

For a faster laptop-friendly option, use `qwen3:4b` instead. If you choose it, set `LLM_MODEL=qwen3:4b` in `rag/.env` during the next step.

## 4. First-Time Setup

Run these commands once from the project folder.

### RAG service

```bash
cd rag
uv sync
cp .env.example .env
cd ..
```

On Windows PowerShell, replace `cp .env.example .env` with:

```powershell
Copy-Item .env.example .env
```

### Express API

```bash
cd backend
npm install
cp .env.example .env
cd ..
```

### React frontend

```bash
cd frontend/Chatbot
npm install
cd ../..
```

Do not commit any `.env` file to Git.

## 5. Start the App

Open four terminals. Keep each command running.

### Terminal 1: Ollama

```bash
ollama serve
```

Skip this terminal if the Ollama desktop app is already running.

### Terminal 2: RAG API

```bash
cd chatBot/rag
uv run python main.py
```

Expected message: the API is running at `http://127.0.0.1:8000`.

### Terminal 3: Express API

```bash
cd chatBot/backend
npm start
```

Expected message: `Backend listening on http://localhost:3000`.

### Terminal 4: React frontend

```bash
cd chatBot/frontend/Chatbot
npm run dev
```

Open the URL shown by Vite, normally `http://localhost:5173`.

## 6. Check That Everything Works

Before opening the frontend, check the Express API:

```bash
curl http://localhost:3000/health
```

It should return:

```json
{"status":"ok"}
```

Then open the React page and ask a question about an SSO service. The frontend sends requests to `/api/chat`; Vite automatically forwards them to the Express API.

## 7. Add or Update PDF Manuals

1. Put PDF files in `rag/data/downloads/`.
2. Stop the RAG service if it is running.
3. Rebuild the search index:

   ```bash
   cd chatBot/rag
   uv run python sync_all.py
   ```

4. Start the RAG service again.

The chatbot can only answer accurately from manuals that have been indexed.

## 8. Change the Chat Model

Edit `rag/.env` and update this line:

```env
LLM_MODEL=qwen3:8b
```

Recommended choices:

| Model | Use it when |
| --- | --- |
| `qwen3:4b` | You need faster responses on a normal laptop. |
| `qwen3:8b` | You want better answer quality and have sufficient RAM/VRAM. |

Download a model before selecting it:

```bash
ollama pull qwen3:4b
```

Restart the RAG service after changing the model.

## 9. Common Problems

### The chatbot says the server is not connected

Make sure the Express API is running in `backend` and the React app is opened at the Vite URL, normally port `5173`.

### The chatbot says the AI engine is offline

Start Ollama and the RAG API. Confirm the required models are installed:

```bash
ollama list
```

### Port already in use

Another program is using the port. Stop the previous terminal process with `Ctrl+C`, then start the service again. The required ports are `5173`, `3000`, `8000`, and `11434`.

### `uv` is not found

Install `uv`, close and reopen the terminal, then run `uv --version` again.

### `npm install` fails

Confirm Node.js 20 or newer is installed, then retry from the affected folder. Do not run `npm install` from the project root because the Node applications live in `backend` and `frontend/Chatbot`.

### Answers are slow

Use `qwen3:4b`, ask shorter questions, and avoid running other memory-heavy applications. For several simultaneous users, host Ollama and the RAG service on a machine with a suitable GPU.

## 10. Stop the App

In every terminal running a service, press `Ctrl+C`. This stops the app safely.

## 11. Run Automated Checks

From the project folder:

```bash
cd rag
uv run python -m unittest discover -s tests -v

cd ../backend
npm test

cd ../frontend/Chatbot
npm run build
```
