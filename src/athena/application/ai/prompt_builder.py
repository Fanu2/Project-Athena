"""
Prompt builder for AI generation.
"""

from __future__ import annotations

from athena.domain.ai.question import Question
from athena.domain.ai.retrieval_result import RetrievalResult


class PromptBuilder:
    """Build prompts for the language model."""

    def build(
        self,
        question: Question,
        evidence: list[RetrievalResult],
    ) -> str:
        """Build a prompt from a question and supporting evidence."""

        sections: list[str] = [
            (
                "You are Athena, an AI research assistant. "
                "Answer the question using only the supplied evidence. "
                "If the evidence is insufficient, state that clearly."
            ),
            "",
            f"Question:\n{question.text}",
            "",
            "Evidence:",
        ]

        if not evidence:
            sections.append("(No supporting evidence available.)")
        else:
            for index, item in enumerate(evidence, start=1):
                sections.extend(
                    [
                        f"[{index}] {item.document_name} (Page {item.page})",
                        item.text,
                        "",
                    ]
                )

        sections.extend(
            [
                "Answer:",
            ]
        )

        return "\n".join(sections)
