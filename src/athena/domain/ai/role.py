"""
AI conversation roles.
"""

from __future__ import annotations

from enum import Enum, auto


class Role(Enum):
    """Role of a conversation participant."""

    USER = auto()
    ASSISTANT = auto()
