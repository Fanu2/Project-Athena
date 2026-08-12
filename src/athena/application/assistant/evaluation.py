"""
Assistant evaluation models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssistantEvaluationCase:
    """
    Defines an assistant benchmark case.
    """

    name: str

    query: str

    expected_capability: str

    expected_actions: tuple[str, ...] = ()
