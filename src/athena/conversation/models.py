"""
Conversation models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class MessageRole(str, Enum):
    """Role of a conversation message."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass(slots=True)
class ConversationMessage:
    """Single conversation message."""

    role: MessageRole
    text: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass(slots=True)
class Conversation:
    """Conversation session."""

    conversation_id: str = field(default_factory=lambda: str(uuid4()))
    title: str = "New Conversation"
    created: datetime = field(default_factory=datetime.now)
    modified: datetime = field(default_factory=datetime.now)
    messages: list[ConversationMessage] = field(default_factory=list)