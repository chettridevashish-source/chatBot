from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    question: str = Field(
        ..., 
        description="The user's question for the SSO bot.", 
        example="How do I apply for an employment card?"
    )

class ChatResponse(BaseModel):
    answer: str = Field(
        ..., 
        description="The AI-generated response based on official SSO documents."
    )