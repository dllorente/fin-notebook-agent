from langchain_core.messages import HumanMessage

from app.engine.agent_factory import build_dynamic_agent


def run_dynamic_agent(question: str, chat_history=None) -> str:
    agent = build_dynamic_agent()
    messages = list(chat_history) if chat_history else []
    messages.append(HumanMessage(content=question))
    result = agent.invoke({"messages": messages})
    return result["messages"][-1].content

