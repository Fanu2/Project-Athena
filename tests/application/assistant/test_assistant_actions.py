"""
Tests for assistant action registry.
"""

from athena.application.assistant.action_registry import (
    ActionRegistry,
)

from athena.application.assistant.capability import (
    AssistantCapability,
)


def test_summary_capability_has_actions():

    registry = ActionRegistry()

    actions = registry.resolve(
        AssistantCapability(
            name="summary",
        )
    )

    assert len(actions) == 4

    assert (
        actions[0].name
        == "retrieve_information"
    )
