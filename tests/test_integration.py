import json
from pathlib import Path

from context_governor.cli import audit
from context_governor.connectors import AnthropicConnector, DeepSeekConnector, OpenAIConnector


def test_cli_audit_runs(tmp_path, capsys):
    (tmp_path / "sample.py").write_text("x = 1\n")
    assert audit(tmp_path, "find issue") == 0
    assert json.loads(capsys.readouterr().out)["files"]


def test_connector_stubs_fail_without_keys(monkeypatch):
    for name, connector in [("OPENAI_API_KEY", OpenAIConnector()), ("ANTHROPIC_API_KEY", AnthropicConnector()), ("DEEPSEEK_API_KEY", DeepSeekConnector())]:
        monkeypatch.delenv(name, raising=False)
        try:
            connector.generate("prompt", "context")
        except RuntimeError as exc:
            assert "not configured" in str(exc)
        else:
            raise AssertionError("connector should require an API key")


def test_synthetic_examples_exist():
    root = Path(__file__).parents[1] / "examples"
    assert (root / "repo1_circular_import" / "README.md").exists()
    assert (root / "repo2_hidden_env" / "README.md").exists()
    assert (root / "repo3_type_mismatch" / "README.md").exists()
