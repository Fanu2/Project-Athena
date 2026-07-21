"""
SQLite implementation of the document repository.
"""

from __future__ import annotations

from pathlib import Path
from uuid import UUID

from sqlalchemy.orm import Session

from athena.domain import Document
from athena.infrastructure.database.models.document_model import DocumentModel
from athena.repositories.document_repository import DocumentRepository


class SqliteDocumentRepository(DocumentRepository):
    """SQLite-backed repository for documents."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(
        self,
        document: Document,
    ) -> None:
        model = DocumentModel(
            id=str(document.id),
            filename=document.filename,
            title=document.title,
            file_path=str(document.file_path),
            file_type=document.file_type,
            file_size=document.file_size,
            created_at=document.created_at,
            updated_at=document.updated_at,
        )

        self._session.add(model)
        self._session.commit()

    def get(
        self,
        document_id: UUID,
    ) -> Document | None:
        model = self._session.get(DocumentModel, str(document_id))

        if model is None:
            return None

        return self._to_domain(model)

    def get_all(
        self,
    ) -> list[Document]:
        models = self._session.query(DocumentModel).order_by(DocumentModel.filename).all()

        return [self._to_domain(model) for model in models]

    def exists(
        self,
        file_path: str,
    ) -> bool:
        return (
            self._session.query(DocumentModel).filter(DocumentModel.file_path == file_path).first()
            is not None
        )

    def get_by_path(
        self,
        file_path: str,
    ) -> Document | None:
        """Find document by file path."""

        model = (
            self._session.query(DocumentModel).filter(DocumentModel.file_path == file_path).first()
        )

        if model is None:
            return None

        return self._to_domain(
            model,
        )

    def update(
        self,
        document: Document,
    ) -> None:
        model = self._session.get(DocumentModel, str(document.id))

        if model is None:
            raise ValueError("Document not found.")

        model.filename = document.filename
        model.title = document.title
        model.file_path = str(document.file_path)
        model.file_type = document.file_type
        model.file_size = document.file_size
        model.updated_at = document.updated_at

        self._session.commit()

    def delete(
        self,
        document_id: UUID,
    ) -> None:
        model = self._session.get(DocumentModel, str(document_id))

        if model is not None:
            self._session.delete(model)
            self._session.commit()

    @staticmethod
    def _to_domain(
        model: DocumentModel,
    ) -> Document:
        return Document(
            id=UUID(model.id),
            filename=model.filename,
            title=model.title,
            file_path=Path(model.file_path),
            file_type=model.file_type,
            file_size=model.file_size,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
