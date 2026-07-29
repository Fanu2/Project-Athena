"""
OpenAI-compatible LLM provider.
"""

from __future__ import annotations

from typing import Any

import requests

from athena.ai.llm.models import LLMRequest, LLMResponse
from athena.ai.llm.provider import LLMProvider
from athena.settings import LLMSettings


class OpenAICompatibleProvider(LLMProvider):
    """Base provider for OpenAI-compatible APIs."""

    def __init__(self, settings: LLMSettings | None = None) -> None:
        self._settings = settings or LLMSettings()

    @property
    def provider_name(self) -> str:
        return self._settings.provider

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> requests.Response:
        """Send an HTTP request."""

        headers = kwargs.pop("headers", {}).copy()

        if self._settings.api_key:
            headers["Authorization"] = (
                f"Bearer {self._settings.api_key}"
            )

        return requests.request(
            method=method,
            url=f"{self._settings.base_url}{endpoint}",
            headers=headers,
            timeout=self._settings.timeout,
            **kwargs,
        )

    def _get(
        self,
        endpoint: str,
        **kwargs: Any,
    ) -> requests.Response:
        """Send a GET request."""
        return self._request(
            "GET",
            endpoint,
            **kwargs,
        )

    def _post(
        self,
        endpoint: str,
        payload: dict[str, Any],
        **kwargs: Any,
    ) -> requests.Response:
        """Send a POST request."""
        return self._request(
            "POST",
            endpoint,
            json=payload,
            **kwargs,
        )

    def health(self) -> bool:
        """Return True if the provider is reachable."""
        try:
            response = self._get("/v1/models")
            return response.status_code == 200
        except requests.RequestException:
            return False

    def list_models(self) -> list[str]:
        """Return available model IDs."""
        response = self._get("/v1/models")
        response.raise_for_status()

        return [
            model["id"]
            for model in response.json().get("data", [])
        ]

    def _post_chat(
        self,
        request: LLMRequest,
    ) -> dict[str, Any]:
        """Send a chat completion request."""

        payload = {
            "model": self._settings.model,
            "messages": [
                {
                    "role": "system",
                    "content": request.system_prompt,
                },
                {
                    "role": "user",
                    "content": request.user_prompt,
                },
            ],
        }

        response = self._post(
            "/v1/chat/completions",
            payload,
        )
        response.raise_for_status()
        return response.json()

    def analyze(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """Generate a response."""

        response = self._post_chat(request)

        return LLMResponse(
            text=response["choices"][0]["message"]["content"],
            model=response["model"],
        )

