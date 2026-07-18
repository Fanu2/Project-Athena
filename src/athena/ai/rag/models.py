"""
RAG models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RAGSource:
    """Reference source used for an answer."""

    chunk_id: str

    document_id: str

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
    """Generated answer with structured sources."""

    answer: str

    sources: list[RAGSource]
