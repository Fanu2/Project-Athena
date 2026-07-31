"""
Athena Knowledge Collection

Logical grouping of related knowledge objects.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4


@dataclass
class KnowledgeCollection:
    """
    Represents a logical knowledge container.

    Examples:
        project
        workspace
        library
        research corpus
    """

    collection_id: UUID = field(default_factory=uuid4)

    name: str = ""

    collection_type: str = "general"

    description: Optional[str] = None

    object_ids: List[UUID] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def add_object(
        self,
        object_id: UUID,
    ) -> None:
        """
        Add a knowledge object to collection.
        """
        self.object_ids.append(object_id)

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Add collection metadata.
        """
        self.metadata[key] = value