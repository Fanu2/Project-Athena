"""
Conversation request builder.
"""

from __future__ import annotations

from athena.ai.llm.context_formatter import (
    ContextFormatter,
)
from athena.ai.llm.conversation_context import (
    ConversationContext,
)
from athena.ai.llm.models import LLMRequest


class ConversationRequestBuilder:
    """Build LLM requests from conversation context."""

    def __init__(
        self,
        formatter: ContextFormatter | None = None,
    ) -> None:
        """Initialize builder."""

        self._formatter = (
            formatter
            if formatter is not None
            else ContextFormatter()
        )

    def build(
        self,
        context: ConversationContext,
        prompt: str,
        model_name: str,
    ) -> LLMRequest:
        """Create enriched LLM request."""

        return LLMRequest(
            system_prompt="",
            user_prompt=self._formatter.format(
                context,
                prompt,
            ),
            model_name=model_name,
        )
