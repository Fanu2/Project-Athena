"""
Dependency graph analyzer.

Builds module dependency information from the parsed repository model.
"""

from __future__ import annotations

from athena.aeaf.models import RepositoryModel


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

        Parameters
        ----------
        repository
            Parsed repository model.

        Returns
        -------
        RepositoryModel
            Repository enriched with dependency information.
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

        Parameters
        ----------
        repository
            Parsed repository model.
        """

        for module in repository.modules:

            if not hasattr(module, "dependencies"):
                module.dependencies = []

            self._collect_outgoing_dependencies(
                module,
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

        Parameters
        ----------
        module
            Parsed module model.
        """

        module.dependencies = []

        for imported_module in getattr(module, "imports", []):

            module.dependencies.append(
                imported_module,
            )


    def _normalize_import(
        self,
        import_name: str,
    ) -> str:
        """
        Normalize an import name.

        Parameters
        ----------
        import_name
            Imported module name.

        Returns
        -------
        str
            Normalized module name.
        """

        return import_name.strip()

    def _calculate_incoming_dependencies(
        self,
        repository: RepositoryModel,
    ) -> None:
        """
        Calculate incoming dependencies for every module.

        Parameters
        ----------
        repository
            Parsed repository model.
        """

        for module in repository.modules:
            module.dependents = []

        module_lookup = {
            module.name: module
            for module in repository.modules
        }

        for module in repository.modules:

            for dependency in getattr(module, "dependencies", []):

                dependency = self._normalize_import(
                    dependency,
                )

                target = module_lookup.get(
                    dependency,
                )

                if target is None:
                    continue

                if module.name not in target.dependents:
                    target.dependents.append(
                        module.name,
                    )


    def _find_module(
        self,
        repository: RepositoryModel,
        module_name: str,
    ):
        """
        Find a module by name.

        Parameters
        ----------
        repository
            Parsed repository model.

        module_name
            Name of the module.

        Returns
        -------
        ModuleModel | None
            Matching module if found.
        """

        for module in repository.modules:

            if module.name == module_name:
                return module

        return None

    def _collect_outgoing_dependencies(
        self,
        module,
    ) -> None:
        """
        Collect outgoing dependencies for a module.

        Parameters
        ----------
        module
            Parsed module model.
        """

        dependencies = []

        for imported_module in getattr(module, "imports", []):

            dependency = self._normalize_import(
                imported_module,
            )

            if dependency and dependency not in dependencies:
                dependencies.append(
                    dependency,
                )

        module.dependencies = dependencies