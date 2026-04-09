# Importamos las librerías necesarias
from app.core.config import get_settings
from pathlib import Path
from datetime import datetime
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

 
# Obtenemos las configuraciones
settings = get_settings()


# Definimos la función para cargar los documentos
def load_documents(file_path: str) -> list[Document]:
    # Cargamos los documentos
    ext= Path(file_path).suffix.lower()  # devuelve ".pdf" o ".txt"
    if ext ==".pdf":
        loader= PyPDFLoader(file_path)
        docs = loader.load()
    elif ext ==".txt":
        loader= TextLoader(file_path)
        docs = loader.load()
    else: 
        raise ValueError(
            f"Tipo de documento aún no soportado: '{ext}'. "
            f"Extensiones válidas: '.pdf', '.txt'"
        )
    
    for doc in docs:
        doc.metadata["source"] = Path(file_path).name
        doc.metadata["file_type"] = ext.lstrip(".")
        doc.metadata["loaded_at"] = datetime.now().isoformat()
    # Retornamos los documentos cargados
    return docs
    

def split_documents(docs: list[Document]) -> list[Document]:
    settings = get_settings()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,     
        chunk_overlap=settings.chunk_overlap    
    )
    return splitter.split_documents(docs)  


