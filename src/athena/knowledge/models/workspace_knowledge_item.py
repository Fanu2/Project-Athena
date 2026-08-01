"""
Athena Knowledge Workspace Read Model

UI-facing representation of knowledge.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class WorkspaceKnowledgeItem:
    """
    Read model for workspace display.

    Separates UI representation from
    internal KnowledgeObject domain model.
    """

    object_id: UUID

    title: str | None

    object_type: str

    confidence: float

    source_reference: str | None

    provider: str | None

    extraction_method: str | None