"""
Athena Provider Contract

Defines external capability providers
used by the Knowledge Compiler.
"""

from abc import ABC, abstractmethod
from typing import Any


class Provider(ABC):
    """
    Base contract for Athena capability providers.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Provider identifier.
        """
        pass

    @property
    @abstractmethod
    def capabilities(self) -> list[str]:
        """
        Provider capabilities.

        Examples:
            pdf_parser
            ocr
            image_analysis
            embeddings
        """
        pass

    @abstractmethod
    def execute(
        self,
        capability: str,
        input_data: Any,
    ) -> Any:
        """
        Execute a provider capability.
        """
        pass