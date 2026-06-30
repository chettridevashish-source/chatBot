from vectorstore.vectorstore import get_vectorstore

class SSORetriever:
    def __init__(self):
        # Initialize your database connection
        self.vectorstore = get_vectorstore()

    def get_retriever(self, **kwargs):
        # Set a default to grab the top 4 chunks if no other kwargs are provided
        if 'search_kwargs' not in kwargs:
            kwargs['search_kwargs'] = {"k": 4}
            
        # Pass any arguments (like search_type="mmr") directly to LangChain
        return self.vectorstore.as_retriever(**kwargs)