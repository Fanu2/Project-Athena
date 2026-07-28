"""
Tests for hybrid retrieval ranking.
"""

import pytest

from athena.ai.retrieval.hybrid_ranker import (
    HybridRanker,
)
from athena.ai.retrieval.models import (
    SemanticResult,
)


def create_result(
    chunk_id: str,
    score: float,
) -> SemanticResult:
    """Create retrieval result."""

    return SemanticResult(
        chunk_id=chunk_id,
        document_id="doc-001",
        document_title="Athena Guide",
        page_number=1,
        start_offset=0,
        end_offset=100,
        text="Athena retrieval content",
        score=score,
    )


def test_hybrid_ranker_removes_duplicates() -> None:
    """Duplicate chunks should be merged."""

    ranker = HybridRanker()

    results = ranker.merge(
        [
            create_result("chunk-1", 0.8),
        ],
        [
            create_result("chunk-1", 0.6),
        ],
        5,
    )

    assert len(results) == 1


def test_hybrid_ranker_combines_scores() -> None:
    """Duplicate candidates should use reranking score."""

    ranker = HybridRanker()

    results = ranker.merge(
        [
            create_result("chunk-1", 0.5),
        ],
        [
            create_result("chunk-1", 0.9),
        ],
        5,
    )

    assert results[0].score == pytest.approx(0.605)


def test_hybrid_ranker_respects_limit() -> None:
    """Result count should respect limit."""

    ranker = HybridRanker()

    results = ranker.merge(
        [
            create_result("chunk-1", 0.9),
            create_result("chunk-2", 0.8),
        ],
        [],
        1,
    )

    assert len(results) == 1

