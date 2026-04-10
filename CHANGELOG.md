# Changelog - Fin-Notebook-Agent

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-04-09
### Added
- `app/models/schemas.py`: Pydantic request/response schemas (AskRequest, AskResponse)
- `app/api/routes.py`: FastAPI endpoints GET /health and POST /ask
- `main.py`: FastAPI app entrypoint with router
- `app/engine/graph/`: LangGraph module scaffolding (state, nodes, router, graph)
- `app/engine/graph/state.py`: AgentState TypedDict with question, intent, context, answer and session_id
- `app/engine/graph/router.py`: keyword-based intent detection router
- `app/engine/graph/state.py`: AgentState TypedDict
- `app/engine/graph/router.py`: keyword-based intent detection
- `app/engine/graph/nodes.py`: qa, summarize and briefing nodes

## [0.2.0] - 2026-04-09
### Added
- `app/index/vector_store.py`: Chroma vector store creation and retriever loading
- `app/engine/prompts.py`: RAG prompt template for banking documentation
- `app/engine/agent.py`: RAG chain built with LCEL

### Fixed
- Removed unused `webbrowser` import in `vector_store.py`
- Added missing type hint imports in `vector_store.py`

## [0.1.0] - 2026-04-09
### Added
- Project structure with Poetry and modular architecture (api, core, engine, index, models)
- `app/core/config.py`: provider-agnostic settings with `get_settings()`, `get_llm()` and `get_embeddings()`
- `app/index/document_loader.py`: document ingestion for PDF and TXT with metadata and chunking
- `.env.example` with all required environment variables
- `.gitignore` for Python, Poetry, and project-specific files


## [0.1.1] - 2026-04-09
### Fixed
- Removed circular import `document_loader → config` in `app/core/config.py`
- Removed duplicate `Field` import in `app/core/config.py`
- Added missing type hint imports `BaseChatModel` and `Embeddings` in `app/core/config.py`
- Removed incorrect `List` import from `ast` in `app/index/document_loader.py`
- Fixed import path `core.config` → `app.core.config` in `app/index/document_loader.py`
