"""
End-to-end assistant workspace workflow tests.
"""

from datetime import datetime

from athena.ai.intent.service import (
    IntentService,
)

from athena.application.assistant.engine import (
    AssistantEngine,
)

from athena.application.assistant.memory import (
    AssistantMemoryItem,
)


def test_assistant_workspace_workflow_plan():

    engine = AssistantEngine(
        IntentService(),
    )

    engine.set_memories(
        (
            AssistantMemoryItem(
                key="style",
                value="concise answers",
                source="user",
                scope="global",
                created_at=datetime.now(),
            ),
        )
    )

    decision = engine.analyze_request(
        "summarize research documents",
        workspace=type(
            "Workspace",
            (),
            {
                "workspace_name": "Research",
                "document_count": 10,
                "knowledge_item_count": 5,
                "conversation_messages": 2,
            },
        )(),
    )

    plan = engine.create_plan(
        decision,
    )

    assert (
        plan.capability
        == "summary"
    )

    assert (
        len(plan.workflow_steps)
        > 0
    )

    assert (
        "Memory:"
        in plan.context_notes
    )
