"""
Athena Chunking Engine.

Structure-aware document chunking pipeline.
"""

from .builder import ChunkBuilder
from .engine import ChunkingEngine
from .metadata import MetadataBuilder
from .models import (
    BlockType,
    ChunkCandidate,
    ChunkType,
    DocumentBlock,
)
from .parser import DocumentParser
from .splitter import ChunkSplitter

__all__ = [
    "BlockType",
    "ChunkType",
    "DocumentBlock",
    "ChunkCandidate",
    "DocumentParser",
    "ChunkSplitter",
    "ChunkBuilder",
    "MetadataBuilder",
    "ChunkingEngine",
]