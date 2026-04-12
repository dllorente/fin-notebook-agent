from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.routes import router

# carga .env en variables de sistema → activa LangSmith
load_dotenv()

# crea la app
app = FastAPI(
    title="FinNotebook Agent",
    description="Agentic RAG assistant for banking documentation",
    version="0.1.0",
)
# registra los endpoints
app.include_router(router)
