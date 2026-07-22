"""
Extraction prompt strategy.
"""

from __future__ import annotations

from .base import PromptStrategy


class ExtractPrompt(PromptStrategy):

    def build(
        self,
        question: str,
        context: str,
    ) -> str:

        return f"""You are Athena, an offline AI research assistant.

Extract only the information requested.

Do not summarize.
Do not explain beyond what is requested.
If the requested information is absent, say so.

Context
-------
{context}

User Request
------------
{question}

Extracted Information:
""".strip()