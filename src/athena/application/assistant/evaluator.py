"""
Assistant plan evaluator.
"""

from __future__ import annotations

from .evaluation import (
    AssistantEvaluationCase,
)

from .evaluation_result import (
    AssistantPlanEvaluation,
)

from .plan import (
    AssistantPlan,
)


class AssistantEvaluator:
    """
    Evaluates assistant plans.
    """

    def evaluate(
        self,
        case: AssistantEvaluationCase,
        plan: AssistantPlan,
    ) -> AssistantPlanEvaluation:
        """
        Compare expected behaviour
        with generated plan.
        """

        capability_match = (
            plan.capability
            == case.expected_capability
        )

        actual_actions = {
            action.name
            for action in plan.actions
        }

        expected_actions = set(
            case.expected_actions,
        )

        if expected_actions:
            action_score = (
                len(
                    actual_actions
                    & expected_actions
                )
                /
                len(expected_actions)
            )
        else:
            action_score = 1.0

        workflow_score = (
            1.0
            if plan.workflow_steps
            else 0.0
        )

        passed = (
            capability_match
            and action_score == 1.0
            and workflow_score > 0
        )

        return AssistantPlanEvaluation(
            capability_match=capability_match,
            action_score=action_score,
            workflow_score=workflow_score,
            passed=passed,
        )
