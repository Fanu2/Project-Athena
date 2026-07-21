"""
Abstract interface for Large Language Model providers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from athena.domain.ai.configuration import AIConfiguration


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        configuration: AIConfiguration,
    ) -> str:
        """
        Generate a response for a prompt.

        Parameters
        ----------
        prompt:
            Prompt to send to the model.

        configuration:
            AI generation configuration.

        Returns
        -------
        str
            Generated response.
        """
        raise NotImplementedError

    @abstractmethod
    def list_models(self) -> list[str]:
        """
        Return the names of installed language models.

        Returns
        -------
        list[str]
            List of installed model names.
        """
        raise NotImplementedError
