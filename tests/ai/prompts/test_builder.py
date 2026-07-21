"""
Tests for prompt builder.
"""

from __future__ import annotations

from athena.ai.citations import Citation
from athena.ai.prompts import PromptBuilder
from athena.ai.prompts import PromptRequest
from athena.ai.retrieval.models import SemanticResult


def test_build_prompt() -> None:
    """Prompt builder includes question and retrieved context."""

    result = SemanticResult(
        chunk_id="chunk-1",
        document_id="doc-1",
        document_title="Guide.pdf",
        page_number=2,
        start_offset=0,
        end_offset=100,
        text="Athena is an offline AI assistant.",
        score=0.95,
    )

    citation = Citation(
        document_id="doc-1",
        title="Guide.pdf",
        page_number=2,
        start_offset=0,
        end_offset=100,
        score=0.95,
    )

    request = PromptRequest(
        question="What is Athena?",
        results=[result],
        citations=[citation],
    )

    prompt = PromptBuilder.build(request)

    assert "What is Athena?" in prompt.user
    assert "Athena is an offline AI assistant." in prompt.user
    assert "offline AI research assistant" in prompt.system
