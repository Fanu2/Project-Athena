"""
Athena Knowledge Representation Model (KRM)

Intermediate representation between imported sources
and canonical Knowledge Objects.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import UUID, uuid4


@dataclass
class KnowledgeRepresentation:
    """
    Structural representation of an imported source.

    Example:

    Document
        |
        +-- Section
        +-- Paragraph
        +-- Figure
        +-- Table
    """

    representation_id: UUID = field(default_factory=uuid4)

    representation_type: str = "document"

    title: str = ""

    nodes: List[UUID] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def add_node(
        self,
        node_id: UUID,
    ) -> None:
        """
        Add a structural node.
        """
        self.nodes.append(node_id)

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Add representation metadata.
        """
        self.metadata[key] = value