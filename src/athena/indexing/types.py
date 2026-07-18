"""
Shared indexing type aliases.
"""

from __future__ import annotations

from pathlib import Path
from typing import TypeAlias

DocumentId: TypeAlias = str

ChunkId: TypeAlias = str

EmbeddingVector: TypeAlias = list[float]

DocumentPath: TypeAlias = Path
