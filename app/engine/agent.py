from app.core.config import get_llm
from app.engine.prompts import get_rag_prompt
from app.index.vector_store import load_vectorstore
from langchain_core.runnables import Runnable




def build_rag_chain() -> Runnable:

    retriever = load_vectorstore()
    llm = get_llm()
    prompt= get_rag_prompt()

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain
