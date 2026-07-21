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

from athena.indexing.repositories.sqlite_document import (
    SQLiteDocumentRepository,
)

from athena.infrastructure.database.repositories.sqlite_document_repository import (
    SqliteDocumentRepository,
)

from athena.services.document_indexing_adapter import (
    DocumentIndexingAdapter,
)


class IndexingService:
    """High-level document indexing service."""

    def __init__(
        self,
        repository: ChunkRepository,
        index_repository: SQLiteDocumentRepository | None = None,
        document_library_repository: SqliteDocumentRepository | None = None,
        embedding_service: EmbeddingService | None = None,
        embedding_repository: EmbeddingRepository | None = None,
        chunking_service: ChunkingService | None = None,
    ) -> None:
        """Initialize indexing service."""

        self._repository = repository

        #
        # Legacy indexing metadata repository
        #

        self._index_repository = index_repository

        #
        # User-facing document library repository
        #

        self._document_adapter = (
            DocumentIndexingAdapter(
                document_library_repository,
            )
            if document_library_repository is not None
            else None
        )

        self._embedding_service = embedding_service

        self._embedding_repository = embedding_repository

        self._chunking = chunking_service if chunking_service is not None else ChunkingService()

    def extract_document(
        self,
        document: Path,
    ) -> ExtractedDocument:
        """Extract text from document."""

        extractor = ExtractorFactory.get_extractor(
            document,
        )

        return extractor.extract(
            document,
        )

    def chunk_document(
        self,
        document: ExtractedDocument,
        document_id: str | None = None,
    ) -> list[DocumentChunk]:
        """Create searchable chunks."""

        return self._chunking.chunk_document(
            document,
            document_id=document_id,
        )

    def index_document(
        self,
        document: Path,
    ) -> list[DocumentChunk]:
        """Extract, chunk, store and embed document."""

        document_hash = sha256_file(
            document,
        )

        #
        # Duplicate protection
        #

        if self._index_repository is not None and self._index_repository.exists_by_hash(
            document_hash,
        ):
            return []

        #
        # Extract
        #

        extracted = self.extract_document(
            document,
        )

        #
        # Register in Athena document library
        #

        registered_document = None

        if self._document_adapter is not None:
            registered_document = self._document_adapter.register(
                document,
            )

        document_id = (
            str(registered_document.id)
            if registered_document is not None
            else extracted.document_id
        )

        #
        # Chunk
        #

        chunks = self.chunk_document(
            extracted,
            document_id=document_id,
        )

        #
        # Store chunks
        #

        self._repository.delete_chunks(
            document_id,
        )

        self._repository.save_chunks(
            chunks,
        )

        #
        # Save legacy indexing metadata
        #

        if self._index_repository is not None:

            self._index_repository.save_document(
                IndexedDocument(
                    document_id=document_id,
                    path=extracted.path,
                    title=extracted.title,
                    sha256=document_hash,
                    page_count=extracted.page_count,
                    indexed_at=datetime.now(),
                )
            )

        #
        # Generate embeddings
        #

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
