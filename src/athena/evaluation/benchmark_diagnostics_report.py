"""
Benchmark diagnostics report generator.
"""

from __future__ import annotations

from athena.evaluation.benchmark_diagnostics_models import (
    BenchmarkDiagnostics,
)


class BenchmarkDiagnosticsReporter:
    """Generate a Markdown diagnostics report."""

    def generate(
        self,
        diagnostics: BenchmarkDiagnostics,
    ) -> str:

        lines: list[str] = []

        lines.append("# Athena Retrieval Diagnostics")
        lines.append("")

        for diagnostic in diagnostics.diagnostics:
            lines.append(f"## Question {diagnostic.question_id}")
            lines.append("")

            lines.append(f"- Expected Document: {diagnostic.expected_document_id}")

            status = "Found" if diagnostic.expected_found else "Not Retrieved"

            lines.append(f"- Status: {status}")

            lines.append(f"- Rank: {diagnostic.expected_rank}")

            lines.append(f"- Expected Score: {diagnostic.expected_document_score}")

            lines.append(f"- Top Document: {diagnostic.top_document_id}")

            lines.append(f"- Top Score: {diagnostic.top_document_score}")

            lines.append("")
            lines.append("### Retrieved Documents")
            lines.append("")

            for index, document_id in enumerate(
                diagnostic.retrieved_document_ids,
                start=1,
            ):
                lines.append(f"{index}. {document_id}")

            lines.append("")
            lines.append("### Notes")
            lines.append("")

            for note in diagnostic.notes:
                lines.append(f"- {note}")

            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)
