"""
In-memory assistant session store.
"""

from __future__ import annotations

from .session import (
    AssistantSession,
)

from .session_store import (
    AssistantSessionStore,
)


class InMemoryAssistantSessionStore(
    AssistantSessionStore,
):
    """
    Simple in-memory session storage.
    """

    def __init__(
        self,
    ) -> None:

        self._sessions: dict[
            str,
            AssistantSession,
        ] = {}


    def save(
        self,
        session: AssistantSession,
    ) -> None:
        """
        Save or update session.
        """

        self._sessions[
            session.session_id
        ] = session


    def get(
        self,
        session_id: str,
    ) -> AssistantSession | None:
        """
        Retrieve session.
        """

        return self._sessions.get(
            session_id,
        )


    def delete(
        self,
        session_id: str,
    ) -> None:
        """
        Delete session.
        """

        self._sessions.pop(
            session_id,
            None,
        )


    def list_sessions(
        self,
    ) -> tuple[
        AssistantSession,
        ...
    ]:
        """
        Return all stored sessions.
        """

        return tuple(
            self._sessions.values(),
        )
