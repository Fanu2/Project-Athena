"""
Athena Calibre Provider

Provides book acquisition from a Calibre library.
"""

from pathlib import Path
from typing import Any

from ..contracts.provider import Provider
from ..domain.import_artifact import ImportArtifact
from .calibre_library import CalibreLibraryReader


class CalibreProvider(Provider):
    """
    Provides Calibre library acquisition.
    """

    def __init__(self) -> None:
        pass

    @property
    def name(self) -> str:
        return "calibre"

    @property
    def capabilities(self) -> list[str]:
        return [
            "library_scan",
            "book_metadata_import",
        ]

    def execute(
        self,
        capability: str,
        input_data: Any,
    ) -> Any:
        """
        Execute Calibre capability.
        """

        if capability not in self.capabilities:
            raise ValueError(
                f"Unsupported capability: {capability}"
            )

        if capability == "library_scan":

            library = CalibreLibraryReader(
                Path(input_data)
            )

            return library.list_books()

        library = CalibreLibraryReader(
            Path(
                input_data["library_path"]
            )
        )

        metadata = library.get_book(
            int(
                input_data["book_id"]
            )
        )

        artifact = ImportArtifact(
            artifact_type="book",
            content_reference=metadata["path"],
        )

        for key, value in metadata.items():
            artifact.add_metadata(
                key,
                value,
            )

        artifact.add_metadata(
            "provider",
            self.name,
        )

        artifact.add_metadata(
            "source_type",
            "calibre",
        )

        return artifact