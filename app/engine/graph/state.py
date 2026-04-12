from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    question: str
    intent: str
    context: str
    answer: str
    session_id: str
    messages: Annotated[list[BaseMessage], add_messages]
