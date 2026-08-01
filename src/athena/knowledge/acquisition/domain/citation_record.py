"""
Athena Citation Record

Represents a traceable citation
generated from evidence.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID, uuid4


@dataclass
class CitationRecord:
    """
    Citation pointing to supporting evidence.
    """

    citation_id: UUID = field(
        default_factory=uuid4
    )

    evidence_id: Optional[UUID] = None

    source_reference: Optional[str] = None

    citation_text: Optional[str] = None

    location: Optional[str] = None

    confidence: float = 1.0

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    created_at: datetime = field(
        default_factory=lambda:
            datetime.now(timezone.utc)
    )

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Add citation metadata.
        """

        self.metadata[key] = value