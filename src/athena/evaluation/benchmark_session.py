"""
Benchmark session model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from athena.evaluation.benchmark_models import BenchmarkRun


@dataclass(slots=True)
class BenchmarkSession:
    """Represents one benchmark execution."""

    session_id: UUID = field(default_factory=uuid4)

    dataset_name: str = ""

    dataset_version: str = "1.0"

    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    finished_at: datetime | None = None

    athena_version: str = ""

    embedding_model: str = ""

    workspace_name: str = ""

    runs: list[BenchmarkRun] = field(default_factory=list)

    @property
    def total_questions(self) -> int:
        """Return the number of benchmark runs."""
        return len(self.runs)

    @property
    def duration_ms(self) -> float:
        """Return total benchmark duration."""
        if self.finished_at is None:
            return 0.0

        return (self.finished_at - self.started_at).total_seconds() * 1000.0

