"""Run the reproducible local showcase."""

from __future__ import annotations

import json
import os
from pathlib import Path

PROVIDERS = {
    "OpenAI GPT-4o": "OPENAI_API_KEY",
    "Anthropic Claude": "ANTHROPIC_API_KEY",
    "DeepSeek": "DEEPSEEK_API_KEY",
}


def run_showcase(output: Path) -> str:
    output.mkdir(parents=True, exist_ok=True)
    rows = []
    for provider, key in PROVIDERS.items():
        status = "READY (live key configured)" if os.getenv(key) else "SKIPPED (no API key)"
        rows.append({"provider": provider, "vanilla": status, "acg_wrapped": status, "token_economy": "not measured", "precision": "not measured", "round_trips": "not measured"})
    raw = {"tasks": ["circular-import", "hidden-env-var", "type-mismatch"], "providers": rows, "mode": "live-if-configured"}
    (output / "showcase_logs").mkdir(exist_ok=True)
    (output / "showcase_logs" / "results.json").write_text(json.dumps(raw, indent=2) + "\n")
    lines = ["# Showcase Results", "", "Results are reproducible and never fabricate scores. Providers without credentials are skipped.", "", "| Provider | Vanilla | ACG-wrapped | Token Economy | Precision | Round Trips |", "|---|---|---|---|---|---|"]
    lines += [f"| {r['provider']} | {r['vanilla']} | {r['acg_wrapped']} | {r['token_economy']} | {r['precision']} | {r['round_trips']} |" for r in rows]
    report = "\n".join(lines) + "\n"
    (output / "showcase_results.md").write_text(report)
    return report


if __name__ == "__main__":
    print(run_showcase(Path("showcase_output")))
