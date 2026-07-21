"""
Import summary domain model.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ImportSummary:
    """Summary of a batch document import."""

    total: int = 0

    imported: int = 0

    skipped: int = 0

    failed: int = 0

    elapsed: float = 0.0

    cancelled: bool = False

    imported_documents: list[str] = field(default_factory=list)

    skipped_documents: list[str] = field(default_factory=list)

    failed_documents: list[str] = field(default_factory=list)
