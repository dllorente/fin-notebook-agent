from langgraph.prebuilt import create_react_agent
from app.core.config import get_llm
from app.engine.tools import search_documents, summarize_documents, generate_briefing
from langchain_community.tools import DuckDuckGoSearchRun


def build_react_agent():
    llm = get_llm()
    # Tools propias
    own_tools = [search_documents, summarize_documents, generate_briefing]
    # Tools de comunidad
    web_search = DuckDuckGoSearchRun()
    tools = own_tools + [web_search]
    agent = create_react_agent(llm, tools)
    return agent
