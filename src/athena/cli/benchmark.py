"""
Athena Benchmark CLI.
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path

from athena.core.application_context import ApplicationContext

from athena.evaluation.benchmark_loader import BenchmarkLoader
from athena.evaluation.benchmark_metrics_engine import (
    BenchmarkMetricsEngine,
)
from athena.evaluation.benchmark_report import (
    MarkdownReporter,
)
from athena.evaluation.benchmark_runner import (
    BenchmarkRunner,
)
from athena.evaluation.benchmark_session import (
    BenchmarkSession,
)


def main() -> None:
    """Benchmark command-line entry point."""

    parser = argparse.ArgumentParser(
        prog="athena-benchmark",
        description="Athena Retrieval Benchmark",
    )

    parser.add_argument(
        "--workspace",
        required=True,
        help="Athena workspace",
    )

    parser.add_argument(
        "--dataset",
        required=True,
        help="Benchmark dataset JSON file",
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Athena Retrieval Benchmark")
    print("=" * 60)

    context = ApplicationContext()

    context.open_workspace(
        Path(args.workspace),
    )

    questions = BenchmarkLoader.load(
        args.dataset,
    )

    runner = BenchmarkRunner(
        context.retrieval_service,
    )

    session = BenchmarkSession(
        dataset_name=Path(args.dataset).name,
        started_at=datetime.now(UTC),
    )

    print(f"Workspace : {args.workspace}")
    print(f"Dataset   : {args.dataset}")
    print(f"Questions : {len(questions)}")
    print()

    for question in questions:
        run = runner.run(question)
        session.runs.append(run)

        print(
            f"[OK] {question.question_id}"
        )

    session.finished_at = datetime.now(UTC)

    metrics = BenchmarkMetricsEngine()

    summary = metrics.summarize(session)

    report = MarkdownReporter().generate(
        session,
        summary,
    )

    output_dir = Path(
        "benchmarks/results",
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_file = (
        output_dir
        / f"{Path(args.dataset).stem}.md"
    )

    report_file.write_text(
        report,
        encoding="utf-8",
    )

    print()
    print("=" * 60)
    print("Benchmark Summary")
    print("=" * 60)

    print(
        f"Questions : {summary.total_questions}"
    )

    print(
        f"Successful : {summary.successful_retrievals}"
    )

    print(
        f"Failed : {summary.failed_retrievals}"
    )

    print(
        f"Average Latency : {summary.average_latency_ms:.2f} ms"
    )

    print()

    print(
        f"Report written to: {report_file}"
    )


if __name__ == "__main__":
    main()
