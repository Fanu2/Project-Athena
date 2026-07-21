"""
RAG models.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class RAGSource:
    """Reference source used for an answer."""

    chunk_id: str

    document_id: str

    document_name: str

    document_path: Path

    page_number: int

    score: float

    text: str


@dataclass(slots=True)
class RAGContext:
    """Prepared context for LLM."""

    question: str

    context: str

    sources: list[RAGSource]


@dataclass(slots=True)
class RAGAnswer:
    """Generated answer with structured metadata and sources."""

    answer: str

    model: str

    sources: list[RAGSource]