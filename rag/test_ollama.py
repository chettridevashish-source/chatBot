from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen3:8b")

print("Invoking model...")

response = llm.invoke("Hello")

print(response.content)