"""Bridge Athena workspace services into the A20 workspace presentation model."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from athena.core.application_context import ApplicationContext
from athena.presentation.workspace.provider import WorkspaceViewProvider

from athena.presentation.workspace.models import (
    CollectionSummary,
    DocumentSummary,
    NoteSummary,
    ProjectSummary,
    WorkspaceSummary,
    WorkspaceViewModel,
)


class AthenaWorkspaceProvider(WorkspaceViewProvider):
    """Build A20 presentation state from Athena workspace services."""

    def __init__(self, context: ApplicationContext) -> None:
        self.context = context

    def build(
        self,
        workspace_id: str,
        active_project_id: str | None = None,
        selected_document_ids: Sequence[str] | None = None,
        selected_note_ids: Sequence[str] | None = None,
    ) -> WorkspaceViewModel:
        workspace = self.context.current_workspace

        if workspace is None:
            raise ValueError("Workspace does not exist")

        if str(workspace.workspace_id) != workspace_id:
            raise ValueError("Workspace does not exist")

        collections = (
            self.context.collection_service.list_collections()
            if self.context.collection_service is not None
            else []
        )

        documents = (
            self.context.document_service.list_documents()
            if self.context.document_service is not None
            else []
        )

        notes = (
            self.context.note_service.list_notes()
            if self.context.note_service is not None
            else []
        )

        document_by_id = {
            document.id: document
            for document in documents
        }

        document_ids = {document.id for document in documents}
        note_ids = {
            note.document_id
            for note in notes
            if note.document_id in document_by_id
        }

        collection_summaries = [
            CollectionSummary(
                id=str(collection.id),
                project_id="",
                name=collection.name,
                document_count=len(
                    self.context.collection_service.list_documents(
                        collection.id,
                    )
                )
                if self.context.collection_service is not None
                else 0,
            )
            for collection in collections
        ]

        document_summaries = [
            DocumentSummary(
                id=document.id,
                collection_id="",
                filename=document.name,
                file_type=Path(document.name).suffix.lstrip("."),
            )
            for document in documents
        ]

        note_summaries = [
            NoteSummary(
                id=note.document_id,
                workspace_id=str(workspace.workspace_id),
                title=(
                    document_by_id[note.document_id].name
                    if note.document_id in document_by_id
                    else note.document_id
                ),
            )
            for note in notes
            if note.document_id in document_by_id
        ]

        valid_selected_documents = [
            document_id
            for document_id in (selected_document_ids or [])
            if document_id in document_ids
        ]

        valid_selected_notes = [
            note_id
            for note_id in (selected_note_ids or [])
            if note_id in note_ids
        ]

        return WorkspaceViewModel(
            workspace=WorkspaceSummary(
                id=str(workspace.workspace_id),
                name=workspace.name,
                project_count=0,
                document_count=len(documents),
                note_count=len(note_summaries),
            ),
            projects=[
                ProjectSummary(
                    id="",
                    workspace_id=str(workspace.workspace_id),
                    name="",
                    collection_count=0,
                )
            ] if False else [],
            collections=collection_summaries,
            documents=document_summaries,
            notes=note_summaries,
            active_project_id=(
                active_project_id
                if active_project_id is not None
                else None
            ),
            selected_document_ids=valid_selected_documents,
            selected_note_ids=valid_selected_notes,
        )
