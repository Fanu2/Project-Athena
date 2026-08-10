"""
Benchmark metrics engine.
"""

from __future__ import annotations

import re
from pathlib import Path
from statistics import mean, median

from athena.evaluation.benchmark_models import (
    BenchmarkSummary,
)

from athena.evaluation.benchmark_session import (
    BenchmarkSession,
)


class BenchmarkMetricsEngine:
    """Calculates retrieval evaluation metrics."""

    @staticmethod
    def _normalize_document_name(
        name: str,
    ) -> str:
        """
        Normalize document identifiers.

        Handles:
        - filenames
        - extensions
        - underscores/hyphens
        - numeric prefixes
        """

        value = Path(
            name,
        ).name.lower().strip()

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
        """
        Match expected document.

        Supports:
        - exact document id match
        - normalized filename match
        """

        expected_name = (
            cls._normalize_document_name(
                expected,
            )
        )

        document_name = (
            cls._normalize_document_name(
                getattr(
                    result,
                    "document_name",
                    "",
                ),
            )
        )

        document_id = str(
            getattr(
                result,
                "document_id",
                "",
            ),
        )

        if document_id == expected:
            return True

        if document_name == expected_name:
            return True

        return False

    def summarize(
        self,
        session: BenchmarkSession,
    ) -> BenchmarkSummary:
        """
        Calculate benchmark summary.
        """

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

        #
        # Latency metrics
        #

        latencies = [
            run.elapsed_ms
            for run in session.runs
        ]

        if latencies:
            summary.average_latency_ms = (
                mean(latencies)
            )

            summary.median_latency_ms = (
                median(latencies)
            )

            summary.fastest_latency_ms = (
                min(latencies)
            )

            summary.slowest_latency_ms = (
                max(latencies)
            )

        #
        # Retrieval quality metrics
        #

        quality_questions = 0

        top1_hits = 0
        top3_hits = 0
        top5_hits = 0

        reciprocal_rank_sum = 0.0

        #
        # Evaluation intelligence counters.
        #
        # Values are:
        # [question_count, top1_hits]
        #

        language_stats: dict[
            str,
            list[int],
        ] = {}

        document_type_stats: dict[
            str,
            list[int],
        ] = {}

        for run in session.runs:

            expected = (
                run.question.expected_document_id
            )

            if expected is None:
                continue

            quality_questions += 1

            results = (
                run.retrieval_results
            )

            #
            # Top-1
            #

            top1_hit = bool(
                results
                and self._matches_expected(
                    expected,
                    results[0],
                )
            )

            if top1_hit:
                top1_hits += 1

            #
            # Top-3
            #

            if any(
                self._matches_expected(
                    expected,
                    result,
                )
                for result in results[:3]
            ):
                top3_hits += 1

            #
            # Top-5
            #

            if any(
                self._matches_expected(
                    expected,
                    result,
                )
                for result in results[:5]
            ):
                top5_hits += 1

            #
            # Reciprocal rank
            #

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

            #
            # Language evaluation
            #

            language = (
                run.question.language
            )

            if language:
                language_stats.setdefault(
                    language,
                    [0, 0],
                )

                language_stats[
                    language
                ][0] += 1

                if top1_hit:
                    language_stats[
                        language
                    ][1] += 1

            #
            # Document type evaluation
            #

            document_type = (
                run.question.document_type
            )

            if document_type:
                document_type_stats.setdefault(
                    document_type,
                    [0, 0],
                )

                document_type_stats[
                    document_type
                ][0] += 1

                if top1_hit:
                    document_type_stats[
                        document_type
                    ][1] += 1

        #
        # Overall quality metrics
        #

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

        #
        # Language metrics
        #

        summary.language_questions = {
            language: values[0]
            for language, values
            in sorted(
                language_stats.items(),
            )
        }

        summary.language_accuracy = {
            language: (
                values[1]
                / values[0]
            )
            for language, values
            in sorted(
                language_stats.items(),
            )
            if values[0]
        }

        #
        # Document-type metrics
        #

        document_type_accuracy: dict[
            str,
            float,
        ] = {}

        for (
            document_type,
            values,
        ) in sorted(
            document_type_stats.items(),
        ):
            if values[0]:
                document_type_accuracy[
                    document_type
                ] = (
                    values[1]
                    / values[0]
                )

        summary.document_type_accuracy = (
            document_type_accuracy
        )

        return summary
