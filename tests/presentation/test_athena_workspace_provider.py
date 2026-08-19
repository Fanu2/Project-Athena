from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

from athena.presentation.workspace.athena_workspace_provider import (
    AthenaWorkspaceProvider,
)


def test_provider_builds_workspace_view():
    workspace_id = uuid4()

    workspace = SimpleNamespace(
        workspace_id=workspace_id,
        name="Athena Research",
    )

    document = SimpleNamespace(
        id="document-1",
        name="research.pdf",
        path=Path("/workspace/documents/research.pdf"),
    )

    collection = SimpleNamespace(
        id=uuid4(),
        name="Research",
    )

    note = SimpleNamespace(
        document_id="document-1",
    )

    collection_service = SimpleNamespace(
        list_collections=lambda: [collection],
        list_documents=lambda collection_id: ["document-1"],
    )

    document_service = SimpleNamespace(
        list_documents=lambda: [document],
    )

    note_service = SimpleNamespace(
        list_notes=lambda: [note],
    )

    context = SimpleNamespace(
        current_workspace=workspace,
        collection_service=collection_service,
        document_service=document_service,
        note_service=note_service,
    )

    provider = AthenaWorkspaceProvider(context)

    model = provider.build(str(workspace_id))

    assert model.workspace is not None
    assert model.workspace.name == "Athena Research"
    assert model.workspace.project_count == 0
    assert model.workspace.document_count == 1
    assert model.workspace.note_count == 1

    assert len(model.collections) == 1
    assert model.collections[0].name == "Research"

    assert len(model.documents) == 1
    assert model.documents[0].filename == "research.pdf"
    assert model.documents[0].file_type == "pdf"

    assert len(model.notes) == 1
    assert model.notes[0].title == "research.pdf"


def test_provider_rejects_wrong_workspace():
    workspace_id = uuid4()

    context = SimpleNamespace(
        current_workspace=SimpleNamespace(
            workspace_id=workspace_id,
            name="Athena Research",
        ),
        collection_service=None,
        document_service=None,
        note_service=None,
    )

    provider = AthenaWorkspaceProvider(context)

    try:
        provider.build(str(uuid4()))
        assert False
    except ValueError as exc:
        assert str(exc) == "Workspace does not exist"
