"""
AEAF configuration.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class AEAFConfig:
    """
    Configuration for an AEAF analysis session.
    """

    project_root: Path

    follow_symlinks: bool = False

    include_hidden: bool = False

    max_file_size: int = 5 * 1024 * 1024

    python_extensions: tuple[str, ...] = (
        ".py",
    )

    exclude_directories: tuple[str, ...] = (
        ".git",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "build",
        "dist",
    )

    exclude_files: tuple[str, ...] = ()

    verbose: bool = False

    @classmethod
    def default(cls, project_root: Path) -> "AEAFConfig":
        """
        Create a configuration using the default AEAF settings.
        """
        return cls(
            project_root=project_root,
        )

    def is_excluded_directory(self, directory_name: str) -> bool:
        """
        Return True if a directory should be skipped.
        """
        return directory_name in self.exclude_directories

    def is_excluded_file(self, filename: str) -> bool:
        """
        Return True if a file should be skipped.
        """
        return filename in self.exclude_files

    def is_supported_file(self, path: Path) -> bool:
        """
        Return True if the file extension is supported.
        """
        return path.suffix.lower() in self.python_extensions

    def validate(self) -> None:
        """
        Validate the configuration.
        """

        if not self.project_root.exists():
            raise FileNotFoundError(
                f"Project root does not exist: {self.project_root}"
            )

        if not self.project_root.is_dir():
            raise NotADirectoryError(
                f"Project root is not a directory: {self.project_root}"
            )

        if self.max_file_size <= 0:
            raise ValueError(
                "Maximum file size must be greater than zero."
            )

    @property
    def max_file_size_mb(self) -> float:
        """
        Return the maximum file size in megabytes.
        """
        return self.max_file_size / (1024 * 1024)

    def __post_init__(self) -> None:
        """
        Normalize the project root.
        """
        self.project_root = self.project_root.resolve()

    def should_scan_directory(self, directory: Path) -> bool:
        """
        Return True if the directory should be scanned.
        """
        return (
            directory.is_dir()
            and not self.is_excluded_directory(directory.name)
        )

    def should_scan_file(self, file: Path) -> bool:
        """
        Return True if the file should be scanned.
        """
        return (
            file.is_file()
            and self.is_supported_file(file)
            and not self.is_excluded_file(file.name)
            and file.stat().st_size <= self.max_file_size
        )

    def copy(self) -> "AEAFConfig":
        """
        Return a copy of this configuration.
        """
        return AEAFConfig(
            project_root=self.project_root,
            follow_symlinks=self.follow_symlinks,
            include_hidden=self.include_hidden,
            max_file_size=self.max_file_size,
            python_extensions=self.python_extensions,
            exclude_directories=self.exclude_directories,
            exclude_files=self.exclude_files,
            verbose=self.verbose,
        )

