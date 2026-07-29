"""
LLM session model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from athena.ai.llm.message import Message


@dataclass(slots=True)
class LLMSession:
    """Conversation session."""

    model: str | None = None

    system_prompt: str = ""

    session_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    messages: list[Message] = field(
        default_factory=list
    )

    def add_message(
        self,
        message: Message,
    ) -> None:
        """Append message to session."""

        self.messages.append(message)

    def history(self) -> list[Message]:
        """Return conversation history."""

        return list(self.messages)

    def clear(self) -> None:
        """Clear session messages."""

        self.messages.clear()
