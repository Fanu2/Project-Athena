# ADR-008: Plugin System

**Status:** Accepted

**Date:** 2026-07-18

---

# Context

Athena will continue growing beyond its core functionality.

To avoid increasing complexity, optional capabilities should be implemented as plugins.

---

# Decision

The core application shall define extension points.

Plugins implement these interfaces.

The core application does not depend on plugins.

---

# Plugin Categories

Document Importers

- PDF
- DOCX
- EPUB

OCR

- Tesseract

Search

- FTS5
- Vector Search

Artificial Intelligence

- Ollama
- llama.cpp
- OpenAI

Export

- Markdown
- PDF
- HTML

---

# Rules

Plugins:

- may extend functionality
- must not modify core modules
- communicate only through published interfaces

---

# Consequences

Future features can be added without redesigning the architecture.