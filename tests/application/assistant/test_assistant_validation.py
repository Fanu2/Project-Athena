"""
Tests for assistant validation models.
"""

from athena.application.assistant.validation import (
    AssistantPlanValidation,
)


def test_validation_model_creation():

    validation = AssistantPlanValidation(
        valid=True,
        checks=(
            "capability_available",
            "workflow_present",
        ),
    )

    assert validation.valid is True

    assert (
        "workflow_present"
        in validation.checks
    )

    assert validation.warnings == ()
