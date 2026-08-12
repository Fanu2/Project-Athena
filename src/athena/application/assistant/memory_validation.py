"""
Assistant memory validation models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssistantMemoryValidation:
    """
    Result of validating an assistant memory item.
    """

    valid: bool

    checks: tuple[str, ...]

    warnings: tuple[str, ...] = ()
