from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="FinNotebook Agent",
    description="Agentic RAG assistant for banking documentation",
    version="0.1.0"
)

app.include_router(router)