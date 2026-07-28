"""
Tests for retrieval candidate ranking.
"""

import pytest

from athena.ai.retrieval.ranking import (
    CandidateScorer,
    RankingFeatures,
)


def test_semantic_only_score() -> None:
    """Semantic score should be weighted correctly."""

    scorer = CandidateScorer()

    result = scorer.score(
        RankingFeatures(
            semantic_score=1.0,
        )
    )

    assert result == pytest.approx(0.65)


def test_combined_score_calculation() -> None:
    """All ranking signals should contribute."""

    scorer = CandidateScorer()

    result = scorer.score(
        RankingFeatures(
            semantic_score=1.0,
            keyword_score=1.0,
            metadata_score=1.0,
        )
    )

    assert result == pytest.approx(0.90)


def test_custom_weights() -> None:
    """Custom ranking weights should be respected."""

    scorer = CandidateScorer(
        semantic_weight=0.5,
        keyword_weight=0.3,
        metadata_weight=0.2,
    )

    result = scorer.score(
        RankingFeatures(
            semantic_score=0.8,
            keyword_score=0.5,
            metadata_score=1.0,
        )
    )

    expected = (
        (0.8 * 0.5)
        +
        (0.5 * 0.3)
        +
        (1.0 * 0.2)
    )

    assert result == pytest.approx(expected)

