from app.engine.graph.state import AgentState
from app.engine.runner import run_engine


def qa_node(state: AgentState) -> AgentState:
    engine_mode = state.get("engine_mode", "rag")
    result = run_engine(
        question=state["question"],
        chat_history=state.get("messages", []),
        mode=engine_mode,
    )
    return {
        **state,
        "answer": result["answer"],
        "intent": result.get("intent", engine_mode),
        "tools_used": result.get("tools_used", []),
    }


def summarize_node(state: AgentState) -> AgentState:
    engine_mode = state.get("engine_mode", "rag")
    result = run_engine(
        question=f"Por favor, genera un resumen estructurado del siguiente contenido: {state['question']}",
        chat_history=state.get("messages", []),
        mode=engine_mode,
    )
    return {
        **state,
        "answer": result["answer"],
        "intent": result.get("intent", engine_mode),
        "tools_used": result.get("tools_used", []),
    }


def briefing_node(state: AgentState) -> AgentState:
    engine_mode = state.get("engine_mode", "rag")
    result = run_engine(
        question=f"Genera un briefing ejecutivo con puntos clave, riesgos y acciones sobre: {state['question']}",
        chat_history=state.get("messages", []),
        mode=engine_mode,
    )
    return {
        **state,
        "answer": result["answer"],
        "intent": result.get("intent", engine_mode),
        "tools_used": result.get("tools_used", []),
    }