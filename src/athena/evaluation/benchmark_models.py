"""
Benchmark domain models.

These models define the data structures used by the Athena Retrieval
Evaluation Framework.

The benchmark framework evaluates retrieval quality while reusing the
existing retrieval models provided by Athena.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from athena.ai.retrieval.models import SemanticResult


@dataclass(slots=True, frozen=True)
class BenchmarkQuestion:
    """Represents one benchmark query."""

    question_id: str
    question: str
    expected_document_id: str | None = None
    expected_chunk_id: str | None = None
    tags: tuple[str, ...] = ()


@dataclass(slots=True)
class BenchmarkMetrics:
    """Evaluation metrics for a benchmark run."""

    top1_hit: bool = False
    top3_hit: bool = False
    recall: float = 0.0
    mrr: float = 0.0
    latency_ms: float = 0.0


@dataclass(slots=True)
class BenchmarkRun:
    """Result of executing one benchmark question."""

    question: BenchmarkQuestion
    retrieval_results: list[SemanticResult] = field(default_factory=list)
    metrics: BenchmarkMetrics = field(default_factory=BenchmarkMetrics)


@dataclass(slots=True)
class BenchmarkSummary:
    """Summary of an entire benchmark session."""

    total_questions: int = 0
    completed_questions: int = 0
    average_recall: float = 0.0
    average_mrr: float = 0.0
    average_latency_ms: float = 0.0
    top1_accuracy: float = 0.0
    top3_accuracy: float = 0.0
