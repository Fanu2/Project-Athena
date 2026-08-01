"""
Athena Knowledge Repository Contract

Defines persistence operations for
canonical Knowledge Objects.
"""

from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from athena.knowledge.acquisition.domain.knowledge_object import (
    KnowledgeObject,
)


class KnowledgeRepository(ABC):
    """
    Abstract repository for Knowledge Objects.

    Persistence implementations may use:
        - SQLite
        - memory storage
        - future databases
    """

    @abstractmethod
    def save(
        self,
        knowledge_object: KnowledgeObject,
    ) -> None:
        """
        Persist a knowledge object.
        """

    @abstractmethod
    def get(
        self,
        object_id: UUID,
    ) -> KnowledgeObject | None:
        """
        Retrieve knowledge object by id.
        """

    @abstractmethod
    def list_all(
        self,
    ) -> List[KnowledgeObject]:
        """
        Return all knowledge objects.
        """

    @abstractmethod
    def find_by_type(
        self,
        object_type: str,
    ) -> List[KnowledgeObject]:
        """
        Find objects by type.
        """