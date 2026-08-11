"""
Assistant capability registry.

Maps detected intents to Athena capabilities.
"""

from __future__ import annotations

from athena.ai.intent.models import (
    IntentType,
)

from .capability import (
    AssistantCapability,
)


class CapabilityRegistry:
    """
    Provides capability routing rules.
    """

    def __init__(self) -> None:

        self._capabilities = {
            IntentType.SEARCH: AssistantCapability(
                name="retrieval",
                requires_retrieval=True,
            ),

            IntentType.SUMMARIZE: AssistantCapability(
                name="summary",
                requires_retrieval=True,
                requires_evidence=True,
                requires_citations=True,
            ),

            IntentType.EXPLAIN: AssistantCapability(
                name="explanation",
                requires_retrieval=True,
                requires_evidence=True,
                requires_citations=True,
            ),

            IntentType.COMPARE: AssistantCapability(
                name="comparison",
                requires_retrieval=True,
                requires_evidence=True,
                requires_citations=True,
            ),

            IntentType.ANALYZE: AssistantCapability(
                name="analysis",
                requires_retrieval=True,
                requires_evidence=True,
                requires_citations=True,
            ),
        }


    def resolve(
        self,
        intent: IntentType,
    ) -> AssistantCapability:
        """
        Resolve intent into capability.
        """

        return self._capabilities.get(
            intent,
            AssistantCapability(
                name="question_answering",
            ),
        )
