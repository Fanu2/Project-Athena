"""
Explanation prompt strategy.
"""

from __future__ import annotations

from .base import PromptStrategy


class ExplainPrompt(PromptStrategy):

    def build(
        self,
        question: str,
        context: str,
    ) -> str:

        return f"""You are Athena, an offline AI research assistant.

Explain the topic clearly and logically.

Use only the supplied context.

If information is missing, state that explicitly.

Context
-------
{context}

Question
--------
{question}

Explanation:
""".strip()