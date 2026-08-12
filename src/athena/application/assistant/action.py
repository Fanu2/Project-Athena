"""
Assistant action models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssistantAction:
    """
    Describes a controlled assistant action.

    Actions are declarative.
    They do not execute.
    """

    name: str

    description: str

    requires_confirmation: bool = False
