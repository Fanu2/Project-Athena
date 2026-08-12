"""
Tests for action-aware plans.
"""

from athena.ai.intent.service import (
    IntentService,
)

from athena.application.assistant.engine import (
    AssistantEngine,
)


def test_summary_plan_contains_actions():

    engine = AssistantEngine(
        IntentService(),
    )

    decision = engine.analyze_request(
        "summarize documents",
        type(
            "Workspace",
            (),
            {
                "workspace_name": "Research",
                "document_count": 10,
                "knowledge_item_count": 5,
                "conversation_messages": 1,
            },
        )(),
    )

    plan = engine.create_plan(
        decision,
    )

    assert len(plan.actions) == 4

    assert (
        plan.actions[0].name
        == "retrieve_information"
    )
