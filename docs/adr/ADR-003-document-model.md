# ADR-003: Document Model

**Status:** Accepted

**Date:** 2026-07-18

---

# Context

Documents are the primary source of knowledge within Athena.

Every subsystem—including indexing, search, and AI—depends on a consistent document model and lifecycle.

To ensure reproducibility, imported documents are treated as immutable source artifacts.

---

# Decision

Athena shall model every document as an immutable resource.

A document follows a well-defined lifecycle.

```text
Import

↓

Validation

↓

Workspace Storage

↓

Text Extraction

↓

Chunk Generation

↓

Repository Storage

↓

Search

↓

AI Retrieval
```

Once imported, the original file is never modified.

If the source document changes, it shall be imported again and re-indexed.

---

# Document Types

Current supported formats:

- PDF
- Plain Text (.txt)
- Markdown (.md)

Planned formats:

- DOCX
- EPUB
- HTML
- Rich Text
- Scanned PDFs (OCR)

---

# Document Identity

Each document receives a unique identifier.

The identifier remains stable throughout the document lifecycle.

It is used to associate:

- extracted text
- chunks
- search results
- citations
- future annotations

---

# Metadata

Every imported document stores the following metadata.

Required

- Document ID
- Title
- File Path
- Page Count

Future

- Import Timestamp
- Language
- SHA-256 Checksum
- Author
- Tags
- User Notes
- OCR Status

---

# Extraction

Extraction converts the original document into an `ExtractedDocument`.

Responsibilities:

- preserve text
- preserve page numbers
- preserve document identity

Extraction never performs:

- search
- chunking
- AI
- ranking

---

# Chunk Generation

Chunking converts an `ExtractedDocument` into multiple `DocumentChunk` objects.

Each chunk stores:

- Chunk ID
- Document ID
- Chunk Index
- Page Number
- Text

Chunks remain immutable.

---

# Repository Storage

Repositories persist chunks.

Repositories never modify chunk contents.

Responsibilities:

- save
- load
- delete
- search (future)

---

# Search

Search operates only on indexed chunks.

Search never opens source documents.

Search never performs extraction.

---

# Artificial Intelligence

The AI subsystem never reads documents directly.

Instead it receives:

```text
Question

↓

Search

↓

Document Chunks

↓

Prompt Builder

↓

LLM

↓

Answer
```

Documents remain the authoritative source.

---

# Dependency Rules

Allowed

```text
Document

↓

Extraction

↓

Chunking

↓

Repository

↓

Search

↓

AI
```

Forbidden

```text
AI

↓

Document
```

```text
Search

↓

Extraction
```

```text
Repository

↓

Document
```

---

# Benefits

The document model provides:

- reproducible indexing
- stable citations
- immutable source data
- reliable AI retrieval
- future extensibility

---

# Future Extensions

The document model supports future capabilities including:

- annotations
- highlights
- bookmarks
- semantic entities
- embeddings
- knowledge graphs
- document relationships

without changing the fundamental lifecycle.

---

# Consequences

Every new feature must integrate into the document lifecycle rather than bypass it.

The original imported document always remains the canonical source of truth.