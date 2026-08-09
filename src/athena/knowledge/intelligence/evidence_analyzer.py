"""
Evidence analyzer for document intelligence.
"""

from __future__ import annotations

from athena.domain.document import Document

from athena.knowledge.intelligence.evidence_profile import (
    EvidenceProfile,
)


class EvidenceAnalyzer:
    """
    Extract evidence intelligence from documents.
    """

    def analyze(
        self,
        document: Document,
    ) -> list[EvidenceProfile]:
        """
        Create evidence profiles.

        Initial implementation:
        captures document provenance.
        """

        return [
            EvidenceProfile(
                source_document=document.id,
                evidence_type="document",
                content=document.title,
                location=str(
                    document.file_path,
                ),
                confidence=1.0,
                metadata={
                    "filename": document.filename,
                    "file_type": document.file_type,
                },
            )
        ]