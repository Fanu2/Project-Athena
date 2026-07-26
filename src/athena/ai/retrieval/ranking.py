"""
Retrieval candidate ranking model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RankingFeatures:
    """Signals used for ranking."""

    semantic_score: float = 0.0

    keyword_score: float = 0.0

    metadata_score: float = 0.0


class CandidateScorer:
    """Combine retrieval signals into final score."""

    def __init__(
        self,
        semantic_weight: float = 0.70,
        keyword_weight: float = 0.20,
        metadata_weight: float = 0.10,
    ) -> None:
        self._semantic_weight = semantic_weight
        self._keyword_weight = keyword_weight
        self._metadata_weight = metadata_weight

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
        )