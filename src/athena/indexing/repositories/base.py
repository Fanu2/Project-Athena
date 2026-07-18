"""
Chunk repository interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from athena.indexing.models import DocumentChunk


class ChunkRepository(ABC):
    """Abstract repository for document chunks."""

    @abstractmethod
    def save_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> None:
        """
        Save document chunks.

        Parameters
        ----------
        chunks:
            Chunks to be stored.
        """

    @abstractmethod
    def load_chunks(
        self,
        document_id: str,
    ) -> list[DocumentChunk]:
        """
        Load all chunks belonging to a document.

        Parameters
        ----------
        document_id:
            Unique document identifier.

        Returns
        -------
        list[DocumentChunk]
            Document chunks in their original order.
        """

    @abstractmethod
    def delete_chunks(
        self,
        document_id: str,
    ) -> None:
        """
        Delete all chunks belonging to a document.

        Parameters
        ----------
        document_id:
            Unique document identifier.
        """

    @abstractmethod
    def search_chunks(
        self,
        query: str,
        limit: int = 20,
    ) -> list[DocumentChunk]:
        """
        Search indexed document chunks.

        Parameters
        ----------
        query:
            Search text.

        limit:
            Maximum number of results to return.

        Returns
        -------
        list[DocumentChunk]
            Matching document chunks.
        """
