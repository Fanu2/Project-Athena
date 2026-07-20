"""
Document version repository interface.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from uuid import UUID

from athena.domain.document_version import DocumentVersion


class DocumentVersionRepository(ABC):
    """Repository interface for document versions."""

    @abstractmethod
    def add(
        self,
        version: DocumentVersion,
    ) -> None:
        """Persist a document version."""

    @abstractmethod
    def get(
        self,
        version_id: UUID,
    ) -> DocumentVersion | None:
        """Return a document version by its identifier."""

    @abstractmethod
    def get_latest(
        self,
        document_id: UUID,
    ) -> DocumentVersion | None:
        """Return the latest version of a document."""

    @abstractmethod
    def get_all(
        self,
        document_id: UUID,
    ) -> list[DocumentVersion]:
        """Return all versions of a document."""

    @abstractmethod
    def get_next_version_number(
        self,
        document_id: UUID,
    ) -> int:
        """Return the next version number."""

    @abstractmethod
    def delete(
        self,
        version_id: UUID,
    ) -> None:
        """Delete a document version."""