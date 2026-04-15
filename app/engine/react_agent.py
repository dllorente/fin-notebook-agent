from concurrent.futures import ThreadPoolExecutor, TimeoutError

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from app.core.config import get_llm
from app.engine.tools import generate_briefing, search_documents, summarize_documents


def build_react_agent():
    llm = get_llm()
    own_tools = [search_documents, summarize_documents, generate_briefing]
    web_search = DuckDuckGoSearchRun()
    tools = own_tools + [web_search]
    agent = create_react_agent(llm, tools)
    return agent


def run_react_with_timeout(agent, messages, timeout_sec=30):
    def invoke_agent():
        return agent.invoke({"messages": messages})
    
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(invoke_agent)
        try:
            return future.result(timeout=timeout_sec)
        except TimeoutError:
            return None

def run_react_agent(question: str, chat_history=None, timeout_sec=30) -> dict:
    agent = build_react_agent()
    messages = list(chat_history) if chat_history else []
    messages.append(HumanMessage(content=question))
    
    result = run_react_with_timeout(agent, messages, timeout_sec)
    
    if result is None:
        return {
            "answer": "⏰ Agent ReAct timeout (loop detectado)",
            "tools_used": ["timeout"],
        }
    
    tools_used = []
    for msg in result["messages"]:
        if hasattr(msg, "name") and msg.name:
            tools_used.append(msg.name)
    tools_used = list(dict.fromkeys(tools_used))
    
    return {
        "answer": result["messages"][-1].content,
        "tools_used": tools_used,
    }