"""
Assistant request context.

Combines intent, workspace,
explicit user-controlled memory,
and assistant session state.
"""

from __future__ import annotations

from dataclasses import dataclass

from athena.ai.intent.models import (
    IntentResult,
)

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)

from .memory import (
    AssistantMemoryItem,
)

from .session import (
    AssistantSession,
)


@dataclass(frozen=True, slots=True)
class AssistantContext:
    """
    Context available during assistant planning.
    """

    intent: IntentResult

    workspace: WorkspaceIntelligenceSnapshot

    memories: tuple[
        AssistantMemoryItem,
        ...
    ] = ()

    session: AssistantSession | None = None