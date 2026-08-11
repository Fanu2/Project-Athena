"""
Assistant workflow models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssistantWorkflowStep:
    """
    Describes one planned assistant workflow step.
    """

    name: str

    description: str

    category: str = "general"
