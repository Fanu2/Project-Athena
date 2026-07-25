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

        #
        # Retrieval Quality
        #

        quality_questions = 0
        top1_hits = 0
        top3_hits = 0
        top5_hits = 0
        reciprocal_rank_sum = 0.0

        for run in session.runs:

            expected = run.question.expected_document_id

            if expected is None:
                continue

            quality_questions += 1

            ids = [
                str(result.document_id)
                for result in run.retrieval_results
            ]

            if ids and ids[0] == expected:
                top1_hits += 1

            if expected in ids[:3]:
                top3_hits += 1

            if expected in ids[:5]:
                top5_hits += 1

            for rank, document_id in enumerate(ids, start=1):
                if document_id == expected:
                    reciprocal_rank_sum += 1.0 / rank
                    break

        if quality_questions:

            summary.top1_accuracy = (
                top1_hits / quality_questions
            )

            summary.top3_accuracy = (
                top3_hits / quality_questions
            )

            summary.top5_accuracy = (
                top5_hits / quality_questions
            )

            summary.mean_reciprocal_rank = (
                reciprocal_rank_sum / quality_questions
            )

        return summary

