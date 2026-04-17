from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from sqlmodel import SQLModel

from app.api.routes import router
from app.api.v1.chat import router as chat_v1_router
from app.db.database import engine  # ← IMPORTA engine
from app.engine.graph.graph import build_graph

# carga .env
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: crea tablas al arrancar
    print("🔥 LIFESPAN START")
    print("DATABASE_URL =", engine.url)
    SQLModel.metadata.create_all(engine)
    print("✅ Base de datos creada: chat_sessions.db")
    yield
    # Shutdown: limpia si hace falta (opcional)
    print("🛑 App shutdown")


# crea la app CON lifespan
app = FastAPI(
    title="FinNotebook Agent",
    description="Agentic RAG assistant for banking documentation",
    version="0.1.0",
    lifespan=lifespan,  # ← AQUÍ va el lifespan
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # prod: ["https://tu-dominio.com"]
    allow_methods=["*"],
    allow_headers=["*"],
)


# registra routers
app.include_router(router)
app.include_router(chat_v1_router, prefix="/api")


# LangServe
add_routes(app, build_graph(), path="/agent")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)