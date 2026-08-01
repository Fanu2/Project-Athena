"""
Athena Knowledge Service

Application service for accessing
persistent knowledge.
"""

from uuid import UUID

from athena.knowledge.acquisition.domain.knowledge_object import (
    KnowledgeObject,
)

from athena.knowledge.repositories.knowledge_repository import (
    KnowledgeRepository,
)


class KnowledgeService:
    """
    Application boundary for knowledge operations.
    """

    def __init__(
        self,
        repository: KnowledgeRepository,
    ) -> None:

        self._repository = repository


    def save(
        self,
        knowledge_object: KnowledgeObject,
    ) -> None:
        """
        Persist knowledge.
        """

        self._repository.save(
            knowledge_object
        )


    def get(
        self,
        object_id: UUID,
    ) -> KnowledgeObject | None:
        """
        Retrieve knowledge by id.
        """

        return self._repository.get(
            object_id
        )


    def list_all(
        self,
    ) -> list[KnowledgeObject]:
        """
        List all knowledge.
        """

        return self._repository.list_all()


    def find_by_type(
        self,
        object_type: str,
    ) -> list[KnowledgeObject]:
        """
        Find knowledge by type.
        """

        return self._repository.find_by_type(
            object_type
        )