"""
Assistant capability models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssistantCapability:
    """
    Represents a capability required
    to complete an assistant task.
    """

    name: str

    requires_retrieval: bool = False

    requires_evidence: bool = False

    requires_citations: bool = False
