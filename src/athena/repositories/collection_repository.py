"""
Collection repository interface.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from uuid import UUID

from athena.domain import Collection


class CollectionRepository(ABC):
    """
    Repository interface for collections.
    """

    @abstractmethod
    def get(
        self,
        collection_id: UUID,
    ) -> Collection | None:
        """Get collection by ID."""

        raise NotImplementedError

    @abstractmethod
    def add(
        self,
        collection: Collection,
    ) -> None:
        """Add collection."""

        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
    ) -> list[Collection]:
        """Return all collections."""

        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        collection: Collection,
    ) -> None:
        """Update collection."""

        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        collection_id: UUID,
    ) -> None:
        """Delete collection."""

        raise NotImplementedError
