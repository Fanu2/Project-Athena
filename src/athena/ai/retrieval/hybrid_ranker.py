"""
Hybrid retrieval ranking.
"""

from __future__ import annotations

from athena.ai.retrieval.models import SemanticResult


class HybridRanker:
    """Merge and rank retrieval results."""

    def merge(
        self,
        semantic_results: list[SemanticResult],
        keyword_results: list[SemanticResult],
        limit: int,
    ) -> list[SemanticResult]:
        """
        Merge semantic and keyword results.

        Semantic scores are preserved.
        Duplicate chunks are removed.
        """

        merged: dict[str, SemanticResult] = {}

        for result in semantic_results:
            merged[result.chunk_id] = result

        for result in keyword_results:
            existing = merged.get(result.chunk_id)

            if existing is None or result.score > existing.score:
                merged[result.chunk_id] = result

        ranked = sorted(
            merged.values(),
            key=lambda item: item.score,
            reverse=True,
        )

        return ranked[:limit]
