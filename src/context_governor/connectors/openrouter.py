"""OpenRouter connector for multi-model ACG experiments.

The API key is read only from OPENROUTER_API_KEY at call time and is never
serialized into logs or repository files.
"""

from __future__ import annotations

import os
from typing import Any

import requests

from .base import LLMConnector


class OpenRouterConnector(LLMConnector):
    """Call any OpenRouter model through the common connector interface."""

    def __init__(self, model: str = "openai/gpt-4o-mini", timeout: int = 90) -> None:
        self.model = model
        self.timeout = timeout
        self.base_url = os.getenv(
            "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1/chat/completions"
        )

    @property
    def configured(self) -> bool:
        return bool(os.getenv("OPENROUTER_API_KEY"))

    def generate(self, prompt: str, context: str = "") -> str:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not configured")
        messages: list[dict[str, str]] = []
        if context:
            messages.append({"role": "system", "content": context})
        messages.append({"role": "user", "content": prompt})
        response = requests.post(
            self.base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": os.getenv(
                    "OPENROUTER_HTTP_REFERER",
                    "https://github.com/rightlyfound/context-governor",
                ),
                "X-OpenRouter-Title": os.getenv(
                    "OPENROUTER_APP_TITLE", "Context Governor"
                ),
            },
            json={"model": self.model, "messages": messages, "temperature": 0.2},
            timeout=self.timeout,
        )
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        return str(data["choices"][0]["message"].get("content", ""))

    def token_count(self, text: str) -> int:
        return max(1, (len(text) + 3) // 4)
