"""
Benchmark report generators.
"""

from __future__ import annotations

from athena.evaluation.benchmark_models import BenchmarkSummary
from athena.evaluation.benchmark_session import BenchmarkSession


class MarkdownReporter:
    """Generate a Markdown benchmark report."""

    def generate(
        self,
        session: BenchmarkSession,
        summary: BenchmarkSummary,
    ) -> str:

        return f"""# Athena Retrieval Benchmark Report

## Session

| Item | Value |
|------|-------|
| Dataset | {session.dataset_name} |
| Started | {session.started_at} |
| Finished | {session.finished_at} |
| Athena Version | {session.athena_version} |
| Embedding Model | {session.embedding_model} |
| Workspace | {session.workspace_name} |

## Dataset

| Metric | Value |
|--------|------:|
| Questions | {summary.total_questions} |
| Successful | {summary.successful_retrievals} |
| Failed | {summary.failed_retrievals} |

## Retrieval Quality

| Metric | Value |
|--------|------:|
| Top-1 Accuracy | {summary.top1_accuracy:.2%} |
| Top-3 Accuracy | {summary.top3_accuracy:.2%} |
| Top-5 Accuracy | {summary.top5_accuracy:.2%} |
| Mean Reciprocal Rank | {summary.mean_reciprocal_rank:.3f} |

## Performance

| Metric | Value |
|--------|------:|
| Average Latency | {summary.average_latency_ms:.2f} ms |
| Median Latency | {summary.median_latency_ms:.2f} ms |
| Fastest | {summary.fastest_latency_ms:.2f} ms |
| Slowest | {summary.slowest_latency_ms:.2f} ms |
"""

