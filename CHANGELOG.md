# Changelog - Fin-Notebook-Agent

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-22
### Added
- Project structure with Poetry and modular architecture (api, core, engine, index, models)
- `app/core/config.py`: provider-agnostic settings with `get_settings()`, `get_llm()` and `get_embeddings()`
- `app/index/document_loader.py`: document ingestion for PDF and TXT with metadata and chunking
- `.env.example` with all required environment variables
- `.gitignore` for Python, Poetry, and project-specific files


## [0.1.1] - 2026-05-22
### Fixed
- Removed circular import `document_loader → config` in `app/core/config.py`
- Removed duplicate `Field` import in `app/core/config.py`
- Added missing type hint imports `BaseChatModel` and `Embeddings` in `app/core/config.py`
- Removed incorrect `List` import from `ast` in `app/index/document_loader.py`
- Fixed import path `core.config` → `app.core.config` in `app/index/document_loader.py`