"""
Assistant evaluation result models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssistantPlanEvaluation:
    """
    Evaluation result for an assistant plan.
    """

    capability_match: bool

    action_score: float

    workflow_score: float

    passed: bool
