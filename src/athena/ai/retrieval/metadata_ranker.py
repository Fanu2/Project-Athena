"""
Metadata-aware retrieval ranking.
"""

from __future__ import annotations

from athena.ai.metadata.models import MetadataResult


class MetadataRanker:
    """Convert metadata matches into ranking signals."""

    def score(
        self,
        metadata: MetadataResult | None,
    ) -> float:
        """
        Calculate metadata relevance score.

        Uses the highest confidence metadata match.
        """

        if metadata is None or not metadata.documents:
            return 0.0

        return max(
            document.confidence
            for document in metadata.documents
        )

