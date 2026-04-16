from pydantic import BaseModel
from typing import Optional
from sqlmodel import SQLModel
from datetime import datetime


class AskRequest(SQLModel):
    question: str
    session_id: str = "default"
    

class AskResponse(BaseModel):
    answer: str
    session_id: str
    intent: str = ""
    
class ChatAskRequest(SQLModel):
    session_id: str
    message: str
    user_id: Optional[str] = None
    model_config = {
        "json_schema_extra": {
            "example": {
                "session_id": "demo-session-2",
                "user_id": "david1",
                "message": "¿Qué es una hipoteca variable?"
            }
        }
    }
class ChatAskResponse(SQLModel):
    ok: bool
    session_id: str
    answer: str
    user_message_id: int
    assistant_message_id: int

class ChatSessionRead(SQLModel):
    id: int
    session_id: str
    user_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class ChatMessageRead(SQLModel):
    id: int
    session_id: str
    role: str
    content: str
    created_at: datetime
