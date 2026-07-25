"""
Benchmark report generation.
"""

from __future__ import annotations

from athena.evaluation.benchmark_models import (
    BenchmarkSummary,
)


class BenchmarkReport:
    """Generates benchmark reports."""

    @staticmethod
    def to_markdown(
        summary: BenchmarkSummary,
    ) -> str:
        """Generate a Markdown report."""

        lines = [
            "# Athena Retrieval Benchmark Report",
            "",
            f"Total Questions: {summary.total_questions}",
            f"Completed Questions: {summary.completed_questions}",
            "",
            "## Metrics",
            "",
            f"- Top-1 Accuracy: {summary.top1_accuracy:.2%}",
            f"- Top-3 Accuracy: {summary.top3_accuracy:.2%}",
            f"- Average Recall: {summary.average_recall:.2%}",
            f"- Mean Reciprocal Rank: {summary.average_mrr:.4f}",
            f"- Average Latency: {summary.average_latency_ms:.2f} ms",
        ]

        return "\n".join(lines)
