"""
LLM exceptions.
"""


class LLMError(Exception):
    """Base exception for LLM failures."""


class ProviderUnavailableError(LLMError):
    """Raised when an LLM provider is unavailable."""


class GenerationError(LLMError):
    """Raised when text generation fails."""