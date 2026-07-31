"""
Athena Knowledge Relationship

Represents a semantic connection between
two Knowledge Objects.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID, uuid4


@dataclass
class KnowledgeRelationship:
    """
    Represents a relationship between knowledge objects.

    Examples:
        supports
        contradicts
        contains
        references
        implements
        derived_from
    """

    relationship_id: UUID = field(default_factory=uuid4)

    source_object_id: Optional[UUID] = None

    target_object_id: Optional[UUID] = None

    relationship_type: str = "related_to"

    confidence: float = 1.0

    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Add relationship metadata.
        """
        self.metadata[key] = value