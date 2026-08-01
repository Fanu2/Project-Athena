"""
Citation validation model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CitationValidation:
    """Validation result for a citation."""

    supported: bool

    confidence: float

    reasons: tuple[str, ...] = ()