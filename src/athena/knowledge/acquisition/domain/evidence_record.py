"""
Athena Evidence Record

Tracks provenance and trust information
for Knowledge Objects.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID, uuid4


@dataclass
class EvidenceRecord:
    """
    Represents provenance evidence for knowledge.

    Evidence answers:
    - Where did this come from?
    - How was it extracted?
    - How reliable is it?
    """

    evidence_id: UUID = field(default_factory=uuid4)

    source_id: Optional[UUID] = None

    source_reference: Optional[str] = None

    location: Optional[str] = None

    extraction_method: Optional[str] = None

    provider: Optional[str] = None

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
        Add evidence metadata.
        """
        self.metadata[key] = value