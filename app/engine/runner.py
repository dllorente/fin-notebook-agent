from app.engine.agent import build_rag_chain
from app.engine.dynamic_agent import run_dynamic_agent
from app.engine.react_agent import run_react_agent


def run_engine(question: str, chat_history=None, mode: str = "rag") -> dict:
    from app.engine.agent import build_rag_chain
from app.engine.react_agent import run_react_agent
from app.engine.dynamic_agent import run_dynamic_agent


def run_engine(
    question: str,
    chat_history=None,
    mode: str = "rag",
    intent: str | None = None,
):
    chat_history = chat_history or []
    resolved_intent = intent or "qa"

    if mode == "rag":
        chain = build_rag_chain()
        answer = chain.invoke(
            {
                "question": question,
                "chat_history": chat_history,
            }
        )
        return {
            "answer": answer,
            "intent": resolved_intent,
            "tools_used": ["search_documents", "generate_answer"],
        }

    elif mode == "react":
        result = run_react_agent(
            question=question,
            chat_history=chat_history,
        )

        if isinstance(result, dict):
            return {
                "answer": result.get("answer", ""),
                "intent": result.get("intent", resolved_intent),
                "tools_used": result.get("tools_used", []),
            }

        return {
            "answer": result,
            "intent": resolved_intent,
            "tools_used": [],
        }

    elif mode == "dynamic":
        result = run_dynamic_agent(
            question=question,
            chat_history=chat_history,
        )

        if isinstance(result, dict):
            return {
                "answer": result.get("answer", ""),
                "intent": result.get("intent", resolved_intent),
                "tools_used": result.get("tools_used", []),
            }

        return {
            "answer": result,
            "intent": resolved_intent,
            "tools_used": [],
        }

    else:
        raise ValueError(f"Unsupported engine mode: {mode}")
