"""
Conversation query orchestration service.
"""

from __future__ import annotations

from athena.conversation.service import (
    ConversationService,
)

from athena.services.athena_query_service import (
    AthenaQueryService,
)


class ConversationQueryService:
    """
    Coordinates conversations with Athena.

    This service records user messages, delegates
    question answering, stores assistant replies,
    and returns the generated response.
    """

    def __init__(
        self,
        conversation_service: ConversationService,
        query_service: AthenaQueryService,
    ) -> None:
        self._conversation = conversation_service
        self._query = query_service

    def ask(
        self,
        question: str,
    ):
        """
        Ask Athena a question while maintaining
        conversation history.
        """

        self._conversation.add_user_message(
            question,
        )

        answer = self._query.answer(
            question,
        )

        reply = (
            answer.answer
            if hasattr(answer, "answer")
            else str(answer)
        )

        self._conversation.add_assistant_message(
            reply,
        )

        return answer
