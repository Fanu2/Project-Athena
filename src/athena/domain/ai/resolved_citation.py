"""
Resolved citation model.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class ResolvedCitation:
    """
    Citation enriched with explanation and navigation data.

    This object is used by:
    - Citation Intelligence UI
    - Citation validation display
    - Document navigation
    """

    document_name: str

    document_path: Path | None = None

    page: int = 1

    snippet: str = ""

    score: float = 0.0

    reasons: tuple[str, ...] = ()