"""
Project Athena

Retrieval Report Generator.
"""

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
        """Generate a retrieval report from ranked results."""

        candidates: list[RetrievalCandidate] = []

        for result in results:

            candidate = RetrievalCandidate(
                document_id=result.document_id,
                title=result.title,
                final_score=result.final_score,
                semantic_score=getattr(result, "semantic_score", 0.0),
                keyword_score=getattr(result, "keyword_score", 0.0),
                metadata_score=getattr(result, "metadata_score", 0.0),
                identity_score=getattr(result, "identity_score", 0.0),
            )

            candidate.explanation = "\n".join(
                self._engine.explain(candidate)
            )

            candidates.append(candidate)

        return RetrievalReport(
            query=query,
            strategy=strategy,
            latency_ms=latency_ms,
            candidate_count=len(candidates),
            results=candidates,
        )

