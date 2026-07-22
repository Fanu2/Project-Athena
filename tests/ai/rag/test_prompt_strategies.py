"""
Unit tests for prompt strategies.
"""

from athena.ai.rag.prompts import (
    AnalyzePrompt,
    ComparePrompt,
    DefaultPrompt,
    ExplainPrompt,
    ExtractPrompt,
    SummaryPrompt,
)


QUESTION = "What is Athena?"
CONTEXT = "Athena is an offline AI research assistant."


def test_default_prompt():
    prompt = DefaultPrompt().build(QUESTION, CONTEXT)

    assert QUESTION in prompt
    assert CONTEXT in prompt
    assert "Answer:" in prompt


def test_summary_prompt():
    prompt = SummaryPrompt().build(QUESTION, CONTEXT)

    assert QUESTION in prompt
    assert CONTEXT in prompt
    assert "Summary:" in prompt


def test_compare_prompt():
    prompt = ComparePrompt().build(QUESTION, CONTEXT)

    assert QUESTION in prompt
    assert CONTEXT in prompt
    assert "Comparison:" in prompt


def test_explain_prompt():
    prompt = ExplainPrompt().build(QUESTION, CONTEXT)

    assert QUESTION in prompt
    assert CONTEXT in prompt
    assert "Explanation:" in prompt


def test_extract_prompt():
    prompt = ExtractPrompt().build(QUESTION, CONTEXT)

    assert QUESTION in prompt
    assert CONTEXT in prompt
    assert "Extracted Information:" in prompt


def test_analyze_prompt():
    prompt = AnalyzePrompt().build(QUESTION, CONTEXT)

    assert QUESTION in prompt
    assert CONTEXT in prompt
    assert "Analysis:" in prompt