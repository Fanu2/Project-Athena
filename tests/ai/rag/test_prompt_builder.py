"""
Unit tests for PromptBuilder.
"""

from athena.ai.intent.models import IntentResult, IntentType
from athena.ai.rag.prompt_builder import PromptBuilder


QUESTION = "What is Athena?"
CONTEXT = "Athena is an offline AI research assistant."


def make_intent(intent: IntentType) -> IntentResult:
    return IntentResult(
        intent=intent,
        confidence=1.0,
        matched_keywords=(),
        normalized_query="",
    )


def test_summary_prompt_selected():
    builder = PromptBuilder()

    prompt = builder.build(
        QUESTION,
        CONTEXT,
        make_intent(IntentType.SUMMARIZE),
    )

    assert "Summary:" in prompt


def test_compare_prompt_selected():
    builder = PromptBuilder()

    prompt = builder.build(
        QUESTION,
        CONTEXT,
        make_intent(IntentType.COMPARE),
    )

    assert "Comparison:" in prompt


def test_explain_prompt_selected():
    builder = PromptBuilder()

    prompt = builder.build(
        QUESTION,
        CONTEXT,
        make_intent(IntentType.EXPLAIN),
    )

    assert "Explanation:" in prompt


def test_extract_prompt_selected():
    builder = PromptBuilder()

    prompt = builder.build(
        QUESTION,
        CONTEXT,
        make_intent(IntentType.EXTRACT),
    )

    assert "Extracted Information:" in prompt


def test_analyze_prompt_selected():
    builder = PromptBuilder()

    prompt = builder.build(
        QUESTION,
        CONTEXT,
        make_intent(IntentType.ANALYZE),
    )

    assert "Analysis:" in prompt


def test_default_prompt_selected():
    builder = PromptBuilder()

    prompt = builder.build(
        QUESTION,
        CONTEXT,
        make_intent(IntentType.UNKNOWN),
    )

    assert "Answer:" in prompt