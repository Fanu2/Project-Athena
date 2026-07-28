"""
Benchmark quality gate models.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class QualityGateStatus(str, Enum):
    """Quality gate outcome."""

    PASS = "pass"
    WARNING = "warning"
    BLOCK = "block"


@dataclass(slots=True, frozen=True)
class QualityGateResult:
    """Final benchmark quality decision."""

    status: QualityGateStatus

    message: str

    checks: list[str]

    @property
    def can_release(self) -> bool:
        """Return whether release is allowed."""

        return self.status != QualityGateStatus.BLOCK

