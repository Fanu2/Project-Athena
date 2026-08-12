"""
Assistant evaluation benchmark dataset.
"""

from __future__ import annotations

from .evaluation import (
    AssistantEvaluationCase,
)


ASSISTANT_CORE_BENCHMARKS = (
    AssistantEvaluationCase(
        name="search_documents",
        query="find documents about revenue records",
        expected_capability="retrieval",
        expected_actions=(
            "retrieve_information",
        ),
    ),

    AssistantEvaluationCase(
        name="summarize_documents",
        query="summarize these documents",
        expected_capability="summary",
        expected_actions=(
            "retrieve_information",
            "build_evidence",
            "generate_response",
            "attach_citations",
        ),
    ),

    AssistantEvaluationCase(
        name="explain_topic",
        query="explain this topic",
        expected_capability="explanation",
        expected_actions=(
            "retrieve_information",
            "build_evidence",
            "generate_response",
            "attach_citations",
        ),
    ),

    AssistantEvaluationCase(
        name="compare_items",
        query="compare these documents",
        expected_capability="comparison",
        expected_actions=(
            "retrieve_information",
            "build_evidence",
            "generate_response",
            "attach_citations",
        ),
    ),

    AssistantEvaluationCase(
        name="analyze_information",
        query="analyze this information",
        expected_capability="analysis",
        expected_actions=(
            "retrieve_information",
            "build_evidence",
            "generate_response",
            "attach_citations",
        ),
    ),
)
