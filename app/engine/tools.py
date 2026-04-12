from langchain_core.tools import tool
from app.engine.agent import build_rag_chain


@tool
def search_documents(query: str) -> str:
    """Busca y responde preguntas sobre los documentos indexados.
    Usa esta herramienta para responder preguntas concretas sobre el contenido.
    Si no sabes la respuesta o no estas seguro que sea verídica no te inventes nada y pide ayuda.
    """
    chain = build_rag_chain()
    return chain.invoke({"question": query, "chat_history": []})


@tool
def summarize_documents(query: str) -> str:
    """Genera un resumen estructurado del contenido de los documentos.
    Usa esta herramienta cuando el usuario pida un resumen o síntesis.
    Puedes responder de un modo sencillo o técnico dependiendo del tono de la pregunta del usuario.
    """
    chain = build_rag_chain()
    question = f"Por favor, genera un resumen estructurado sobre: {query}"
    return chain.invoke({"question": question, "chat_history": []})


@tool
def generate_briefing(query: str) -> str:
    """Genera un briefing ejecutivo con puntos clave, riesgos y acciones.
    Usa esta herramienta cuando el usuario pida un briefing o análisis ejecutivo.
    Puedes responder de un modo sencillo o técnico dependiendo del tono de la pregunta del usuario.
    """
    chain = build_rag_chain()
    question = f"Genera un briefing ejecutivo con puntos clave, riesgos y acciones sobre: {query}"
    return chain.invoke({"question": question, "chat_history": []})
