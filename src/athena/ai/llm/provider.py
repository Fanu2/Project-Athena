"""
Base interface for LLM providers.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from athena.ai.llm.models import (
    LLMRequest,
    LLMResponse,
)


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return provider identifier."""

    @abstractmethod
    def analyze(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """Generate a response."""

    def list_models(self) -> list[str]:
        """Return available models."""

        return []

    def health(self) -> bool:
        """Return provider health."""

        return True

    def validate_configuration(self) -> None:
        """Validate provider configuration."""

        return

    def capabilities(self) -> dict[str, bool]:
        """Return provider capabilities."""

        return {
            "chat": True,
            "vision": False,
            "embedding": False,
            "streaming": False,
            "tools": False,
        }
