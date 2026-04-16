from typing import Literal

from fastapi import APIRouter, HTTPException
from langsmith import traceable

from app.engine.graph.graph import build_graph
from app.models.schemas import AskRequest, AskResponse

router = APIRouter()
graph = build_graph()

EngineMode = Literal["rag", "react", "dynamic"]


def _invoke_graph(question: str, session_id: str, engine_mode: EngineMode) -> dict:
    try:
        return graph.invoke(
            {
                "question": question,
                "session_id": session_id,
                "intent": "",
                "context": "",
                "answer": "",
                "messages": [],
                "engine_mode": engine_mode,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/ragAsk", response_model=AskResponse)
@traceable(name="ask_endpoint", metadata={"version": "0.5.0"})
def ask(request: AskRequest):
    result = _invoke_graph(request.question, request.session_id, "rag")
    return AskResponse(
        answer=result["answer"],
        session_id=request.session_id,
        intent=result["intent"],
    )


@router.post("/agent/reactAsk", response_model=AskResponse)
@traceable(name="react_agent_endpoint", metadata={"version": "0.6.0"})
def agent_react_ask(request: AskRequest):
    result = _invoke_graph(request.question, request.session_id, "react")
    return AskResponse(
        answer=result["answer"],
        session_id=request.session_id,
        intent=result["intent"],
    )


@router.post("/agent/dynamicAsk", response_model=AskResponse)
@traceable(name="dynamic_agent_endpoint", metadata={"version": "0.6.0"})
def agent_dynamic_ask(request: AskRequest):
    result = _invoke_graph(request.question, request.session_id, "dynamic")
    return AskResponse(
        answer=result["answer"],
        session_id=request.session_id,
        intent=result["intent"],
    )