"""
Application service for semantic search.
"""

from __future__ import annotations

from athena.ai.search.models import SearchResult
from athena.ai.search.service import SearchService


class SemanticSearchService:
    """Application-level semantic search."""

    def __init__(
        self,
        search_service: SearchService,
    ) -> None:
        self._search_service = search_service

    def search(
        self,
        query: str,
        limit: int = 10,
    ) -> list[SearchResult]:
        """Search indexed documents."""

        return self._search_service.search(
            query=query,
            limit=limit,
        )