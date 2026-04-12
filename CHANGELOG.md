# Changelog - Fin-Notebook-Agent

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-04-12
### Fixed
- `package-mode = false` removed from pyproject.toml

## [0.9.0] - 2026-04-12
### Added
- add professional README with CI badge, stack, architecture, usage and project structure

- `package-mode = false` removed from pyproject.toml
## [0.8.0] - 2026-04-12
### Added
- add `Dockerfile` `.dockerignore` Docker support for app containerization
- add `.github/workflows/ci.yml`
- add GitHub Actions CI pipeline
- set line-length to 120 in ruff and black config
- add initial smoke test
- chore: fix chromadb/protobuf/opentelemetry dependency conflicts
- remove models/ from .gitignore and track app/models

## [0.7.0] - 2026-04-12
### Added
- `app/engine/tools.py`: search_documents, summarize_documents, generate_briefing tools
- `app/engine/react_agent.py`: ReAct agent with create_react_agent and DuckDuckGo
- `app/api/routes.py`: new POST /agent/ask endpoint
- Streamlit mode selector: Grafo estático vs Agente ReAct
- Tools and intent history persisted in session_state
- Keyword scoring metric in evaluate.py
- Baseline evaluation score: 0.33

### Changed
- `scripts/ingest.py`: indexes all files in data/
- `scripts/evaluate.py`: added scoring metric

## [0.6.0] - 2026-04-12
### Added
- LangSmith `@traceable` decorator in Streamlit `invoke_graph` function
- `tests/eval_dataset.json`: 10 evaluation questions about professional profile
- `scripts/evaluate.py`: automated evaluation script
- `data/skills.txt`: skills knowledge base for better retrieval
- Updated `scripts/ingest.py` to index all files in data/

## [0.5.0] - 2026-04-12
### Added
- Conversational memory with `add_messages` in `AgentState`
- `MessagesPlaceholder` in RAG prompt for chat history
- `RunnableLambda` in agent to extract question from dict
- Current date injected in system prompt
- Streamlit UI with chat interface, history and intent badge

### Fixed
- Fixed dict/string type error in RAG chain invocation
- Fixed module name conflict in Streamlit app

## [0.4.0] - 2026-04-12
### Added
- LangSmith tracing via `load_dotenv()` in `main.py`
- `streamlit_app/main.py`: Streamlit chat UI with history and intent badge
- `scripts/ingest.py`: local ingestion script

### Fixed
- Fixed chain invocation in nodes
- Fixed missing imports in `agent.py`
- Renamed Streamlit app to avoid module conflict

## [0.3.0] - 2026-04-10
### Added
- LangSmith tracing activated via `load_dotenv()` in `main.py`
- Added LangSmith variables to `.env.example`

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
- `app/engine/graph/graph.py`: LangGraph with intent routing to qa, summarize and briefing nodes
- `streamlit_app/`: Streamlit UI module scaffolding
### Changed 
- `app/api/routes.py`: renamed chain to graph, API now uses LangGraph
### Fixed
- Fixed `RunnablePassthrough` invocation in nodes: pass string directly instead of dict
- Added missing `RunnablePassthrough` and `StrOutputParser` imports in `agent.py`
- Added `format_docs` helper to convert retrieved documents to plain text
- Removed `intent` field from `AskRequest` schema

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
