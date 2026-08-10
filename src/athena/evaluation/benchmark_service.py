"""
Benchmark orchestration service.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from athena.application.ai.retrieval_service import (
    RetrievalService,
)

from athena.evaluation.benchmark_diagnostics_engine import (
    BenchmarkDiagnosticsEngine,
)

from athena.evaluation.benchmark_diagnostics_report import (
    BenchmarkDiagnosticsReporter,
)

from athena.evaluation.benchmark_export import (
    BenchmarkExporter,
)

from athena.evaluation.benchmark_loader import (
    BenchmarkLoader,
)

from athena.evaluation.benchmark_metrics_engine import (
    BenchmarkMetricsEngine,
)

from athena.evaluation.benchmark_report import (
    MarkdownReporter,
)

from athena.evaluation.benchmark_retrieval_report_builder import (
    BenchmarkRetrievalReportBuilder,
)

from athena.evaluation.benchmark_retrieval_report_reporter import (
    BenchmarkRetrievalReportReporter,
)

from athena.evaluation.benchmark_runner import (
    BenchmarkRunner,
)

from athena.evaluation.benchmark_session import (
    BenchmarkSession,
)

from athena.evaluation.benchmark_validator import (
    BenchmarkValidator,
)


class BenchmarkService:
    """
    Coordinates benchmark execution.
    """

    def __init__(
        self,
        retrieval_service: RetrievalService,
    ) -> None:

        self._runner = BenchmarkRunner(
            retrieval_service,
        )

        self._metrics = BenchmarkMetricsEngine()

        self._diagnostics = (
            BenchmarkDiagnosticsEngine()
        )

        self._retrieval_builder = (
            BenchmarkRetrievalReportBuilder()
        )

        self._reporter = MarkdownReporter()

        self._diagnostics_reporter = (
            BenchmarkDiagnosticsReporter()
        )

        self._retrieval_reporter = (
            BenchmarkRetrievalReportReporter()
        )

    def run(
        self,
        dataset_path: str,
        output_directory: str | Path | None = None,
    ) -> None:
        """
        Execute a benchmark.
        """

        questions = BenchmarkLoader.load(
            dataset_path,
        )

        errors = BenchmarkValidator.validate(
            questions,
        )

        if errors:
            raise ValueError(
                "\n".join(errors),
            )

        session = BenchmarkSession()

        session.dataset_name = (
            Path(dataset_path).name
        )

        for question in questions:
            session.runs.append(
                self._runner.run(
                    question,
                )
            )

        session.finished_at = (
            datetime.now(
                UTC,
            )
        )

        summary = self._metrics.summarize(
            session,
        )

        diagnostics = (
            self._diagnostics.analyze(
                session,
            )
        )

        retrieval_report = (
            self._retrieval_builder.build(
                session.runs,
                metadata={
                    "language_questions": (
                        summary.language_questions
                    ),
                    "language_accuracy": (
                        summary.language_accuracy
                    ),
                    "document_type_accuracy": (
                        summary.document_type_accuracy
                    ),
                },
            )
        )

        benchmark_report = (
            self._reporter.analyze(
                session,
                summary,
            )
        )

        diagnostics_report = (
            self._diagnostics_reporter.analyze(
                diagnostics,
            )
        )

        retrieval_markdown = (
            self._retrieval_reporter.analyze(
                retrieval_report,
            )
        )

        results_directory = (
            Path(output_directory)
            if output_directory
            else Path(
                "benchmarks/results",
            )
        )

        results_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        BenchmarkExporter.export_markdown(
            benchmark_report,
            results_directory
            / "benchmark_report.md",
        )

        BenchmarkExporter.export_markdown(
            diagnostics_report,
            results_directory
            / "benchmark_diagnostics.md",
        )

        BenchmarkExporter.export_markdown(
            retrieval_markdown,
            results_directory
            / "benchmark_retrieval_report.md",
        )

        BenchmarkExporter.export_json(
            summary,
            results_directory
            / "benchmark_summary.json",
        )
