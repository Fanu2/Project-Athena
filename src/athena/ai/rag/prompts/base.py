"""
Base prompt strategy.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class PromptStrategy(ABC):
    """
    Base class for all prompt strategies.
    """

    @abstractmethod
    def build(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Build the prompt presented to the language model.
        """
        raise NotImplementedError