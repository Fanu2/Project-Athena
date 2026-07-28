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
            sections.append(
                f"[Context {index}]\n{result.text}"
            )

        context = "\n\n".join(sections)

        user_prompt = (
            f"Question:\n"
            f"{request.question}\n\n"
            f"Context:\n"
            f"{context}"
        )

        if request.citations:

            citation_lines = []

            for index, citation in enumerate(
                request.citations,
                start=1,
            ):
                citation_lines.append(
                    f"[{index}] "
                    f"{citation.title} "
                    f"(Page {citation.page_number})"
                )

            user_prompt += (
                "\n\nSources:\n"
                + "\n".join(citation_lines)
            )

        return Prompt(
            system=SYSTEM_PROMPT,
            user=user_prompt,
        )
