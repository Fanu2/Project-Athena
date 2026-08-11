"""
Tests for assistant workflow planning.
"""

from athena.ai.intent.service import (
    IntentService,
)

from athena.application.assistant.engine import (
    AssistantEngine,
)

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)


def test_summary_plan_contains_workflow_steps():

    engine = AssistantEngine(
        IntentService(),
    )

    snapshot = WorkspaceIntelligenceSnapshot(
        workspace_id="test",
        workspace_name="Research",
        document_count=10,
        knowledge_item_count=5,
        conversation_messages=2,
    )

    decision = engine.analyze_request(
        "Summarize my documents",
        snapshot,
    )

    plan = engine.create_plan(
        decision,
    )

    assert len(
        plan.workflow_steps
    ) == 4

    assert (
        plan.workflow_steps[0].name
        == "retrieve_information"
    )

    assert (
        plan.workflow_steps[-1].name
        == "attach_citations"
    )
