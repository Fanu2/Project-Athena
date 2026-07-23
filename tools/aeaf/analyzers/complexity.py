"""
Complexity analyzer.

Calculates basic structural complexity metrics
from the parsed repository model.
"""

from __future__ import annotations

from ..models import (
    ComplexityInfo,
    RepositoryModel,
)


class ComplexityAnalyzer:
    """
    Analyze structural complexity of repository code.
    """

    def analyze(
        self,
        repository: RepositoryModel,
    ) -> RepositoryModel:
        """
        Calculate complexity metrics.

        Parameters
        ----------
        repository
            Parsed repository model.

        Returns
        -------
        RepositoryModel
            Repository enriched with complexity information.
        """

        repository.complexity.clear()

        for module in repository.modules:

            self._analyze_module(
                repository,
                module,
            )

        return repository

    def _analyze_module(
        self,
        repository: RepositoryModel,
        module,
    ) -> None:
        """
        Analyze module complexity.
        """

        score = (
            len(module.classes)
            + len(module.functions)
        )

        repository.complexity.append(
            ComplexityInfo(
                name=module.name,
                kind="module",
                score=score,
                details={
                    "classes": len(module.classes),
                    "functions": len(module.functions),
                },
            )
        )

        for class_info in module.classes:

            self._analyze_class(
                repository,
                class_info,
            )

        for function in module.functions:

            self._analyze_function(
                repository,
                function,
            )


    def _analyze_class(
        self,
        repository: RepositoryModel,
        class_info,
    ) -> None:
        """
        Analyze class complexity.
        """

        score = len(
            class_info.methods,
        )

        repository.complexity.append(
            ComplexityInfo(
                name=class_info.name,
                kind="class",
                score=score,
                details={
                    "methods": len(
                        class_info.methods,
                    ),
                },
            )
        )

        for method in class_info.methods:

            self._analyze_function(
                repository,
                method,
            )


    def _analyze_function(
        self,
        repository: RepositoryModel,
        function,
    ) -> None:
        """
        Analyze function complexity.
        """

        lines = 0

        if function.end_lineno is not None:

            lines = (
                function.end_lineno
                - function.lineno
                + 1
            )

        score = (
            len(function.parameters)
            + lines
        )

        repository.complexity.append(
            ComplexityInfo(
                name=function.name,
                kind="function",
                score=score,
                details={
                    "parameters": len(
                        function.parameters,
                    ),
                    "lines": lines,
                },
            )
        )

