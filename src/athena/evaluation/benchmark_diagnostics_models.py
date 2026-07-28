"""
Benchmark diagnostic models.

Provides detailed diagnostics explaining retrieval quality for each
benchmark question.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RetrievalDiagnostic:
    """Diagnostic information for a single benchmark question."""

    question_id: str

    expected_document_id: str | None

    expected_found: bool

    expected_rank: int | None

    top_document_id: str | None

    top_document_score: float | None

    expected_document_score: float | None

    retrieved_document_ids: list[str] = field(default_factory=list)

    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class BenchmarkDiagnostics:
    """Collection of diagnostics for a benchmark session."""

    diagnostics: list[RetrievalDiagnostic] = field(default_factory=list)

