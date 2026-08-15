"""
AI provider plugin contract.

Allows plugins to provide Athena LLM providers.
"""

from __future__ import annotations

from abc import abstractmethod

from athena.ai.llm.provider import LLMProvider

from athena.plugins.base import AthenaPlugin


class AIProviderPlugin(AthenaPlugin):
    """
    Plugin capable of providing an LLM provider.
    """

    @abstractmethod
    def create_provider(
        self,
    ) -> LLMProvider:
        """
        Create an LLM runtime provider.
        """

        raise NotImplementedError
