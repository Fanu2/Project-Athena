"""
Base interface for LLM providers.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from athena.ai.llm.metadata import ProviderMetadata
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

    @property
    def metadata(self) -> ProviderMetadata:
        """Return provider metadata."""

        return ProviderMetadata(
            name=self.provider_name,
            display_name=self.provider_name.title(),
            local=True,
            requires_api_key=False,
            supports_chat=True,
            supports_streaming=False,
            supports_tools=False,
            supports_vision=False,
        )

    def capabilities(self) -> dict[str, bool]:
        """Return provider capabilities."""

        return {
            "chat": True,
            "vision": False,
            "embedding": False,
            "streaming": False,
            "tools": False,
        }
