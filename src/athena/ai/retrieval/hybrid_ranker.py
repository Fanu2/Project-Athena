"""
Hybrid retrieval ranking.
"""

from __future__ import annotations

from athena.ai.metadata.models import MetadataResult

from athena.ai.retrieval.document_authority_ranker import (
    DocumentAuthorityRanker,
)

from athena.ai.retrieval.identity_ranker import (
    IdentityRanker,
)

from athena.ai.retrieval.metadata_ranker import (
    MetadataRanker,
)

from athena.ai.retrieval.models import (
    SemanticResult,
)

from athena.ai.retrieval.ranking import (
    CandidateScorer,
    RankingFeatures,
)


class HybridRanker:
    """Merge and rerank retrieval results."""

    def __init__(
        self,
        scorer: CandidateScorer | None = None,
        metadata_ranker: MetadataRanker | None = None,
        identity_ranker: IdentityRanker | None = None,
        document_authority_ranker: DocumentAuthorityRanker | None = None,
    ) -> None:
        """Initialize ranker."""

        self._scorer = (
            scorer
            or CandidateScorer()
        )

        self._metadata_ranker = (
            metadata_ranker
            or MetadataRanker()
        )

        self._identity_ranker = (
            identity_ranker
            or IdentityRanker()
        )

        self._document_authority_ranker = (
            document_authority_ranker
            or DocumentAuthorityRanker()
        )

    def merge(
        self,
        semantic_results: list[SemanticResult],
        keyword_results: list[SemanticResult],
        limit: int,
        metadata: MetadataResult | None = None,
        query: str = "",
    ) -> list[SemanticResult]:
        """
        Merge candidates and rerank.
        """

        candidates: dict[str, SemanticResult] = {}

        for result in semantic_results:
            candidates[result.chunk_id] = result

        for result in keyword_results:
            if result.chunk_id not in candidates:
                candidates[result.chunk_id] = result

        ranked: list[SemanticResult] = []

        for result in candidates.values():

            #
            # Preserve keyword evidence already
            # attached to the candidate.
            #

            keyword_score = getattr(
                result,
                "keyword_score",
                0.0,
            )

            #
            # Fallback lookup for keyword-only
            # candidates.
            #

            if keyword_score == 0.0:

                for keyword_result in keyword_results:

                    if (
                        keyword_result.chunk_id
                        == result.chunk_id
                    ):
                        keyword_score = (
                            keyword_result.score
                        )
                        break

            metadata_score = (
                self._metadata_score(
                    metadata,
                    result,
                )
            )

            identity_score = (
                self._identity_ranker.score(
                    query,
                    result.document_name,
                    result.document_title,
                )
            )

            document_authority_score = (
                self._document_authority_ranker.score(
                    result.document_name,
                )
            )

            final_score = self._scorer.score(
                RankingFeatures(
                    semantic_score=result.score,
                    keyword_score=keyword_score,
                    metadata_score=metadata_score,
                    identity_score=identity_score,
                    document_authority_score=(
                        document_authority_score
                    ),
                ),
            )

            ranked.append(
                SemanticResult(
                    chunk_id=result.chunk_id,
                    document_id=result.document_id,
                    document_name=result.document_name,
                    document_title=result.document_title,
                    document_path=result.document_path,
                    page_number=result.page_number,
                    start_offset=result.start_offset,
                    end_offset=result.end_offset,
                    text=result.text,
                    score=final_score,

                    semantic_score=result.score,

                    keyword_score=keyword_score,

                    metadata_score=metadata_score,

                    identity_score=identity_score,

                    document_authority_score=(
                        document_authority_score
                    ),
                )
            )

        ranked.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        return ranked[:limit]

    def _metadata_score(
        self,
        metadata: MetadataResult | None,
        result: SemanticResult,
    ) -> float:
        """
        Calculate metadata score.
        """

        if metadata is None:
            return 0.0

        for document in metadata.documents:

            if (
                document.document_id
                == result.document_id
                or document.title
                == result.document_title
            ):
                return document.confidence

        return 0.0
