from pydantic import BaseModel, Field


class ChatDto(BaseModel):
    session_id: str = Field(default="test")
    person_id: str = Field(default="test")
    user_input: str
