"""
RAG prompt builder.
"""

from __future__ import annotations


class PromptBuilder:
    """Build prompts for document-based answers."""

    def build(
        self,
        question: str,
        context: str,
    ) -> str:
        """Create an instruction prompt."""

        return f"""
You are Athena, a document research assistant.

Rules:
- Answer only using the supplied context.
- Do not invent information.
- If the answer is not in the context, say:
  "The documents do not contain this information."
- Provide a clear explanation.
- Mention relevant sources when available.

Context:
----------------
{context}
----------------

Question:
{question}

Answer:
""".strip()
