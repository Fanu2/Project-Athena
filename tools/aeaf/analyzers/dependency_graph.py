"""
Dependency graph analyzer.

Builds module dependency information from the parsed repository model.
"""

from __future__ import annotations

from ..models import (
    DependencyEdge,
    RepositoryModel,
)


class DependencyGraphAnalyzer:
    """
    Analyze dependencies between repository modules.
    """

    def analyze(
        self,
        repository: RepositoryModel,
    ) -> RepositoryModel:
        """
        Build dependency relationships.
        """

        self._build_dependency_graph(
            repository,
        )

        return repository


    def _build_dependency_graph(
        self,
        repository: RepositoryModel,
    ) -> None:
        """
        Build the repository dependency graph.
        """

        repository.dependency_graph.edges.clear()

        for module in repository.modules:

            module.dependencies.clear()

            self._collect_outgoing_dependencies(
                module,
            )

            for dependency in module.dependencies:

                repository.dependency_graph.edges.append(
                    DependencyEdge(
                        source=module.name,
                        target=dependency,
                    )
                )

        self._calculate_incoming_dependencies(
            repository,
        )


    def _collect_outgoing_dependencies(
        self,
        module,
    ) -> None:
        """
        Collect outgoing dependencies for a module.
        """

        dependencies = []

        for imported_module in module.imports:

            dependency = self._normalize_import(
                imported_module.module,
            )

            if (
                dependency
                and dependency not in dependencies
            ):
                dependencies.append(
                    dependency,
                )

        module.dependencies.extend(
            dependencies,
        )


    def _normalize_import(
        self,
        import_name: str,
    ) -> str:
        """
        Normalize an import name.
        """

        return import_name.strip()


    def _calculate_incoming_dependencies(
        self,
        repository: RepositoryModel,
    ) -> None:
        """
        Calculate incoming dependencies.
        """

        for module in repository.modules:

            module.dependents.clear()

        module_lookup = {
            module.name: module
            for module in repository.modules
        }

        for module in repository.modules:

            for dependency in module.dependencies:

                normalized = dependency.split(".")[-1]

                target = module_lookup.get(
                    normalized,
                )

                if target is None:
                    continue

                if module.name not in target.dependents:

                    target.dependents.append(
                        module.name,
                    )