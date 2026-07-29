"""
Conversation intelligence facade.
"""

from __future__ import annotations

from dataclasses import dataclass

from athena.ai.llm.conversation import Conversation
from athena.ai.llm.conversation_analyzer import (
    ConversationAnalyzer,
)
from athena.ai.llm.conversation_metadata import (
    ConversationMetadata,
)
from athena.ai.llm.conversation_summary import (
    ConversationSummary,
    ConversationSummaryService,
)


@dataclass(slots=True)
class ConversationInsight:
    """Combined conversation intelligence."""

    metadata: ConversationMetadata

    summary: ConversationSummary


class ConversationIntelligence:
    """Analyze conversations."""

    def __init__(
        self,
        analyzer: ConversationAnalyzer | None = None,
        summarizer: ConversationSummaryService | None = None,
    ) -> None:
        """Initialize intelligence."""

        self._analyzer = (
            analyzer
            if analyzer is not None
            else ConversationAnalyzer()
        )

        self._summarizer = (
            summarizer
            if summarizer is not None
            else ConversationSummaryService()
        )

    def analyze(
        self,
        conversation: Conversation,
    ) -> ConversationInsight:
        """Generate conversation insight."""

        return ConversationInsight(
            metadata=self._analyzer.analyze(
                conversation
            ),
            summary=self._summarizer.summarize(
                conversation
            ),
        )
