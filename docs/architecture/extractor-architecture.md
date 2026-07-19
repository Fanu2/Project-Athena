@'
# Extractor Architecture

## Purpose

The extractor subsystem converts supported document formats into a common
ExtractedDocument model used by the indexing pipeline.

## Components

- BaseExtractor
- ExtractorFactory
- PDFExtractor
- MarkdownExtractor
- TextExtractor
- DOCXExtractor (planned)

## Pipeline

Import
↓
ExtractorFactory
↓
Extractor
↓
ExtractedDocument
↓
Chunking
↓
Embeddings
↓
Storage

## Design Principles

- Single Responsibility
- Open/Closed Principle
- No extractor-specific logic outside the extractor.
- New document formats are added by implementing BaseExtractor.
- Existing extractors must not be modified unless fixing defects.

## Supported Formats

- PDF
- Markdown
- Text
- DOCX (planned)

## Status

Frozen for Athena 1.0.
'@ | Set-Content "docs\architecture\extractor-architecture.md"