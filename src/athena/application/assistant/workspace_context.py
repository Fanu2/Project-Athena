"""
Assistant workspace context.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssistantWorkspaceContext:
    """
    Context supplied to the assistant planner.
    """

    workspace_name: str

    document_count: int

    knowledge_item_count: int

    conversation_messages: int

    recent_documents: tuple[str, ...] = ()

    recent_queries: tuple[str, ...] = ()

    recent_sessions: tuple[str, ...] = ()
