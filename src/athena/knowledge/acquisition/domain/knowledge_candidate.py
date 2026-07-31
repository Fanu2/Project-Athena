"""
Athena Knowledge Candidate

Temporary semantic discovery before becoming
a canonical Knowledge Object.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID, uuid4


@dataclass
class KnowledgeCandidate:
    """
    Represents a potential knowledge entity.

    Candidates require validation before
    becoming persistent Knowledge Objects.
    """

    candidate_id: UUID = field(default_factory=uuid4)

    candidate_type: str = "unknown"

    value: Optional[str] = None

    source_node_id: Optional[UUID] = None

    confidence: float = 0.0

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
        Add candidate metadata.
        """
        self.metadata[key] = value