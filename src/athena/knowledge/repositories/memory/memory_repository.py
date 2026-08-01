"""
Athena Memory Knowledge Repository

In-memory persistence implementation.
"""

from typing import Dict, List
from uuid import UUID

from athena.knowledge.acquisition.domain.knowledge_object import (
    KnowledgeObject,
)

from ..knowledge_repository import (
    KnowledgeRepository,
)


class MemoryKnowledgeRepository(
    KnowledgeRepository
):
    """
    Stores KnowledgeObjects in memory.

    Used for:
        - tests
        - development
        - repository validation
    """

    def __init__(self) -> None:

        self._objects: Dict[
            UUID,
            KnowledgeObject,
        ] = {}

    def save(
        self,
        knowledge_object: KnowledgeObject,
    ) -> None:
        """
        Save knowledge object.
        """

        self._objects[
            knowledge_object.object_id
        ] = knowledge_object

    def get(
        self,
        object_id: UUID,
    ) -> KnowledgeObject | None:
        """
        Retrieve object.
        """

        return self._objects.get(
            object_id
        )

    def list_all(
        self,
    ) -> List[KnowledgeObject]:
        """
        Return all objects.
        """

        return list(
            self._objects.values()
        )

    def find_by_type(
        self,
        object_type: str,
    ) -> List[KnowledgeObject]:
        """
        Find objects by type.
        """

        return [
            obj
            for obj in self._objects.values()
            if obj.object_type
            == object_type
        ]