"""
Documentation analyzer.

Analyzes documentation coverage across the repository.
"""

from __future__ import annotations

from ..models import (
    DocumentationInfo,
    RepositoryModel,
)


class DocumentationAnalyzer:
    """
    Analyze repository documentation.
    """

    def analyze(
        self,
        repository: RepositoryModel,
    ) -> RepositoryModel:
        """
        Analyze documentation coverage.

        Parameters
        ----------
        repository
            Parsed repository model.

        Returns
        -------
        RepositoryModel
            Repository enriched with documentation metrics.
        """

        self._analyze_modules(
            repository,
        )

        self._analyze_classes(
            repository,
        )

        self._analyze_functions(
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
        Validate module documentation metadata.
        """

        for module in repository.modules:

            if module.documentation is None:
                module.documentation = DocumentationInfo()


    def _analyze_classes(
        self,
        repository: RepositoryModel,
    ) -> None:
        """
        Analyze class documentation.
        """

        for module in repository.modules:

            for class_model in module.classes:

                if class_model.documentation is None:
                    class_model.documentation = DocumentationInfo()


    def _analyze_functions(
        self,
        repository: RepositoryModel,
    ) -> None:
        """
        Analyze function and method documentation.
        """

        for module in repository.modules:

            for function in module.functions:

                if function.documentation is None:
                    function.documentation = DocumentationInfo()

            for class_model in module.classes:

                for method in class_model.methods:

                    if method.documentation is None:
                        method.documentation = DocumentationInfo()

    def _has_docstring(
        self,
        obj,
    ) -> bool:
        """
        Determine whether documentation exists.
        """

        documentation = getattr(
            obj,
            "documentation",
            None,
        )

        if documentation is None:
            return False

        return documentation.has_docstring

    def _build_summary(
        self,
        repository: RepositoryModel,
    ) -> None:
        """
        Build repository documentation summary.
        """

        module_total = 0
        module_documented = 0

        class_total = 0
        class_documented = 0

        function_total = 0
        function_documented = 0

        method_total = 0
        method_documented = 0

        for module in repository.modules:

            module_total += 1

            if self._has_docstring(
                module,
            ):
                module_documented += 1

            for class_model in module.classes:

                class_total += 1

                if self._has_docstring(
                    class_model,
                ):
                    class_documented += 1

                for method in class_model.methods:

                    method_total += 1

                    if self._has_docstring(
                        method,
                    ):
                        method_documented += 1

            for function in module.functions:

                function_total += 1

                if self._has_docstring(
                    function,
                ):
                    function_documented += 1

        def coverage(
            documented: int,
            total: int,
        ) -> float:
            """
            Calculate documentation coverage percentage.
            """

            if total == 0:
                return 100.0

            return round(
                documented * 100 / total,
                2,
            )


        total_items = (
            module_total
            + class_total
            + function_total
            + method_total
        )

        documented_items = (
            module_documented
            + class_documented
            + function_documented
            + method_documented
        )


        repository.documentation = {
            "modules": {
                "documented": module_documented,
                "total": module_total,
                "coverage": coverage(
                    module_documented,
                    module_total,
                ),
            },

            "classes": {
                "documented": class_documented,
                "total": class_total,
                "coverage": coverage(
                    class_documented,
                    class_total,
                ),
            },

            "functions": {
                "documented": function_documented,
                "total": function_total,
                "coverage": coverage(
                    function_documented,
                    function_total,
                ),
            },

            "methods": {
                "documented": method_documented,
                "total": method_total,
                "coverage": coverage(
                    method_documented,
                    method_total,
                ),
            },

            "overall": {
                "documented": documented_items,
                "total": total_items,
                "coverage": coverage(
                    documented_items,
                    total_items,
                ),
            },
        }