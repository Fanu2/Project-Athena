"""
Assistant action validation models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssistantActionValidation:
    """
    Result of validating assistant actions.
    """

    valid: bool

    checks: tuple[str, ...]

    warnings: tuple[str, ...] = ()
