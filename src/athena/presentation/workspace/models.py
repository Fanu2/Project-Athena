"""Workspace presentation models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class WorkspaceSummary(BaseModel):
    id: str
    name: str
    project_count: int = 0
    document_count: int = 0
    note_count: int = 0


class ProjectSummary(BaseModel):
    id: str
    workspace_id: str
    name: str
    collection_count: int = 0


class CollectionSummary(BaseModel):
    id: str
    project_id: str
    name: str
    document_count: int = 0


class DocumentSummary(BaseModel):
    id: str
    collection_id: str
    filename: str
    file_type: str
    storage_key: str | None = None


class NoteSummary(BaseModel):
    id: str
    workspace_id: str
    title: str


class WorkspaceViewModel(BaseModel):
    workspace: WorkspaceSummary | None = None
    projects: list[ProjectSummary] = Field(
        default_factory=list,
    )
    collections: list[CollectionSummary] = Field(
        default_factory=list,
    )
    documents: list[DocumentSummary] = Field(
        default_factory=list,
    )
    notes: list[NoteSummary] = Field(
        default_factory=list,
    )
    active_project_id: str | None = None
    selected_document_ids: list[str] = Field(
        default_factory=list,
    )
    selected_note_ids: list[str] = Field(
        default_factory=list,
    )
