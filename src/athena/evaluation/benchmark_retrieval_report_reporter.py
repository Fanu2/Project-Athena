"""
Project Athena

Benchmark Retrieval Report Reporter.
"""

from __future__ import annotations

from athena.evaluation.benchmark_retrieval_report import (
    BenchmarkRetrievalReport,
)
from athena.evaluation.retrieval_report_reporter import (
    RetrievalReportReporter,
)


class BenchmarkRetrievalReportReporter:
    """Render benchmark retrieval reports as Markdown."""

    def __init__(self) -> None:
        self._reporter = RetrievalReportReporter()

    def analyze(
        self,
        report: BenchmarkRetrievalReport,
    ) -> str:

        lines = [
            "# Benchmark Retrieval Intelligence Report",
            "",
            "## Summary",
            f"- Total Queries: {report.total_queries}",
            f"- Average Latency: {report.average_latency_ms:.2f} ms",
            f"- Average Candidates: {report.average_candidates:.2f}",
            "",
        ]

        for index, retrieval in enumerate(report.reports, start=1):

            lines.extend(
                [
                    "---",
                    "",
                    f"## Retrieval {index}",
                    "",
                    self._reporter.analyze(retrieval),
                    "",
                ]
            )

        return "\n".join(lines)
