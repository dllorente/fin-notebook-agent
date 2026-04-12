from langchain_chroma import Chroma
from app.core.config import get_settings, get_embeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever

def create_vectorstore(docs: list[Document]) -> Chroma:
    
    settings = get_settings()

    return Chroma.from_documents(
        documents=docs,        # lista de chunks
        embedding=get_embeddings(),   # función de embeddings
        persist_directory=settings.vectorstore_dir # ruta donde guardar en disco
    )

def load_vectorstore() -> VectorStoreRetriever:
    settings = get_settings()
    vectorstore = Chroma(
        persist_directory=settings.vectorstore_dir,   
        embedding_function=get_embeddings()   
    )
    
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k":6}
    )