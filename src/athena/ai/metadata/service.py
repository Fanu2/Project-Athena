"""
Public Metadata API.
"""

from __future__ import annotations

from .detector import MetadataDetector
from .models import MetadataResult


class MetadataService:
    """
    Public entry point for metadata detection.
    """

    def __init__(
        self,
        document_titles: tuple[str, ...],
    ) -> None:
        self._detector = MetadataDetector(document_titles)

    def detect(
        self,
        query: str,
    ) -> MetadataResult:
        return self._detector.detect(query)