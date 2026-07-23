"""
Repository filesystem scanner.

Discovers Python source files and basic repository metadata.
"""

from __future__ import annotations

from pathlib import Path

from ..config import AEAFConfig
from ..models import RepositoryMetadata
from ..models import RepositoryModel
from ..models import SourceFile


class RepositoryScanner:
    """
    Discover Python source files inside a repository.
    """

    DEFAULT_IGNORES = {
        ".git",
        ".idea",
        ".vscode",
        ".venv",
        "venv",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "build",
        "dist",
        ".tox",
        "node_modules",
    }

    def __init__(self, config: AEAFConfig):
        self.config = config

    def scan(self, root: Path) -> RepositoryModel:
        """
        Scan a repository and return a populated RepositoryModel.
        """

        root = root.resolve()

        repository = RepositoryModel()

        repository.metadata = RepositoryMetadata(
            name=root.name,
            root=root,
        )

        for file in self._discover_python_files(root):
            relative = file.relative_to(root)

            repository.source_files.append(
                SourceFile(
                    path=file,
                    module=file.stem,
                    package=self._package_name(relative),
                )
            )

        repository.statistics.files = len(repository.source_files)

        return repository

    def _discover_python_files(self, root: Path):
        """
        Yield Python source files.
        """

        for path in root.rglob("*.py"):

            if self._is_ignored(path):
                continue

            yield path

    def _is_ignored(self, path: Path) -> bool:
        """
        Determine whether a path should be skipped.
        """

        return any(
            part in self.DEFAULT_IGNORES
            for part in path.parts
        )

    @staticmethod
    def _package_name(path: Path) -> str:
        """
        Compute package name from relative path.
        """

        if len(path.parts) <= 1:
            return ""

        return ".".join(path.parts[:-1])