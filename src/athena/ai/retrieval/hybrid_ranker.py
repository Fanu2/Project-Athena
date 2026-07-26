"""
Hybrid retrieval ranking.
"""

from __future__ import annotations

from athena.ai.retrieval.models import SemanticResult
from athena.ai.retrieval.ranking import (
    CandidateScorer,
    RankingFeatures,
)


class HybridRanker:
    """Merge and rerank retrieval results."""

    def __init__(
        self,
        scorer: CandidateScorer | None = None,
    ) -> None:
        """Initialize ranker."""

        self._scorer = scorer or CandidateScorer()

    def merge(
        self,
        semantic_results: list[SemanticResult],
        keyword_results: list[SemanticResult],
        limit: int,
    ) -> list[SemanticResult]:
        """Merge candidates and calculate final ranking score."""

        candidates: dict[
            str,
            tuple[SemanticResult, RankingFeatures],
        ] = {}

        for result in semantic_results:
            candidates[result.chunk_id] = (
                result,
                RankingFeatures(
                    semantic_score=result.score,
                ),
            )

        for result in keyword_results:
            existing = candidates.get(
                result.chunk_id,
            )

            if existing is None:
                candidates[result.chunk_id] = (
                    result,
                    RankingFeatures(
                        keyword_score=result.score,
                    ),
                )

            else:
                current_result, features = existing

                candidates[result.chunk_id] = (
                    current_result,
                    RankingFeatures(
                        semantic_score=features.semantic_score,
                        keyword_score=result.score,
                    ),
                )

        ranked: list[SemanticResult] = []

        for result, features in candidates.values():
            final_score = self._scorer.score(
                features,
            )

            ranked.append(
                SemanticResult(
                    chunk_id=result.chunk_id,
                    document_id=result.document_id,
                    document_title=result.document_title,
                    page_number=result.page_number,
                    start_offset=result.start_offset,
                    end_offset=result.end_offset,
                    text=result.text,
                    score=final_score,
                )
            )

        ranked.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        return ranked[:limit]
