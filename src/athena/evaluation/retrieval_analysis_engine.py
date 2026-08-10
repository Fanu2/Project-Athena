"""
Project Athena

Retrieval Report Generator.
"""

from __future__ import annotations

from athena.evaluation.retrieval_report import (
    RetrievalCandidate,
    RetrievalReport,
)

from athena.evaluation.score_explanation_engine import (
    ScoreExplanationEngine,
)


class RetrievalAnalysisEngine:
    """Generates Retrieval Intelligence Reports."""

    def __init__(self) -> None:
        self._engine = ScoreExplanationEngine()

    def analyze(
        self,
        *,
        query: str,
        strategy: str,
        latency_ms: float,
        results,
    ) -> RetrievalReport:
        """
        Generate a retrieval report from ranked results.
        """

        candidates: list[RetrievalCandidate] = []

        for result in results:

            semantic_score = getattr(
                result,
                "semantic_score",
                getattr(
                    result,
                    "score",
                    getattr(
                        result,
                        "final_score",
                        0.0,
                    ),
                ),
            )

            candidate = RetrievalCandidate(
                document_id=result.document_id,

                document_name=getattr(
                    result,
                    "document_name",
                    "",
                ),

                title=getattr(
                    result,
                    "document_title",
                    getattr(
                        result,
                        "title",
                        "",
                    ),
                ),

                chunk_id=getattr(
                    result,
                    "chunk_id",
                    "",
                ),

                page=getattr(
                    result,
                    "page_number",
                    getattr(
                        result,
                        "page",
                        0,
                    ),
                ),

                final_score=getattr(
                    result,
                    "score",
                    getattr(
                        result,
                        "final_score",
                        0.0,
                    ),
                ),

                semantic_score=semantic_score,

                keyword_score=getattr(
                    result,
                    "keyword_score",
                    0.0,
                ),

                metadata_score=getattr(
                    result,
                    "metadata_score",
                    0.0,
                ),

                identity_score=getattr(
                    result,
                    "identity_score",
                    0.0,
                ),

                document_authority_score=getattr(
                    result,
                    "document_authority_score",
                    0.0,
                ),
            )

            candidate.explanation = "\n".join(
                self._engine.explain(
                    candidate,
                )
            )

            candidates.append(
                candidate,
            )

        return RetrievalReport(
            query=query,
            strategy=strategy,
            latency_ms=latency_ms,
            candidate_count=len(candidates),
            results=candidates,
        )
