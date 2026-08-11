"""
Assistant plan validation models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssistantPlanValidation:
    """
    Result of validating an assistant plan.
    """

    valid: bool

    checks: tuple[str, ...]

    warnings: tuple[str, ...] = ()
