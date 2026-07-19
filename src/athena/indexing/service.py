"""
Document indexing service.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from athena.ai.embeddings.models import EmbeddingRecord
from athena.ai.embeddings.repository import EmbeddingRepository
from athena.ai.embeddings.service import EmbeddingService
from athena.indexing.chunking import ChunkingService
from athena.indexing.extractors.factory import ExtractorFactory
from athena.indexing.hashing import sha256_file
from athena.indexing.models import (
    DocumentChunk,
    ExtractedDocument,
    IndexedDocument,
)
from athena.indexing.repositories.base import ChunkRepository
from athena.indexing.repositories.document_base import DocumentRepository


class IndexingService:
    """High-level document indexing service."""

    def __init__(
        self,
        repository: ChunkRepository,
        document_repository: DocumentRepository | None = None,
        embedding_service: EmbeddingService | None = None,
        embedding_repository: EmbeddingRepository | None = None,
        chunking_service: ChunkingService | None = None,
    ) -> None:
        """Initialize the indexing service."""

        self._repository = repository

        self._document_repository = document_repository

        self._embedding_service = embedding_service

        self._embedding_repository = embedding_repository

        self._chunking = chunking_service if chunking_service is not None else ChunkingService()

    def extract_document(
        self,
        document: Path,
    ) -> ExtractedDocument:
        """Extract text from a document."""

        extractor = ExtractorFactory.get_extractor(
            document,
        )

        return extractor.extract(
            document,
        )

    def chunk_document(
        self,
        document: ExtractedDocument,
    ) -> list[DocumentChunk]:
        """Split document into chunks."""

        return self._chunking.chunk_document(
            document,
        )

    def index_document(
        self,
        document: Path,
    ) -> list[DocumentChunk]:
        """Extract, chunk and store document data."""

        document_hash = sha256_file(
            document,
        )

        if self._document_repository is not None and self._document_repository.exists_by_hash(
            document_hash,
        ):
            return []

        extracted = self.extract_document(
            document,
        )

        chunks = self.chunk_document(
            extracted,
        )

        self._repository.delete_chunks(
            extracted.document_id,
        )

        self._repository.save_chunks(
            chunks,
        )

        if self._document_repository is not None:
            self._document_repository.save_document(
                IndexedDocument(
                    document_id=extracted.document_id,
                    path=extracted.path,
                    title=extracted.title,
                    sha256=document_hash,
                    page_count=extracted.page_count,
                    indexed_at=datetime.now(),
                )
            )

        if self._embedding_service is not None and self._embedding_repository is not None:
            for chunk in chunks:
                vector = self._embedding_service.embed(
                    chunk.text,
                )

                record = EmbeddingRecord(
                    chunk_id=chunk.chunk_id,
                    model_name="BAAI/bge-m3",
                    vector=vector,
                    created=datetime.now(),
                )

                self._embedding_repository.save(
                    record,
                )

        return chunks
