"""
Public scanning API for AEAF.

This module provides the high-level interface for discovering source files
within a software repository. The actual filesystem traversal is delegated
to the RepositoryScanner implementation.

The scanner stage is responsible only for locating files and collecting
basic repository metadata. It does not parse source code or perform any
analysis.
"""

from __future__ import annotations

from pathlib import Path

from .config import AEAFConfig
from .models import RepositoryModel
from .scanners.repository_scanner import RepositoryScanner


class Scanner:
    """
    Public interface for repository scanning.
    """

    def __init__(self, config: AEAFConfig | None = None) -> None:
        self._config = config or AEAFConfig()
        self._scanner = RepositoryScanner(self._config)

    def scan(self, root: str | Path) -> RepositoryModel:
        """
        Scan a project directory.

        Parameters
        ----------
        root:
            Root directory of the repository.

        Returns
        -------
        RepositoryModel
            Repository populated with discovered files.
        """
        return self._scanner.scan(Path(root))


def scan(
    root: str | Path,
    config: AEAFConfig | None = None,
) -> RepositoryModel:
    """
    Convenience function.

    Example
    -------
    >>> repository = scan("C:/Projects/Athena")
    """

    return Scanner(config).scan(root)