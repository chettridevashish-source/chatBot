from langchain_ollama import ChatOllama
from retriever.retriever import SSORetriever
from chains.prompts import sso_qa_prompt
from config import LLM_MODEL

class SSORagChain:
    def __init__(self):
        self.retriever = SSORetriever().get_retriever(search_type="mmr")
        self.llm = ChatOllama(model=LLM_MODEL, temperature=0.0)
        self.prompt = sso_qa_prompt

    def _format_docs(self, docs: list) -> str:
        if not docs:
            return ""
        return "\n\n".join(doc.page_content for doc in docs)

    def invoke(self, question: str, debug: bool = False) -> str:
        # 1. Retrieve
        docs = self.retriever.invoke(question)
        
        # 2. Format
        context = self._format_docs(docs)

        if debug:
            print(f"\n[DEBUG] Retrieved {len(docs)} documents.")
            if context:
                print(f"[DEBUG] Context Payload:\n{context[:500]}...\n")
            else:
                print("[DEBUG] WARNING: Context is empty! Check if Chroma has data.")

        # 3. Build Prompt Payload
        messages = self.prompt.format_messages(context=context, question=question)

        # 4. Generate Answer
        response = self.llm.invoke(messages)

        return response.content