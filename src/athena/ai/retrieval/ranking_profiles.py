"""
Ranking profiles for retrieval experiments.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RankingProfile:
    """Weights used by the retrieval candidate scorer."""

    semantic_weight: float
    keyword_weight: float
    metadata_weight: float
    identity_weight: float
    document_authority_weight: float


DEFAULT_RANKING_PROFILE = RankingProfile(
    semantic_weight=0.65,
    keyword_weight=0.20,
    metadata_weight=0.05,
    identity_weight=0.10,
    document_authority_weight=0.0,
)


AUTHORITY_EXPERIMENT_PROFILE = RankingProfile(
    semantic_weight=0.62,
    keyword_weight=0.20,
    metadata_weight=0.05,
    identity_weight=0.08,
    document_authority_weight=0.05,
)
