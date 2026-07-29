"""
Conversation manager.
"""

from __future__ import annotations

from athena.ai.llm.conversation import Conversation
from athena.ai.llm.conversation_store import ConversationStore
from athena.ai.llm.session import LLMSession
from athena.ai.llm.session_manager import SessionManager


class ConversationManager:
    """Manage persistent conversations."""

    def __init__(
        self,
        store: ConversationStore,
        sessions: SessionManager | None = None,
    ) -> None:
        """Initialize manager."""

        self._store = store

        self._sessions = (
            sessions
            if sessions is not None
            else SessionManager()
        )

    def create(
        self,
        title: str = "",
    ) -> Conversation:
        """Create and persist conversation."""

        conversation = Conversation(
            title=title,
        )

        self._store.save(
            conversation
        )

        return conversation

    def get(
        self,
        conversation_id: str,
    ) -> Conversation:
        """Retrieve conversation."""

        return self._store.get(
            conversation_id
        )

    def open_session(
        self,
        conversation_id: str,
    ) -> LLMSession:
        """Open conversation as session."""

        conversation = self.get(
            conversation_id
        )

        session = self._sessions.create()

        for message in conversation.history():
            session.add_message(
                message
            )

        return session

    def save_session(
        self,
        conversation: Conversation,
        session: LLMSession,
    ) -> None:
        """Persist session messages."""

        conversation.messages = (
            session.history()
        )

        self._store.save(
            conversation
        )
