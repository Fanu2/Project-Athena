"""
Athena Docling Provider

Adapter around Athena's document extraction layer.
"""

from pathlib import Path
from typing import Any, Protocol

from athena.indexing.extractors.docling_pdf import (
    DoclingPDFExtractor,
)

from ..contracts.provider import Provider
from ..domain.import_artifact import ImportArtifact


class DocumentExtractor(Protocol):
    """
    Extraction contract used by provider.
    """

    def extract(
        self,
        document: Path,
    ) -> Any:
        ...


class DoclingProvider(Provider):
    """
    Provides document acquisition through Docling.
    """

    def __init__(
        self,
        extractor: DocumentExtractor | None = None,
    ) -> None:

        self._extractor = (
            extractor
            if extractor is not None
            else DoclingPDFExtractor()
        )

    @property
    def name(self) -> str:
        return "docling"

    @property
    def capabilities(self) -> list[str]:
        return [
            "document_structure_extraction",
        ]

    def execute(
        self,
        capability: str,
        input_data: Any,
    ) -> ImportArtifact:
        """
        Extract document and create
        normalized acquisition artifact.
        """

        if capability not in self.capabilities:
            raise ValueError(
                f"Unsupported capability: {capability}"
            )

        extracted = self._extractor.extract(
            Path(input_data)
        )

        artifact = ImportArtifact(
            artifact_type="document",
            content_reference=str(
                extracted.path
            ),
        )

        artifact.add_metadata(
            "title",
            extracted.title,
        )

        artifact.add_metadata(
            "document_id",
            extracted.document_id,
        )

        artifact.add_metadata(
            "page_count",
            extracted.page_count,
        )

        artifact.add_metadata(
            "text_length",
            len(extracted.text),
        )

        # Provenance metadata
        artifact.add_metadata(
            "source_path",
            str(extracted.path),
        )

        artifact.add_metadata(
            "provider",
            self.name,
        )

        artifact.add_metadata(
            "extraction_method",
            "docling",
        )

        return artifact