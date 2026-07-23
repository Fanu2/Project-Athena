"""
AEAF analysis pipeline.

Coordinates the complete repository analysis workflow.

The pipeline orchestrates scanners, parsers and analyzers
while keeping them independent.
"""

from __future__ import annotations

from pathlib import Path

from ..analyzers.inventory import InventoryAnalyzer
from ..analyzers.dependency_graph import DependencyGraphAnalyzer
from ..analyzers.complexity import ComplexityAnalyzer
from ..config import AEAFConfig
from ..models import RepositoryModel
from ..parser import Parser
from ..scanner import Scanner


class AnalysisPipeline:
    """
    Execute the complete AEAF analysis pipeline.
    """

    def __init__(
        self,
        config: AEAFConfig,
    ) -> None:
        """
        Initialize the analysis pipeline.
        """

        self.config = config

        self.scanner = Scanner(
            config,
        )

        self.parser = Parser(
            config,
        )

        #
        # Ordered list of repository analyzers.
        #
        # The order is important:
        #
        # 1. Inventory collects basic repository statistics.
        # 2. DependencyGraph builds relationships between modules.
        #
        self.analyzers = [
            InventoryAnalyzer(),
            DependencyGraphAnalyzer(),
            ComplexityAnalyzer(),
        ]

    def run(
        self,
        repository_path: Path,
    ) -> RepositoryModel:
        """
        Execute the complete AEAF analysis pipeline.

        Parameters
        ----------
        repository_path
            Root directory of the repository.

        Returns
        -------
        RepositoryModel
            Fully analyzed repository.
        """

        repository = self.scanner.scan(
            repository_path,
        )

        repository = self.parser.parse(
            repository,
        )

        for analyzer in self.analyzers:

            repository = analyzer.analyze(
                repository,
            )

        return repository

    def validate_repository(
        self,
        repository_path: Path,
    ) -> Path:
        """
        Validate the repository path.

        Parameters
        ----------
        repository_path
            Repository root directory.

        Returns
        -------
        Path
            Resolved repository path.

        Raises
        ------
        FileNotFoundError
            If the repository does not exist.

        NotADirectoryError
            If the path is not a directory.
        """

        repository_path = repository_path.resolve()

        if not repository_path.exists():
            raise FileNotFoundError(
                f"Repository does not exist: {repository_path}"
            )

        if not repository_path.is_dir():
            raise NotADirectoryError(
                f"Not a directory: {repository_path}"
            )

        return repository_path