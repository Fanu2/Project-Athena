"""
Unit tests for the IntentDetector.
"""

from athena.ai.intent.detector import IntentDetector
from athena.ai.intent.models import IntentType


def test_detect_summary_intent():
    detector = IntentDetector()

    result = detector.detect("Summarize this document.")

    assert result.intent == IntentType.SUMMARIZE
    assert result.confidence > 0.0
    assert "summarize" in result.matched_keywords


def test_detect_compare_intent():
    detector = IntentDetector()

    result = detector.detect("Compare these documents.")

    assert result.intent == IntentType.COMPARE
    assert result.confidence > 0.0


def test_detect_explain_intent():
    detector = IntentDetector()

    result = detector.detect("Explain quantum computing.")

    assert result.intent == IntentType.EXPLAIN
    assert result.confidence > 0.0


def test_detect_extract_intent():
    detector = IntentDetector()

    result = detector.detect("Extract all dates from this report.")

    assert result.intent == IntentType.EXTRACT
    assert result.confidence > 0.0


def test_detect_unknown_intent():
    detector = IntentDetector()

    result = detector.detect("asdf qwerty zxcv")

    assert result.intent == IntentType.UNKNOWN
    assert result.confidence == 0.0
    assert result.matched_keywords == ()


def test_query_is_normalized():
    detector = IntentDetector()

    result = detector.detect("   SUMMARIZE   THIS document!! ")

    assert result.normalized_query == "summarize this document"