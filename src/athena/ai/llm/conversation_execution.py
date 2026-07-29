"""
Conversation execution models.
"""

from __future__ import annotations

from dataclasses import dataclass

from athena.ai.llm.models import LLMResponse


@dataclass(slots=True)
class ConversationExecutionResult:
    """Result of conversational execution."""

    response: LLMResponse

    conversation_id: str
