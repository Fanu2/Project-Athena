"""
Document structure intelligence model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(slots=True)
class DocumentStructureNode:
    """
    Represents a detected document structure element.
    """

    node_id: UUID = field(
        default_factory=uuid4,
    )

    node_type: str = "unknown"

    title: str = ""

    level: int = 0

    parent_id: UUID | None = None