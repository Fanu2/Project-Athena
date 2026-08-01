"""
Application-wide UI events.

This module provides a lightweight event bus used to notify
independent UI components about application events without
creating direct dependencies between pages.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QObject, Signal


class ApplicationEvents(QObject):
    """
    Application-wide event dispatcher.

    Events are shared between independent UI components.
    """

    #: Emitted whenever one or more documents have been imported
    #: and indexing has completed successfully.
    #:
    #: Payload:
    #: {
    #:     "total": int,
    #:     "imported": int,
    #:     "skipped": int,
    #:     "failed": int,
    #:     "elapsed": float,
    #: }
    documents_imported = Signal(dict)

    #: Emitted whenever one or more documents have been deleted.
    document_deleted = Signal()

    #: Emitted when a workspace has been opened.
    workspace_opened = Signal()

    #: Emitted when the current workspace has been closed.
    workspace_closed = Signal()


# Global singleton used throughout the application.
events = ApplicationEvents()