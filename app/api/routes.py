# Es la puerta de entrada de tu aplicación.
# Es lo primero que recibe la petición del usuario
# y lo último que le devuelve la respuesta.

from fastapi import APIRouter
from langsmith import traceable

from app.engine.graph.graph import build_graph
from app.models.schemas import AskRequest, AskResponse

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/ragAsk", response_model=AskResponse)
@traceable(name="ask_endpoint", metadata={"version": "0.5.0"})
def ask(request: AskRequest):
    graph = build_graph()
    result = graph.invoke(
        {
            "question": request.question,
            "session_id": request.session_id,
            "intent": "",
            "context": "",
            "answer": "",
            "messages": [],
            "engine_mode": "rag",
        }
    )
    return AskResponse(answer=result["answer"], session_id=request.session_id, intent=result["intent"])


@router.post("/agent/reactAsk", response_model=AskResponse)
@traceable(name="react_agent_endpoint", metadata={"version": "0.6.0"})
def agent_react_ask(request: AskRequest):
    graph = build_graph()
    result = graph.invoke(
        {
            "question": request.question,
            "session_id": request.session_id,
            "intent": "",
            "context": "",
            "answer": "",
            "messages": [],
            "engine_mode": "react",
        }
    )
    return AskResponse(
        answer=result["answer"],
        session_id=request.session_id,
        intent=result["intent"],
    )


@router.post("/agent/dynamicAsk", response_model=AskResponse)
@traceable(name="dynamic_agent_endpoint", metadata={"version": "0.6.0"})
def agent_dynamic_ask(request: AskRequest):
    graph = build_graph()
    result = graph.invoke(
        {
            "question": request.question,
            "session_id": request.session_id,
            "intent": "",
            "context": "",
            "answer": "",
            "messages": [],
            "engine_mode": "dynamic",
        }
    )
    return AskResponse(
        answer=result["answer"],
        session_id=request.session_id,
        intent=result["intent"],
    )
