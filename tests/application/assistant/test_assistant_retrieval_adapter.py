"""
Tests for assistant retrieval integration.
"""

from athena.application.assistant.retrieval_adapter import (
    AssistantRetrievalAdapter,
)


class FakeRetrievalService:

    def retrieve(self, question):
        return [
            question.text
        ]

    def retrieve_evidence(self, question):
        return [
            question.text
        ]


def test_assistant_retrieval_adapter():

    adapter = AssistantRetrievalAdapter(
        FakeRetrievalService(),
    )

    results = adapter.retrieve(
        "find documents",
    )

    assert results == [
        "find documents"
    ]


def test_assistant_retrieval_evidence():

    adapter = AssistantRetrievalAdapter(
        FakeRetrievalService(),
    )

    results = adapter.retrieve_evidence(
        "find evidence",
    )

    assert results == [
        "find evidence"
    ]
