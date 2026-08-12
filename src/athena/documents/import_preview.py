"""
Workspace import preview models.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class ImportPreview:
    """
    Summary of a folder before importing.
    """

    source_folder: Path

    supported_files: tuple[Path, ...]

    unsupported_count: int

    file_types: dict[str, int]

    @property
    def supported_count(
        self,
    ) -> int:
        """
        Return supported document count.
        """

        return len(
            self.supported_files,
        )
