"""
Benchmark diagnostics engine.
"""

from __future__ import annotations

import re
from pathlib import Path

from athena.evaluation.benchmark_diagnostics_models import (
    BenchmarkDiagnostics,
    RetrievalDiagnostic,
)
from athena.evaluation.benchmark_session import BenchmarkSession


class BenchmarkDiagnosticsEngine:
    """Produces detailed diagnostics for benchmark runs."""

    @staticmethod
    def _normalize_document_name(
        document_name: str,
    ) -> str:
        """Normalize document names for comparison."""

        name = Path(
            document_name,
        ).name.lower().strip()

        name = re.sub(
            r".[a-z0-9]+$",
            "",
            name,
        )

        name = name.replace(
            "_",
            "-",
        )

        name = re.sub(
            r"^\d+-",
            "",
            name,
        )

        return name.strip("-")

    def analyze(
        self,
        session: BenchmarkSession,
    ) -> BenchmarkDiagnostics:
        """Analyze benchmark runs and produce retrieval diagnostics."""

        diagnostics = BenchmarkDiagnostics()

        for run in session.runs:
            expected = run.question.expected_document_id

            ids = [
                result.document_name
                for result in run.retrieval_results
            ]

            expected_found = False
            expected_rank = None
            expected_score = None

            normalized_expected = None

            if expected:
                normalized_expected = (
                    self._normalize_document_name(
                        expected,
                    )
                )

            for rank, result in enumerate(
                run.retrieval_results,
                start=1,
            ):
                normalized_name = (
                    self._normalize_document_name(
                        result.document_name,
                    )
                )

                if normalized_name == normalized_expected:
                    expected_found = True
                    expected_rank = rank
                    expected_score = result.score
                    break

            top_document_id = None
            top_document_score = None

            if run.retrieval_results:
                top = run.retrieval_results[0]

                top_document_id = top.document_name

                top_document_score = top.score

            notes: list[str] = []

            if expected is None:
                notes.append(
                    "No expected document defined.",
                )

            elif not run.retrieval_results:
                notes.append(
                    "No retrieval results returned.",
                )

            elif expected_found:
                if expected_rank == 1:
                    notes.append(
                        "Expected document ranked first.",
                    )
                else:
                    notes.append(
                        f"Expected document retrieved at rank {expected_rank}.",
                    )

            else:
                notes.append(
                    "Expected document was not retrieved.",
                )

            diagnostics.diagnostics.append(
                RetrievalDiagnostic(
                    question_id=run.question.question_id,
                    expected_document_id=expected,
                    expected_found=expected_found,
                    expected_rank=expected_rank,
                    top_document_id=top_document_id,
                    top_document_score=top_document_score,
                    expected_document_score=expected_score,
                    retrieved_document_ids=ids,
                    notes=notes,
                )
            )

        return diagnostics

