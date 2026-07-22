"""
Models used by the Metadata Engine.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DocumentReference:
    """
    A detected document reference.
    """

    document_id: str
    title: str
    confidence: float


@dataclass(frozen=True, slots=True)
class MetadataResult:
    """
    Result returned by the metadata detector.
    """

    documents: tuple[DocumentReference, ...]

    @property
    def found(self) -> bool:
        return bool(self.documents)