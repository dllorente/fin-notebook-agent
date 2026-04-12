# Es la puerta de entrada de tu aplicación.
# Es lo primero que recibe la petición del usuario
# y lo último que le devuelve la respuesta.

from fastapi import APIRouter
from langchain_core.messages import HumanMessage
from langsmith import traceable

from app.engine.graph.graph import build_graph
from app.engine.react_agent import build_react_agent
from app.models.schemas import AskRequest, AskResponse

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/ask", response_model=AskResponse)
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
        }
    )
    return AskResponse(answer=result["answer"], session_id=request.session_id, intent=result["intent"])


@router.post("/agent/ask", response_model=AskResponse)
@traceable(name="react_agent_endpoint", metadata={"version": "0.6.0"})
def agent_ask(request: AskRequest):
    agent = build_react_agent()
    result = agent.invoke({"messages": [HumanMessage(content=request.question)]})
    answer = result["messages"][-1].content
    return AskResponse(answer=answer, session_id=request.session_id, intent="react")
