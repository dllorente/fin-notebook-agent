from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
from app.core.config import get_llm
from app.engine.prompts import get_agent_system_prompt
from app.engine.tools import generate_briefing, search_documents, summarize_documents

web_search = DuckDuckGoSearchRun()
AGENT_TOOLS = [search_documents, summarize_documents, generate_briefing, web_search]


def build_dynamic_agent():
    """Agente único que elige tools dinámicamente según la consulta."""

    llm = get_llm()
    prompt = get_agent_system_prompt()
    agent = create_react_agent(model=llm, tools=AGENT_TOOLS, prompt=prompt)
    return agent
