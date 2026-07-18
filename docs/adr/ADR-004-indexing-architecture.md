# ADR-004: Indexing Architecture

**Status:** Accepted  
**Date:** 2026-07-18

---

# Context

Athena transforms imported documents into searchable knowledge.

Indexing is responsible for converting source documents into structured, searchable chunks while remaining completely independent from the user interface, search engine, and AI engine.

The indexing subsystem is designed as a processing pipeline where each stage has a single responsibility.

---

# Decision

Athena shall implement indexing as a sequential processing pipeline.

```text
Document

↓

Document Import

↓

Text Extraction

↓

Chunk Generation

↓

Repository

↓

Persistent Storage
```

Each stage performs one well-defined task.

Data flows in only one direction.

---

# Architecture

```text
                    Document

                        │
                        ▼
                DocumentService

                        │
                        ▼
          WorkspaceDocumentService

                        │
                        ▼
                IndexingService

        ┌───────────────┴───────────────┐
        ▼                               ▼
ExtractorFactory                  ChunkingService
        │
        ▼
Document Extractor
        │
        ▼
ExtractedDocument
        │
        ▼
DocumentChunk
        │
        ▼
ChunkRepository
        │
        ▼
SQLiteChunkRepository
        │
        ▼
SQLite Database
```

---

# Processing Stages

## Stage 1 – Document Import

Responsible for:

- importing files
- validating file types
- copying files into the workspace

Implemented by:

- DocumentService
- WorkspaceDocumentService

---

## Stage 2 – Text Extraction

Responsible for:

- reading document contents
- extracting plain text
- preserving page boundaries
- creating an ExtractedDocument

Supported formats:

- PDF
- TXT
- Markdown

Future formats:

- DOCX
- EPUB
- HTML
- OCR

---

## Stage 3 – Chunk Generation

Responsible for:

- splitting extracted text
- generating ordered chunks
- preserving page numbers
- assigning chunk identifiers

Output:

```text
DocumentChunk
```

---

## Stage 4 – Repository Persistence

Responsible for:

- saving chunks
- loading chunks
- deleting chunks

Implemented through:

```text
ChunkRepository
```

Current implementation:

```text
SQLiteChunkRepository
```

Future implementations:

- SQLite FTS5
- ChromaDB
- PostgreSQL
- Elasticsearch

---

# Dependency Rules

Allowed:

```text
Importer

↓

Extractor

↓

Chunker

↓

Repository
```

Forbidden:

```text
Repository

↓

Extractor
```

```text
Repository

↓

User Interface
```

```text
Search

↓

Extractor
```

```text
AI

↓

Extractor
```

---

# Responsibilities

## DocumentService

Responsible only for document storage.

It never performs indexing.

---

## WorkspaceDocumentService

Coordinates document operations.

After importing a document it requests indexing.

It does not perform indexing itself.

---

## IndexingService

Coordinates the indexing pipeline.

It does not know:

- SQLite
- Qt
- Search
- AI

It depends only on the repository interface.

---

## ChunkRepository

Provides persistent storage.

It contains no business logic.

---

# Error Handling

Failures in one pipeline stage prevent later stages from executing.

Examples:

Extraction failure

↓

Chunk generation skipped

↓

Repository not modified

This prevents partially indexed documents.

---

# Benefits

The pipeline architecture provides:

- clear separation of responsibilities
- independent testing
- replaceable implementations
- easier debugging
- future extensibility
- stable interfaces

---

# Future Extensions

The pipeline allows additional stages without redesign.

Examples:

```text
Document

↓

OCR

↓

Language Detection

↓

Metadata Extraction

↓

Entity Recognition

↓

Chunk Generation

↓

Embeddings

↓

Repository
```

Each stage remains independent.

---

# Consequences

Future indexing improvements should extend individual stages rather than modifying unrelated components.

Examples include:

- OCR support
- smarter chunking algorithms
- automatic language detection
- document metadata extraction
- embedding generation

These enhancements should integrate naturally into the pipeline while preserving the existing architecture.