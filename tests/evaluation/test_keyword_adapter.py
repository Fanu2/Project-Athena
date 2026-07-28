"""
Tests for keyword retrieval adapter.
"""

from athena.ai.retrieval.keyword_adapter import (
    KeywordAdapter,
)
from athena.indexing.models import (
    DocumentChunk,
)


def create_chunk(
    chunk_id: str,
    text: str,
) -> DocumentChunk:
    """Create test document chunk."""

    return DocumentChunk(
        chunk_id=chunk_id,
        document_id="doc-001",
        chunk_index=0,
        page_number=1,
        start_offset=0,
        end_offset=len(text),
        text=text,
        heading="Test Document",
    )


def test_keyword_adapter_converts_chunks() -> None:
    """Adapter should convert chunks into SemanticResult."""

    adapter = KeywordAdapter()

    chunks = [
        create_chunk(
            "chunk-001",
            "Athena retrieval architecture",
        ),
    ]

    results = adapter.convert(
        chunks,
        "Athena retrieval",
    )

    assert len(results) == 1

    result = results[0]

    assert result.chunk_id == "chunk-001"
    assert result.document_id == "doc-001"
    assert result.text == (
        "Athena retrieval architecture"
    )


def test_keyword_adapter_calculates_score() -> None:
    """Matching terms should produce score."""

    adapter = KeywordAdapter()

    chunks = [
        create_chunk(
            "chunk-001",
            "Athena retrieval architecture",
        ),
    ]

    results = adapter.convert(
        chunks,
        "Athena retrieval",
    )

    assert results[0].score == 1.0


def test_keyword_adapter_sorts_by_score() -> None:
    """Higher keyword matches should rank first."""

    adapter = KeywordAdapter()

    chunks = [
        create_chunk(
            "chunk-low",
            "Athena document",
        ),
        create_chunk(
            "chunk-high",
            "Athena retrieval architecture system",
        ),
    ]

    results = adapter.convert(
        chunks,
        "Athena retrieval system",
    )

    assert results[0].chunk_id == "chunk-high"
    assert (
        results[0].score
        >
        results[1].score
    )

