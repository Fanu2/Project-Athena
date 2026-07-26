"""
Tests for metadata-aware ranking.
"""

import pytest

from athena.ai.metadata.models import (
    DocumentReference,
    MetadataResult,
)
from athena.ai.retrieval.metadata_ranker import (
    MetadataRanker,
)


def test_metadata_ranker_returns_zero_without_metadata() -> None:
    """No metadata should produce zero score."""

    ranker = MetadataRanker()

    assert ranker.score(None) == 0.0


def test_metadata_ranker_uses_confidence() -> None:
    """Matching metadata confidence should become score."""

    ranker = MetadataRanker()

    metadata = MetadataResult(
        documents=(
            DocumentReference(
                document_id="doc-1",
                title="Athena Guide",
                confidence=0.85,
            ),
        ),
    )

    assert ranker.score(metadata) == pytest.approx(0.85)


def test_metadata_ranker_uses_highest_match() -> None:
    """Highest confidence match should be selected."""

    ranker = MetadataRanker()

    metadata = MetadataResult(
        documents=(
            DocumentReference(
                document_id="doc-1",
                title="Low Match",
                confidence=0.40,
            ),
            DocumentReference(
                document_id="doc-2",
                title="High Match",
                confidence=0.90,
            ),
        ),
    )

    assert ranker.score(metadata) == pytest.approx(0.90)
