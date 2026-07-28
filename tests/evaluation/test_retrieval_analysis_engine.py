from dataclasses import dataclass

from athena.evaluation.retrieval_analysis_engine import (
    RetrievalAnalysisEngine,
)


@dataclass
class FakeResult:
    document_id: str
    title: str
    final_score: float
    semantic_score: float
    keyword_score: float
    metadata_score: float
    identity_score: float


def test_generate_retrieval_report():

    generator = RetrievalAnalysisEngine()

    report = generator.analyze(
        query="history",
        strategy="hybrid",
        latency_ms=95.0,
        results=[
            FakeResult(
                document_id="doc1",
                title="History",
                final_score=0.95,
                semantic_score=0.91,
                keyword_score=0.82,
                metadata_score=0.55,
                identity_score=1.00,
            )
        ],
    )

    assert report.query == "history"
    assert report.strategy == "hybrid"
    assert report.candidate_count == 1

    candidate = report.results[0]

    assert candidate.document_id == "doc1"
    assert candidate.title == "History"
    assert candidate.final_score == 0.95

    assert "semantic" in candidate.explanation.lower()
    assert "keyword" in candidate.explanation.lower()
    assert "metadata" in candidate.explanation.lower()
    assert "identity" in candidate.explanation.lower()

