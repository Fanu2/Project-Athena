"""
Assistant decision models.
"""

from __future__ import annotations

from dataclasses import dataclass

from athena.ai.intent.models import IntentType

from .capability import AssistantCapability


@dataclass(slots=True)
class AssistantDecision:
    """
    Represents the assistant routing decision.
    """

    intent: IntentType

    capability: AssistantCapability

    confidence: float
