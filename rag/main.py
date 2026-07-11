import sys
import uvicorn
from pathlib import Path

# 1. Safely resolve the root 'rag' directory
root_dir = Path(__file__).resolve().parent

# 2. INSERT at index 0 to guarantee Python prioritizes your local folders
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

if __name__ == "__main__":
    print("🚀 Starting Uvicorn Server for Sikkim SSO API...")
    
    # 3. Target "main:app" because the app instance is in this exact file
    # (Assuming this file is named main.py and sits in the root rag/ folder)
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)