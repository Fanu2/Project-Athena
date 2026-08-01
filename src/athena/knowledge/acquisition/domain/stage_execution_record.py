"""
Athena Stage Execution Record

Tracks execution information for compiler stages.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class StageExecutionRecord:
    """
    Records one pipeline stage execution.
    """

    stage_name: str

    status: str = "success"

    started_at: datetime = field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )

    completed_at: datetime | None = None

    input_type: str | None = None

    output_type: str | None = None

    error: str | None = None