"""
Tests for assistant evidence integration.
"""

from athena.application.assistant.evidence_adapter import (
    AssistantEvidenceAdapter,
)


def test_evidence_adapter_builds_context():

    adapter = AssistantEvidenceAdapter()

    context = adapter.build_context(
        [],
    )

    assert (
        context.records
        == ()
    )
