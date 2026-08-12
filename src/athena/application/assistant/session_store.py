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
    Storage interface for assistant sessions.
    """

    @abstractmethod
    def save(
        self,
        session: AssistantSession,
    ) -> None:
        """
        Store assistant session.
        """

        raise NotImplementedError


    @abstractmethod
    def get(
        self,
        session_id: str,
    ) -> AssistantSession | None:
        """
        Retrieve assistant session.
        """

        raise NotImplementedError
