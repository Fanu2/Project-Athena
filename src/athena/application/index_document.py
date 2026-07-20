"""
Document indexing application service.

Flow:

File
 ↓
Extractor
 ↓
ExtractedDocument
 ↓
Chunking
 ↓
Chunk Repository
 ↓
Embedding Pipeline
 ↓
Embedding Repository
"""

from __future__ import annotations

from pathlib import Path

from athena.ai.embeddings.pipeline import (
    EmbeddingPipeline,
)
from athena.ai.embeddings.repository import (
    EmbeddingRepository,
)
from athena.ai.embeddings.service import (
    EmbeddingService,
)
from athena.indexing.chunking import (
    ChunkingService,
)
from athena.indexing.extractors.factory import (
    ExtractorFactory,
)
from athena.indexing.repositories.sqlite import (
    SQLiteChunkRepository,
)


def index_document(
    file_path: Path,
    chunk_database: Path,
    embedding_database: Path,
) -> int:
    """
    Extract, chunk, and index a document.

    Returns
    -------
    int
        Number of chunks created.
    """

    #
    # Extract document
    #

    extractor = ExtractorFactory.get_extractor(
        file_path,
    )

    document = extractor.extract(
        file_path,
    )

    #
    # Chunk document
    #

    chunking_service = ChunkingService()

    chunks = chunking_service.chunk_document(
        document,
    )

    if not chunks:
        return 0

    #
    # Store chunks
    #

    chunk_repository = SQLiteChunkRepository(
        chunk_database,
    )

    chunk_repository.save_chunks(
        chunks,
    )

    #
    # Generate embeddings
    #

    embedding_repository = EmbeddingRepository(
        embedding_database,
    )

    embedding_service = EmbeddingService()

    embedding_pipeline = EmbeddingPipeline(
        embedding_service,
        embedding_repository,
    )

    embedding_pipeline.embed_chunks(
        chunks,
    )

    return len(chunks)