"""
Workspace collection service.

Provides high-level collection operations.
"""

from __future__ import annotations

from uuid import UUID

from athena.domain.collection import Collection

from athena.repositories.collection_repository import (
    CollectionRepository,
)

from athena.repositories.collection_document_repository import (
    CollectionDocumentRepository,
)


class CollectionService:
    """
    Business logic for workspace collections.
    """

    def __init__(
        self,
        repository: CollectionRepository,
        document_repository: CollectionDocumentRepository,
    ) -> None:
        self._repository = repository
        self._document_repository = document_repository

    def create_collection(
        self,
        name: str,
        description: str = "",
    ) -> Collection:
        """
        Create a new collection.
        """

        collection = Collection(
            name=name,
            description=description,
        )

        self._repository.add(
            collection,
        )

        return collection

    def list_collections(
        self,
    ) -> list[Collection]:
        """
        Return all collections.
        """

        return self._repository.get_all()

    def get_collection(
        self,
        collection_id: UUID,
    ) -> Collection | None:
        """
        Return collection by ID.
        """

        return self._repository.get(
            collection_id,
        )

    def delete_collection(
        self,
        collection_id: UUID,
    ) -> None:
        """
        Delete a collection.
        """

        self._repository.delete(
            collection_id,
        )

    def add_document(
        self,
        collection_id: UUID,
        document_id: UUID,
    ) -> None:
        """
        Add document to collection.
        """

        self._document_repository.add_document(
            collection_id,
            document_id,
        )

    def remove_document(
        self,
        collection_id: UUID,
        document_id: UUID,
    ) -> None:
        """
        Remove document from collection.
        """

        self._document_repository.remove_document(
            collection_id,
            document_id,
        )

    def list_documents(
        self,
        collection_id: UUID,
    ) -> list[UUID]:
        """
        Return documents in collection.
        """

        return self._document_repository.get_documents(
            collection_id,
        )

    def list_document_collections(
        self,
        document_id: UUID,
    ) -> list[UUID]:
        """
        Return collections containing document.
        """

        return self._document_repository.get_collections(
            document_id,
        )
