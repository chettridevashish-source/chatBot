import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chains.rag_chain import SSORagChain
from langchain_core.documents import Document


class FakeRetriever:
    def __init__(self, docs):
        self.docs = docs
        self.question = None

    def get_retriever(self, question, **_kwargs):
        self.question = question
        return self

    def invoke(self, question):
        self.question = question
        return self.docs


class FakePrompt:
    def __init__(self):
        self.context = None
        self.question = None

    def format_messages(self, *, context, question):
        self.context = context
        self.question = question
        return ["prompt"]


class FakeLLM:
    def __init__(self):
        self.messages = None

    def invoke(self, messages):
        self.messages = messages
        return type("Response", (), {"content": "Generated answer"})()


class RAGChainTests(unittest.TestCase):
    def test_every_query_sends_all_retrieved_top_chunks_to_prompt(self):
        top_chunks = [
            Document(page_content="Top chunk one"),
            Document(page_content="Top chunk two"),
            Document(page_content="Top chunk three"),
        ]
        retriever = FakeRetriever(top_chunks)
        prompt = FakePrompt()
        llm = FakeLLM()
        chain = SSORagChain(retriever=retriever, llm=llm, prompt=prompt)

        answer = chain.invoke("What documents are required?")

        self.assertEqual(answer, "Generated answer")
        self.assertEqual(retriever.question, "What documents are required?")
        self.assertEqual(prompt.question, "What documents are required?")
        self.assertEqual(
            prompt.context,
            "Top chunk one\n\nTop chunk two\n\nTop chunk three",
        )
        self.assertEqual(llm.messages, ["prompt"])


if __name__ == "__main__":
    unittest.main()
