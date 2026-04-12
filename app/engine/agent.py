from app.core.config import get_llm
from app.engine.prompts import get_rag_prompt
from app.index.vector_store import load_vectorstore
from langchain_core.runnables import Runnable,RunnablePassthrough,RunnableLambda
from langchain_core.output_parsers import StrOutputParser

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def build_rag_chain() -> Runnable:

    retriever = load_vectorstore()
    llm = get_llm()
    prompt= get_rag_prompt()

    chain = (
        {
            "context": RunnableLambda(lambda x: x["question"]) |retriever | format_docs, 
            "question": lambda x: x["question"],
            "chat_history": lambda x: x.get("chat_history", []) 
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain
