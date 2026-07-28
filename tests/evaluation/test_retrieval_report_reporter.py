from athena.evaluation.retrieval_report import (
    RetrievalCandidate,
    RetrievalReport,
)
from athena.evaluation.retrieval_report_reporter import (
    RetrievalReportReporter,
)


def test_format_retrieval_report():

    report = RetrievalReport(
        query="history",
        strategy="hybrid",
        latency_ms=95.0,
        candidate_count=1,
        results=[
            RetrievalCandidate(
                document_id="doc1",
                title="History",
                final_score=0.95,
                semantic_score=0.91,
                keyword_score=0.82,
                metadata_score=0.55,
                identity_score=1.00,
                explanation="High semantic similarity",
            )
        ],
    )

    formatter = RetrievalReportReporter()

    output = formatter.format(report)

    assert "Retrieval Intelligence Report" in output
    assert "history" in output
    assert "hybrid" in output
    assert "History" in output
    assert "High semantic similarity" in output

