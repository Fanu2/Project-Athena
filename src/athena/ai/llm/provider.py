"""
LLM provider interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from athena.ai.llm.models import (
    LLMRequest,
    LLMResponse,
)


class LLMProvider(ABC):
    """Abstract language model provider."""

    @abstractmethod
    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """Generate a response."""

        raise NotImplementedError
