from fastapi import FastAPI

app = FastAPI(
    title="SSO AI Assistant",
    version="2.0.0"
)

@app.get("/")
def root():
    return {
        "message": "SSO AI Assistant API Running"
    }