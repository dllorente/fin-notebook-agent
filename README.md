# 🏦 Fin-Notebook-Agent

> Agentic RAG assistant for banking documentation, inspired by NotebookLM.

![CI](https://github.com/dllorente/fin-notebook-agent/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![LangChain](https://img.shields.io/badge/LangChain-0.3-green)
![LangGraph](https://img.shields.io/badge/LangGraph-agentic-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Fin-Notebook-Agent is a portfolio project focused on building an internal-style assistant for financial documentation with an agentic RAG architecture.

It combines:
- LangGraph orchestration and specialized tools (search, summarize, briefing, web fallback),
- retrieval over local indexed documents with Chroma,
- a FastAPI backend and Streamlit UI,
- observability and reproducible evaluation workflows.

## Quick demo setup

```bash
git clone https://github.com/dllorente/fin-notebook-agent.git
cd fin-notebook-agent
poetry install
cp .env.example .env
poetry run python scripts/ingest.py
poetry run uvicorn main:app --reload
```

In another terminal:

```bash
poetry run streamlit run streamlit_app/main.py
```

## Tech stack

- Python 3.12
- LangChain + LangGraph
- Chroma vector store
- FastAPI + Streamlit
- Poetry + Docker + GitHub Actions

## Project notes

- `models/vectorstores/` is generated locally by ingestion and is not intended for version control.
- `chat_sessions.db` is local runtime state.

## Full documentation

For detailed setup, environment variables, architecture, repository map, troubleshooting, evaluation, roadmap, and lessons learned, see:

- [`docs/README_FULL.md`](docs/README_FULL.md)

## License

MIT - David Llorente Raposo