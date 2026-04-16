from datetime import UTC, datetime
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db.database import get_session
from app.db.models import ChatSession, ChatMessage
from app.engine.graph.graph import build_graph
from app.models.schemas import ChatAskRequest
from langchain_core.messages import HumanMessage, AIMessage
from app.models.schemas import ChatAskRequest, ChatAskResponse, ChatMessageRead, ChatSessionRead
from typing import Annotated
from fastapi import Body

router = APIRouter(prefix="/v1/chat", tags=["chat"])

graph = build_graph()

@router.get("/sessions", response_model=list[ChatSessionRead])
def list_sessions(session: Session = Depends(get_session)):
    statement = select(ChatSession).order_by(ChatSession.updated_at.desc())
    sessions = session.exec(statement).all()
    return sessions

@router.get("/sessions/{session_id}/messages",response_model=list[ChatMessageRead])
def get_messages(session_id: str, session: Session = Depends(get_session)):
    chat_session = session.exec(
        select(ChatSession).where(ChatSession.session_id == session_id)
    ).first()

    if not chat_session:
        raise HTTPException(status_code=404, detail="Session not found")

    statement = (
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
    )
    messages = session.exec(statement).all()
    return messages

@router.post("/ask", response_model=ChatAskResponse)
def chat_ask(payload: ChatAskRequest, session: Session = Depends(get_session)):
    chat_session = session.exec(
        select(ChatSession).where(ChatSession.session_id == payload.session_id)
    ).first()

    if not chat_session:
        chat_session = ChatSession(
            session_id=payload.session_id,
            user_id=payload.user_id,
        )
        session.add(chat_session)
        session.commit()
        session.refresh(chat_session)

    user_message = ChatMessage(
        session_id=payload.session_id,
        role="user",
        content=payload.message,
    )
    session.add(user_message)
    session.commit()
    session.refresh(user_message)

    history_stmt = (
        select(ChatMessage)
        .where(ChatMessage.session_id == payload.session_id)
        .order_by(ChatMessage.created_at.asc())
    )
    history = session.exec(history_stmt).all()
    conversation_messages = []

    for msg in history:
        if msg.role == "user":
            conversation_messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            conversation_messages.append(AIMessage(content=msg.content))


    # Invoca tu grafo
    result: dict[str, Any] = graph.invoke({
        "question": payload.message,
        "session_id": payload.session_id,
        "messages": conversation_messages,
    })

    assistant_text = (
        result.get("answer")
        or result.get("response")
        or result.get("context")
        or "No se pudo generar respuesta"
    )

    assistant_message = ChatMessage(
        session_id=payload.session_id,
        role="assistant",
        content=assistant_text,
    )
    session.add(assistant_message)

    chat_session.updated_at = datetime.now(UTC)
    session.add(chat_session)

    session.commit()
    session.refresh(assistant_message)

    return {
        "ok": True,
        "session_id": payload.session_id,
        "answer": assistant_text,
        "user_message_id": user_message.id,
        "assistant_message_id": assistant_message.id,
    }