from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from langserve import add_routes
from app.engine.graph.graph import build_graph

# carga .env en variables de sistema → activa LangSmith
load_dotenv()


# crea la app
app = FastAPI(
    title="FinNotebook Agent",
    description="Agentic RAG assistant for banking documentation",
    version="0.1.0",
)

# CORS — necesario si Streamlit y FastAPI corren en puertos distintos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en prod: ["https://tu-dominio.com"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# registra los endpoints
app.include_router(router)

# LangServe playground
add_routes(app, build_graph(), path="/agent")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)