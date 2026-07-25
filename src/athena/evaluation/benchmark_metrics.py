"""
Benchmark metrics calculator.
"""

from __future__ import annotations

from athena.domain.ai.retrieval_result import RetrievalResult
from athena.evaluation.benchmark_models import BenchmarkMetrics


class BenchmarkMetricsCalculator:
    """Calculates retrieval evaluation metrics."""

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

        document_ids = [
            str(result.document_id)
            for result in retrieval_results
        ]

        if document_ids:
            metrics.top1_hit = (
                document_ids[0] == expected_document_id
            )

            metrics.top3_hit = (
                expected_document_id in document_ids[:3]
            )

            metrics.recall = (
                1.0
                if expected_document_id in document_ids
                else 0.0
            )

            if expected_document_id in document_ids:
                rank = (
                    document_ids.index(expected_document_id)
                    + 1
                )
                metrics.mrr = 1.0 / rank

        return metrics
