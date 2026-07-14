import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import run_in_threadpool

from api.schemas import ChatRequest, ChatResponse
from chains.rag_chain import SSORagChain
from config import CORS_ORIGINS

# Configure basic logging for the API layer
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Global variable to hold our AI model in memory
rag_chain = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events.
    Loads the heavy RAG chain into memory exactly once at boot time.
    """
    global rag_chain
    logger.info("Initializing SSO RAG Chain into memory...")
    try:
        rag_chain = SSORagChain()
        logger.info("✅ SSO RAG Chain loaded successfully. Ready for traffic.")
    except Exception as e:
        logger.error(f"❌ Failed to initialize RAG Chain: {e}")
        raise RuntimeError("Could not load AI components.") from e
    
    # The application runs while yielded
    yield 
    
    logger.info("Shutting down API...")

# Initialize FastAPI App
app = FastAPI(
    title="Sikkim SSO AI Chatbot API",
    description="RAG-powered API microservice for answering SSO portal queries.",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS so your Node.js backend can communicate with it
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Accepts a JSON payload with a question and returns the AI answer.
    """
    if not rag_chain:
        raise HTTPException(status_code=503, detail="AI Service is currently initializing or unavailable.")

    logger.info("Incoming query (%d characters)", len(request.question))
    
    try:
        # Pass debug=False in production to keep terminal logs clean
        # Ollama and Chroma calls are synchronous. Offloading them keeps the
        # async server responsive to health checks and other requests.
        answer = await run_in_threadpool(rag_chain.invoke, request.question, False)
        return ChatResponse(answer=answer)
    except Exception:
        logger.exception("Error during RAG generation")
        raise HTTPException(status_code=500, detail="An internal server error occurred while processing the query.")
