"""Connector interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod


class LLMConnector(ABC):
    """Minimal interface shared by provider connectors."""

    model: str

    @abstractmethod
    def generate(self, prompt: str, context: str) -> str:
        """Generate a response from prompt and context."""
        raise NotImplementedError

    def token_count(self, text: str) -> int:
        """Approximate token count without requiring a provider SDK."""
        return max(0, len(text.split()))
