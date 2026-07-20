"""
LLM client.
"""

from __future__ import annotations

from athena.ai.llm.models import LLMRequest
from athena.ai.llm.models import LLMResponse
from athena.ai.llm.provider import LLMProvider


class LLMClient:
    """High-level interface for Athena AI generation."""

    def __init__(
        self,
        provider: LLMProvider,
    ) -> None:
        """Initialize client."""

        self._provider = provider

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Generate text using configured provider.
        """

        return self._provider.generate(
            request,
        )