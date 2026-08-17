"""Optional integration with the llmfit local-model recommender.

llmfit remains an external executable. This module never downloads or executes
code automatically; it only invokes an executable already present on PATH or a
caller-supplied command and parses its JSON output.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass


class LlmfitUnavailable(RuntimeError):
    """Raised when llmfit is not installed or returns invalid output."""


@dataclass(frozen=True)
class LocalModelRecommendation:
    """Normalized recommendation fields used by Context Governor."""

    name: str
    fit: str | None = None
    score: float | None = None
    estimated_tps: float | None = None
    context_length: int | None = None
    runtime: str | None = None

    @classmethod
    def from_mapping(cls, value: dict) -> "LocalModelRecommendation":
        return cls(
            name=str(value.get("name") or value.get("model") or "unknown"),
            fit=value.get("fit"),
            score=value.get("score"),
            estimated_tps=value.get("estimated_tps", value.get("tps")),
            context_length=value.get("context_length", value.get("ctx")),
            runtime=value.get("runtime"),
        )


def recommend_local_models(
    *,
    use_case: str = "coding",
    limit: int = 5,
    executable: str = "llmfit",
    timeout: int = 30,
) -> list[LocalModelRecommendation]:
    """Return llmfit JSON recommendations for the current machine.

    The command follows llmfit's documented automation interface:
    ``llmfit recommend --json --use-case ... --limit ...``.
    """
    if limit < 1:
        raise ValueError("limit must be positive")
    command = shutil.which(executable) if "/" not in executable else executable
    if not command:
        raise LlmfitUnavailable(
            "llmfit is not installed; install it from https://github.com/AlexsJones/llmfit"
        )
    result = subprocess.run(
        [command, "recommend", "--json", "--use-case", use_case, "--limit", str(limit)],
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode:
        raise LlmfitUnavailable(result.stderr.strip() or "llmfit recommendation failed")
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise LlmfitUnavailable("llmfit returned non-JSON output") from exc
    rows = payload.get("models", payload) if isinstance(payload, dict) else payload
    if not isinstance(rows, list):
        raise LlmfitUnavailable("llmfit JSON did not contain a model list")
    return [LocalModelRecommendation.from_mapping(row) for row in rows if isinstance(row, dict)]
