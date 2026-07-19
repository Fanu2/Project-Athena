"""
Workspace AI settings.

Provides persistence and access to workspace-specific AI configuration.
"""

from .models import AISettings
from .service import AISettingsService

__all__ = [
    "AISettings",
    "AISettingsService",
]