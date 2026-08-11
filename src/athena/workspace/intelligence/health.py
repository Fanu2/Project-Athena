"""
Workspace intelligence health models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class WorkspaceHealthReport:
    """
    Represents workspace readiness signals.
    """

    documents_ready: bool = False

    knowledge_ready: bool = False

    evidence_ready: bool = False

    citation_ready: bool = False

    retrieval_ready: bool = False

    ai_ready: bool = False
