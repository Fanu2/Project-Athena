"""
Ranking profile resolver.
"""

from __future__ import annotations

from athena.ai.retrieval.ranking_profiles import (
    AUTHORITY_EXPERIMENT_PROFILE,
    DEFAULT_RANKING_PROFILE,
    RankingProfile,
)


class RankingProfileResolver:
    """Resolve ranking profiles by name."""

    def resolve(
        self,
        profile_name: str,
    ) -> RankingProfile:
        """
        Return ranking profile.

        Unknown profiles fall back
        to the default profile.
        """

        profiles = {
            "default": (
                DEFAULT_RANKING_PROFILE
            ),
            "legal_document": (
                AUTHORITY_EXPERIMENT_PROFILE
            ),
            "authority": (
                AUTHORITY_EXPERIMENT_PROFILE
            ),
            "technical": (
                DEFAULT_RANKING_PROFILE
            ),
        }

        return profiles.get(
            profile_name,
            DEFAULT_RANKING_PROFILE,
        )
