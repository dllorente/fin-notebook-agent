from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from app.core.config import get_llm
from app.engine.tools import generate_briefing, search_documents, summarize_documents


def build_react_agent():
    llm = get_llm()
    # Tools propias
    own_tools = [search_documents, summarize_documents, generate_briefing]
    # Tools de comunidad
    web_search = DuckDuckGoSearchRun()
    tools = own_tools + [web_search]
    agent = create_react_agent(llm, tools)
    return agent

def run_react_agent(question: str, chat_history=None) -> str:
    agent = build_react_agent()

    # Historial en formato lista
    messages = list(chat_history) if chat_history else []
    # Añadimos la nueva pregunta del usuario
    messages.append(HumanMessage(content=question))

    # Ejecutamos el agente ReAct
    result = agent.invoke({"messages": messages})

    # Devolvemos solo el texto del último mensaje del asistente
    return result["messages"][-1].content
