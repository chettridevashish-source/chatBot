import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import run_in_threadpool

import asyncio
from api.schemas import ChatRequest, ChatResponse
from chains.rag_chain import SSORagChain
from config import (
    CORS_ORIGINS,
    MAX_CONCURRENT_REQUESTS,
    MAX_QUEUE_SIZE,
    QUEUE_TIMEOUT
)

# Configure basic logging for the API layer
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class InferenceQueue:
    def __init__(self, max_concurrent: int, max_queue_size: int):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.max_queue_size = max_queue_size
        self.current_waiters = 0

    async def wait_and_acquire(self, timeout: float):
        if self.current_waiters >= self.max_queue_size:
            logger.warning("Queue full. Rejecting request.")
            raise HTTPException(status_code=429, detail="Server is overloaded. Too many requests in queue.")
        
        self.current_waiters += 1
        try:
            await asyncio.wait_for(self.semaphore.acquire(), timeout=timeout)
        except asyncio.TimeoutError:
            logger.warning("Queue timeout. Rejecting request.")
            raise HTTPException(status_code=504, detail="Request timed out waiting for an available worker.")
        finally:
            self.current_waiters -= 1
            
    def release(self):
        self.semaphore.release()

inference_queue = InferenceQueue(max_concurrent=MAX_CONCURRENT_REQUESTS, max_queue_size=MAX_QUEUE_SIZE)

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

from fastapi.responses import StreamingResponse

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Accepts a JSON payload with a question and returns a streamed AI answer.
    """
    if not rag_chain:
        raise HTTPException(status_code=503, detail="AI Service is currently initializing or unavailable.")

    logger.info("Incoming query (%d characters)", len(request.question))
    
    # 1. Wait in queue before accepting the streaming response
    await inference_queue.wait_and_acquire(timeout=QUEUE_TIMEOUT)
    
    async def generate():
        try:
            async for chunk in rag_chain.astream_with_telemetry(request.question):
                yield chunk
        except Exception as e:
            logger.exception("Error during RAG generation")
            yield " [Error: An internal server error occurred while processing the query.]"
        finally:
            # 2. Release when stream ends or disconnects
            inference_queue.release()

    return StreamingResponse(generate(), media_type="text/plain")
