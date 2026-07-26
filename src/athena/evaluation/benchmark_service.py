"""
Benchmark orchestration service.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from athena.application.ai.retrieval_service import RetrievalService
from athena.evaluation.benchmark_diagnostics_engine import BenchmarkDiagnosticsEngine
from athena.evaluation.benchmark_diagnostics_report import (
    BenchmarkDiagnosticsReporter,
)
from athena.evaluation.benchmark_loader import BenchmarkLoader
from athena.evaluation.benchmark_metrics_engine import BenchmarkMetricsEngine
from athena.evaluation.benchmark_report import MarkdownReporter
from athena.evaluation.benchmark_runner import BenchmarkRunner
from athena.evaluation.benchmark_session import BenchmarkSession
from athena.evaluation.benchmark_validator import BenchmarkValidator


class BenchmarkService:
    """Coordinates benchmark execution."""

    def __init__(
        self,
        retrieval_service: RetrievalService,
    ) -> None:
        self._runner = BenchmarkRunner(retrieval_service)
        self._metrics = BenchmarkMetricsEngine()
        self._diagnostics = BenchmarkDiagnosticsEngine()
        self._reporter = MarkdownReporter()
        self._diagnostics_reporter = BenchmarkDiagnosticsReporter()

    def run(
        self,
        dataset_path: str,
    ) -> None:
        """Execute a benchmark."""

        questions = BenchmarkLoader.load(dataset_path)

        errors = BenchmarkValidator.validate(questions)

        if errors:
            raise ValueError("\n".join(errors))

        session = BenchmarkSession()
        session.dataset_name = Path(dataset_path).name

        for question in questions:
            session.runs.append(
                self._runner.run(question),
            )

        session.finished_at = datetime.now(UTC)

        summary = self._metrics.summarize(session)

        diagnostics = self._diagnostics.analyze(session)

        report = self._reporter.generate(
            session,
            summary,
        )

        diagnostics_report = self._diagnostics_reporter.generate(
            diagnostics,
        )

        # Export integration will be added in a later sprint.
        _ = report
        _ = diagnostics_report
