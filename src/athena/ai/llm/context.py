"""
LLM execution context builder.
"""

from __future__ import annotations

from dataclasses import dataclass

from athena.ai.llm.message import Message
from athena.ai.llm.models import LLMRequest
from athena.ai.llm.session import LLMSession


@dataclass(frozen=True, slots=True)
class LLMContext:
    """Execution context."""

    system_prompt: str

    messages: list[Message]


class ContextBuilder:
    """Build execution context from session."""

    def build(
        self,
        session: LLMSession,
    ) -> LLMContext:
        """Create context from session."""

        return LLMContext(
            system_prompt=session.system_prompt,
            messages=session.history(),
        )

    def build_request(
        self,
        session: LLMSession,
        user_prompt: str,
    ) -> LLMRequest:
        """Create provider request from session."""

        return LLMRequest(
            system_prompt=session.system_prompt,
            user_prompt=user_prompt,
            model_name=(
                session.model
                if session.model is not None
                else "gemma3:4b"
            ),
        )
