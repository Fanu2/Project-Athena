"""
Document indexing application service.

Flow:

File
 ↓
Document Registration
 ↓
Extractor
 ↓
ExtractedDocument
 ↓
Chunking
 ↓
Attach Athena Document ID
 ↓
Chunk Repository
 ↓
Embedding Pipeline
 ↓
Embedding Repository
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from uuid import uuid4

from athena.ai.embeddings.pipeline import (
    EmbeddingPipeline,
)
from athena.ai.embeddings.repository import (
    EmbeddingRepository,
)
from athena.ai.embeddings.service import (
    EmbeddingService,
)
from athena.domain import Document
from athena.indexing.chunking import (
    ChunkingService,
)
from athena.indexing.extractors.factory import (
    ExtractorFactory,
)
from athena.indexing.models import DocumentChunk
from athena.indexing.repositories.sqlite import (
    SQLiteChunkRepository,
)
from athena.infrastructure.database.initializer import (
    initialize_database,
)
from athena.infrastructure.database.repositories.sqlite_document_repository import (
    SqliteDocumentRepository,
)
from athena.infrastructure.database.session import (
    SessionFactory,
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
    # Initialize Athena database
    #

    initialize_database()

    #
    # Register document
    #

    with SessionFactory() as session:

        repository = SqliteDocumentRepository(
            session,
        )

        document = repository.get_by_path(
            str(file_path),
        )

        if document is None:

            document = Document(
                id=uuid4(),
                filename=file_path.name,
                title=file_path.stem,
                file_path=file_path,
                file_type=file_path.suffix.lower(),
                file_size=file_path.stat().st_size,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            repository.add(
                document,
            )

    #
    # Extract document
    #

    extractor = ExtractorFactory.get_extractor(
        file_path,
    )

    extracted_document = extractor.extract(
        file_path,
    )

    #
    # Chunk document
    #

    chunking_service = ChunkingService()

    chunks = chunking_service.chunk_document(
        extracted_document,
    )

    if not chunks:
        return 0

    #
    # Attach Athena document identity
    #

    chunks = [
        DocumentChunk(
            chunk_id=chunk.chunk_id,
            document_id=str(document.id),
            chunk_index=chunk.chunk_index,
            page_number=chunk.page_number,
            start_offset=chunk.start_offset,
            end_offset=chunk.end_offset,
            text=chunk.text,
        )
        for chunk in chunks
    ]

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