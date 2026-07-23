"""
Public parsing API for AEAF.

This module provides the high-level interface for parsing Python source
files. The actual parsing implementation is delegated to PythonASTParser.

The parser enriches an existing RepositoryModel with information extracted
from the source code, including imports, classes, functions and methods.

The parser never performs architectural analysis.
"""

from __future__ import annotations

from .config import AEAFConfig
from .models import RepositoryModel
from .parsers.python_ast import PythonASTParser


class Parser:
    """
    Public interface for parsing repositories.
    """

    def __init__(self, config: AEAFConfig | None = None) -> None:
        self._config = config or AEAFConfig()
        self._parser = PythonASTParser(self._config)

    def parse(self, repository: RepositoryModel) -> RepositoryModel:
        """
        Parse every discovered source file.

        Parameters
        ----------
        repository
            RepositoryModel produced by the scanner.

        Returns
        -------
        RepositoryModel
            Repository enriched with parsed source code information.
        """
        return self._parser.parse(repository)


def parse(
    repository: RepositoryModel,
    config: AEAFConfig | None = None,
) -> RepositoryModel:
    """
    Convenience function.

    Example
    -------
    >>> repository = parse(repository)
    """

    return Parser(config).parse(repository)