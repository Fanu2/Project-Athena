from athena.presentation.workspace.provider import WorkspaceViewProvider


class FakeWorkspaceProvider:
    def build(
        self,
        workspace_id: str,
        active_project_id: str | None = None,
        selected_document_ids: list[str] | None = None,
        selected_note_ids: list[str] | None = None,
    ):
        return {
            "workspace_id": workspace_id,
            "active_project_id": active_project_id,
            "selected_document_ids": selected_document_ids or [],
            "selected_note_ids": selected_note_ids or [],
        }


def test_workspace_provider_protocol():
    provider = FakeWorkspaceProvider()

    assert isinstance(provider, WorkspaceViewProvider)

    result = provider.build(
        "workspace-1",
        active_project_id="project-1",
        selected_document_ids=["document-1"],
        selected_note_ids=["note-1"],
    )

    assert result["workspace_id"] == "workspace-1"
    assert result["active_project_id"] == "project-1"
    assert result["selected_document_ids"] == ["document-1"]
    assert result["selected_note_ids"] == ["note-1"]
