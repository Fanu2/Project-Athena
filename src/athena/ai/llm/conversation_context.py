"""
Conversation context model.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ConversationContext:
    """Context assembled for conversation execution."""

    conversation_id: str

    recent_messages: list[str] = field(
        default_factory=list
    )

    summary: str = ""

    retrieved_knowledge: list[str] = field(
        default_factory=list
    )
