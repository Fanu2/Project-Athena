"""
Tests for assistant action validation.
"""

from athena.application.assistant.action import (
    AssistantAction,
)

from athena.application.assistant.action_quality import (
    AssistantActionQualityService,
)


def test_action_quality_accepts_valid_actions():

    service = AssistantActionQualityService()

    result = service.validate(
        (
            AssistantAction(
                name="retrieve_information",
                description=(
                    "Search workspace documents"
                ),
            ),
        )
    )

    assert result.valid is True

    assert (
        "actions_present"
        in result.checks
    )


def test_action_quality_rejects_empty_actions():

    service = AssistantActionQualityService()

    result = service.validate(
        ()
    )

    assert result.valid is False

    assert (
        "no_actions"
        in result.warnings
    )
