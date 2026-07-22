"""
Default prompt strategy.
"""

from __future__ import annotations

from .base import PromptStrategy


class DefaultPrompt(PromptStrategy):
    """
    Generic question answering prompt.
    """

    def build(
        self,
        question: str,
        context: str,
    ) -> str:

        return f"""You are Athena, an offline AI research assistant.

Answer the user's question using ONLY the supplied context.

If the answer cannot be found in the supplied context, clearly state that the information is unavailable.

Do not invent facts.
Do not use outside knowledge.

Context
-------
{context}

Question
--------
{question}

Answer:
""".strip()