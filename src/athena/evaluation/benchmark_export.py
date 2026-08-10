"""
Benchmark export utilities.
"""

from __future__ import annotations

import json
from pathlib import Path

from athena.evaluation.benchmark_models import BenchmarkSummary


class BenchmarkExporter:
    """Exports benchmark results."""

    @staticmethod
    def export_markdown(
        report: str,
        path: str | Path,
    ) -> None:
        """
        Write a Markdown report.
        """

        output = Path(path)

        output.write_text(
            report,
            encoding="utf-8",
        )

    @staticmethod
    def export_json(
        summary: BenchmarkSummary,
        path: str | Path,
    ) -> None:
        """
        Write benchmark summary as JSON.

        Includes retrieval quality metrics,
        latency metrics, and evaluation intelligence
        breakdowns.
        """

        output = Path(path)

        data = {
            #
            # Overall metrics
            #

            "total_questions": (
                summary.total_questions
            ),

            "successful_retrievals": (
                summary.successful_retrievals
            ),

            "failed_retrievals": (
                summary.failed_retrievals
            ),


            #
            # Retrieval accuracy
            #

            "top1_accuracy": (
                summary.top1_accuracy
            ),

            "top3_accuracy": (
                summary.top3_accuracy
            ),

            "top5_accuracy": (
                summary.top5_accuracy
            ),

            "mean_reciprocal_rank": (
                summary.mean_reciprocal_rank
            ),


            #
            # Latency
            #

            "average_latency_ms": (
                summary.average_latency_ms
            ),

            "median_latency_ms": (
                summary.median_latency_ms
            ),

            "fastest_latency_ms": (
                summary.fastest_latency_ms
            ),

            "slowest_latency_ms": (
                summary.slowest_latency_ms
            ),


            #
            # Multilingual evaluation intelligence
            #

            "language_questions": (
                summary.language_questions
            ),

            "language_accuracy": (
                summary.language_accuracy
            ),

            "document_type_accuracy": (
                summary.document_type_accuracy
            ),
        }

        output.write_text(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
