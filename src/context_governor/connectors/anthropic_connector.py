"""Anthropic connector."""

from __future__ import annotations

import os

from .base import LLMConnector


class AnthropicConnector(LLMConnector):
    def __init__(self, model: str = "claude-3-5-sonnet-latest") -> None:
        self.model = model

    def generate(self, prompt: str, context: str) -> str:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not configured")
        try:
            import anthropic
        except ImportError as exc:
            raise RuntimeError("Install the connectors extra to use Anthropic") from exc
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[{"role": "user", "content": f"{context}\n\n{prompt}"}],
        )
        return "".join(getattr(block, "text", "") for block in response.content)
