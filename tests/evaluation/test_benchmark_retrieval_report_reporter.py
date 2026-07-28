from athena.evaluation.benchmark_retrieval_report import (
    BenchmarkRetrievalReport,
)
from athena.evaluation.benchmark_retrieval_report_reporter import (
    BenchmarkRetrievalReportReporter,
)


def test_empty_report():

    reporter = BenchmarkRetrievalReportReporter()

    report = BenchmarkRetrievalReport()

    output = reporter.analyze(report)

    assert "Benchmark Retrieval Intelligence Report" in output
    assert "Total Queries" in output
