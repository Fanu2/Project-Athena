"""
Chunking engine.

Coordinates the complete chunking pipeline.
"""

from __future__ import annotations

from athena.indexing.models import (
    DocumentChunk,
    ExtractedDocument,
)

from athena.indexing.chunking.builder import ChunkBuilder
from athena.indexing.chunking.metadata import MetadataBuilder
from athena.indexing.chunking.parser import DocumentParser
from athena.indexing.chunking.splitter import ChunkSplitter


class ChunkingEngine:
    """
    High-level orchestration for the chunking pipeline.

    Pipeline

        ExtractedDocument
                ↓
        DocumentParser
                ↓
        ChunkSplitter
                ↓
        ChunkBuilder
                ↓
        MetadataBuilder
                ↓
        DocumentChunk[]
    """

    def __init__(
        self,
        parser: DocumentParser | None = None,
        splitter: ChunkSplitter | None = None,
        builder: ChunkBuilder | None = None,
        metadata: MetadataBuilder | None = None,
    ) -> None:

        self._parser = parser or DocumentParser()
        self._splitter = splitter or ChunkSplitter()
        self._builder = builder or ChunkBuilder()
        self._metadata = metadata or MetadataBuilder()

    def chunk_document(
        self,
        document: ExtractedDocument,
    ) -> list[DocumentChunk]:
        """
        Execute the complete chunking pipeline.
        """

        #
        # Parse document
        #

        blocks = self._parser.parse(document)

        #
        # Split oversized blocks
        #

        split_blocks = []

        for block in blocks:
            split_blocks.extend(self._splitter.split(block))

        #
        # Build chunk candidates
        #

        candidates = self._builder.build(split_blocks)

        #
        # Build final metadata
        #

        return self._metadata.build(
            document.document_id,
            candidates,
        )
