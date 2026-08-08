"""
Embedding service.

Converts text into vector embeddings.
"""

from __future__ import annotations

import os
from typing import cast

# Prevent ML libraries from creating aggressive worker pools
# inside the Qt application process.

os.environ.setdefault(
    "TOKENIZERS_PARALLELISM",
    "false",
)

os.environ.setdefault(
    "OMP_NUM_THREADS",
    "1",
)

os.environ.setdefault(
    "MKL_NUM_THREADS",
    "1",
)

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """Generate text embeddings."""

    def __init__(
        self,
        model_name: str = "BAAI/bge-m3",
    ) -> None:
        """Initialize embedding model."""

        self._model = SentenceTransformer(
            model_name,
        )

    def embed(
        self,
        text: str,
    ) -> list[float]:
        """Generate embedding for text."""

        vector = self._model.encode(
            text,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return cast(
            list[float],
            vector.tolist(),
        )

    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Generate embeddings for multiple texts."""

        vectors = self._model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
            batch_size=1,
        )

        return cast(
            list[list[float]],
            vectors.tolist(),
        )