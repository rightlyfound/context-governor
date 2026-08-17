"""Generate a lightweight HTML dashboard from showcase JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def generate_dashboard(results: Path, output: Path) -> None:
    data = json.loads(results.read_text())
    rows = "".join(f"<tr><td>{r['provider']}</td><td>{r['vanilla']}</td><td>{r['acg_wrapped']}</td><td>{r['precision']}</td></tr>" for r in data.get("providers", []))
    html = f"""<!doctype html><html><head><meta charset='utf-8'><title>ACG Showcase Dashboard</title><style>body{{font-family:system-ui;max-width:960px;margin:40px auto}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ddd;padding:10px;text-align:left}}th{{background:#172033;color:white}}</style></head><body><h1>ACG Showcase Dashboard</h1><p>Provider status and measured results from the auditable showcase run.</p><table><thead><tr><th>Provider</th><th>Vanilla</th><th>ACG-wrapped</th><th>Precision</th></tr></thead><tbody>{rows}</tbody></table></body></html>"""
    output.write_text(html)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=Path("showcase_output/showcase_logs/results.json"))
    parser.add_argument("--output", type=Path, default=Path("showcase_output/dashboard.html"))
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    generate_dashboard(args.results, args.output)
