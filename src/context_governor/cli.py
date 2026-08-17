"""Command-line interface for Context Governor."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="acg-cli",
        description="Audit a repository with the Adaptive Context Governor.",
    )
    subparsers = parser.add_subparsers(dest="command")
    audit = subparsers.add_parser("audit", help="Run a local context-density audit.")
    audit.add_argument("--path", required=True, help="Repository path to inspect.")
    audit.add_argument("--question", required=True, help="Question used for the audit.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "audit":
        print(f"ACG audit initialized for {args.path}")
        print(f"Question: {args.question}")
        return 0
    build_parser().print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
