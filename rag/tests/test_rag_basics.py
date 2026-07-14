import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api.schemas import ChatRequest
from ingestion.splitter import DocumentSplitter
from langchain_core.documents import Document
import retriever.retriever as retriever_module


class FakeVectorStore:
    def __init__(self):
        self.kwargs = None

    def as_retriever(self, **kwargs):
        self.kwargs = kwargs
        return "fake-retriever"


class RAGBasicsTests(unittest.TestCase):
    def test_question_is_trimmed_and_blank_input_is_rejected(self):
        self.assertEqual(ChatRequest(question="  How do I apply?  ").question, "How do I apply?")
        with self.assertRaises(ValueError):
            ChatRequest(question="   ")

    def test_splitter_creates_bounded_chunks_with_metadata(self):
        splitter = DocumentSplitter(chunk_size=30, chunk_overlap=5)
        chunks = splitter.split_documents([
            Document(page_content="one two three four five six seven eight nine ten", metadata={"file_name": "guide.pdf"})
        ])
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(chunk.metadata["file_name"] == "guide.pdf" for chunk in chunks))
        self.assertEqual([chunk.metadata["chunk_index"] for chunk in chunks], list(range(len(chunks))))

    def test_retriever_filters_when_query_names_a_manual(self):
        fake_store = FakeVectorStore()
        original_factory = retriever_module.get_vectorstore
        retriever_module.get_vectorstore = lambda: fake_store
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                Path(temp_dir, "USER MANUAL FOR ST CERTIFICATE.pdf").touch()
                retriever = retriever_module.SSORetriever()
                retriever.downloads_dir = Path(temp_dir)
                result = retriever.get_retriever("How can I get an ST certificate?", search_type="mmr")
        finally:
            retriever_module.get_vectorstore = original_factory

        self.assertEqual(result, "fake-retriever")
        self.assertEqual(
            fake_store.kwargs["search_kwargs"]["filter"],
            {"file_name": "USER MANUAL FOR ST CERTIFICATE.pdf"},
        )


if __name__ == "__main__":
    unittest.main()
