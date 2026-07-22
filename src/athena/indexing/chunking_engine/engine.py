"""
Structure-aware chunking engine.

Coordinates the complete chunking pipeline.

Pipeline:

ExtractedDocument
        │
        ▼
DocumentParser
        ▼
ChunkSplitter
        ▼
ChunkBuilder
        ▼
MetadataBuilder
        ▼
DocumentChunk[]
"""

from __future__ import annotations

from athena.indexing.chunking_engine.builder import ChunkBuilder
from athena.indexing.chunking_engine.metadata import MetadataBuilder
from athena.indexing.chunking_engine.parser import DocumentParser
from athena.indexing.chunking_engine.splitter import ChunkSplitter
from athena.indexing.models import (
    DocumentChunk,
    ExtractedDocument,
)


class ChunkingEngine:
    """
    Orchestrates the structure-aware chunking pipeline.
    """

    def __init__(
        self,
        parser: DocumentParser | None = None,
        splitter: ChunkSplitter | None = None,
        builder: ChunkBuilder | None = None,
        metadata_builder: MetadataBuilder | None = None,
    ) -> None:
        self._parser = parser or DocumentParser()
        self._splitter = splitter or ChunkSplitter()
        self._builder = builder or ChunkBuilder()
        self._metadata_builder = (
            metadata_builder or MetadataBuilder()
        )

    def process(
        self,
        document: ExtractedDocument,
    ) -> list[DocumentChunk]:
        """
        Run the complete structure-aware chunking pipeline.
        """

        blocks = self._parser.parse(document)

        blocks = self._splitter.split(blocks)

        candidates = self._builder.build(blocks)

        return self._metadata_builder.build(
            document=document,
            candidates=candidates,
        )