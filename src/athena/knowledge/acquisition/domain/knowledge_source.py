"""
Athena Knowledge Source

Represents the origin of information entering Athena.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID, uuid4


@dataclass
class KnowledgeSource:
    """
    Origin of knowledge entering Athena.

    Examples:
        PDF file
        repository
        website
        email archive
    """

    source_id: UUID = field(default_factory=uuid4)

    name: str = ""

    source_type: str = "unknown"

    location: Optional[str] = None

    mime_type: Optional[str] = None

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
        Add source metadata.
        """
        self.metadata[key] = value