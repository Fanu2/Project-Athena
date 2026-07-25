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
        """Write a Markdown report."""

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
        """Write benchmark summary as JSON."""

        output = Path(path)

        data = {
            "total_questions": summary.total_questions,
            "completed_questions": summary.completed_questions,
            "top1_accuracy": summary.top1_accuracy,
            "top3_accuracy": summary.top3_accuracy,
            "average_recall": summary.average_recall,
            "average_mrr": summary.average_mrr,
            "average_latency_ms": summary.average_latency_ms,
        }

        output.write_text(
            json.dumps(
                data,
                indent=4,
            ),
            encoding="utf-8",
        )
