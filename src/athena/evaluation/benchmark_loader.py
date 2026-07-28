"""
Benchmark dataset loader.
"""

from __future__ import annotations

import json
from pathlib import Path

from athena.evaluation.benchmark_models import BenchmarkQuestion


class BenchmarkLoader:
    """Loads benchmark datasets from JSON."""

    @staticmethod
    def load(path: str | Path) -> list[BenchmarkQuestion]:
        """Load benchmark questions from a JSON file."""

        dataset_path = Path(path)

        with dataset_path.open("r", encoding="utf-8-sig") as fp:
            data = json.load(fp)

        questions: list[BenchmarkQuestion] = []

        for item in data:
            questions.append(
                BenchmarkQuestion(
                    question_id=item["question_id"],
                    question=item["question"],
                    expected_document_id=item.get("expected_document_id"),
                    expected_chunk_id=item.get("expected_chunk_id"),
                    tags=tuple(item.get("tags", [])),
                )
            )

        return questions

