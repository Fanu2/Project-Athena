"""
Benchmark metrics engine.
"""

from __future__ import annotations

from statistics import mean, median

from athena.evaluation.benchmark_models import BenchmarkSummary
from athena.evaluation.benchmark_session import BenchmarkSession


class BenchmarkMetricsEngine:
    """Calculates summary metrics for a benchmark session."""

    def summarize(
        self,
        session: BenchmarkSession,
    ) -> BenchmarkSummary:

        summary = BenchmarkSummary()

        summary.total_questions = session.total_questions

        summary.successful_retrievals = sum(
            1
            for run in session.runs
            if run.retrieval_results
        )

        summary.failed_retrievals = (
            summary.total_questions
            - summary.successful_retrievals
        )

        latencies = [
            run.elapsed_ms
            for run in session.runs
        ]

        if latencies:
            summary.average_latency_ms = mean(latencies)
            summary.median_latency_ms = median(latencies)
            summary.fastest_latency_ms = min(latencies)
            summary.slowest_latency_ms = max(latencies)

        return summary
