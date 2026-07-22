"""
RAG prompt builder.
"""

from __future__ import annotations

from athena.ai.intent.models import IntentResult, IntentType

from athena.ai.rag.prompts import (
    AnalyzePrompt,
    ComparePrompt,
    DefaultPrompt,
    ExplainPrompt,
    ExtractPrompt,
    PromptStrategy,
    SummaryPrompt,
)


class PromptBuilder:
    """Select the appropriate prompt strategy based on user intent."""

    _STRATEGIES: dict[IntentType, PromptStrategy] = {
        IntentType.SUMMARIZE: SummaryPrompt(),
        IntentType.COMPARE: ComparePrompt(),
        IntentType.EXPLAIN: ExplainPrompt(),
        IntentType.EXTRACT: ExtractPrompt(),
        IntentType.ANALYZE: AnalyzePrompt(),
        IntentType.QUESTION: DefaultPrompt(),
        IntentType.SEARCH: DefaultPrompt(),
        IntentType.TRANSFORM: DefaultPrompt(),
        IntentType.CREATIVE: DefaultPrompt(),
        IntentType.UNKNOWN: DefaultPrompt(),
    }

    def build(
        self,
        question: str,
        context: str,
        intent: IntentResult,
    ) -> str:
        """
        Build a prompt using the strategy associated with the detected intent.

        Parameters
        ----------
        question
            User's original question.

        context
            Retrieved document context.

        intent
            Detected user intent.

        Returns
        -------
        str
            Prompt presented to the language model.
        """

        strategy = self._STRATEGIES.get(
            intent.intent,
            DefaultPrompt(),
        )

        return strategy.build(
            question=question,
            context=context,
        )