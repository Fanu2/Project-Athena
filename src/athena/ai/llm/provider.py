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

    @abstractmethod
    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Generate a response.

        Implemented by concrete providers.
        """
        raise NotImplementedError
