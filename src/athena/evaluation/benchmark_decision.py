"""
Benchmark decision models.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BenchmarkDecisionStatus(str, Enum):
    """Benchmark release decision."""

    PASS = "pass"
    WARNING = "warning"
    BLOCK = "block"


@dataclass(slots=True, frozen=True)
class BenchmarkDecision:
    """Result of benchmark evaluation."""

    status: BenchmarkDecisionStatus

    reasons: list[str]

    @property
    def allowed_to_freeze(self) -> bool:
        """Return whether release can be frozen."""

        return (
            self.status
            != BenchmarkDecisionStatus.BLOCK
        )

