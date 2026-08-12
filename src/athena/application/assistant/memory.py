"""
Assistant memory models.

Defines explicit user-controlled memory items.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class AssistantMemoryItem:
    """
    A user-controlled assistant memory entry.
    """

    key: str

    value: str

    source: str

    scope: str

    created_at: datetime
