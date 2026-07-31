
"""
Athena Knowledge Node

Represents a structural element inside
the Knowledge Representation Model (KRM).
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4


@dataclass
class KnowledgeNode:
    """
    A node inside the Knowledge Representation Model.

    Examples:
        document
        section
        paragraph
        table
        figure
        equation
    """

    node_id: UUID = field(default_factory=uuid4)

    node_type: str = "unknown"

    content: Optional[str] = None

    parent_id: Optional[UUID] = None

    children: List[UUID] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def add_child(
        self,
        child_id: UUID,
    ) -> None:
        """
        Add a child node.
        """
        self.children.append(child_id)

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Add node metadata.
        """
        self.metadata[key] = value