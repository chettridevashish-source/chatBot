import sys
from pathlib import Path

# 1. Force Python to recognize the root 'rag' directory FIRST
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Import your smart retriever to see the dynamic filtering in action
from retriever.retriever import SSORetriever

def test_my_search(query_text: str):
    print(f"\n🔍 Testing Search for: '{query_text}'")
    print("=" * 80)
    
    # 2. Initialize the retriever and pass the query to trigger the router
    retriever_manager = SSORetriever()
    retriever = retriever_manager.get_retriever(query_text=query_text, search_type="mmr")
    
    # 3. Fetch the documents using invoke()
    matched_docs = retriever.invoke(query_text)
    
    if not matched_docs:
        print("⚠️ No results found.")
        return

    print(f"✅ Successfully retrieved {len(matched_docs)} relevant chunks!\n")

    # 4. Display the results cleanly
    for i, doc in enumerate(matched_docs):
        metadata = doc.metadata
        file_name = metadata.get('file_name', 'Unknown')
        page_num = metadata.get('page_label', 'N/A')
        
        print(f"🏆 MATCH #{i + 1}")
        print(f"📄 Source File : {file_name}")
        print(f"📑 Page Number : {page_num}")
        print("-" * 80)
        # Show a 500-character preview of the matched chunk
        print(f"📝 Text Preview:\n{doc.page_content[:500].strip()}...\n")
        print("=" * 80 + "\n")

if __name__ == "__main__":
    # Your specific test query
    test_query = "how to apply for st certificate"
    
    test_my_search(test_query)