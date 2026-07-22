"""
Analysis prompt strategy.
"""

from __future__ import annotations

from .base import PromptStrategy


class AnalyzePrompt(PromptStrategy):

    def build(
        self,
        question: str,
        context: str,
    ) -> str:

        return f"""You are Athena, an offline AI research assistant.

Analyze the supplied information carefully.

Identify important patterns, relationships, implications, and conclusions.

Support every conclusion using only the supplied context.

Context
-------
{context}

User Request
------------
{question}

Analysis:
""".strip()