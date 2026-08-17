"""Command-line interface for Context Governor."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import build_anchor_request, compute_density, should_halt
from .llmfit import LlmfitUnavailable, recommend_local_models


def _files(path: Path) -> list[Path]:
    return [p for p in path.rglob("*") if p.is_file() and ".git" not in p.parts]


def audit(path: Path, question: str) -> int:
    records = [{"file": str(p), "density": compute_density(p.read_text(errors="ignore"))} for p in _files(path)]
    overall = round(sum(r["density"] for r in records) / len(records), 6) if records else 0.0
    payload = {"question": question, "overall_density": overall, "files": records}
    if should_halt(overall):
        payload["anchor_request"] = build_anchor_request([r["file"] for r in records if r["density"] < 0.65])
    print(json.dumps(payload, indent=2))
    return 0


def benchmark(path: Path, model: str) -> int:
    from challenge import score_repository
    print(json.dumps(score_repository(path, model=model), indent=2))
    return 0


def local_models(use_case: str, limit: int) -> int:
    try:
        recommendations = recommend_local_models(use_case=use_case, limit=limit)
    except LlmfitUnavailable as exc:
        print(json.dumps({"status": "UNAVAILABLE", "error": str(exc)}, indent=2))
        return 2
    print(json.dumps({"status": "OK", "models": [r.__dict__ for r in recommendations]}, indent=2))
    return 0


def showcase(output: Path) -> int:
    from scripts.showcase import run_showcase
    output.mkdir(parents=True, exist_ok=True)
    report = run_showcase(output)
    print(report)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="acg-cli", description="Adaptive Context Governor tools")
    subparsers = parser.add_subparsers(dest="command", required=True)
    audit_parser = subparsers.add_parser("audit")
    audit_parser.add_argument("--path", type=Path, required=True)
    audit_parser.add_argument("--question", required=True)
    bench_parser = subparsers.add_parser("benchmark")
    bench_parser.add_argument("--path", type=Path, required=True)
    bench_parser.add_argument("--model", default="mock")
    local_parser = subparsers.add_parser("local-models", help="Recommend local models using llmfit.")
    local_parser.add_argument("--use-case", default="coding")
    local_parser.add_argument("--limit", type=int, default=5)
    show_parser = subparsers.add_parser("showcase")
    show_parser.add_argument("--output", type=Path, default=Path("showcase_output"))
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "audit":
        return audit(args.path, args.question)
    if args.command == "benchmark":
        return benchmark(args.path, args.model)
    if args.command == "local-models":
        return local_models(args.use_case, args.limit)
    return showcase(args.output)


if __name__ == "__main__":
    raise SystemExit(main())
