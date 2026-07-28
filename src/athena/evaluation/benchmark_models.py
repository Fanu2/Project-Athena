"""
Benchmark domain models.

Core domain objects for the Athena Evaluation Framework.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from athena.domain.ai.retrieval_result import RetrievalResult


@dataclass(slots=True, frozen=True)
class BenchmarkQuestion:
    """Represents one benchmark query."""

    question_id: str
    question: str
    expected_document_id: str | None = None
    expected_chunk_id: str | None = None
    tags: tuple[str, ...] = ()


@dataclass(slots=True)
class BenchmarkRun:
    """Represents one executed benchmark question."""

    question: BenchmarkQuestion

    retrieval_results: list[RetrievalResult] = field(
        default_factory=list,
    )

    elapsed_ms: float = 0.0


@dataclass(slots=True)
class BenchmarkSummary:
    """Summary statistics for a benchmark session."""

    total_questions: int = 0

    successful_retrievals: int = 0
    failed_retrievals: int = 0

    top1_accuracy: float = 0.0
    top3_accuracy: float = 0.0
    top5_accuracy: float = 0.0

    mean_reciprocal_rank: float = 0.0

    average_latency_ms: float = 0.0
    median_latency_ms: float = 0.0

    fastest_latency_ms: float = 0.0
    slowest_latency_ms: float = 0.0

