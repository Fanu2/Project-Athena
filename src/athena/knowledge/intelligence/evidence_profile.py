"""
Document evidence intelligence model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4


@dataclass(slots=True)
class EvidenceProfile:
    """
    Represents evidence discovered in a document.
    """

    evidence_id: UUID = field(
        default_factory=uuid4,
    )

    source_document: UUID | None = None

    evidence_type: str = "text"

    content: str = ""

    location: str = ""

    confidence: float = 1.0

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )