"""
Tests for assistant evaluation models.
"""

from athena.application.assistant.evaluation import (
    AssistantEvaluationCase,
)


def test_evaluation_case_creation():

    case = AssistantEvaluationCase(
        name="summary",
        query="summarize documents",
        expected_capability="summary",
        expected_actions=(
            "retrieve_information",
        ),
    )

    assert case.name == "summary"

    assert (
        case.expected_capability
        == "summary"
    )

    assert (
        "retrieve_information"
        in case.expected_actions
    )
