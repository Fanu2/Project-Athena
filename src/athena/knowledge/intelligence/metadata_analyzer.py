"""
Document metadata analyzer.
"""

from __future__ import annotations

from athena.domain.document import Document

from athena.knowledge.intelligence.document_metadata_profile import (
    DocumentMetadataProfile,
)


class MetadataAnalyzer:
    """
    Analyze document metadata.
    """

    def analyze(
        self,
        document: Document,
    ) -> DocumentMetadataProfile:
        """
        Generate metadata intelligence.
        """

        return DocumentMetadataProfile(
            document_type=document.file_type,
            metadata={
                "filename": document.filename,
                "file_size": document.file_size,
            },
            confidence=1.0,
        )