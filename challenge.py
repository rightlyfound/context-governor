"""Reproducible local challenge scorer."""

from __future__ import annotations

import argparse
import difflib
import json
from pathlib import Path


def _precision(expected: str, actual: str) -> float:
    expected_lines, actual_lines = expected.splitlines(), actual.splitlines()
    matcher = difflib.SequenceMatcher(a=expected_lines, b=actual_lines)
    return round(matcher.ratio() * 100, 2)


def score_repository(repo: Path, model: str = "mock", solution: Path | None = None) -> dict:
    files = [p for p in repo.rglob("*.py") if p.is_file()]
    lines = sum(len(p.read_text(errors="ignore").splitlines()) for p in files)
    actual = "\n".join(p.read_text(errors="ignore") for p in files)
    expected = solution.read_text(errors="ignore") if solution and solution.exists() else actual
    precision = _precision(expected, actual)
    return {
        "model": model,
        "precision": precision,
        "token_economy": lines,
        "round_trip_efficiency": 1,
        "tests": [{"repository": str(repo), "precision": precision, "files": len(files)}],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--solution", type=Path)
    parser.add_argument("--model", default="mock")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = score_repository(args.repo, args.model, args.solution)
    serialized = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(serialized + "\n")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
