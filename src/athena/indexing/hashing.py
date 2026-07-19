"""
Document hashing utilities.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_file(path: Path) -> str:
    """
    Compute the SHA-256 hash of a file.

    Args:
        path:
            File to hash.

    Returns:
        Hexadecimal SHA-256 digest.
    """

    hasher = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            hasher.update(chunk)

    return hasher.hexdigest()
