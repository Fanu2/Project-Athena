"""
Conversation message model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from athena.domain.ai.role import Role


@dataclass(slots=True)
class Message:
    """A single conversation message."""

    role: Role

    text: str

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )
