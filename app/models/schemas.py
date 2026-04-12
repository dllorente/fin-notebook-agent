from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str
    session_id: str = "default"


class AskResponse(BaseModel):
    answer: str
    session_id: str
    intent: str = ""
