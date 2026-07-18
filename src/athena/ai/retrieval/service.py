"""
Semantic retrieval service.
"""

from __future__ import annotations

from athena.ai.embeddings.repository import (
    EmbeddingRepository,
)
from athena.ai.embeddings.service import (
    EmbeddingService,
)
from athena.ai.retrieval.models import (
    SemanticResult,
)
from athena.ai.retrieval.similarity import (
    SimilarityCalculator,
)
from athena.indexing.repositories.sqlite import (
    SQLiteChunkRepository,
)


class RetrievalService:
    """Retrieve semantically similar chunks."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        embedding_repository: EmbeddingRepository,
        chunk_repository: SQLiteChunkRepository,
    ) -> None:
        """Initialize retrieval service."""

        self._embedding_service = embedding_service

        self._embedding_repository = embedding_repository

        self._chunk_repository = chunk_repository

        self._similarity = SimilarityCalculator()

    def search_similar(
        self,
        query: str,
        limit: int = 5,
    ) -> list[SemanticResult]:
        """Find semantically similar chunks."""

        query_vector = self._embedding_service.embed(
            query,
        )

        results: list[SemanticResult] = []

        embeddings = self._embedding_repository.list_all()

        scored = []

        for embedding in embeddings:
            score = self._similarity.cosine_similarity(
                query_vector,
                embedding.vector,
            )

            scored.append(
                (
                    embedding,
                    score,
                )
            )

        scored.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        for embedding, score in scored[:limit]:
            chunk = self._chunk_repository.get_chunk(
                embedding.chunk_id,
            )

            if chunk is None:
                continue

            results.append(
                SemanticResult(
                    chunk_id=chunk.chunk_id,
                    document_id=chunk.document_id,
                    page_number=chunk.page_number,
                    text=chunk.text,
                    score=score,
                )
            )

        return results
