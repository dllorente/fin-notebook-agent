from typing import TypedDict,Annotated     
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    question: str
    intent: str
    context: str
    answer: str
    session_id: str
    messages: Annotated[list[BaseMessage], add_messages]  