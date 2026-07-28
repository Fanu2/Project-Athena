from athena.evaluation.retrieval_report import (
    RetrievalCandidate,
    RetrievalReport,
)


def test_create_retrieval_report():
    candidate = RetrievalCandidate(
        document_id="doc1",
        title="Sample Document",
        final_score=0.95,
        semantic_score=0.91,
        keyword_score=0.88,
        metadata_score=0.40,
        identity_score=1.00,
    )

    report = RetrievalReport(
        query="sample query",
        strategy="hybrid",
        latency_ms=100.5,
        candidate_count=1,
        results=[candidate],
    )

    assert report.query == "sample query"
    assert report.candidate_count == 1
    assert report.results[0].final_score == 0.95

