"""
Confidence calculation for the Athena Intent Engine.

This module converts raw intent scores into a confidence estimate.
"""

from __future__ import annotations

from .models import ConfidenceResult, IntentType


class ConfidenceCalculator:
    """
    Calculates the most likely intent and its confidence.
    """

    def calculate(
        self,
        scores: dict[IntentType, int],
    ) -> ConfidenceResult:
        """
        Calculate confidence from raw scores.
        """
        if not scores:
            return ConfidenceResult(
                intent=IntentType.UNKNOWN,
                confidence=0.0,
                scores={},
            )

        total = sum(scores.values())

        winner = max(scores, key=scores.get)

        confidence = scores[winner] / total

        return ConfidenceResult(
            intent=winner,
            confidence=confidence,
            scores=scores,
        )