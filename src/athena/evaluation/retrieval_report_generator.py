"""
Project Athena

Retrieval Report Generator.
"""

from athena.evaluation.retrieval_report import (
    RetrievalCandidate,
    RetrievalReport,
)


class RetrievalReportGenerator:
    """Builds a RetrievalReport from ranked retrieval results."""

    def generate(
        self,
        *,
        query: str,
        strategy: str,
        latency_ms: float,
        results,
    ) -> RetrievalReport:

        candidates = []

        for result in results:
            candidates.append(
                RetrievalCandidate(
                    document_id=result.document_id,
                    title=result.title,
                    final_score=result.final_score,
                    semantic_score=getattr(result, "semantic_score", 0.0),
                    keyword_score=getattr(result, "keyword_score", 0.0),
                    metadata_score=getattr(result, "metadata_score", 0.0),
                    identity_score=getattr(result, "identity_score", 0.0),
                )
            )

        return RetrievalReport(
            query=query,
            strategy=strategy,
            latency_ms=latency_ms,
            candidate_count=len(candidates),
            results=candidates,
        )
