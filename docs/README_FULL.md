# 🏦 Fin-Notebook-Agent

> Agentic RAG assistant for banking documentation, inspired by NotebookLM.

![CI](https://github.com/dllorente/fin-notebook-agent/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![LangChain](https://img.shields.io/badge/LangChain-0.3-green)
![LangGraph](https://img.shields.io/badge/LangGraph-agentic-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## Overview

Fin-Notebook-Agent is a portfolio project that explores how to build an **agentic RAG system for banking documentation** with a production-style Python stack.

The system combines:
- document ingestion and vector search,
- a LangGraph-based orchestration layer,
- specialized tools for answering, summarizing, and briefing,
- a FastAPI backend,
- and a Streamlit interface.

The goal is to simulate an internal knowledge assistant for financial documentation: a system that can answer questions, summarize content, generate structured briefings, and evolve toward multi-source knowledge workflows.

## Quick start

If you want to run the project quickly with local data:

```bash
git clone https://github.com/dllorente/fin-notebook-agent.git
cd fin-notebook-agent
poetry install && cp .env.example .env
poetry run python scripts/ingest.py
poetry run uvicorn main:app --reload
```

In another terminal:

```bash
poetry run streamlit run streamlit_app/main.py
```

## Why this project

This project was built to show practical skills in:
- AI Engineering,
- Agentic systems,
- LLMOps,
- RAG architecture,
- backend/API design,
- and production-oriented developer workflows.

It is inspired by NotebookLM, but focused on **banking and financial documentation**, where retrieval quality, traceability, and orchestration are more important than generic chat UX.

## Current capabilities

At its current stage, the project includes:

- Retrieval-Augmented Generation over indexed documents.
- Question answering over banking-oriented content.
- Specialized tools for:
  - document search,
  - summarization,
  - briefing generation,
  - and web fallback when needed.
- LangGraph orchestration for intent-driven flows.
- FastAPI API layer.
- Streamlit frontend for interactive use.
- Local document ingestion pipeline.
- Persistent chat session storage.
- CI checks for formatting and tests.
- Docker-based execution.

## Architecture

```text
User
│
├── Streamlit UI
│
└── FastAPI API
    │
    ▼
LangGraph Orchestration Layer
    │
    ├── search_documents
    │     └── Chroma Vector Store
    │
    ├── summarize_documents
    │
    ├── generate_briefing
    │
    └── web_search (fallback)
          └── Internet
    │
    ▼
LLM Provider
(OpenAI / Anthropic)
    │
    ▼
Grounded answer with retrieved context
```

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| LLM Providers | OpenAI / Anthropic |
| Orchestration | LangGraph |
| RAG Framework | LangChain |
| Vector Store | Chroma |
| API | FastAPI |
| Frontend | Streamlit |
| Observability | LangSmith |
| CI/CD | GitHub Actions |
| Containerization | Docker |
| Dependency management | Poetry |

## Repository structure

```bash
fin-notebook-agent/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   └── chat.py
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logging.py
│   ├── db/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── session.py
│   ├── engine/
│   │   ├── graph/
│   │   │   ├── __init__.py
│   │   │   ├── graph.py
│   │   │   ├── nodes.py
│   │   │   ├── router.py
│   │   │   └── state.py
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── agent_factory.py
│   │   ├── dynamic_agent.py
│   │   ├── prompts.py
│   │   ├── react_agent.py
│   │   ├── runner.py
│   │   └── tools.py
│   ├── index/
│   │   ├── __init__.py
│   │   ├── document_loader.py
│   │   └── vector_store.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── __init__.py
├── data/
│   ├── faq/
│   │   └── faqs.json
│   ├── CV_David_LLorente_Raposo_2026.pdf
│   └── skills.txt
├── icons/
│   └── finotebook_agent_icon_v2.svg
├── models/
│   └── vectorstores/
│       ├── 22c94222-d507-4b86-9ef6-e423d1e0375b/
│       │   ├── data_level0.bin
│       │   ├── header.bin
│       │   ├── length.bin
│       │   └── link_lists.bin
│       └── chroma.sqlite3
├── output/
├── scripts/
│   ├── evaluate.py
│   └── ingest.py
├── streamlit_app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── eval_dataset_grounded.json
│   └── test_main.py
├── .dockerignore
├── .env
├── .env.example
├── .gitignore
├── .python-version
├── CHANGELOG.md
├── Dockerfile
├── main.py
├── poetry.lock
├── pyproject.toml
└── README.md
```

Notes:
- `models/vectorstores/` is generated locally by ingestion and is not intended for version control.
- `chat_sessions.db` is local runtime state.

## Local setup

Clone the repository and install dependencies:

```bash
git clone https://github.com/dllorente/fin-notebook-agent.git
cd fin-notebook-agent
poetry install
cp .env.example .env
```

Then complete your environment variables in `.env`.

## Environment variables

Provider selection and required keys:

| `LLM_PROVIDER` | Required key |
|---|---|
| `openai` | `OPENAI_API_KEY` |
| `anthropic` | `ANTHROPIC_API_KEY` |

Optional observability:
- `LANGCHAIN_API_KEY`
- `LANGCHAIN_TRACING_V2=true`
- `LANGCHAIN_PROJECT=fin-notebook-agent`

Example:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
LANGCHAIN_API_KEY=...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=fin-notebook-agent
```

## Usage

### 1) Ingest documents

```bash
poetry run python scripts/ingest.py
```

### 2) Start the API

```bash
poetry run uvicorn main:app --reload
```

### 3) Start the Streamlit UI

```bash
poetry run streamlit run streamlit_app/main.py
```

### 4) Run tests

```bash
poetry run pytest
```

### 5) Run linting and formatting checks

```bash
poetry run ruff check .
poetry run black --check .
```

## Vector store reset

If you want to rebuild the vector database from scratch:

```bash
rm -rf models/vectorstores
poetry run python scripts/ingest.py
```

## Troubleshooting

- If retrieval returns weak results, run ingestion again with `poetry run python scripts/ingest.py`.
- If vector store files are stale or corrupted, remove `models/vectorstores/` and ingest again.
- If the API starts but the UI fails, verify the backend is running at the expected host/port.
- If provider calls fail, verify `LLM_PROVIDER` and the corresponding API key in `.env`.

## Evaluation

The project includes evaluation outputs and scripts to measure behavior across different prompts and tasks.

Example:

```bash
poetry run python scripts/evaluate.py
```

## Known limitations

This repository is a **portfolio MVP**, not a fully productionized banking platform.

Current limitations include:
- dependency friction around Chroma and related packages in some local environments;
- some code paths still reflecting the transition from classic RAG to dynamic agent flows;
- retrieval evaluation is useful but still lightweight;
- the frontend is functional but not a polished end-user product;
- some roadmap items remain intentionally unfinished.

## Roadmap

Planned next steps include:
- stronger dynamic tool selection,
- multi-source ingestion expansion,
- improved evaluation and observability,
- a cleaner frontend/server split,
- cloud deployment,
- and future extensions toward authenticated financial customer data use cases.

## What I learned

This project helped me practice:
- RAG system design,
- agent orchestration patterns,
- vector store integration,
- Python backend development,
- CI/CD debugging,
- dependency conflict resolution,
- and technical documentation for portfolio use.

## License

MIT - David Llorente Raposo
