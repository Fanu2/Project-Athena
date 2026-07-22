"""
Comparison prompt strategy.
"""

from __future__ import annotations

from .base import PromptStrategy


class ComparePrompt(PromptStrategy):

    def build(
        self,
        question: str,
        context: str,
    ) -> str:

        return f"""You are Athena, an offline AI research assistant.

Compare the supplied information.

Highlight similarities.
Highlight differences.
Identify agreements and conflicts.

Use only the supplied context.

Context
-------
{context}

User Request
------------
{question}

Comparison:
""".strip()