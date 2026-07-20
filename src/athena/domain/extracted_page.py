"""
Extracted page domain model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ExtractedPage:
    """Represents a single page extracted from a document."""

    page_number: int

    text: str