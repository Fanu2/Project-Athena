"""
Tests for assistant workspace integration.
"""

from athena.application.assistant.workspace_adapter import (
    AssistantWorkspaceAdapter,
)


class FakeWorkspaceService:

    def library_summary(self):
        return {
            "documents": 3,
            "pages": 20,
        }

    def describe_library(self):
        return None


def test_workspace_adapter_summary():

    adapter = AssistantWorkspaceAdapter(
        FakeWorkspaceService(),
    )

    summary = adapter.library_summary()

    assert summary["documents"] == 3

    assert summary["pages"] == 20
