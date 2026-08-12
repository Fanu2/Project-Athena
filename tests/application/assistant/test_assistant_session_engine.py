"""
Tests for assistant engine session integration.
"""

from athena.ai.intent.service import (
    IntentService,
)

from athena.application.assistant.engine import (
    AssistantEngine,
)

from athena.application.assistant.session import (
    create_assistant_session,
)


def test_engine_accepts_session():

    engine = AssistantEngine(
        IntentService(),
    )

    session = create_assistant_session(
        workspace_name="Research",
        workspace_id="workspace-001",
        conversation_id="conv-001",
    )

    engine.set_session(
        session,
    )

    assert (
        engine.get_session()
        == session
    )
