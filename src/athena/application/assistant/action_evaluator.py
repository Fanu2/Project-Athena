"""
Assistant action evaluator.
"""

from __future__ import annotations

from .action_evaluation import (
    AssistantActionEvaluation,
)

from .plan import (
    AssistantPlan,
)

from .evaluation import (
    AssistantEvaluationCase,
)


class AssistantActionEvaluator:
    """
    Evaluates action quality.
    """

    def evaluate(
        self,
        case: AssistantEvaluationCase,
        plan: AssistantPlan,
    ) -> AssistantActionEvaluation:
        """
        Compare expected and actual actions.
        """

        expected = set(
            case.expected_actions,
        )

        actual = {
            action.name
            for action in plan.actions
        }

        matched = (
            expected
            &
            actual
        )

        if expected:
            score = (
                len(matched)
                /
                len(expected)
            )
        else:
            score = 1.0

        return AssistantActionEvaluation(
            expected_count=len(expected),
            actual_count=len(actual),
            matched_count=len(matched),
            coverage_score=score,
            passed=score == 1.0,
        )
