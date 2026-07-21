"""
End-to-end RAG pipeline test.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from uuid import UUID

from athena.ai.embeddings.pipeline import EmbeddingPipeline
from athena.ai.embeddings.repository import EmbeddingRepository
from athena.ai.llm import LLMClient
from athena.ai.llm.models import LLMRequest
from athena.ai.llm.models import LLMResponse
from athena.ai.llm.provider import LLMProvider
from athena.ai.prompts import PromptBuilder
from athena.ai.prompts import PromptRequest
from athena.ai.retrieval.service import RetrievalService
from athena.domain import Document
from athena.indexing.models import DocumentChunk
from athena.indexing.repositories.sqlite import SQLiteChunkRepository
from athena.repositories.document_repository import (
    DocumentRepository,
)


class FakeEmbeddingService:
    """Fake embedding service for testing."""

    def embed(
        self,
        text: str,
    ) -> list[float]:
        """Return deterministic vector."""

        if "Athena" in text:
            return [1.0, 0.0, 0.0]

        return [0.0, 1.0, 0.0]


class FakeLLMProvider(LLMProvider):
    """Fake LLM provider."""

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:

        return LLMResponse(
            text="Athena is an offline AI research assistant.",
            model="fake-model",
        )


class FakeDocumentRepository(DocumentRepository):
    """Fake document repository."""

    def __init__(
        self,
        document: Document,
    ) -> None:
        self._document = document

    def get(
        self,
        document_id: UUID,
    ) -> Document | None:

        if document_id == self._document.id:
            return self._document

        return None

    def add(
        self,
        document: Document,
    ) -> None:
        pass

    def get_all(
        self,
    ) -> list[Document]:
        return [self._document]

    def exists(
        self,
        file_path: str,
    ) -> bool:
        return False

    def update(
        self,
        document: Document,
    ) -> None:
        pass

    def delete(
        self,
        document_id: UUID,
    ) -> None:
        pass


def test_complete_rag_pipeline(
    tmp_path: Path,
) -> None:
    """Full retrieval augmented generation workflow."""

    chunk_database = tmp_path / "chunks.db"

    embedding_database = tmp_path / "embeddings.db"

    chunk_repository = SQLiteChunkRepository(
        chunk_database,
    )

    embedding_repository = EmbeddingRepository(
        embedding_database,
    )

    document_id = UUID("11111111-1111-1111-1111-111111111111")

    document = Document(
        id=document_id,
        filename="AthenaGuide.pdf",
        title="Athena Research Guide",
        file_path=Path("AthenaGuide.pdf"),
        file_type="pdf",
        file_size=1000,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    document_repository = FakeDocumentRepository(
        document,
    )

    chunk = DocumentChunk(
        chunk_id="chunk-1",
        document_id=str(document_id),
        chunk_index=0,
        page_number=1,
        start_offset=0,
        end_offset=50,
        text=("Athena is an offline AI research assistant."),
    )

    chunk_repository.save_chunks(
        [chunk],
    )

    pipeline = EmbeddingPipeline(
        FakeEmbeddingService(),
        embedding_repository,
    )

    pipeline.embed_chunks(
        [chunk],
    )

    retrieval = RetrievalService(
        FakeEmbeddingService(),
        embedding_repository,
        chunk_repository,
        document_repository,
    )

    results = retrieval.search_similar(
        "What is Athena?",
    )

    assert len(results) > 0

    assert results[0].document_title == "Athena Research Guide"

    prompt = PromptBuilder.build(
        PromptRequest(
            question="What is Athena?",
            results=results,
            citations=[],
        )
    )

    assert "What is Athena?" in prompt.user

    client = LLMClient(
        FakeLLMProvider(),
    )

    answer = client.generate(
        LLMRequest(
            system_prompt=prompt.system,
            user_prompt=prompt.user,
        )
    )

    assert answer.text == "Athena is an offline AI research assistant."
