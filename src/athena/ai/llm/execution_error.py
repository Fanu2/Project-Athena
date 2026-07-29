"""
Execution errors for Athena LLM runtime.
"""

from __future__ import annotations


class ExecutionError(Exception):
    """Base execution error."""


class ExecutionUnavailableError(ExecutionError):
    """Provider unavailable during execution."""


class ExecutionFailedError(ExecutionError):
    """Provider execution failed."""
