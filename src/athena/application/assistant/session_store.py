"""
Assistant session storage boundary.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .session import (
    AssistantSession,
)


class AssistantSessionStore(ABC):
    """
    Storage boundary for assistant sessions.
    """

    @abstractmethod
    def save(
        self,
        session: AssistantSession,
    ) -> None:
        """
        Store or update session.
        """

        raise NotImplementedError


    @abstractmethod
    def get(
        self,
        session_id: str,
    ) -> AssistantSession | None:
        """
        Retrieve session.
        """

        raise NotImplementedError


    @abstractmethod
    def delete(
        self,
        session_id: str,
    ) -> None:
        """
        Remove session.
        """

        raise NotImplementedError


    @abstractmethod
    def list_sessions(
        self,
    ) -> tuple[
        AssistantSession,
        ...
    ]:
        """
        Return stored sessions.
        """

        raise NotImplementedError
