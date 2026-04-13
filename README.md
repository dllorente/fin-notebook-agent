# 🏦 Fin-Notebook-Agent

> Agentic RAG assistant for banking documentation, inspired by NotebookLM

![CI](https://github.com/dllorente/fin-notebook-agent/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![LangChain](https://img.shields.io/badge/LangChain-0.3-green)
![LangGraph](https://img.shields.io/badge/LangGraph-agentic-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## ¿Qué es esto?

Asistente conversacional agnostico especializado en documentación bancaria.
Permite consultar, resumir y analizar documentos financieros mediante un
agente ReAct con herramientas especializadas y un grafo de intención con LangGraph.

Inspirado en NotebookLM pero orientado al sector financiero y construido
con un stack de producción: FastAPI + LangGraph + Chroma + Streamlit.

## 🛠️ Stack

| Capa | Tecnología |
|------|-----------|
| LLM | OpenAI GPT-4o / Anthropic Claude |
| Orquestación | LangGraph + ReAct Agent |
| RAG | LangChain + Chroma |
| API | FastAPI |
| Frontend | Streamlit |
| Observabilidad | LangSmith |
| CI/CD | GitHub Actions |
| Contenedor | Docker |

## 🏗️ Arquitectura
Usuario
│
▼
Streamlit UI / FastAPI
│
▼
ReAct Agent (LangGraph)
├── search_documents → Chroma Vector Store
├── summarize_documents
├── generate_briefing
└── DuckDuckGo Search → Internet
│
▼
LLM (OpenAI / Anthropic)
│
▼
Respuesta con fuente citada

## 🚀 Instalación

```bash
git clone https://github.com/dllorente/fin-notebook-agent.git
cd fin-notebook-agent
poetry install
cp .env.example .env  # añade tus API keys
```

## ▶️ Uso

**Indexar documentos:**
```bash
poetry run python scripts/ingest.py
```

**Arrancar API:**
```bash
poetry run uvicorn main:app --reload
```

**Arrancar Streamlit:**
```bash
poetry run streamlit run streamlit_app/main.py
```

**Ejecutar evaluación:**
```bash
poetry run python scripts/evaluate.py
```


## 📁 Estructura

```bash
fin-notebook-agent/
├── app/
│   ├── api/              # FastAPI routes
│   ├── core/             # Config, LLM, embeddings
│   ├── engine/           # RAG chain, prompts, tools, ReAct agent
│   │   └── graph/        # LangGraph state, router, nodes, graph
│   ├── index/            # Vector store, document loader
│   └── models/           # Pydantic schemas
├── streamlit_app/        # Streamlit UI
├── scripts/              # ingest.py, evaluate.py
├── tests/                # Pytest tests
├── data/                 # Documentos bancarios indexados
├── Dockerfile
└── .github/
    └── workflows/
        └── ci.yml
```

## 🔑 Variables de entorno

Copia `.env.example` a `.env` y rellena:

```env
LLM_PROVIDER=openai          # openai | anthropic
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
LANGCHAIN_API_KEY=...        # LangSmith tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=fin-notebook-agent
```

## VectorStore

Borra el vectorstore
```bash
rm -rf .vectorstore
```
Reindexado de documentos
```bash
poetry run python scripts/ingest.py
```

## 🧪 Tests

```bash
poetry run pytest
```

## 🔍 Linting & Formatting

```bash
poetry run ruff check --fix
poetry run black --check .
```

## 📄 Licencia

MIT — David Llorente Raposo