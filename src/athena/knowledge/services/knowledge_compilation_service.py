"""
Athena Knowledge Compilation Service

Application service connecting
document acquisition with Athena knowledge.
"""

from __future__ import annotations

from typing import Any

from athena.knowledge.acquisition.engine.knowledge_acquisition_engine import (
    KnowledgeAcquisitionEngine,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)


class KnowledgeCompilationService:
    """
    Application entry point for knowledge compilation.

    Maintains the AKC runtime context so that
    compilation stages can access:

    - knowledge repository
    - evidence services
    - citation services
    - index services
    - relationship services
    """

    def __init__(
        self,
        engine: KnowledgeAcquisitionEngine | None = None,
        context: KnowledgeContext | None = None,
    ) -> None:
        """
        Initialize knowledge compiler.
        """

        self._engine = (
            engine
            if engine is not None
            else KnowledgeAcquisitionEngine()
        )

        self._context = context

    def compile_document(
        self,
        document: Any,
        context: KnowledgeContext | None = None,
    ) -> Any:
        """
        Compile a document into Athena knowledge.

        A provided context takes priority.
        Otherwise the configured runtime context
        is used.
        """

        runtime_context = (
            context
            if context is not None
            else self._context
        )

        return self._engine.compile(
            document,
            runtime_context,
        )

    def compile_with_report(
        self,
        document: Any,
        context: KnowledgeContext | None = None,
    ) -> Any:
        """
        Compile document and return execution report.
        """

        runtime_context = (
            context
            if context is not None
            else self._context
        )

        return self._engine.compile_with_report(
            document,
            runtime_context,
        )