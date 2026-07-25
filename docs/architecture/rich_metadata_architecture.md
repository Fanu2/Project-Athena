@'
# Rich Metadata Architecture

## Status

Proposed

---

# Purpose

The Rich Metadata subsystem extends Athena's knowledge layer by storing
AI-generated metadata separately from the core Document entity.

This preserves a clean separation between document identity and document
knowledge.

---

# Design Goals

- Keep Document small and stable.
- Store AI-derived information independently.
- Support future metadata expansion without modifying the Document schema.
- Maintain complete backward compatibility.
- Enable metadata-aware retrieval.

---

# Layered Architecture

Document
    │
    ▼
Metadata Repository
    │
    ▼
SQLite Metadata Repository
    │
    ▼
DocumentMetadataModel
    │
    ▼
SQLite Database

---

# Domain Model

DocumentMetadata

Fields:

- document_id
- language
- page_count
- last_indexed
- metadata_version

---

# Relationship

documents
    │
    └── document_metadata

Relationship:

One Document

↓

One Metadata Record

---

# Separation of Responsibilities

Document

Responsible for:

- identity
- filename
- title
- file path
- file type
- timestamps

DocumentMetadata

Responsible for:

- language
- page count
- indexing state
- future AI metadata

---

# Runtime Metadata

MetadataResult is NOT persistent.

It represents temporary metadata detected while processing a query.

DocumentMetadata represents persistent knowledge.

---

# Future Metadata

Future versions may include:

- author
- keywords
- entities
- summaries
- collections
- topics
- OCR confidence
- embedding information

These additions should not require changes to the Document model.

---

# Benefits

- Separation of concerns
- Stable database schema
- Easier migrations
- Better retrieval
- Future AI extensibility
- Zero impact on existing Document workflows

---

# Roadmap

A6.4.1
DocumentMetadata

✓ Complete

A6.4.2
MetadataRepository

✓ Complete

A6.4.3
DocumentMetadataModel

Next

A6.4.4
SQLiteMetadataRepository

Pending

A6.4.5
Migration

Pending

A6.4.6
Metadata Extraction

Pending

A6.4.7
Metadata-aware Retrieval

Pending
'@ | Set-Content .\docs\architecture\rich_metadata_architecture.md