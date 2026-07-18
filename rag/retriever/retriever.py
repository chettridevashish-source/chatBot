import os
from pathlib import Path
from vectorstore.vectorstore import get_vectorstore
from config import RETRIEVER_K

class SSORetriever:
    def __init__(self):
        self.vectorstore = get_vectorstore()
        
        # Safely resolve the path to your downloads folder
        current_script_dir = Path(__file__).resolve().parent
        # Adjust the parent traversal depending on where retriever.py is located
        # Assuming it is in rag/retriever/retriever.py
        self.downloads_dir = current_script_dir.parent / "data" / "downloads"
        
        self._cached_pdfs = []
        if self.downloads_dir.exists():
            self._cached_pdfs = [f for f in os.listdir(self.downloads_dir) if f.endswith(".pdf")]

    def _get_all_downloaded_filenames(self) -> list[str]:
        """Returns the cached list of PDF filenames."""
        return self._cached_pdfs

    def get_retriever(self, query_text: str, **kwargs):
        if 'search_type' not in kwargs:
            kwargs['search_type'] = "similarity"

        search_kwargs = kwargs.get('search_kwargs', {})
        
        # ─── THE SMART DYNAMIC ROUTER ───
        clean_query = query_text.lower()
        available_pdfs = self._get_all_downloaded_filenames()
        
        # Ignore these generic words so they don't cause accidental cross-matches
        IGNORE_WORDS = {"user", "manual", "for", "certificate", "to", "acquire", "issue", "of", "other", "classes"}
        
        for pdf_name in available_pdfs:
            # Clean the filename into tokens (words)
            name_content = pdf_name.lower().replace(".pdf", "").replace("-", " ").replace("_", " ")
            name_tokens = set(name_content.split())
            
            # Remove the generic words to leave ONLY the unique identifiers (e.g., 'st', 'obc', 'primitive')
            unique_identifiers = name_tokens - IGNORE_WORDS
            
            # 1. Check if a standard unique word (like 'obc') is in the user's query
            has_unique_match = any(word in clean_query for word in unique_identifiers if len(word) > 2)
            
            # 2. Safely check for the 'st' abbreviation without accidentally matching words like 'test'
            has_st_match = "st" in unique_identifiers and ("st " in clean_query or "st certificate" in clean_query or "scheduled tribe" in clean_query)
            
            if has_unique_match or has_st_match:
                # Lock the vector search to ONLY this specific PDF
                search_kwargs['filter'] = {"file_name": pdf_name}
                break 

        # Configuration baseline
        if 'k' not in search_kwargs:
            search_kwargs['k'] = RETRIEVER_K
        if kwargs['search_type'] == "mmr" and 'fetch_k' not in search_kwargs:
            search_kwargs['fetch_k'] = 15
            
        kwargs['search_kwargs'] = search_kwargs
        
        return self.vectorstore.as_retriever(**kwargs)
