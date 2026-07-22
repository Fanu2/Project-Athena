"""
Athena RAG demonstration runner.
"""

from __future__ import annotations

from pathlib import Path

from athena.ai.embeddings.repository import (
    EmbeddingRepository,
)
from athena.ai.embeddings.service import (
    EmbeddingService,
)
from athena.ai.llm import (
    LLMClient,
    LLMRequest,
)
from athena.ai.llm.providers import (
    OllamaProvider,
)
from athena.ai.prompts import (
    PromptBuilder,
    PromptRequest,
)
from athena.ai.retrieval.service import (
    RetrievalService,
)
from athena.application.index_document import (
    index_document,
)
from athena.indexing.repositories.sqlite import (
    SQLiteChunkRepository,
)
from athena.infrastructure.database.repositories.sqlite_document_repository import (
    SqliteDocumentRepository,
)
from athena.infrastructure.database.session import (
    SessionFactory,
)


def run_demo(
    file_path: Path,
    question: str,
) -> None:
    """Run Athena document question answering."""

    print("Athena RAG Demo")
    print("-" * 40)

    chunk_database = Path.home() / ".athena" / "chunks.db"

    embedding_database = Path.home() / ".athena" / "embeddings.db"

    print("Indexing document...")

    count = index_document(
        file_path,
        chunk_database,
        embedding_database,
    )

    print(f"Created {count} chunks")

    chunk_repository = SQLiteChunkRepository(
        chunk_database,
    )

    embedding_repository = EmbeddingRepository(
        embedding_database,
    )

    with SessionFactory() as session:
        document_repository = SqliteDocumentRepository(
            session,
        )

        retrieval = RetrievalService(
            EmbeddingService(),
            embedding_repository,
            chunk_repository,
            document_repository,
        )

        print()
        print(f"Question: {question}")

        results = retrieval.search_similar(
            question,
        )

    if not results:
        print("No relevant information found.")
        return

    prompt = PromptBuilder.build(
        PromptRequest(
            question=question,
            results=results,
            citations=[],
        )
    )

    client = LLMClient(
        OllamaProvider(),
    )

    answer = client.generate(
        LLMRequest(
            system_prompt=prompt.system,
            user_prompt=prompt.user,
        )
    )

    print()
    print("ANSWER")
    print("=" * 40)
    print(answer.text)

    print()
    print("SOURCES")
    print("=" * 40)

    for result in results:
        print(f"{result.document_title} | Page {result.page_number} | Score {result.score:.3f}")


if __name__ == "__main__":
    run_demo(
        Path("Athena_Test_Document.pdf"),
        "What is this document about?",
    )
