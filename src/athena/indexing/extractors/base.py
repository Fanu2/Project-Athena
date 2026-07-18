"""
Base document extractor.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from pathlib import Path

from athena.indexing.models import ExtractedDocument


class BaseExtractor(ABC):
    """Abstract base class for all document extractors."""

    @property
    @abstractmethod
    def supported_extensions(self) -> tuple[str, ...]:
        """Return supported filename extensions."""

    @abstractmethod
    def extract(
        self,
        document: Path,
    ) -> ExtractedDocument:
        """
        Extract text from a document.

        Args:
            document:
                Path to the document.

        Returns:
            ExtractedDocument.
        """
