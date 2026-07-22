"""
Active document service.
"""

from __future__ import annotations

from athena.workspace.models import ActiveDocument


class ActiveDocumentService:
    """Manage the active document."""

    def __init__(self) -> None:
        self._active: ActiveDocument | None = None

    def set_active(
        self,
        document: ActiveDocument,
    ) -> None:
        self._active = document

    def active_document(
        self,
    ) -> ActiveDocument | None:
        return self._active

    def clear(self) -> None:
        self._active = None

    def has_active_document(self) -> bool:
        return self._active is not None