"""
Benchmark metrics calculator.
"""

from __future__ import annotations

import re
from pathlib import Path

from athena.domain.ai.retrieval_result import RetrievalResult

from athena.evaluation.benchmark_models import BenchmarkMetrics


class BenchmarkMetricsCalculator:
    """Calculates retrieval evaluation metrics."""

    @staticmethod
    def _normalize_document_id(document_id: str) -> str:
        """
        Normalize document identifiers for comparison.

        Handles differences such as:
        constitution.md
        01-CONSTITUTION.md
        """

        name = Path(document_id).name.lower()

        name = re.sub(
            r".[a-z0-9]+$",
            "",
            name,
        )

        name = name.replace(
            "_",
            "-",
        )

        name = re.sub(
            r"^\d+-",
            "",
            name,
        )

        return name.strip("-")

    @staticmethod
    def calculate(
        expected_document_id: str | None,
        retrieval_results: list[RetrievalResult],
        latency_ms: float,
    ) -> BenchmarkMetrics:
        """Calculate benchmark metrics."""

        metrics = BenchmarkMetrics(
            latency_ms=latency_ms,
        )

        if not expected_document_id:
            return metrics

        expected = (
            BenchmarkMetricsCalculator
            ._normalize_document_id(
                expected_document_id,
            )
        )

        document_names = [
            BenchmarkMetricsCalculator
            ._normalize_document_id(
                result.document_name,
            )
            for result in retrieval_results
        ]

        if document_names:
            metrics.top1_hit = (
                document_names[0] == expected
            )

            metrics.top3_hit = (
                expected in document_names[:3]
            )

            metrics.recall = (
                1.0
                if expected in document_names
                else 0.0
            )

            if expected in document_names:
                rank = (
                    document_names.index(expected)
                    + 1
                )

                metrics.mrr = 1.0 / rank

        return metrics

