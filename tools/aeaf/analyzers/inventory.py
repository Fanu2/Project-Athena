"""
Repository inventory analyzer.

Collects high-level statistics from a RepositoryModel.

This analyzer performs no engineering analysis.
It only counts discovered repository objects.
"""

from __future__ import annotations

from ..models import RepositoryModel


class InventoryAnalyzer:
    """
    Analyze repository inventory.

    Produces aggregate statistics about the repository
    contents.
    """

    def analyze(
        self,
        repository: RepositoryModel,
    ) -> RepositoryModel:
        """
        Analyze repository inventory.

        Parameters
        ----------
        repository
            Parsed repository model.

        Returns
        -------
        RepositoryModel
            Repository with updated statistics.
        """

        self._count_modules(repository)

        self._count_classes(repository)

        self._count_functions(repository)

        self._count_methods(repository)

        self._count_imports(repository)

        return repository

    def _count_modules(
        self,
        repository: RepositoryModel,
    ) -> None:
        """
        Count parsed Python modules.
        """

        repository.statistics.modules = len(
            repository.modules
        )

    def _count_classes(
        self,
        repository: RepositoryModel,
    ) -> None:
        """
        Count all classes in the repository.
        """

        total = 0

        for module in repository.modules:
            total += len(module.classes)

        repository.statistics.classes = total

    def _count_functions(
        self,
        repository: RepositoryModel,
    ) -> None:
        """
        Count all top-level functions in the repository.
        """

        total = 0

        for module in repository.modules:
            total += len(module.functions)

        repository.statistics.functions = total

    def _count_methods(
        self,
        repository: RepositoryModel,
    ) -> None:
        """
        Count all class methods in the repository.
        """

        total = 0

        for module in repository.modules:

            for class_info in module.classes:
                total += len(class_info.methods)

        repository.statistics.methods = total

    def _count_imports(
        self,
        repository: RepositoryModel,
    ) -> None:
        """
        Count all import statements in the repository.
        """

        total = 0

        for module in repository.modules:
            total += len(module.imports)

        repository.statistics.imports = total

    def _count_source_files(
        self,
        repository: RepositoryModel,
    ) -> None:
        """
        Count discovered source files.
        """

        repository.statistics.source_files = len(
            repository.source_files
        )

