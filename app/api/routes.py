from fastapi import APIRouter
from app.models.schemas import AskRequest, AskResponse
from app.engine.agent import build_rag_chain


router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    chain = build_rag_chain()
    return AskResponse(
        answer = chain.invoke({"question": request.question}) ,  
        session_id=request.session_id
)