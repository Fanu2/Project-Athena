

python tools\rewrite.py `
  docs\architecture\05-Knowledge-Architecture.md `
@'
# Athena Knowledge Architecture
Version: 1.0-Draft

Status: Draft

---

# 1. Vision

Project Athena is an offline-first personal knowledge companion. Its primary purpose is not merely to answer questions but to help users accumulate, organize, connect, and reuse knowledge over a lifetime.

Knowledge is treated as a first-class asset. Conversations are transient, while knowledge is persistent and continuously enriched.

The Knowledge Architecture provides the foundation for all future workspaces.

---

# 2. Guiding Principles

## 2.1 User Owns the Knowledge
All notes, evidence, citations, documents, and metadata belong to the user.

## 2.2 Offline First
Core functionality operates without Internet connectivity.

## 2.3 Evidence First
Every AI-generated conclusion should be traceable.

## 2.4 Knowledge Over Conversation
Knowledge persists.
Conversations do not.

## 2.5 AI Assists Human Thinking
Athena augments human reasoning.

## 2.6 Composable Architecture
Every subsystem is reusable.

## 2.7 Long-Term Compatibility
Future features extend the model instead of replacing it.

---

# 3. Knowledge Ontology

The Knowledge Ontology defines every persistent object managed by Athena.


## 4.1 Domain Entities

### KnowledgeCollection

Responsibilities:

- Organize knowledge
- Support nested collections
- Maintain ordering
- Store metadata

Attributes:

- id
- workspace_id
- parent_collection_id
- name
- description
- icon
- color
- created_at
- updated_at

---

### KnowledgeNote

Responsibilities:

- Store user knowledge
- Preserve Markdown
- Reference evidence
- Maintain metadata

Attributes:

- id
- workspace_id
- collection_id
- title
- markdown
- summary
- favorite
- archived
- created_at
- updated_at

---

### EvidenceReference

Responsibilities:

- Reference retrieved evidence
- Preserve provenance
- Support citation generation

Attributes:

- id
- note_id
- document_id
- chunk_id
- citation_id
- retrieval_score
- page_number
- created_at

---

### Tag

Attributes:

- id
- workspace_id
- name
- color

---

### Attachment

Attributes:

- id
- note_id
- filename
- mime_type
- storage_path
- created_at

---

# 5. Persistence Architecture

The Knowledge Workspace uses SQLite through repository implementations consistent with the existing Athena persistence layer.

## Database Tables

knowledge_collections

knowledge_notes

knowledge_note_tags

knowledge_tags

knowledge_attachments

knowledge_evidence

---

## Repository Interfaces

KnowledgeCollectionRepository

KnowledgeNoteRepository

KnowledgeTagRepository

KnowledgeEvidenceRepository

AttachmentRepository

---

## Repository Responsibilities

Repositories are responsible only for persistence.

They must never contain business logic.

Business rules belong exclusively in Application Services.

---

## Design Rules

- UUID primary keys
- Foreign key integrity
- Soft deletion where appropriate
- Immutable evidence records
- Markdown stored without transformation
- References preferred over duplication

---
python tools\rewrite.py `
  docs\architecture\05-Knowledge-Architecture.md `
@'
# 6. Application Services

Application Services coordinate business workflows while keeping domain entities independent of infrastructure.

They orchestrate repositories, AI services, indexing, retrieval, and persistence.

---

## Service Responsibilities

### KnowledgeWorkspaceService

Coordinates the overall Knowledge Workspace.

Responsibilities:

- create collections
- move notes
- archive notes
- delete notes
- search notes

---

### KnowledgeNoteService

Responsible for note lifecycle.

Operations:

- create
- update
- delete
- duplicate
- favorite
- archive
- restore

---

### EvidenceService

Responsible for attaching and validating evidence.

Operations:

- attach evidence
- remove evidence
- regenerate citations
- validate references

---

### KnowledgeSearchService

Provides unified search across:

- notes
- collections
- documents
- conversations
- evidence

---

### KnowledgeImportService

Promotes information into permanent knowledge.

Supported sources:

- AI conversations
- imported documents
- markdown
- manual notes

---

# 7. AI Integration

The Knowledge Workspace does not communicate directly with language models.

Instead, it reuses the existing A2 runtime.
