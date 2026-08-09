"""
Document intelligence profile.

Provides enriched understanding metadata
for imported Athena documents.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class DocumentProfile:
    """
    Intelligence summary of a document.

    This does not replace Document.
    It enriches the existing knowledge pipeline.
    """

    title: str = ""

    document_type: str = "unknown"

    page_count: int = 0

    section_count: int = 0

    entity_count: int = 0

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    confidence: float = 1.0