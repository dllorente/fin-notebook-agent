# Objetivo: detectar la intención del usuario y devolver una cadena que indique qué nodo ejecutar.
from app.engine.graph.state import AgentState


def detect_intent(state: AgentState) -> AgentState:
    question = state["question"].lower()
    if any(
        word in question for word in ["resume", "resumen", "sintetiza"]
    ):  # palabras de resumen
        intent = "summarize"
    elif any(
        word in question
        for word in ["briefing", "ejecutivo", "puntos clave", "riesgos"]
    ):  # palabras de briefing
        intent = "briefing"
    else:
        intent = "qa"

    return {**state, "intent": intent}
