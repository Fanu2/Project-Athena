"""
Benchmark history storage.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from athena.evaluation.benchmark_models import BenchmarkSummary


class BenchmarkHistoryStore:
    """Stores benchmark execution history."""

    def __init__(
        self,
        history_directory: Path | str = "benchmarks/history",
    ) -> None:
        self._directory = Path(history_directory)

        self._directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(
        self,
        suite_name: str,
        summary: BenchmarkSummary,
    ) -> Path:
        """Save a benchmark summary."""

        timestamp = datetime.now(
            UTC,
        ).strftime(
            "%Y%m%d_%H%M%S",
        )

        path = self._directory / f"{timestamp}.json"

        data = {
            "timestamp": datetime.now(UTC).isoformat(),
            "suite": suite_name,
            "total_questions": summary.total_questions,
            "successful_retrievals": summary.successful_retrievals,
            "failed_retrievals": summary.failed_retrievals,
            "top1_accuracy": summary.top1_accuracy,
            "top3_accuracy": summary.top3_accuracy,
            "top5_accuracy": summary.top5_accuracy,
            "mean_reciprocal_rank": summary.mean_reciprocal_rank,
            "average_latency_ms": summary.average_latency_ms,
        }

        path.write_text(
            json.dumps(
                data,
                indent=4,
            ),
            encoding="utf-8",
        )

        return path

    def list_history(self) -> list[Path]:
        """Return saved benchmark runs."""

        return sorted(
            self._directory.glob("*.json"),
        )
