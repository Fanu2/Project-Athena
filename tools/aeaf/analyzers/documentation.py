"""
Documentation analyzer.

Analyzes documentation coverage across the repository.
"""

from __future__ import annotations

from athena.aeaf.models import RepositoryModel


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
        Analyze module documentation.

        Parameters
        ----------
        repository
            Parsed repository model.
        """

        for module in repository.modules:

            docstring = getattr(
                module,
                "docstring",
                None,
            )

            module.documentation = {
                "has_docstring": bool(
                    docstring and docstring.strip(),
                ),
            }


    def _module_has_docstring(
        self,
        module,
    ) -> bool:
        """
        Determine whether a module has a docstring.

        Parameters
        ----------
        module
            Parsed module model.

        Returns
        -------
        bool
            True if a non-empty docstring exists.
        """

        docstring = getattr(
            module,
            "docstring",
            None,
        )

        return bool(
            docstring and docstring.strip(),
        )

    def _analyze_classes(
        self,
        repository: RepositoryModel,
    ) -> None:
        """
        Analyze class documentation.

        Parameters
        ----------
        repository
            Parsed repository model.
        """

        for module in repository.modules:

            for class_model in getattr(
                module,
                "classes",
                [],
            ):

                class_model.documentation = {
                    "has_docstring": self._has_docstring(
                        class_model,
                    ),
                }


    def _analyze_functions(
        self,
        repository: RepositoryModel,
    ) -> None:
        """
        Analyze function documentation.

        Parameters
        ----------
        repository
            Parsed repository model.
        """

        for module in repository.modules:

            for function in getattr(
                module,
                "functions",
                [],
            ):

                function.documentation = {
                    "has_docstring": self._has_docstring(
                        function,
                    ),
                }

            for class_model in getattr(
                module,
                "classes",
                [],
            ):

                for method in getattr(
                    class_model,
                    "methods",
                    [],
                ):

                    method.documentation = {
                        "has_docstring": self._has_docstring(
                            method,
                        ),
                    }


    def _has_docstring(
        self,
        obj,
    ) -> bool:
        """
        Determine whether an object has a docstring.

        Parameters
        ----------
        obj
            Parsed repository object.

        Returns
        -------
        bool
            True if a non-empty docstring exists.
        """

        docstring = getattr(
            obj,
            "docstring",
            None,
        )

        return bool(
            docstring and docstring.strip(),
        )

    def _build_summary(
        self,
        repository: RepositoryModel,
    ) -> None:
        """
        Build repository documentation summary.

        Parameters
        ----------
        repository
            Parsed repository model.
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

            if getattr(
                module,
                "documentation",
                {},
            ).get(
                "has_docstring",
                False,
            ):
                module_documented += 1

            for class_model in getattr(
                module,
                "classes",
                [],
            ):

                class_total += 1

                if getattr(
                    class_model,
                    "documentation",
                    {},
                ).get(
                    "has_docstring",
                    False,
                ):
                    class_documented += 1

                for method in getattr(
                    class_model,
                    "methods",
                    [],
                ):

                    method_total += 1

                    if getattr(
                        method,
                        "documentation",
                        {},
                    ).get(
                        "has_docstring",
                        False,
                    ):
                        method_documented += 1

            for function in getattr(
                module,
                "functions",
                [],
            ):

                function_total += 1

                if getattr(
                    function,
                    "documentation",
                    {},
                ).get(
                    "has_docstring",
                    False,
                ):
                    function_documented += 1

        def coverage(
            documented: int,
            total: int,
        ) -> float:
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

        def coverage(
            documented: int,
            total: int,
        ) -> float:
            if total == 0:
                return 100.0

            return round(
                documented * 100 / total,
                2,
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
        }

