"""
Assistant session recovery service.

Restores persisted assistant sessions.
"""

from __future__ import annotations

from .session import (
    AssistantSession,
)

from .session_store import (
    AssistantSessionStore,
)


class AssistantRecoveryService:
    """
    Restores assistant workspace sessions.
    """

    def __init__(
        self,
        session_store: AssistantSessionStore,
    ) -> None:

        self._session_store = session_store


    def restore(
        self,
        session_id: str,
    ) -> AssistantSession | None:
        """
        Restore a persisted session.
        """

        return self._session_store.get(
            session_id,
        )


    def available_sessions(
        self,
    ) -> tuple[
        AssistantSession,
        ...
    ]:
        """
        Return recoverable sessions.
        """

        return self._session_store.list_sessions()
