# Athena Architecture

**Version:** 1.0

---

# Overview

Athena is an offline-first desktop research platform built around a modular architecture.

The system is divided into independent subsystems with clearly defined responsibilities and interfaces.

Each subsystem should be replaceable without requiring changes to unrelated parts of the application.

---

# High-Level Architecture

```
                        User
                         │
                         ▼
                  Presentation Layer
                         │
                         ▼
                 Application Context
                         │
     ┌───────────────────┼────────────────────┐
     │                   │                    │
     ▼                   ▼                    ▼
Workspace Engine   Document Engine    Search Engine
     │                   │                    │
     └──────────────┬────┴────────────┬───────┘
                    ▼                 ▼
             Indexing Engine      AI Engine
                    │
                    ▼
             Repository Layer
                    │
        ┌───────────┴────────────┐
        │                        │
        ▼                        ▼
   SQLite Repository      Future Repositories
                         (FTS5, ChromaDB, ...)
```

---

# System Layers

Athena follows a layered architecture.

```
Presentation

↓

Application Services

↓

Domain Services

↓

Repositories

↓

Storage
```

Dependencies flow downward only.

Lower layers never depend on upper layers.

---

# Core Components

## Presentation

Responsibilities

- User interface
- Windows
- Dialogs
- Widgets
- User interaction

Presentation contains no business logic.

---

## Application Context

Responsibilities

- Creates shared services
- Creates workspace-specific services
- Wires dependencies
- Manages application lifetime

The Application Context is the composition root.

---

## Workspace Engine

Responsibilities

- Open workspace
- Close workspace
- Create workspace
- Workspace configuration

Every workspace is self-contained.

---

## Document Engine

Responsibilities

- Import documents
- Remove documents
- List documents
- Validate documents

Document storage is independent from indexing.

---

## Indexing Engine

Responsibilities

- Text extraction
- Chunk generation
- Repository persistence

Pipeline

```
Document

↓

Extractor

↓

Chunker

↓

Repository
```

The indexing engine has no knowledge of search or AI.

---

## Search Engine

Responsibilities

- Query validation
- Search execution
- Ranking
- Retrieval

The search engine depends only on the repository interface.

---

## AI Engine

Responsibilities

- Prompt construction
- Context retrieval
- LLM communication
- Response generation

The AI engine never reads files directly.

Instead

```
Question

↓

Search

↓

Retrieved Chunks

↓

Prompt Builder

↓

LLM

↓

Answer
```

---

# Repository Layer

Repositories isolate storage implementation.

```
ChunkRepository

▲

├── MemoryChunkRepository

├── SQLiteChunkRepository

├── SQLiteFTSRepository

└── ChromaRepository
```

The remainder of the application depends only on the interface.

---

# Workspace Structure

```
Workspace/

documents/

.athena/
    index.db

notes/

exports/
```

A workspace is portable.

Copying the folder copies the entire project.

---

# Dependency Rules

Allowed

Presentation

↓

Services

↓

Repositories

↓

Storage

Forbidden

Storage

↓

Presentation

Repositories

↓

Qt

AI

↓

SQLite

Business Logic

↓

Widgets

---

# Quality Standards

Every subsystem must satisfy:

- Complete type hints
- Unit tests
- Ruff clean
- Black formatted
- mypy clean

Architecture changes require documentation updates.

---

# Future Extensions

Athena is designed to support additional capabilities without architectural redesign.

Examples

- OCR

- EPUB

- DOCX

- Markdown

- Full-text search

- Vector search

- Local LLMs

- Cloud LLMs

- Knowledge graphs

- Plugins

---

# Design Philosophy

Athena values:

- Simplicity
- Explicitness
- Testability
- Replaceable components
- Stable interfaces
- Long-term maintainability

Architecture should evolve carefully.

Features should evolve rapidly.

The architecture exists to support decades of development rather than individual releases.