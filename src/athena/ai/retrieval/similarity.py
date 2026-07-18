"""
Vector similarity utilities.
"""

from __future__ import annotations

import math


class SimilarityCalculator:
    """Calculate vector similarity."""

    @staticmethod
    def cosine_similarity(
        first: list[float],
        second: list[float],
    ) -> float:
        """
        Calculate cosine similarity.

        Returns:
            Value between -1 and 1.
        """

        if len(first) != len(second):
            raise ValueError(
                "Vectors must have same dimensions.",
            )

        dot_product = sum(
            a * b
            for a, b in zip(
                first,
                second,
            )
        )

        first_norm = math.sqrt(sum(value * value for value in first))

        second_norm = math.sqrt(sum(value * value for value in second))

        if first_norm == 0 or second_norm == 0:
            return 0.0

        return dot_product / (first_norm * second_norm)
