# Athena Capability Test Document

## Purpose

This document is used to validate Athena's intelligence pipeline.

Tests:

- Document ingestion
- Knowledge extraction
- Semantic retrieval
- Context building
- RAG answering
- Citation generation
- Model capability routing


# Project Athena Overview

Project Athena is a personal offline AI workstation designed around:

- User-owned data
- Offline-first operation
- Replaceable AI models
- Modular architecture
- Evidence-backed AI answers


# AI Runtime Test

Athena supports multiple AI providers and models.

Current default local runtime:

Provider:
Ollama

Default model:
qwen2.5:1.5b

Purpose:

- Low resource usage
- Fast local inference
- Offline operation


# Model Capability Test

Models may have different roles:

## Chat Models

Examples:

- qwen2.5:1.5b
- qwen3:4b
- llama models

Capabilities:

- conversation
- reasoning
- question answering


## Embedding Models

Example:

- nomic-embed-text

Capabilities:

- document vector creation
- semantic search
- retrieval support


# Retrieval Intelligence Test

Athena should answer:

Question:

"What are the main design principles of Project Athena?"

Expected concepts:

- offline first
- user owns data
- modular architecture
- replaceable AI models


# Evidence Test

Athena should identify evidence from this document.

Expected citation:

Section:
Project Athena Overview


# Reasoning Test

Question:

"Why does Athena use smaller local models as the default?"

Expected answer:

Because resource-efficient models:

- require less memory
- run faster
- support offline usage
- allow deployment on modest hardware


# Provider Intelligence Test

Question:

"Which model should be used for embeddings?"

Expected answer:

nomic-embed-text

Reason:

It provides embedding capability rather than chat generation.


# End of Test
