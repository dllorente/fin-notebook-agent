# Changelog - Fin-Notebook-Agent

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
*Espacio para cambios que estás desarrollando actualmente pero que aún no han sido "lanzados" oficialmente.*

## [0.1.0] - 2024-05-22
### Added
- Project structure with Poetry and modular architecture (api, core, engine, index, models)
- `app/core/config.py`: provider-agnostic settings with `get_settings()`, `get_llm()` and `get_embeddings()`
- `app/index/document_loader.py`: document ingestion for PDF and TXT with metadata and chunking
- `.env.example` with all required environment variables
- `.gitignore` for Python, Poetry, and project-specific files