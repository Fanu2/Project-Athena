from athena.evaluation.benchmark_retrieval_report_builder import (
    BenchmarkRetrievalReportBuilder,
)


def test_empty_builder():

    builder = BenchmarkRetrievalReportBuilder()

    report = builder.build([])

    assert report.total_queries == 0
    assert report.average_latency_ms == 0.0
    assert report.average_candidates == 0.0
    assert report.reports == []
