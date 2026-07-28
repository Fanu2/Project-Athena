"""
Benchmark comparison engine.
"""

from __future__ import annotations

from dataclasses import dataclass

from athena.evaluation.benchmark_models import BenchmarkSummary


@dataclass(slots=True, frozen=True)
class BenchmarkComparison:
    """Result of comparing two benchmark runs."""

    improved: bool
    degraded: bool
    warnings: list[str]


class BenchmarkComparator:
    """Compare benchmark execution results."""

    ACCURACY_THRESHOLD = 0.05
    LATENCY_THRESHOLD = 0.20

    def compare(
        self,
        previous: BenchmarkSummary,
        current: BenchmarkSummary,
    ) -> BenchmarkComparison:
        """Compare previous and current benchmark results."""

        warnings: list[str] = []

        if current.top5_accuracy < previous.top5_accuracy - self.ACCURACY_THRESHOLD:
            warnings.append(
                "Top-5 accuracy degraded.",
            )

        if current.mean_reciprocal_rank < previous.mean_reciprocal_rank - self.ACCURACY_THRESHOLD:
            warnings.append(
                "MRR degraded.",
            )

        if current.average_latency_ms > previous.average_latency_ms * (1 + self.LATENCY_THRESHOLD):
            warnings.append(
                "Latency increased significantly.",
            )

        return BenchmarkComparison(
            improved=not warnings,
            degraded=bool(warnings),
            warnings=warnings,
        )

