"""
Benchmark orchestration service.
"""

from __future__ import annotations

from athena.application.ai.retrieval_service import RetrievalService
from athena.evaluation.benchmark_loader import BenchmarkLoader
from athena.evaluation.benchmark_validator import BenchmarkValidator
from athena.evaluation.benchmark_runner import BenchmarkRunner
from athena.evaluation.benchmark_metrics_engine import BenchmarkMetricsEngine
from athena.evaluation.benchmark_diagnostics_engine import BenchmarkDiagnosticsEngine
from athena.evaluation.benchmark_report import MarkdownReporter
from athena.evaluation.benchmark_diagnostics_report import BenchmarkDiagnosticsReporter
from athena.evaluation.benchmark_export import BenchmarkExporter
from athena.evaluation.benchmark_session import BenchmarkSession


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

    def run(self, dataset_path: str) -> None:
        """Execute a benchmark."""

        # TODO: Load dataset
        # TODO: Validate dataset
        # TODO: Create session
        # TODO: Execute benchmark runs
        # TODO: Generate metrics
        # TODO: Generate diagnostics
        # TODO: Generate reports
        # TODO: Export reports

        raise NotImplementedError
