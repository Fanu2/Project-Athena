"""
SQLite implementation of the collection repository.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from athena.domain.collection import Collection
from athena.infrastructure.database.models.collection_model import (
    CollectionModel,
)

from athena.repositories.collection_repository import (
    CollectionRepository,
)


class SqliteCollectionRepository(CollectionRepository):
    """
    SQLite-backed repository for collections.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def add(
        self,
        collection: Collection,
    ) -> None:
        model = CollectionModel(
            id=str(collection.id),
            name=collection.name,
            description=collection.description,
            created_at=collection.created_at,
            updated_at=collection.updated_at,
        )

        self._session.add(model)
        self._session.commit()

    def get(
        self,
        collection_id: UUID,
    ) -> Collection | None:

        model = self._session.get(
            CollectionModel,
            str(collection_id),
        )

        if model is None:
            return None

        return self._to_domain(model)

    def get_all(
        self,
    ) -> list[Collection]:

        models = (
            self._session
            .query(CollectionModel)
            .order_by(CollectionModel.name)
            .all()
        )

        return [
            self._to_domain(model)
            for model in models
        ]

    def update(
        self,
        collection: Collection,
    ) -> None:

        model = self._session.get(
            CollectionModel,
            str(collection.id),
        )

        if model is None:
            raise ValueError(
                "Collection not found."
            )

        model.name = collection.name
        model.description = collection.description
        model.updated_at = collection.updated_at

        self._session.commit()

    def delete(
        self,
        collection_id: UUID,
    ) -> None:

        model = self._session.get(
            CollectionModel,
            str(collection_id),
        )

        if model is not None:
            self._session.delete(model)
            self._session.commit()

    @staticmethod
    def _to_domain(
        model: CollectionModel,
    ) -> Collection:

        return Collection(
            id=UUID(model.id),
            name=model.name,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
