# Indexing Pipeline

## Overview

The indexing pipeline converts imported documents into searchable knowledge.

## Pipeline

Workspace
    ?
Importer
    ?
ExtractorFactory
    ?
BaseExtractor
    ?
ExtractedDocument
    ?
ChunkingService
    ?
EmbeddingService
    ?
Repository
    ?
Search Index

## Responsibilities

### Importer

- Detect document type
- Invoke ExtractorFactory

### ExtractorFactory

- Select extractor implementation

### BaseExtractor

- Convert document into ExtractedDocument

### ChunkingService

- Split text into semantic chunks

### EmbeddingService

- Generate vector embeddings

### Repository

- Persist documents, chunks and embeddings

## Extension Rules

To support a new format:

1. Create a new extractor.
2. Implement BaseExtractor.
3. Register in ExtractorFactory.
4. Add unit tests.
5. Update documentation.

No other subsystem should require modification.

## Status

Frozen for Athena 1.0.
