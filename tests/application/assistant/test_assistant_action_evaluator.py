"""
Tests for assistant action evaluation.
"""

from athena.application.assistant.action import (
    AssistantAction,
)

from athena.application.assistant.action_evaluator import (
    AssistantActionEvaluator,
)

from athena.application.assistant.evaluation import (
    AssistantEvaluationCase,
)

from athena.application.assistant.plan import (
    AssistantPlan,
)


def test_action_evaluation_full_match():

    evaluator = AssistantActionEvaluator()

    case = AssistantEvaluationCase(
        name="summary",
        query="summarize documents",
        expected_capability="summary",
        expected_actions=(
            "retrieve_information",
            "generate_response",
        ),
    )

    plan = AssistantPlan(
        capability="summary",
        steps=(),
        actions=(
            AssistantAction(
                name="retrieve_information",
                description="Search documents",
            ),
            AssistantAction(
                name="generate_response",
                description="Generate response",
            ),
        ),
    )

    result = evaluator.evaluate(
        case,
        plan,
    )

    assert result.passed is True

    assert (
        result.coverage_score
        == 1.0
    )


def test_action_evaluation_partial_match():

    evaluator = AssistantActionEvaluator()

    case = AssistantEvaluationCase(
        name="summary",
        query="summarize documents",
        expected_capability="summary",
        expected_actions=(
            "retrieve_information",
            "generate_response",
        ),
    )

    plan = AssistantPlan(
        capability="summary",
        steps=(),
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

    assert result.passed is False

    assert (
        result.coverage_score
        == 0.5
    )
