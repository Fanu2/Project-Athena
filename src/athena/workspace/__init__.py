"""
Workspace services.
"""

from athena.workspace.models import ActiveDocument
from athena.workspace.service import ActiveDocumentService

__all__ = [
    "ActiveDocument",
    "ActiveDocumentService",
]