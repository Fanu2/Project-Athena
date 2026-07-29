"""
LLM message model.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class Message:
    """A single conversation message."""

    role: str

    content: str

    timestamp: datetime | None = None

    def __post_init__(self) -> None:
        """Set timestamp when missing."""

        if self.timestamp is None:
            object.__setattr__(
                self,
                "timestamp",
                datetime.now(timezone.utc),
            )
