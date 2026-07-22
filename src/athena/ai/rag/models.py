"""
RAG models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from athena.ai.retrieval.models import SemanticResult


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
    """
    Generated answer together with the retrieval evidence.

    This object is the primary output of the RAG pipeline and is
    intended to power both the chat interface and the Retrieval
    Inspector.
    """

    answer: str

    model: str

    sources: list[RAGSource]

    retrieval_results: list[SemanticResult] = field(
        default_factory=list,
    )