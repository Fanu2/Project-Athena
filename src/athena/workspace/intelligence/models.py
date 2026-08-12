"""
Athena Workspace Intelligence models.

Read models used to expose workspace state
and historical workspace context.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class WorkspaceIntelligenceSnapshot:
    """
    Represents the current intelligence state
    of an Athena workspace.
    """

    workspace_id: UUID

    workspace_name: str

    document_count: int = 0

    page_count: int = 0

    indexed_document_count: int = 0

    knowledge_item_count: int = 0

    evidence_count: int = 0

    citation_count: int = 0

    conversation_id: str | None = None

    conversation_messages: int = 0

    active_document: str | None = None

    #
    # A20.3 Workspace Activity Intelligence
    #

    last_activity: datetime | None = None

    #
    # A20.4 Workspace Intelligence Context
    #

    recent_documents: tuple[str, ...] = ()

    recent_queries: tuple[str, ...] = ()

    recent_sessions: tuple[str, ...] = ()
