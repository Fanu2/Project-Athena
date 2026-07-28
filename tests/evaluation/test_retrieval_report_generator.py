from dataclasses import dataclass

from athena.evaluation.retrieval_report_generator import RetrievalReportGenerator


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
    generator = RetrievalReportGenerator()

    report = generator.generate(
        query="history",
        strategy="hybrid",
        latency_ms=95.0,
        results=[
            FakeResult(
                document_id="doc1",
                title="History",
                final_score=0.95,
                semantic_score=0.90,
                keyword_score=0.80,
                metadata_score=0.60,
                identity_score=1.00,
            )
        ],
    )

    assert report.query == "history"
    assert report.candidate_count == 1
    assert report.results[0].title == "History"
    assert report.results[0].identity_score == 1.0
