"""OpenAI connector."""

from __future__ import annotations

import os

from .base import LLMConnector


class OpenAIConnector(LLMConnector):
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.model = model

    def generate(self, prompt: str, context: str) -> str:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install the connectors extra to use OpenAI") from exc
        client = OpenAI(api_key=api_key, base_url=os.getenv("OPENAI_API_BASE") or os.getenv("OPENAI_BASE_URL"))
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": f"{context}\n\n{prompt}"}],
        )
        return response.choices[0].message.content or ""

    def token_count(self, text: str) -> int:
        try:
            import tiktoken
            encoding = tiktoken.encoding_for_model(self.model)
            return len(encoding.encode(text))
        except Exception:
            return super().token_count(text)
