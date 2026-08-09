"""
Combined document intelligence result.
"""

from __future__ import annotations

from dataclasses import dataclass

from athena.knowledge.intelligence.document_metadata_profile import (
    DocumentMetadataProfile,
)

from athena.knowledge.intelligence.document_profile import (
    DocumentProfile,
)

from athena.knowledge.intelligence.document_structure import (
    DocumentStructureNode,
)


@dataclass(slots=True)
class DocumentIntelligence:
    """
    Complete intelligence result for a document.
    """

    profile: DocumentProfile

    metadata: DocumentMetadataProfile

    structure: list[DocumentStructureNode]