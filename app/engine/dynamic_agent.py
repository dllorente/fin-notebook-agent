from langchain_core.messages import HumanMessage, ToolMessage

from app.engine.agent_factory import build_dynamic_agent


def run_dynamic_agent(question: str, chat_history=None) -> dict:
    agent = build_dynamic_agent()

    messages = list(chat_history) if chat_history else []
    messages.append(HumanMessage(content=question))

    result = agent.invoke({"messages": messages})
    result_messages = result.get("messages", [])

    tools_used = []
    for msg in result_messages:
        if isinstance(msg, ToolMessage):
            if getattr(msg, "name", None):
                tools_used.append(msg.name)

    tools_used = list(dict.fromkeys(tools_used))

    final_answer = ""
    if result_messages:
        last_message = result_messages[-1]
        final_answer = getattr(last_message, "content", "")

    return {
        "answer": final_answer,
        "tools_used": tools_used,
    }