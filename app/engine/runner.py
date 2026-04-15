
from app.engine.agent import build_rag_chain
from app.engine.dynamic_agent import run_dynamic_agent
from app.engine.react_agent import run_react_agent


def run_engine(question: str, chat_history=None, mode: str= "rag") -> str:
    if mode == "rag" :
        chain = build_rag_chain()
        return chain.invoke({
            "question": question,
            "chat_history": chat_history or []
        })
    elif mode == "react" :
        return run_react_agent(
            question=question, 
            chat_history=chat_history)
    elif mode == "dynamic" :  
        return run_dynamic_agent(
            question=question,
            chat_history=chat_history or [],
        )
    else: 
        raise ValueError(f"Unsupported engine mode: {mode}")
