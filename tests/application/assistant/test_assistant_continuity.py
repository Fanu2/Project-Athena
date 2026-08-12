"""
Tests for assistant continuity integration.

Validates that workspace intelligence,
assistant memory, and assistant session
can coexist in AssistantContext.
"""

from datetime import datetime

from athena.ai.intent.service import (
    IntentService,
)

from athena.application.assistant.context import (
    AssistantContext,
)

from athena.application.assistant.engine import (
    AssistantEngine,
)

from athena.application.assistant.memory import (
    AssistantMemoryItem,
)

from athena.application.assistant.session import (
    create_assistant_session,
)

from athena.application.assistant.in_memory_store import (
    InMemoryAssistantMemoryStore,
)

from athena.application.assistant.in_memory_session_store import (
    InMemoryAssistantSessionStore,
)

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)


def test_assistant_continuity_combines_workspace_memory_session():

    workspace = WorkspaceIntelligenceSnapshot(
        workspace_id="workspace-001",
        workspace_name="Research",
        document_count=3,
        recent_documents=(
            "Athena Architecture.docx",
        ),
        recent_queries=(
            "Explain retrieval pipeline",
        ),
        recent_sessions=(),
    )

    memory = AssistantMemoryItem(
        key="response_style",
        value="prefer detailed technical explanations",
        source="user",
        scope="global",
        created_at=datetime.now(),
    )

    memory_store = InMemoryAssistantMemoryStore()

    memory_store.save(
        memory,
    )

    session = create_assistant_session(
        workspace_id="workspace-001",
        workspace_name="Research",
        conversation_id="conversation-001",
    )

    session_store = InMemoryAssistantSessionStore()

    session_store.save(
        session,
    )

    engine = AssistantEngine(
        IntentService(),
    )

    engine.set_memory_store(
        memory_store,
    )

    engine.set_session_store(
        session_store,
    )

    engine.set_memories(
        (
            memory,
        )
    )

    engine.set_session(
        session,
    )

    context = AssistantContext(
        intent=None,
        workspace=workspace,
        memories=(
            memory,
        ),
        session=session,
    )

    assert (
        context.workspace.workspace_name
        == "Research"
    )

    assert (
        context.memories[0].key
        == "response_style"
    )

    assert (
        context.session.workspace_name
        == "Research"
    )

    assert (
        context.session.conversation_id
        == "conversation-001"
    )
