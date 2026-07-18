from __future__ import annotations

from athena.indexing.models import DocumentChunk
from athena.indexing.repositories.base import ChunkRepository


class SearchService:
    """
    Application service for document search.

    This service validates search requests and delegates
    storage-specific searching to the configured repository.
    """

    def __init__(self, repository: ChunkRepository) -> None:
        self._repository = repository

    def search(
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
            Maximum number of results.

        Returns
        -------
        list[DocumentChunk]
        """
        query = query.strip()

        if not query:
            return []

        return self._repository.search_chunks(
            query=query,
            limit=limit,
        )
