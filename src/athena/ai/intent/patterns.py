"""
Intent Engine keyword patterns.

This module contains the vocabulary used by the rule-based
Intent Engine. It intentionally contains no detection logic.
"""

from __future__ import annotations

from .models import IntentType

INTENT_PATTERNS: dict[IntentType, tuple[str, ...]] = {

    IntentType.SUMMARIZE: (
        "summarize",
        "summary",
        "summarise",
        "brief",
        "overview",
        "condense",
        "shorten",
        "gist",
    ),

    IntentType.COMPARE: (
        "compare",
        "comparison",
        "contrast",
        "difference",
        "differences",
        "similarity",
        "similarities",
        "versus",
        "vs",
    ),

    IntentType.EXPLAIN: (
        "explain",
        "clarify",
        "describe",
        "interpret",
        "meaning",
        "understand",
        "why",
        "how",
    ),

    IntentType.TRANSFORM: (
        "rewrite",
        "convert",
        "transform",
        "paraphrase",
        "translate",
        "poem",
        "email",
        "letter",
        "story",
    ),

    IntentType.EXTRACT: (
        "extract",
        "list",
        "find",
        "identify",
        "show",
        "collect",
        "action items",
        "key points",
    ),

    IntentType.ANALYZE: (
        "analyze",
        "analyse",
        "evaluate",
        "review",
        "critique",
        "assess",
        "examine",
    ),

    IntentType.SEARCH: (
        "search",
        "lookup",
        "locate",
        "find",
        "where",
    ),

    IntentType.QUESTION: (
        "what",
        "when",
        "who",
        "which",
        "whose",
        "whom",
        "can",
        "could",
        "does",
        "do",
        "did",
        "is",
        "are",
        "was",
        "were",
    ),

    IntentType.CREATIVE: (
        "brainstorm",
        "idea",
        "ideas",
        "creative",
        "invent",
        "design",
        "compose",
        "imagine",
    ),

}