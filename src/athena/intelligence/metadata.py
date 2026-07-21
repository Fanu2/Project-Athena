"""
Document metadata models.

These models represent computed metadata about a document.
They are independent of document extraction and indexing.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class DocumentMetadata:
    """Computed metadata describing a document."""

    # Basic statistics
    word_count: int

    character_count: int

    line_count: int

    page_count: int

    # Estimated reading time (minutes)
    estimated_reading_minutes: int