"""Workspace presentation provider contract."""

from __future__ import annotations

from typing import Protocol, Sequence, runtime_checkable


@runtime_checkable
class WorkspaceViewProvider(Protocol):
    """Provides workspace presentation state to the Athena UI."""

    def build(
        self,
        workspace_id: str,
        active_project_id: str | None = None,
        selected_document_ids: Sequence[str] | None = None,
        selected_note_ids: Sequence[str] | None = None,
    ):
        """Build the current workspace presentation state."""
        ...
