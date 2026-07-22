"""
Prompt strategies for Athena's RAG system.
"""

from .base import PromptStrategy
from .default import DefaultPrompt
from .summarize import SummaryPrompt
from .compare import ComparePrompt
from .explain import ExplainPrompt
from .extract import ExtractPrompt
from .analyze import AnalyzePrompt

__all__ = [
    "PromptStrategy",
    "DefaultPrompt",
    "SummaryPrompt",
    "ComparePrompt",
    "ExplainPrompt",
    "ExtractPrompt",
    "AnalyzePrompt",
]