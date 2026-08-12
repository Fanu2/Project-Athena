"""
Assistant action evaluation models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssistantActionEvaluation:
    """
    Evaluates generated actions.
    """

    expected_count: int

    actual_count: int

    matched_count: int

    coverage_score: float

    passed: bool
