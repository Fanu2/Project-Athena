"""
Tests for assistant plan evaluation.
"""

from athena.application.assistant.evaluation import (
    AssistantEvaluationCase,
)

from athena.application.assistant.evaluator import (
    AssistantEvaluator,
)

from athena.application.assistant.plan import (
    AssistantPlan,
)

from athena.application.assistant.action import (
    AssistantAction,
)

from athena.application.assistant.workflow import (
    AssistantWorkflowStep,
)


def test_summary_plan_evaluation():

    evaluator = AssistantEvaluator()

    case = AssistantEvaluationCase(
        name="summary",
        query="summarize documents",
        expected_capability="summary",
        expected_actions=(
            "retrieve_information",
        ),
    )

    plan = AssistantPlan(
        capability="summary",
        steps=(
            "retrieve_information",
        ),
        workflow_steps=(
            AssistantWorkflowStep(
                name="retrieve_information",
                description="Search documents",
                category="retrieval",
            ),
        ),
        actions=(
            AssistantAction(
                name="retrieve_information",
                description="Search documents",
            ),
        ),
    )

    result = evaluator.evaluate(
        case,
        plan,
    )

    assert result.passed is True

    assert result.action_score == 1.0
