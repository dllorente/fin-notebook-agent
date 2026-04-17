from app.engine.dynamic_agent import run_dynamic_agent
from app.engine.graph.state import AgentState
from app.engine.runner import run_engine


def _run_by_mode(question: str, state: AgentState) -> dict:
    engine_mode = state.get("engine_mode", "rag")

    if engine_mode == "dynamic":
        return run_dynamic_agent(
            question=question,
            chat_history=state.get("messages", []),
        )

    return run_engine(
        question=question,
        chat_history=state.get("messages", []),
        mode=engine_mode,
    )


def qa_node(state: AgentState) -> AgentState:
    result = _run_by_mode(
        question=state["question"],
        state=state,
    )
    return {
        **state,
        "answer": result["answer"],
        "intent": result.get("intent", state.get("intent", "qa")),
        "tools_used": result.get("tools_used", []),
    }


def summarize_node(state: AgentState) -> AgentState:
    result = _run_by_mode(
        question=f"Por favor, genera un resumen estructurado del siguiente contenido: {state['question']}",
        state=state,
    )
    return {
        **state,
        "answer": result["answer"],
        "intent": result.get("intent", state.get("intent", "summarize")),
        "tools_used": result.get("tools_used", []),
    }


def briefing_node(state: AgentState) -> AgentState:
    result = _run_by_mode(
        question=f"Genera un briefing ejecutivo con puntos clave, riesgos y acciones sobre: {state['question']}",
        state=state,
    )
    return {
        **state,
        "answer": result["answer"],
        "intent": result.get("intent", state.get("intent", "briefing")),
        "tools_used": result.get("tools_used", []),
    }