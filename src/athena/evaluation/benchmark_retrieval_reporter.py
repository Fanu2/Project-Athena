"""
Project Athena

Benchmark Retrieval Report Reporter.
"""

from __future__ import annotations

from athena.evaluation.benchmark_retrieval_report import (
    BenchmarkRetrievalReport,
)

from athena.evaluation.retrieval_report_reporter import (
    RetrievalReportReporter,
)


class BenchmarkRetrievalReportReporter:
    """
    Render benchmark retrieval reports as Markdown.
    """

    def __init__(self) -> None:
        self._reporter = RetrievalReportReporter()

    def analyze(
        self,
        report: BenchmarkRetrievalReport,
    ) -> str:
        """
        Generate benchmark retrieval report.
        """

        lines = [
            "# Benchmark Retrieval Intelligence Report",
            "",
            "## Summary",
            "",
            f"- Total Queries: {report.total_queries}",
            (
                "- Average Latency: "
                f"{report.average_latency_ms:.2f} ms"
            ),
            (
                "- Average Candidates: "
                f"{report.average_candidates:.2f}"
            ),
            "",
        ]

        #
        # Evaluation intelligence
        #

        metadata = report.metadata

        language_questions = metadata.get(
            "language_questions",
            {},
        )

        language_accuracy = metadata.get(
            "language_accuracy",
            {},
        )

        document_type_accuracy = metadata.get(
            "document_type_accuracy",
            {},
        )

        if language_questions:

            lines.extend(
                [
                    "---",
                    "",
                    "## Language Performance",
                    "",
                    "| Language | Questions | Accuracy |",
                    "|----------|----------:|---------:|",
                ]
            )

            for language in sorted(
                language_questions
            ):
                lines.append(
                    "| "
                    f"{language} | "
                    f"{language_questions[language]} | "
                    f"{language_accuracy.get(language, 0.0):.1%} |"
                )

            lines.append("")

        if document_type_accuracy:

            lines.extend(
                [
                    "---",
                    "",
                    "## Document Type Performance",
                    "",
                    "| Document Type | Accuracy |",
                    "|---------------|---------:|",
                ]
            )

            for document_type in sorted(
                document_type_accuracy
            ):
                lines.append(
                    "| "
                    f"{document_type} | "
                    f"{document_type_accuracy[document_type]:.1%} |"
                )

            lines.append("")

        #
        # Individual retrieval reports
        #

        for index, retrieval in enumerate(
            report.reports,
            start=1,
        ):

            lines.extend(
                [
                    "---",
                    "",
                    f"## Retrieval {index}",
                    "",
                    self._reporter.analyze(
                        retrieval,
                    ),
                    "",
                ]
            )

        return "\n".join(lines)
