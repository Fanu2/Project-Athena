"""
Metadata detection pipeline.
"""

from __future__ import annotations

from .matcher import MetadataMatcher
from .models import MetadataResult


class MetadataDetector:
    """
    Detect document references.
    """

    def __init__(
        self,
        document_titles: tuple[str, ...],
    ) -> None:
        self._matcher = MetadataMatcher(document_titles)

    def detect(
        self,
        query: str,
    ) -> MetadataResult:
        matches = self._matcher.match(query)

        return MetadataResult(
            documents=matches,
        )