"""
Project Athena

Benchmark Retrieval Report Builder.
"""

from __future__ import annotations

from typing import Any

from athena.evaluation.benchmark_retrieval_report import (
    BenchmarkRetrievalReport,
)

from athena.evaluation.retrieval_analysis_engine import (
    RetrievalAnalysisEngine,
)


class BenchmarkRetrievalReportBuilder:
    """
    Build benchmark-level retrieval reports.
    """

    def __init__(self) -> None:
        self._analysis = RetrievalAnalysisEngine()

    def build(
        self,
        retrievals,
        metadata: dict[str, Any] | None = None,
    ) -> BenchmarkRetrievalReport:
        """
        Build a benchmark retrieval report.
        """

        reports = []

        total_latency = 0.0

        total_candidates = 0

        for retrieval in retrievals:

            report = self._analysis.analyze(
                query=(
                    retrieval.question.question
                ),
                strategy="retrieval",
                latency_ms=(
                    retrieval.elapsed_ms
                ),
                results=(
                    retrieval.retrieval_results
                ),
            )

            reports.append(report)

            total_latency += (
                report.latency_ms
            )

            total_candidates += (
                report.candidate_count
            )

        count = len(reports)

        return BenchmarkRetrievalReport(
            reports=reports,
            total_queries=count,
            average_latency_ms=(
                total_latency / count
                if count
                else 0.0
            ),
            average_candidates=(
                total_candidates / count
                if count
                else 0.0
            ),
            metadata=(
                metadata
                if metadata
                else {}
            ),
        )
