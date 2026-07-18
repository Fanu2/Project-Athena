"""
Indexing exceptions.
"""


class IndexingError(Exception):
    """Base indexing exception."""


class ExtractionError(IndexingError):
    """Raised when document extraction fails."""


class UnsupportedDocumentError(ExtractionError):
    """Raised for unsupported document types."""


class ChunkingError(IndexingError):
    """Raised when chunk generation fails."""


class EmbeddingError(IndexingError):
    """Raised when embedding generation fails."""


class StorageError(IndexingError):
    """Raised when index storage fails."""
