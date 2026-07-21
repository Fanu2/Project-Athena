"""
Document checksum domain model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class DocumentChecksum:
    """Checksum information for a document."""

    algorithm: str

    value: str
