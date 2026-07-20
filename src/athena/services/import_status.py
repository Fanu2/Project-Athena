"""
Import status constants.
"""

from __future__ import annotations

from enum import StrEnum


class ImportStatus(StrEnum):
    COPYING = "Copying document..."
    EXTRACTING = "Extracting text..."
    CHUNKING = "Creating chunks..."
    EMBEDDING = "Generating embeddings..."
    SAVING = "Saving index..."
    FINISHED = "Import complete."