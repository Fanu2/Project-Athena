"""
Metadata detection package.
"""

from .models import (
    DocumentReference,
    MetadataResult,
)
from .service import MetadataService

__all__ = [
    "DocumentReference",
    "MetadataResult",
    "MetadataService",
]