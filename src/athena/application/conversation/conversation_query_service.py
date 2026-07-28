"""
Conversation query orchestration service.

This service coordinates the complete question-answering workflow by
maintaining conversation history while delegating AI response generation
to AthenaQueryService.
"""

from __future__ import annotations

from typing import Any

from athena.conversation.service import (
    ConversationService,
)
from athena.services.athena_query_service import (
    AthenaQueryService,
)


class ConversationQueryService:
    """
    Coordinates the complete conversation workflow.

    Responsibilities
    ----------------
    - Record the user's question.
    - Delegate question answering to AthenaQueryService.
    - Record Athena's response.
    - Return the original response object unchanged.

    This service provides a presentation-independent conversation
    orchestration layer so that UI components do not directly manage
    conversation persistence.
    """

    def __init__(
        self,
        conversation_service: ConversationService,
        query_service: AthenaQueryService,
    ) -> None:
        """Initialize the conversation query service."""

        self._conversation_service = conversation_service
        self._query_service = query_service

    def answer(
        self,
        question: str,
    ) -> Any:
        """
        Answer a question while maintaining conversation history.

        The returned value is passed through unchanged from
        AthenaQueryService, preserving compatibility with existing
        callers.
        """

        self._conversation_service.add_user_message(
            question,
        )

        result = self._query_service.answer(
            question,
        )

        assistant_reply = result.answer if hasattr(result, "answer") else str(result)

        self._conversation_service.add_assistant_message(
            assistant_reply,
        )

        return result

