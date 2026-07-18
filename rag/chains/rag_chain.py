import time
import psutil
import os
from langchain_ollama import ChatOllama
from retriever.retriever import SSORetriever
from chains.prompts import sso_qa_prompt
from config import LLM_MODEL

class SSORagChain:
    def __init__(self):
        self.retriever = SSORetriever()
        # Optimized context and token generation limit
        self.llm = ChatOllama(
            model=LLM_MODEL, 
            temperature=0.0, 
            keep_alive=-1,
            num_ctx=2048
        )
        self.prompt = sso_qa_prompt

    def _format_docs(self, docs: list) -> str:
        if not docs:
            return ""
        return "\n\n".join(doc.page_content for doc in docs)

    async def astream_with_telemetry(self, question: str):
        overall_start = time.perf_counter()
        
        # 1. Retrieve (Instrumented)
        retrieval_start = time.perf_counter()
        retriever = self.retriever.get_retriever(question, search_type="similarity")
        docs = retriever.invoke(question) # SSORetriever uses sync invoke internally
        retrieval_time = time.perf_counter() - retrieval_start
        
        # 2. Format & Build Prompt (Instrumented)
        prompt_start = time.perf_counter()
        context = self._format_docs(docs)
        messages = self.prompt.format_messages(context=context, question=question)
        prompt_time = time.perf_counter() - prompt_start
        
        # 3. Generate Answer (Streaming & Instrumented)
        generation_start = time.perf_counter()
        response_metadata = {}
        generated_text_length = 0
        
        async for chunk in self.llm.astream(messages):
            if chunk.content:
                generated_text_length += len(chunk.content)
                yield chunk.content
            
            if hasattr(chunk, "response_metadata") and chunk.response_metadata:
                response_metadata.update(chunk.response_metadata)

        generation_time = time.perf_counter() - generation_start
        overall_time = time.perf_counter() - overall_start
        
        # 4. Telemetry Logging
        prompt_tokens = response_metadata.get("prompt_eval_count", 0)
        completion_tokens = response_metadata.get("eval_count", 0)
        
        # Fallback approximation if metadata isn't returned
        if completion_tokens == 0:
            completion_tokens = generated_text_length // 4 
            
        tokens_per_sec = completion_tokens / generation_time if generation_time > 0 else 0
        
        process = psutil.Process(os.getpid())
        mem_usage = process.memory_info().rss / (1024 * 1024)
        cpu_usage = process.cpu_percent()
        
        print("\n" + "="*50)
        print("🚀 [TELEMETRY] SSO RAG PERFORMANCE METRICS")
        print("="*50)
        print(f"Retrieval Time         : {retrieval_time:.4f} s (Includes embedding)")
        print(f"Prompt Construct Time  : {prompt_time:.4f} s")
        print(f"Generation Time        : {generation_time:.4f} s")
        print(f"Total Latency          : {overall_time:.4f} s")
        print("-" * 50)
        print(f"Prompt Tokens          : {prompt_tokens}")
        print(f"Completion Tokens      : {completion_tokens}")
        print(f"Tokens Per Second      : {tokens_per_sec:.2f} t/s")
        if "load_duration" in response_metadata:
            load_sec = response_metadata["load_duration"] / 1e9
            print(f"Model Load Time        : {load_sec:.4f} s")
        print("-" * 50)
        print(f"Memory Usage (RSS)     : {mem_usage:.2f} MB")
        print(f"CPU Usage              : {cpu_usage:.1f} %")
        print("="*50 + "\n")

    def invoke(self, question: str, debug: bool = False) -> str:
        # Fallback for synchronous non-streaming if still needed anywhere
        retriever = self.retriever.get_retriever(question, search_type="similarity")
        docs = retriever.invoke(question)
        context = self._format_docs(docs)
        messages = self.prompt.format_messages(context=context, question=question)
        return self.llm.invoke(messages).content
