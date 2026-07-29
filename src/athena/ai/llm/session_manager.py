"""
LLM session manager.
"""

from __future__ import annotations

from athena.ai.llm.session import LLMSession


class SessionManager:
    """Manage LLM sessions."""

    def __init__(self) -> None:
        """Initialize session storage."""

        self._sessions: dict[str, LLMSession] = {}

    def create(
        self,
        model: str | None = None,
        system_prompt: str = "",
    ) -> LLMSession:
        """Create a new session."""

        session = LLMSession(
            model=model,
            system_prompt=system_prompt,
        )

        self._sessions[session.session_id] = session

        return session

    def get(
        self,
        session_id: str,
    ) -> LLMSession:
        """Return existing session."""

        return self._sessions[session_id]

    def exists(
        self,
        session_id: str,
    ) -> bool:
        """Return whether session exists."""

        return session_id in self._sessions

    def sessions(self) -> list[LLMSession]:
        """Return all sessions."""

        return list(self._sessions.values())

    def remove(
        self,
        session_id: str,
    ) -> None:
        """Remove session."""

        del self._sessions[session_id]
