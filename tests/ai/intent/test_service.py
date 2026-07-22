"""
Unit tests for the IntentService.
"""

from athena.ai.intent.models import IntentType
from athena.ai.intent.service import IntentService


def test_service_detect_summary_intent():
    service = IntentService()

    result = service.detect("Summarize this document.")

    assert result.intent == IntentType.SUMMARIZE
    assert result.confidence > 0.0


def test_service_detect_compare_intent():
    service = IntentService()

    result = service.detect("Compare these documents.")

    assert result.intent == IntentType.COMPARE
    assert result.confidence > 0.0


def test_service_detect_explain_intent():
    service = IntentService()

    result = service.detect("Explain quantum computing.")

    assert result.intent == IntentType.EXPLAIN
    assert result.confidence > 0.0


def test_service_detect_extract_intent():
    service = IntentService()

    result = service.detect("Extract all dates from this report.")

    assert result.intent == IntentType.EXTRACT
    assert result.confidence > 0.0


def test_service_detect_unknown_intent():
    service = IntentService()

    result = service.detect("asdf qwerty zxcv")

    assert result.intent == IntentType.UNKNOWN