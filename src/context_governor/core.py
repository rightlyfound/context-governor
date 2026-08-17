"""Core Adaptive Context Governor functionality."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

_TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|\d+(?:\.\d+)?|[^\s]")
_SECTION_RE = re.compile(
    r"\[CODE_SNIPPET\]\s*(?P<file>[^\n]+)\n(?P<code>.*?)"
    r"(?=\n\[(?:CONTEXT_PREV|CONTEXT_NEXT|CODE_SNIPPET)\]|\Z)",
    re.DOTALL,
)


def _tokens(text: str) -> list[str]:
    return _TOKEN_RE.findall(text)


def compute_density(text: str, window: int = 512) -> float:
    """Return weighted lexical density in the range 0..1.

    Density is unique-token ratio, with structural identifiers receiving a
    modest weight. The window bounds work for large repositories while making
    the metric deterministic.
    """
    if not text or window <= 0:
        return 0.0
    tokens = _tokens(text)[:window]
    if not tokens:
        return 0.0
    counts = Counter(tokens)
    unique = len(counts)
    structural = sum(
        1
        for token in tokens
        if token in {"import", "from", "def", "class", "return", "async"}
    )
    weighted_unique = min(len(tokens), unique + structural * 0.15)
    return round(weighted_unique / len(tokens), 6)


def should_halt(density: float, threshold: float = 0.65) -> bool:
    """Return whether density indicates a context deficit."""
    return density < threshold


def build_anchor_request(missing_files: list[str]) -> dict[str, Any]:
    """Build the stable JSON-compatible payload requested by PRAR."""
    files = list(dict.fromkeys(missing_files))
    return {
        "status": "ANCHOR_REQUEST",
        "missing_anchors": files,
        "delimiters": {
            "code": "[CODE_SNIPPET]",
            "previous": "[CONTEXT_PREV]",
            "next": "[CONTEXT_NEXT]",
        },
    }


def process_anchors(anchor_text: str) -> dict[str, Any]:
    """Parse anchored blocks into a structured mapping by file."""
    result: dict[str, Any] = {"files": {}, "previous": [], "next": []}
    for match in _SECTION_RE.finditer(anchor_text or ""):
        result["files"][match.group("file").strip()] = match.group("code").strip()
    prev = re.search(r"\[CONTEXT_PREV\]\s*(.*?)(?=\n\[(?:CODE_SNIPPET|CONTEXT_NEXT)\]|\Z)", anchor_text or "", re.DOTALL)
    nxt = re.search(r"\[CONTEXT_NEXT\]\s*(.*?)(?=\n\[(?:CODE_SNIPPET|CONTEXT_PREV)\]|\Z)", anchor_text or "", re.DOTALL)
    if prev:
        result["previous"] = [line.strip() for line in prev.group(1).splitlines() if line.strip()]
    if nxt:
        result["next"] = [line.strip() for line in nxt.group(1).splitlines() if line.strip()]
    return result
