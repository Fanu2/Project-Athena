"""
Conversation execution service.
"""

from __future__ import annotations

from athena.ai.llm.conversation import Conversation
from athena.ai.llm.conversation_context_builder import (
    ConversationContextBuilder,
)
from athena.ai.llm.conversation_context_enricher import (
    ConversationContextEnricher,
)
from athena.ai.llm.conversation_execution import (
    ConversationExecutionResult,
)
from athena.ai.llm.conversation_request_builder import (
    ConversationRequestBuilder,
)
from athena.ai.llm.execution_service import (
    ExecutionService,
)
from athena.ai.llm.message import Message
from athena.ai.llm.runtime_request import (
    RuntimeRequest,
)


class ConversationExecutionService:
    """Execute conversational LLM requests."""

    def __init__(
        self,
        context_builder: ConversationContextBuilder | None = None,
        enricher: ConversationContextEnricher | None = None,
        request_builder: ConversationRequestBuilder | None = None,
        executor: ExecutionService | None = None,
    ) -> None:
        """Initialize service."""

        self._context_builder = (
            context_builder
            if context_builder is not None
            else ConversationContextBuilder()
        )

        self._enricher = enricher

        self._request_builder = (
            request_builder
            if request_builder is not None
            else ConversationRequestBuilder()
        )

        self._executor = (
            executor
            if executor is not None
            else ExecutionService()
        )

    def execute(
        self,
        conversation: Conversation,
        prompt: str,
        runtime_request: RuntimeRequest,
    ) -> ConversationExecutionResult:
        """Execute conversational request."""

        context = self._context_builder.build(
            conversation
        )

        if self._enricher is not None:
            context = self._enricher.enrich(
                context,
                prompt,
            )

        request = self._request_builder.build(
            context,
            prompt,
            runtime_request.preferred_model
            or "gemma3:4b",
        )

        response = self._executor.execute(
            runtime_request,
            request,
        )

        conversation.add_message(
            Message(
                role="assistant",
                content=response.text,
            )
        )

        return ConversationExecutionResult(
            response=response,
            conversation_id=(
                conversation.conversation_id
            ),
        )


