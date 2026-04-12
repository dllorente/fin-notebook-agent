# Objetivo: armar el grafo completo conectando router y nodos.

from langgraph.graph import END, StateGraph

from app.engine.graph.nodes import briefing_node, qa_node, summarize_node
from app.engine.graph.router import detect_intent
from app.engine.graph.state import AgentState


def build_graph():
    graph = StateGraph(AgentState)

    # Añadir nodos
    graph.add_node("detect_intent", detect_intent)
    graph.add_node("qa", qa_node)
    graph.add_node("summarize", summarize_node)
    graph.add_node("briefing", briefing_node)

    # Punto de entrada
    graph.set_entry_point("detect_intent")

    # Edge condicional
    graph.add_conditional_edges(
        "detect_intent",
        lambda state: state["intent"],  # lee la intención del estado
        {"qa": "qa", "summarize": "summarize", "briefing": "briefing"},
    )

    # Conectar nodos finales a END
    graph.add_edge("qa", END)
    graph.add_edge("summarize", END)
    graph.add_edge("briefing", END)
    return graph.compile()
