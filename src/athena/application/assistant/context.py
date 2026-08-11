"""
Assistant execution context.

Provides the information available to
Athena Assistant when handling a request.
"""

from __future__ import annotations

from dataclasses import dataclass

from athena.ai.intent.models import IntentResult

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)


@dataclass(slots=True)
class AssistantContext:
    """
    Runtime context available to Athena Assistant.
    """

    intent: IntentResult

    workspace: WorkspaceIntelligenceSnapshot

    model_name: str | None = None
