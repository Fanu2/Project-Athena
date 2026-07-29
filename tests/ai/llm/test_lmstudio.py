"""
Tests for LMStudioProvider.
"""

from __future__ import annotations

from unittest.mock import Mock, patch

import requests

from athena.ai.llm.models import (
    LLMRequest,
    LLMResponse,
)
from athena.ai.llm.providers import LMStudioProvider
from athena.settings import LLMSettings


def test_provider_name() -> None:
    provider = LMStudioProvider()

    assert provider.provider_name == "lmstudio"


@patch.object(LMStudioProvider, "_request")
def test_health_success(mock_request: Mock) -> None:
    response = Mock()
    response.status_code = 200

    mock_request.return_value = response

    provider = LMStudioProvider()

    assert provider.health() is True


@patch.object(LMStudioProvider, "_request")
def test_health_failure(mock_request: Mock) -> None:
    mock_request.side_effect = requests.RequestException()

    provider = LMStudioProvider()

    assert provider.health() is False


@patch.object(LMStudioProvider, "_request")
def test_list_models(mock_request: Mock) -> None:
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "data": [
            {"id": "model-a"},
            {"id": "model-b"},
        ]
    }

    mock_request.return_value = response

    provider = LMStudioProvider()

    assert provider.list_models() == [
        "model-a",
        "model-b",
    ]


@patch.object(LMStudioProvider, "_post_chat")
def test_analyze(mock_post_chat: Mock) -> None:
    mock_post_chat.return_value = {
        "model": "lmstudio",
        "choices": [
            {
                "message": {
                    "content": "Hello from LM Studio"
                }
            }
        ],
    }

    provider = LMStudioProvider()

    response = provider.analyze(
        LLMRequest(
            system_prompt="You are Athena.",
            user_prompt="Hello",
        )
    )

    assert response.text == "Hello from LM Studio"
    assert response.model == "lmstudio"


def test_custom_settings() -> None:
    settings = LLMSettings(
        provider="lmstudio",
        model="test-model",
        base_url="http://localhost:8080",
        timeout=30,
    )

    provider = LMStudioProvider(settings)

    assert provider._settings == settings
