import sys
from pathlib import Path

# Add the root 'rag' directory to Python's system path to fix ImportErrors
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

from chains.rag_chain import SSORagChain

def main():
    print("Initializing Sikkim SSO RAG Pipeline...")
    try:
        rag_chain = SSORagChain()
        print("Pipeline initialized successfully. Using MMR retrieval.")
    except Exception as e:
        print(f"Failed to initialize pipeline: {e}")
        return

    print("\n" + "="*50)
    print("Sikkim SSO Bot Test Terminal")
    print("Type 'exit' or 'quit' to close.")
    print("="*50 + "\n")

    while True:
        try:
            question = input("User Question: ")
            if question.lower() in ['exit', 'quit']:
                print("Shutting down...")
                break

            if not question.strip():
                continue

            print("\nThinking...")
            # debug=True ensures we see if documents are actually being pulled
            answer = rag_chain.invoke(question, debug=True)
            
            print(f"\nBot Answer:\n{answer}\n")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nShutting down...")
            break
        except Exception as e:
            print(f"\n[ERROR] An error occurred: {e}\n")

if __name__ == "__main__":
    main()