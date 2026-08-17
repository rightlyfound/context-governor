import pytest

from context_governor.connectors import OpenRouterConnector


def test_openrouter_uses_environment_at_call_time(monkeypatch):
    connector = OpenRouterConnector(model="test/model")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    assert not connector.configured
    with pytest.raises(RuntimeError, match="OPENROUTER_API_KEY"):
        connector.generate("hello")


def test_openrouter_token_count_is_deterministic():
    connector = OpenRouterConnector()
    assert connector.token_count("abcd") == 1
    assert connector.token_count("abcdefgh") == 2
