"""
Complexity analyzer.

Calculates basic repository, module, and class complexity metrics.
"""

from __future__ import annotations

from athena.aeaf.models import RepositoryModel


class ComplexityAnalyzer:
    """
    Analyze repository complexity.
    """

    def analyze(
        self,
        repository: RepositoryModel,
    ) -> RepositoryModel:
        """
        Analyze repository complexity.

        Parameters
        ----------
        repository
            Parsed repository model.

        Returns
        -------
        RepositoryModel
            Repository enriched with complexity metrics.
        """

        self._analyze_modules(
            repository,
        )

        self._analyze_classes(
            repository,
        )

        self._build_summary(
            repository,
        )

        return repository

    def _analyze_modules(
        self,
        repository: RepositoryModel,
    ) -> None:
        """
        Analyze module-level metrics.

        Parameters
        ----------
        repository
            Parsed repository model.
        """

        for module in repository.modules:

            module.metrics = {
                "classes": len(
                    getattr(module, "classes", []),
                ),
                "functions": len(
                    getattr(module, "functions", []),
                ),
                "methods": self._count_methods(
                    module,
                ),
                "imports": len(
                    getattr(module, "imports", []),
                ),
            }


    def _count_methods(
        self,
        module,
    ) -> int:
        """
        Count methods defined in a module.

        Parameters
        ----------
        module
            Parsed module model.

        Returns
        -------
        int
            Total number of methods.
        """

        return sum(
            len(
                getattr(class_model, "methods", []),
            )
            for class_model in getattr(module, "classes", [])
        )

    def _analyze_classes(
        self,
        repository: RepositoryModel,
    ) -> None:
        """
        Analyze class-level metrics.

        Parameters
        ----------
        repository
            Parsed repository model.
        """

        for module in repository.modules:

            for class_model in getattr(module, "classes", []):

                class_model.metrics = {
                    "methods": len(
                        getattr(class_model, "methods", []),
                    ),
                    "decorators": len(
                        getattr(class_model, "decorators", []),
                    ),
                    "base_classes": len(
                        getattr(class_model, "base_classes", []),
                    ),
                }


    def _largest_class(
        self,
        repository: RepositoryModel,
    ):
        """
        Return the class with the most methods.

        Parameters
        ----------
        repository
            Parsed repository model.

        Returns
        -------
        ClassModel | None
            Largest class, if any.
        """

        largest = None
        largest_count = -1

        for module in repository.modules:

            for class_model in getattr(module, "classes", []):

                method_count = len(
                    getattr(class_model, "methods", []),
                )

                if method_count > largest_count:
                    largest = class_model
                    largest_count = method_count

        return largest

    def _build_summary(
        self,
        repository: RepositoryModel,
    ) -> None:
        """
        Build repository-wide complexity summary.

        Parameters
        ----------
        repository
            Parsed repository model.
        """

        total_modules = len(repository.modules)
        total_classes = 0
        total_functions = 0
        total_methods = 0
        total_imports = 0

        largest_module = None
        largest_module_methods = -1

        for module in repository.modules:

            metrics = getattr(module, "metrics", {})

            total_classes += metrics.get("classes", 0)
            total_functions += metrics.get("functions", 0)
            total_methods += metrics.get("methods", 0)
            total_imports += metrics.get("imports", 0)

            if metrics.get("methods", 0) > largest_module_methods:
                largest_module = module
                largest_module_methods = metrics.get("methods", 0)

        largest_class = self._largest_class(
            repository,
        )

        average_methods_per_class = (
            total_methods / total_classes
            if total_classes > 0
            else 0.0
        )

        repository.complexity = {
            "modules": total_modules,
            "classes": total_classes,
            "functions": total_functions,
            "methods": total_methods,
            "imports": total_imports,
            "average_methods_per_class": round(
                average_methods_per_class,
                2,
            ),
            "largest_module": (
                largest_module.name
                if largest_module is not None
                else None
            ),
            "largest_class": (
                largest_class.name
                if largest_class is not None
                else None
            ),
        }


