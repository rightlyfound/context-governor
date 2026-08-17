"""Run the reproducible local showcase, optionally through OpenRouter."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from time import perf_counter

import requests

from context_governor.connectors.openrouter import OpenRouterConnector

MODELS = {
    "OpenAI GPT-4o": "openai/gpt-4o",
    "Anthropic Claude": "anthropic/claude-3.5-sonnet",
    "DeepSeek": "deepseek/deepseek-chat",
}
TASKS = {
    "circular-import": "a.py imports value_b from b.py while b.py imports value_a from a.py. State the minimal safe fix.",
    "hidden-env-var": "service.py reads SERVICE_PORT directly from os.environ and fails when absent. State the minimal safe fix.",
    "type-mismatch": "format_user(user_id: int) is called with the string 42. State the minimal safe fix.",
}


def _row(provider: str, status: str, **values: object) -> dict[str, object]:
    return {"provider": provider, "status": status, **values}


def _call(connector: OpenRouterConnector, task: str, wrapped: bool) -> tuple[str, int, float]:
    prompt = TASKS[task]
    context = "Use only the supplied repository anchor. Request missing context before guessing." if wrapped else ""
    started = perf_counter()
    response = connector.generate(prompt, context)
    elapsed = round(perf_counter() - started, 3)
    return response, connector.token_count(prompt + context + response), elapsed


def run_showcase(output: Path, openrouter: bool = False, models: dict[str, str] | None = None) -> str:
    output.mkdir(parents=True, exist_ok=True)
    logs = output / "showcase_logs"
    logs.mkdir(exist_ok=True)
    selected = models or MODELS
    rows: list[dict[str, object]] = []
    raw: dict[str, object] = {"tasks": list(TASKS), "mode": "openrouter" if openrouter else "offline", "results": []}
    for name, model in selected.items():
        if not openrouter:
            rows.append(_row(name, "SKIPPED (offline mode)", model=model))
            continue
        connector = OpenRouterConnector(model=model)
        if not connector.configured:
            rows.append(_row(name, "SKIPPED (no API key)", model=model))
            continue
        for task in TASKS:
            for wrapped in (False, True):
                try:
                    response, tokens, elapsed = _call(connector, task, wrapped)
                    raw["results"].append({"provider": name, "model": model, "task": task, "mode": "acg" if wrapped else "vanilla", "response": response, "tokens": tokens, "round_trips": 1, "elapsed_seconds": elapsed})
                except requests.RequestException as exc:
                    raw["results"].append({"provider": name, "model": model, "task": task, "mode": "acg" if wrapped else "vanilla", "status": f"ERROR: {exc}"})
        rows.append(_row(name, "MEASURED", model=model))
    (logs / "results.json").write_text(json.dumps(raw, indent=2) + "\n")
    lines = ["# Showcase Results", "", "All provider statuses and raw responses are saved in `showcase_logs/results.json`.", "", "| Provider | Model | Status |", "|---|---|---|"]
    lines += [f"| {r['provider']} | {r['model']} | {r['status']} |" for r in rows]
    report = "\n".join(lines) + "\n"
    (output / "showcase_results.md").write_text(report)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("showcase_output"))
    parser.add_argument("--openrouter", action="store_true")
    args = parser.parse_args()
    print(run_showcase(args.output, args.openrouter))
