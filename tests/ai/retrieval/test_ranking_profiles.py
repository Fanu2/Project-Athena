"""
Tests for ranking profiles.
"""

from athena.ai.retrieval.ranking import CandidateScorer
from athena.ai.retrieval.ranking_profiles import (
    DEFAULT_RANKING_PROFILE,
    AUTHORITY_EXPERIMENT_PROFILE,
)


def test_default_profile_weights() -> None:
    """Default profile should preserve baseline ranking."""

    assert DEFAULT_RANKING_PROFILE.semantic_weight == 0.65
    assert DEFAULT_RANKING_PROFILE.keyword_weight == 0.20
    assert DEFAULT_RANKING_PROFILE.metadata_weight == 0.05
    assert DEFAULT_RANKING_PROFILE.identity_weight == 0.10
    assert (
        DEFAULT_RANKING_PROFILE.document_authority_weight
        == 0.0
    )


def test_authority_profile_weights() -> None:
    """Authority profile should enable authority signal."""

    assert AUTHORITY_EXPERIMENT_PROFILE.semantic_weight == 0.62
    assert AUTHORITY_EXPERIMENT_PROFILE.keyword_weight == 0.20
    assert AUTHORITY_EXPERIMENT_PROFILE.metadata_weight == 0.05
    assert AUTHORITY_EXPERIMENT_PROFILE.identity_weight == 0.08
    assert (
        AUTHORITY_EXPERIMENT_PROFILE.document_authority_weight
        == 0.05
    )


def test_candidate_scorer_accepts_profile() -> None:
    """Candidate scorer should accept ranking profiles."""

    from athena.ai.retrieval.ranking import RankingFeatures

    scorer = CandidateScorer(
        profile=AUTHORITY_EXPERIMENT_PROFILE,
    )

    score = scorer.score(
        RankingFeatures(
            semantic_score=1.0,
        )
    )

    assert score == 0.62