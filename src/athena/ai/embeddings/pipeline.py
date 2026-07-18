"""
Embedding pipeline.

Coordinates embedding generation and storage.
"""

from __future__ import annotations

from datetime import datetime

from athena.ai.embeddings.models import EmbeddingRecord
from athena.ai.embeddings.repository import EmbeddingRepository
from athena.ai.embeddings.service import EmbeddingService
from athena.indexing.models import DocumentChunk


class EmbeddingPipeline:
    """Generate and store document embeddings."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        repository: EmbeddingRepository,
    ) -> None:
        """Initialize pipeline."""

        self._service = embedding_service

        self._repository = repository

    def embed_chunk(
        self,
        chunk: DocumentChunk,
    ) -> None:
        """Create embedding for a chunk."""

        if self._repository.exists(
            chunk.chunk_id,
        ):
            return

        vector = self._service.embed(
            chunk.text,
        )

        embedding = EmbeddingRecord(
            chunk_id=chunk.chunk_id,
            model_name="BAAI/bge-m3",
            vector=vector,
            created=datetime.now(),
        )

        self._repository.save(
            embedding,
        )

    def embed_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> None:
        """Create embeddings for multiple chunks."""

        for chunk in chunks:
            self.embed_chunk(
                chunk,
            )
