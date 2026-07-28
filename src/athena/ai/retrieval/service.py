"""
Semantic retrieval service.
"""

from __future__ import annotations

from uuid import UUID
from pathlib import Path

from athena.ai.embeddings.repository import (
    EmbeddingRepository,
)
from athena.ai.embeddings.service import (
    EmbeddingService,
)
from athena.ai.metadata.models import (
    MetadataResult,
)
from athena.ai.retrieval.hybrid_ranker import (
    HybridRanker,
)
from athena.ai.retrieval.keyword_adapter import (
    KeywordAdapter,
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
from athena.retrieval.metadata_filter import MetadataFilter
from athena.retrieval.query_planner import QueryPlanner


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

        self._query_planner = QueryPlanner()

        self._metadata_filter = MetadataFilter()

        self._hybrid_ranker = HybridRanker()

        self._keyword_adapter = KeywordAdapter()

        self._max_chunks_per_document = max_chunks_per_document

    def search_similar(
        self,
        query: str,
        limit: int = 5,
        metadata: MetadataResult | None = None,
    ) -> list[SemanticResult]:
        """Find semantically similar chunks."""

        intent = self._query_planner.parse(query)

        query_vector = self._embedding_service.embed(
            intent.semantic_query,
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

        semantic_results: list[SemanticResult] = []

        for embedding, score in scored:

            chunk = self._chunk_repository.get_chunk(
                embedding.chunk_id,
            )

            if chunk is None:
                continue

            document_name = chunk.document_id

            document_title = chunk.document_id

            if self._document_repository is not None:
                try:
                    document = self._document_repository.get(
                        UUID(chunk.document_id),
                    )

                    if document is not None:
                        document_name = Path(document.filename).name

                        document_title = (
                            document.title
                            or Path(document.filename).name
                        )

                except ValueError:
                    pass

            semantic_results.append(
                SemanticResult(
                    chunk_id=chunk.chunk_id,
                    document_id=chunk.document_id,
                    document_name=document_name,
                    document_title=document_title,
                    page_number=chunk.page_number,
                    start_offset=chunk.start_offset,
                    end_offset=chunk.end_offset,
                    text=chunk.text,
                    score=score,
                )
            )

        semantic_results.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        semantic_results = semantic_results[:limit]

        keyword_chunks = self._chunk_repository.search_chunks(
            query,
            limit=limit * 2,
        )

        keyword_results = self._keyword_adapter.convert(
            keyword_chunks,
            query,
        )

        return self._hybrid_ranker.merge(
            semantic_results,
            keyword_results,
            limit,
            metadata,
            query,
        )

