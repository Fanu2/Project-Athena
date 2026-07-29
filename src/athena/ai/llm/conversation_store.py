"""
Conversation storage abstraction.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from athena.ai.llm.conversation import Conversation


class ConversationStore(ABC):
    """Abstract conversation persistence."""

    @abstractmethod
    def save(
        self,
        conversation: Conversation,
    ) -> None:
        """Persist conversation."""

    @abstractmethod
    def get(
        self,
        conversation_id: str,
    ) -> Conversation:
        """Retrieve conversation."""

    @abstractmethod
    def exists(
        self,
        conversation_id: str,
    ) -> bool:
        """Check conversation existence."""

    @abstractmethod
    def delete(
        self,
        conversation_id: str,
    ) -> None:
        """Delete conversation."""

    @abstractmethod
    def list_all(self) -> list[Conversation]:
        """List conversations."""
