"""
Document indexing service.
"""

from __future__ import annotations

from pathlib import Path

from athena.indexing.chunking import ChunkingService
from athena.indexing.extractors.factory import ExtractorFactory
from athena.indexing.models import (
    DocumentChunk,
    ExtractedDocument,
)
from athena.indexing.repositories.base import ChunkRepository


class IndexingService:
    """High-level document indexing service."""

    def __init__(
        self,
        repository: ChunkRepository,
        chunking_service: ChunkingService | None = None,
    ) -> None:
        """Initialize the indexing service."""

        self._repository = repository
        self._chunking = chunking_service if chunking_service is not None else ChunkingService()

    def extract_document(
        self,
        document: Path,
    ) -> ExtractedDocument:
        """
        Extract text from a document.
        """

        extractor = ExtractorFactory.get_extractor(document)
        return extractor.extract(document)

    def chunk_document(
        self,
        document: ExtractedDocument,
    ) -> list[DocumentChunk]:
        """
        Split an extracted document into chunks.
        """

        return self._chunking.chunk_document(document)

    def index_document(
        self,
        document: Path,
    ) -> list[DocumentChunk]:
        """
        Extract, chunk and store a document.
        """

        extracted = self.extract_document(document)

        chunks = self.chunk_document(extracted)

        self._repository.delete_chunks(
            extracted.document_id,
        )

        self._repository.save_chunks(chunks)

        return chunks
