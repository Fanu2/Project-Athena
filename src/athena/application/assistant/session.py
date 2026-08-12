"""
Assistant session models.

Provides workspace-aware assistant state.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class AssistantSession:
    """
    Represents an assistant interaction session.

    Conversation history is managed by the
    existing conversation subsystem.
    """

    session_id: str

    workspace_name: str

    conversation_id: str

    created_at: datetime


def create_assistant_session(
    workspace_name: str,
    conversation_id: str,
) -> AssistantSession:
    """
    Create a new assistant session.
    """

    return AssistantSession(
        session_id=str(uuid4()),
        workspace_name=workspace_name,
        conversation_id=conversation_id,
        created_at=datetime.now(
            timezone.utc
        ),
    )
