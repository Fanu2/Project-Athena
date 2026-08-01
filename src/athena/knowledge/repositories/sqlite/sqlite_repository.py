"""
Athena SQLite Knowledge Repository
"""

from uuid import UUID

from sqlalchemy.orm import Session

from athena.knowledge.acquisition.domain.knowledge_object import (
    KnowledgeObject,
)

from athena.knowledge.repositories.knowledge_repository import (
    KnowledgeRepository,
)

from athena.infrastructure.database.models.knowledge_object_model import (
    KnowledgeObjectModel,
)


class SQLiteKnowledgeRepository(
    KnowledgeRepository
):
    """
    SQLite persistence for Knowledge Objects.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:

        self._session = session


    def save(
        self,
        knowledge_object: KnowledgeObject,
    ) -> None:

        model = KnowledgeObjectModel(
            object_id=str(
                knowledge_object.object_id
            ),
            object_type=(
                knowledge_object.object_type
            ),
            title=knowledge_object.title,
            content=knowledge_object.content,
            metadata_json=(
                knowledge_object.metadata
            ),
            confidence=(
                knowledge_object.confidence
            ),
            created_at=(
                knowledge_object.created_at
            ),
            updated_at=(
                knowledge_object.updated_at
            ),
        )

        self._session.merge(
            model
        )

        self._session.commit()


    def get(
        self,
        object_id: UUID,
    ) -> KnowledgeObject | None:

        model = (
            self._session.query(
                KnowledgeObjectModel
            )
            .filter_by(
                object_id=str(object_id)
            )
            .first()
        )

        if model is None:
            return None

        return KnowledgeObject(
            object_id=UUID(
                model.object_id
            ),
            object_type=(
                model.object_type
            ),
            title=model.title,
            content=model.content,
            metadata=(
                model.metadata_json
            ),
            confidence=(
                model.confidence
            ),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


    def list_all(
        self,
    ) -> list[KnowledgeObject]:

        return []


    def find_by_type(
        self,
        object_type: str,
    ) -> list[KnowledgeObject]:

        return []