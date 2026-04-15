from app.engine.agent import build_rag_chain
from app.engine.dynamic_agent import run_dynamic_agent
from app.engine.react_agent import run_react_agent


def run_engine(question: str, chat_history=None, mode: str = "rag") -> dict:
    if mode == "rag":
        chain = build_rag_chain()
        answer = chain.invoke({
            "question": question,
            "chat_history": chat_history or []
        })
        return {
            "answer": answer,
            "intent": "rag",
            "tools_used": ["search_documents", "generate_answer"]
        }

    elif mode == "react":
        result = run_react_agent(
            question=question,
            chat_history=chat_history or []
        )
        return {
            "answer": result.get("answer", result) if isinstance(result, dict) else result,
            "intent": "react",
            "tools_used": result.get("tools_used", []) if isinstance(result, dict) else []
        }

    elif mode == "dynamic":
        result = run_dynamic_agent(
            question=question,
            chat_history=chat_history or [],
        )
        return {
            "answer": result["answer"],
            "intent": "dynamic",
            "tools_used": result.get("tools_used", []),
        }

    else:
        raise ValueError(f"Unsupported engine mode: {mode}")