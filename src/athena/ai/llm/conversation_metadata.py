"""
Conversation metadata model.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ConversationMetadata:
    """Metadata extracted from conversation."""

    title: str = ""

    summary: str = ""

    topics: list[str] = field(
        default_factory=list
    )

    tags: list[str] = field(
        default_factory=list
    )

    message_count: int = 0

    model: str | None = None
