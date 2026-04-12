# Es la puerta de entrada de tu aplicación. 
# Es lo primero que recibe la petición del usuario y lo último que le devuelve la respuesta.

from app.models.schemas import AskRequest, AskResponse
from app.engine.graph.graph import build_graph    
from fastapi import APIRouter
from langsmith import traceable

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/ask", response_model=AskResponse)
@traceable(name="ask_endpoint", metadata={"version": "0.5.0"})
def ask(request: AskRequest):
    graph = build_graph()
    result = graph.invoke({
            "question": request.question,
            "session_id": request.session_id,
            "intent": "",
            "context": "",
            "answer": "",
            "messages": [] 
        })
    return AskResponse(
        answer=result["answer"],  
        session_id=request.session_id,
        intent=result["intent"]
)