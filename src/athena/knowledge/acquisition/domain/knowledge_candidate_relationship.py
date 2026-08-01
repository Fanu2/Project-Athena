"""
Athena Knowledge Candidate Relationship

Temporary semantic relationship before
canonical KnowledgeRelationship creation.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID, uuid4


@dataclass
class KnowledgeCandidateRelationship:
    """
    Represents a possible relationship
    between semantic candidates.
    """

    relationship_id: UUID = field(
        default_factory=uuid4
    )

    source_candidate_id: Optional[UUID] = None

    target_candidate_id: Optional[UUID] = None

    relationship_type: str = "related_to"

    confidence: float = 0.5

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
        Add relationship metadata.
        """
        self.metadata[key] = value