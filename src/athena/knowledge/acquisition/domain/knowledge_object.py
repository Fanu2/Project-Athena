"""
Athena Knowledge Object

The canonical representation of knowledge inside Athena.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID, uuid4


@dataclass
class KnowledgeObject:
    """
    Base canonical knowledge entity.

    All persistent knowledge entities in Athena
    derive from this concept.
    """

    object_id: UUID = field(default_factory=uuid4)

    object_type: str = "generic"

    title: Optional[str] = None

    content: Optional[str] = None

    metadata: Dict[str, Any] = field(default_factory=dict)

    confidence: float = 1.0

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def update_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Add or update metadata.
        """
        self.metadata[key] = value

        self.updated_at = datetime.now(timezone.utc)