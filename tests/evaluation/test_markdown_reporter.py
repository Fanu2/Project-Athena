"""
Unit tests for MarkdownReporter.
"""

from __future__ import annotations

from datetime import UTC, datetime

from athena.evaluation.benchmark_models import BenchmarkSummary
from athena.evaluation.benchmark_session import BenchmarkSession
from athena.evaluation.benchmark_report import MarkdownReporter


def test_generate_returns_string():

    reporter = MarkdownReporter()

    session = BenchmarkSession(
        dataset_name="athena_core_v1",
        athena_version="1.0",
        embedding_model="nomic-embed-text",
        workspace_name="Default",
        started_at=datetime.now(UTC),
        finished_at=datetime.now(UTC),
    )

    summary = BenchmarkSummary(
        total_questions=25,
        successful_retrievals=24,
        failed_retrievals=1,
        top1_accuracy=0.96,
        top3_accuracy=1.00,
        top5_accuracy=1.00,
        mean_reciprocal_rank=0.98,
        average_latency_ms=21.5,
        median_latency_ms=20.0,
        fastest_latency_ms=12.0,
        slowest_latency_ms=41.0,
    )

    report = reporter.analyze(session, summary)

    assert isinstance(report, str)


def test_report_contains_title():

    reporter = MarkdownReporter()

    report = reporter.analyze(
        BenchmarkSession(),
        BenchmarkSummary(),
    )

    assert "# Athena Retrieval Benchmark Report" in report


def test_report_contains_dataset():

    reporter = MarkdownReporter()

    report = reporter.analyze(
        BenchmarkSession(dataset_name="athena_core_v1"),
        BenchmarkSummary(),
    )

    assert "athena_core_v1" in report


def test_report_contains_metrics():

    reporter = MarkdownReporter()

    report = reporter.analyze(
        BenchmarkSession(),
        BenchmarkSummary(
            top1_accuracy=0.95,
            average_latency_ms=25.0,
        ),
    )

    assert "95.00%" in report
    assert "25.00 ms" in report

