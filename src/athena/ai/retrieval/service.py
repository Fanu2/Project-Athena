"""
Semantic retrieval service.
"""

from __future__ import annotations

from uuid import UUID

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
from athena.repositories.document_repository import (
    DocumentRepository,
)
from athena.ai.metadata.models import (
    MetadataResult,
)


class RetrievalService:
    """Retrieve semantically similar chunks."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        embedding_repository: EmbeddingRepository,
        chunk_repository: SQLiteChunkRepository,
        document_repository: DocumentRepository | None = None,
        max_chunks_per_document: int = 2,
    ) -> None:
        """Initialize retrieval service."""

        self._embedding_service = embedding_service

        self._embedding_repository = embedding_repository

        self._chunk_repository = chunk_repository

        self._document_repository = document_repository

        self._similarity = SimilarityCalculator()

        self._max_chunks_per_document = max_chunks_per_document

    def search_similar(
        self,
        query: str,
        limit: int = 5,
        metadata: MetadataResult | None = None,
    ) -> list[SemanticResult]:
        """Find semantically similar chunks."""

        query_vector = self._embedding_service.embed(
            query,
        )

        embeddings = self._embedding_repository.list_all()

        scored: list[tuple] = []

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

        results: list[SemanticResult] = []

        document_counts: dict[str, int] = {}

        for embedding, score in scored:
            chunk = self._chunk_repository.get_chunk(
                embedding.chunk_id,
            )

            if chunk is None:
                continue

            count = document_counts.get(
                chunk.document_id,
                0,
            )

            if count >= self._max_chunks_per_document:
                continue

            document_title = chunk.document_id

            if self._document_repository is not None:
                try:
                    document = self._document_repository.get(
                        UUID(chunk.document_id),
                    )

                    if document is not None:
                        document_title = document.title or document.filename

                except ValueError:
                    pass

            results.append(
                SemanticResult(
                    chunk_id=chunk.chunk_id,
                    document_id=chunk.document_id,
                    document_title=document_title,
                    page_number=chunk.page_number,
                    start_offset=chunk.start_offset,
                    end_offset=chunk.end_offset,
                    text=chunk.text,
                    score=score,
                )
            )

            document_counts[chunk.document_id] = count + 1

            if len(results) >= limit:
                break

        return results
