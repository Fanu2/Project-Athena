"""
Summary prompt strategy.
"""

from __future__ import annotations

from .base import PromptStrategy


class SummaryPrompt(PromptStrategy):
    """
    Prompt for document summarization.
    """

    def build(
        self,
        question: str,
        context: str,
    ) -> str:

        return f"""You are Athena, an offline AI research assistant.

Produce a concise, accurate, and well-organized summary of the supplied context.

Use only the supplied context.
Do not introduce outside knowledge.
Preserve important facts and key ideas.

Context
-------
{context}

User Request
------------
{question}

Summary:
""".strip()