"""
Athena Compilation Report

Summarizes one Knowledge Compiler execution.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .stage_execution_record import (
    StageExecutionRecord,
)


@dataclass
class CompilationReport:
    """
    Report generated after AKC execution.
    """

    source: Any = None

    status: str = "success"

    stages: list[StageExecutionRecord] = field(
        default_factory=list
    )

    objects_created: int = 0

    started_at: datetime = field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )

    completed_at: datetime | None = None

    error: str | None = None

    def complete(self) -> None:
        """
        Mark compilation complete.
        """

        self.completed_at = (
            datetime.now(timezone.utc)
        )

    @property
    def stage_count(self) -> int:
        """
        Return number of executed stages.
        """

        return len(self.stages)