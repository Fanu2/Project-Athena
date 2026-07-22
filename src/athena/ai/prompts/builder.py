"""
Prompt builder.
"""

from __future__ import annotations

from athena.ai.prompts.models import Prompt
from athena.ai.prompts.models import PromptRequest
from athena.ai.prompts.templates import SYSTEM_PROMPT


class PromptBuilder:
    """Build prompts for the language model."""

    @staticmethod
    def build(
        request: PromptRequest,
    ) -> Prompt:
        """Build a prompt from retrieved context."""

        sections: list[str] = []

        for index, result in enumerate(request.results, start=1):
            sections.append(f"[Context {index}]\n{result.text}")

        context = "\n\n".join(sections)

        user_prompt = f"Question:\n{request.question}\n\nContext:\n{context}"

        return Prompt(
            system=SYSTEM_PROMPT,
            user=user_prompt,
        )
