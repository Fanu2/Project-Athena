"""
Conversation serialization utilities.
"""

from __future__ import annotations

from datetime import datetime

from athena.ai.llm.conversation import Conversation
from athena.ai.llm.conversation_metadata import (
    ConversationMetadata,
)
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
            "metadata": (
                {
                    "title": conversation.metadata.title,
                    "summary": conversation.metadata.summary,
                    "topics": conversation.metadata.topics,
                    "tags": conversation.metadata.tags,
                    "message_count": (
                        conversation.metadata.message_count
                    ),
                    "model": conversation.metadata.model,
                }
                if conversation.metadata
                else None
            ),
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

        metadata = data.get(
            "metadata"
        )

        if metadata:
            conversation.metadata = (
                ConversationMetadata(
                    title=metadata.get(
                        "title",
                        "",
                    ),
                    summary=metadata.get(
                        "summary",
                        "",
                    ),
                    topics=metadata.get(
                        "topics",
                        [],
                    ),
                    tags=metadata.get(
                        "tags",
                        [],
                    ),
                    message_count=metadata.get(
                        "message_count",
                        0,
                    ),
                    model=metadata.get(
                        "model"
                    ),
                )
            )

        return conversation
