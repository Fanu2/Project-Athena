"""
Workspace models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ActiveDocument:
    """Currently selected document."""

    document_id: str
    filename: str
    path: str