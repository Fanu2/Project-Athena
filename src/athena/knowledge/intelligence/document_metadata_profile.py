"""
Document metadata intelligence model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class DocumentMetadataProfile:
    """
    Enriched metadata extracted from a document.
    """

    document_type: str = "unknown"

    language: str = "unknown"

    author: str | None = None

    tags: list[str] = field(
        default_factory=list,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    confidence: float = 1.0