"""
RAG models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from athena.ai.retrieval.models import SemanticResult
from athena.domain.ai.citation import Citation
from athena.domain.ai.evidence_record import EvidenceRecord
from athena.domain.ai.resolved_citation import ResolvedCitation


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
    Generated answer together with retrieval evidence.

    This object is the primary output of the RAG pipeline and
    powers chat, citations, retrieval inspection, and citation
    intelligence.
    """

    answer: str

    model: str

    sources: list[RAGSource]

    retrieval_results: list[SemanticResult] = field(
        default_factory=list,
    )

    evidence: list[EvidenceRecord] = field(
        default_factory=list,
    )

    citations: list[Citation] = field(
        default_factory=list,
    )

    resolved_citations: list[ResolvedCitation] = field(
        default_factory=list,
    )