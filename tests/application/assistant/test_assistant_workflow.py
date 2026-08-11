"""
Tests for assistant workflow models.
"""

from athena.application.assistant.workflow import (
    AssistantWorkflowStep,
)


def test_workflow_step_creation():

    step = AssistantWorkflowStep(
        name="retrieve_information",
        description="Search workspace documents",
        category="retrieval",
    )

    assert step.name == "retrieve_information"

    assert (
        step.description
        == "Search workspace documents"
    )

    assert (
        step.category
        == "retrieval"
    )
