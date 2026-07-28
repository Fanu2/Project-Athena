from athena.evaluation.benchmark_retrieval_report import (
    BenchmarkRetrievalReport,
)


def test_default_report():

    report = BenchmarkRetrievalReport()

    assert report.reports == []
    assert report.total_queries == 0
    assert report.average_latency_ms == 0.0
    assert report.average_candidates == 0.0
    assert report.metadata == {}
