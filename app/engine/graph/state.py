from typing import TypedDict    


class AgentState(TypedDict):
    question: str
    intent: str
    context: str
    answer: str
    session_id: str