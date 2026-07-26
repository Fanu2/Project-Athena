"""
Benchmark metrics engine.
"""

from __future__ import annotations

import re
from pathlib import Path
from statistics import mean, median

from athena.evaluation.benchmark_models import BenchmarkSummary
from athena.evaluation.benchmark_session import BenchmarkSession


class BenchmarkMetricsEngine:
    """Calculates retrieval evaluation metrics."""

    @staticmethod
    def _normalize_document_name(
        name: str,
    ) -> str:
        """Normalize document identifiers."""

        value = Path(name).name.lower().strip()

        value = re.sub(
            r"\.[a-z0-9]+$",
            "",
            value,
        )

        value = value.replace(
            "_",
            "-",
        )

        value = re.sub(
            r"^\d+-",
            "",
            value,
        )

        return value.strip("-")

    @classmethod
    def _matches_expected(
        cls,
        expected: str,
        result,
    ) -> bool:
        """Match expected document."""

        expected_name = cls._normalize_document_name(
            expected,
        )

        document_name = cls._normalize_document_name(
            result.document_name,
        )

        if str(result.document_id) == expected:
            return True

        if document_name == expected_name:
            return True

        return False

    def summarize(
        self,
        session: BenchmarkSession,
    ) -> BenchmarkSummary:
        """Calculate benchmark summary."""

        summary = BenchmarkSummary()

        summary.total_questions = (
            session.total_questions
        )

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

        quality_questions = 0
        top1_hits = 0
        top3_hits = 0
        top5_hits = 0
        reciprocal_rank_sum = 0.0

        for run in session.runs:

            expected = (
                run.question.expected_document_id
            )

            if expected is None:
                continue

            quality_questions += 1

            results = run.retrieval_results
            if results and self._matches_expected(
                expected,
                results[0],
            ):
                top1_hits += 1

            if any(
                self._matches_expected(
                    expected,
                    result,
                )
                for result in results[:3]
            ):
                top3_hits += 1

            if any(
                self._matches_expected(
                    expected,
                    result,
                )
                for result in results[:5]
            ):
                top5_hits += 1

            for rank, result in enumerate(
                results,
                start=1,
            ):
                if self._matches_expected(
                    expected,
                    result,
                ):
                    reciprocal_rank_sum += (
                        1.0 / rank
                    )
                    break

        if quality_questions:
            summary.top1_accuracy = (
                top1_hits
                / quality_questions
            )

            summary.top3_accuracy = (
                top3_hits
                / quality_questions
            )

            summary.top5_accuracy = (
                top5_hits
                / quality_questions
            )

            summary.mean_reciprocal_rank = (
                reciprocal_rank_sum
                / quality_questions
            )

        return summary

