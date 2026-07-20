"""
Checksum repository interface.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from uuid import UUID

from athena.domain.document_checksum import DocumentChecksum


class ChecksumRepository(ABC):
    """Repository interface for document checksums."""

    @abstractmethod
    def exists(
        self,
        checksum: DocumentChecksum,
    ) -> bool:
        """Return True if the checksum already exists."""

    @abstractmethod
    def get_document_id(
        self,
        checksum: DocumentChecksum,
    ) -> UUID | None:
        """Return the document identifier associated with a checksum."""

    @abstractmethod
    def save(
        self,
        checksum: DocumentChecksum,
        document_id: UUID,
    ) -> None:
        """Persist a checksum."""

    @abstractmethod
    def delete(
        self,
        checksum: DocumentChecksum,
    ) -> None:
        """Delete a checksum."""