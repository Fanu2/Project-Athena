"""
Project Athena

Benchmark Retrieval Intelligence Report domain models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from athena.evaluation.retrieval_report import (
    RetrievalReport,
)


@dataclass(slots=True)
class BenchmarkRetrievalReport:
    """
    Aggregated retrieval intelligence
    for a benchmark session.
    """

    reports: list[RetrievalReport] = field(
        default_factory=list,
    )

    total_queries: int = 0

    average_latency_ms: float = 0.0

    average_candidates: float = 0.0

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )
