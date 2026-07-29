"""
LLM provider interface.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from athena.ai.llm.models import LLMRequest
from athena.ai.llm.models import LLMResponse


class LLMProvider(ABC):
    """Abstract LLM provider."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Unique provider identifier.

        Examples:
            "ollama"
            "lmstudio"
        """
        raise NotImplementedError

    @abstractmethod
    def analyze(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Generate a response.

        Implemented by concrete providers.
        """
        raise NotImplementedError

    def list_models(self) -> list[str]:
        """
        Return available models.

        Providers supporting model discovery should override this.
        """
        raise NotImplementedError(
            f"{self.provider_name} does not support model discovery."
        )

    def health(self) -> bool:
        """
        Return provider health.

        Providers may override this.
        """
        return True
