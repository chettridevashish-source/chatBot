import sys
import uvicorn
from pathlib import Path

# Add the root 'rag' directory to Python's system path to fix ImportErrors globally
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

if __name__ == "__main__":
    print("Starting Uvicorn Server for Sikkim SSO API...")
    # 'api.main:app' points to the FastAPI instance we created above.
    # reload=True is great for development; set it to False in actual production.
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)