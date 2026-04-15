# Aquí defines los skills del agente. Cada nodo recibe el estado,
# hace su trabajo y devuelve el estado actualizado con answer relleno.
from app.engine.agent import build_rag_chain
from app.engine.graph.state import AgentState


def qa_node(state: AgentState) -> AgentState:
    chain = build_rag_chain()
    answer = chain.invoke({"question": state["question"], "chat_history": state.get("messages", [])})
    return {**state, "answer": answer}



def summarize_node(state: AgentState) -> AgentState:
    chain = build_rag_chain()
    answer = chain.invoke(
        {
            "question": f"Por favor, genera un resumen estructurado del siguiente contenido: {state['question']}",
            "chat_history": state.get("messages", []),
        }
    )
    return {**state, "answer": answer}


def briefing_node(state: AgentState) -> AgentState:
    chain = build_rag_chain()
    answer = chain.invoke(
        {
            "question": f"Genera un briefing ejecutivo con puntos clave, riesgos y acciones sobre: {state['question']}",
            "chat_history": state.get("messages", []),
        }
    )
    return {**state, "answer": answer}
