"""
Conversation serialization utilities.
"""

from __future__ import annotations

from datetime import datetime

from athena.ai.llm.conversation import Conversation
from athena.ai.llm.message import Message


class ConversationSerializer:
    """Serialize and deserialize conversations."""

    def to_dict(
        self,
        conversation: Conversation,
    ) -> dict:
        """Convert conversation to dictionary."""

        return {
            "conversation_id": conversation.conversation_id,
            "title": conversation.title,
            "created_at": (
                conversation.created_at.isoformat()
            ),
            "updated_at": (
                conversation.updated_at.isoformat()
            ),
            "messages": [
                {
                    "role": message.role,
                    "content": message.content,
                    "timestamp": (
                        message.timestamp.isoformat()
                        if message.timestamp
                        else None
                    ),
                }
                for message in conversation.messages
            ],
        }

    def from_dict(
        self,
        data: dict,
    ) -> Conversation:
        """Create conversation from dictionary."""

        conversation = Conversation(
            title=data.get(
                "title",
                "",
            ),
            conversation_id=data[
                "conversation_id"
            ],
            created_at=datetime.fromisoformat(
                data["created_at"]
            ),
            updated_at=datetime.fromisoformat(
                data["updated_at"]
            ),
        )

        for item in data.get(
            "messages",
            [],
        ):
            conversation.messages.append(
                Message(
                    role=item["role"],
                    content=item["content"],
                    timestamp=(
                        datetime.fromisoformat(
                            item["timestamp"]
                        )
                        if item.get("timestamp")
                        else None
                    ),
                )
            )

        return conversation
