"""
Retrieval candidate ranking model.
"""

from __future__ import annotations

from dataclasses import dataclass

from athena.ai.retrieval.ranking_profiles import (
    DEFAULT_RANKING_PROFILE,
    RankingProfile,
)


@dataclass(slots=True, frozen=True)
class RankingFeatures:
    """Signals used for ranking."""

    semantic_score: float = 0.0

    keyword_score: float = 0.0

    metadata_score: float = 0.0

    identity_score: float = 0.0

    document_authority_score: float = 0.0


class CandidateScorer:
    """Combine retrieval signals into final score."""

    def __init__(
        self,
        profile: RankingProfile = DEFAULT_RANKING_PROFILE,
        semantic_weight: float | None = None,
        keyword_weight: float | None = None,
        metadata_weight: float | None = None,
        identity_weight: float | None = None,
        document_authority_weight: float | None = None,
    ) -> None:

        self._semantic_weight = (
            semantic_weight
            if semantic_weight is not None
            else profile.semantic_weight
        )

        self._keyword_weight = (
            keyword_weight
            if keyword_weight is not None
            else profile.keyword_weight
        )

        self._metadata_weight = (
            metadata_weight
            if metadata_weight is not None
            else profile.metadata_weight
        )

        self._identity_weight = (
            identity_weight
            if identity_weight is not None
            else profile.identity_weight
        )

        self._document_authority_weight = (
            document_authority_weight
            if document_authority_weight is not None
            else profile.document_authority_weight
        )

    def score(
        self,
        features: RankingFeatures,
    ) -> float:
        """Calculate final ranking score."""

        return (
            features.semantic_score
            * self._semantic_weight
            +
            features.keyword_score
            * self._keyword_weight
            +
            features.metadata_score
            * self._metadata_weight
            +
            features.identity_score
            * self._identity_weight
            +
            features.document_authority_score
            * self._document_authority_weight
        )