"""
Benchmark dataset validator.
"""

from __future__ import annotations

from athena.evaluation.benchmark_models import BenchmarkQuestion


class BenchmarkValidator:
    """Validates benchmark datasets before execution."""

    @staticmethod
    def validate(
        questions: list[BenchmarkQuestion],
    ) -> list[str]:
        """Validate a benchmark dataset.

        Returns
        -------
        list[str]
            Validation errors. Empty list means the dataset is valid.
        """

        errors: list[str] = []

        if not questions:
            errors.append("Benchmark dataset is empty.")
            return errors

        seen_ids: set[str] = set()
        seen_questions: set[str] = set()

        for index, question in enumerate(questions, start=1):
            if not question.question_id.strip():
                errors.append(f"Question #{index} has an empty question_id.")

            if not question.question.strip():
                errors.append(f"Question '{question.question_id}' has an empty question.")

            if question.question_id in seen_ids:
                errors.append(f"Duplicate question_id: '{question.question_id}'.")
            else:
                seen_ids.add(question.question_id)

            if question.question in seen_questions:
                errors.append(f"Duplicate question text: '{question.question}'.")
            else:
                seen_questions.add(question.question)

        return errors

