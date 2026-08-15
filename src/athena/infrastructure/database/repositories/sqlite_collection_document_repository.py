"""
SQLite implementation of collection-document relationships.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from athena.infrastructure.database.models.collection_document_model import (
    CollectionDocumentModel,
)

from athena.repositories.collection_document_repository import (
    CollectionDocumentRepository,
)


class SqliteCollectionDocumentRepository(CollectionDocumentRepository):
    """
    SQLite repository for collection-document links.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def add_document(
        self,
        collection_id: UUID,
        document_id: UUID,
    ) -> None:
        """
        Add a document to a collection.
        """

        link = CollectionDocumentModel(
            collection_id=str(collection_id),
            document_id=str(document_id),
        )

        self._session.add(
            link,
        )

        self._session.commit()

    def remove_document(
        self,
        collection_id: UUID,
        document_id: UUID,
    ) -> None:
        """
        Remove a document from a collection.
        """

        link = (
            self._session
            .query(CollectionDocumentModel)
            .filter(
                CollectionDocumentModel.collection_id
                == str(collection_id),
                CollectionDocumentModel.document_id
                == str(document_id),
            )
            .first()
        )

        if link is not None:
            self._session.delete(link)
            self._session.commit()

    def get_documents(
        self,
        collection_id: UUID,
    ) -> list[UUID]:
        """
        Return document IDs in a collection.
        """

        rows = (
            self._session
            .query(CollectionDocumentModel)
            .filter(
                CollectionDocumentModel.collection_id
                == str(collection_id),
            )
            .all()
        )

        return [
            UUID(row.document_id)
            for row in rows
        ]

    def get_collections(
        self,
        document_id: UUID,
    ) -> list[UUID]:
        """
        Return collection IDs for a document.
        """

        rows = (
            self._session
            .query(CollectionDocumentModel)
            .filter(
                CollectionDocumentModel.document_id
                == str(document_id),
            )
            .all()
        )

        return [
            UUID(row.collection_id)
            for row in rows
        ]
