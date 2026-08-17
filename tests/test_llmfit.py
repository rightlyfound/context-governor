import json
import subprocess

import pytest

from context_governor.llmfit import LlmfitUnavailable, recommend_local_models


def test_recommend_local_models_parses_documented_json(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/llmfit")
    captured = {}

    def fake_run(command, **kwargs):
        captured["command"] = command
        return subprocess.CompletedProcess(command, 0, json.dumps({"models": [{"name": "Qwen", "fit": "good", "tps": 22.5}]}), "")

    monkeypatch.setattr(subprocess, "run", fake_run)
    results = recommend_local_models(use_case="coding", limit=3)
    assert captured["command"][-4:] == ["--use-case", "coding", "--limit", "3"]
    assert results[0].name == "Qwen"
    assert results[0].estimated_tps == 22.5


def test_recommend_local_models_missing_executable(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda _: None)
    with pytest.raises(LlmfitUnavailable):
        recommend_local_models()
