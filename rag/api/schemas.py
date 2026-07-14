from pydantic import BaseModel, Field, field_validator

class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="The user's question for the SSO bot.", 
        example="How do I apply for an employment card?"
    )

    @field_validator("question")
    @classmethod
    def question_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Question must not be blank")
        return value

class ChatResponse(BaseModel):
    answer: str = Field(
        ..., 
        description="The AI-generated response based on official SSO documents."
    )
