"""
Document import reporting models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class ImportReport:
    """
    Result of importing a folder into Athena.
    """

    source_folder: Path

    discovered: int = 0

    imported: list[Path] = field(
        default_factory=list,
    )

    failed: list[str] = field(
        default_factory=list,
    )

    unsupported: list[Path] = field(
        default_factory=list,
    )

    @property
    def imported_count(
        self,
    ) -> int:
        """Return number of imported documents."""

        return len(self.imported)

    @property
    def failed_count(
        self,
    ) -> int:
        """Return number of failed imports."""

        return len(self.failed)
