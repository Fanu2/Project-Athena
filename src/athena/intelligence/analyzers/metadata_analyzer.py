"""
Metadata analyzer.

Computes basic document statistics.
"""

from __future__ import annotations

from athena.indexing.models import ExtractedDocument

from athena.intelligence.metadata import DocumentMetadata


class MetadataAnalyzer:
    """Computes metadata from extracted documents."""

    def analyze(
        self,
        document: ExtractedDocument,
    ) -> DocumentMetadata:
        """Analyze an extracted document."""

        text = document.text

        word_count = len(text.split())

        character_count = len(text)

        line_count = len(text.splitlines())

        estimated_reading_minutes = max(
            1,
            (word_count + 199) // 200,
        )

        return DocumentMetadata(
            word_count=word_count,
            character_count=character_count,
            line_count=line_count,
            page_count=document.page_count,
            estimated_reading_minutes=estimated_reading_minutes,
        )
