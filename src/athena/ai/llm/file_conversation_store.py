"""
File based conversation store.
"""

from __future__ import annotations

import json
from pathlib import Path

from athena.ai.llm.conversation import Conversation
from athena.ai.llm.conversation_serializer import (
    ConversationSerializer,
)
from athena.ai.llm.conversation_store import (
    ConversationStore,
)


class FileConversationStore(
    ConversationStore
):
    """Store conversations as JSON files."""

    def __init__(
        self,
        directory: Path,
    ) -> None:
        """Initialize file store."""

        self._directory = directory

        self._directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._serializer = (
            ConversationSerializer()
        )

    def _path(
        self,
        conversation_id: str,
    ) -> Path:
        """Return storage path."""

        return (
            self._directory
            / f"{conversation_id}.json"
        )

    def save(
        self,
        conversation: Conversation,
    ) -> None:
        """Save conversation."""

        path = self._path(
            conversation.conversation_id
        )

        path.write_text(
            json.dumps(
                self._serializer.to_dict(
                    conversation
                ),
                indent=2,
            ),
            encoding="utf-8",
        )

    def get(
        self,
        conversation_id: str,
    ) -> Conversation:
        """Load conversation."""

        path = self._path(
            conversation_id
        )

        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        return self._serializer.from_dict(
            data
        )

    def exists(
        self,
        conversation_id: str,
    ) -> bool:
        """Check existence."""

        return self._path(
            conversation_id
        ).exists()

    def delete(
        self,
        conversation_id: str,
    ) -> None:
        """Delete conversation."""

        self._path(
            conversation_id
        ).unlink()

    def list_all(
        self,
    ) -> list[Conversation]:
        """List stored conversations."""

        conversations: list[Conversation] = []

        for path in self._directory.glob(
            "*.json"
        ):
            conversations.append(
                self._serializer.from_dict(
                    json.loads(
                        path.read_text(
                            encoding="utf-8"
                        )
                    )
                )
            )

        return conversations
