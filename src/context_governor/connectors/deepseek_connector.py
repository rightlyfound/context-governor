"""DeepSeek connector."""

from __future__ import annotations

import os

import requests

from .base import LLMConnector


class DeepSeekConnector(LLMConnector):
    def __init__(self, model: str = "deepseek-chat", base_url: str | None = None) -> None:
        self.model = model
        self.base_url = base_url or os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

    def generate(self, prompt: str, context: str) -> str:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise RuntimeError("DEEPSEEK_API_KEY is not configured")
        response = requests.post(
            f"{self.base_url.rstrip('/')}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": self.model, "messages": [{"role": "user", "content": f"{context}\n\n{prompt}"}]},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
