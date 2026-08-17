# Context Governor

Context Governor is an open-source Python project for experimenting with the Adaptive Context Governor (ACG) and Proactive Refusal with Anchored Reasoning (PRAR).

The project will provide context-density auditing, anchor-request middleware, provider connector abstractions, a command-line interface, benchmark utilities, and a Streamlit demonstration.

## Status

This repository has been initialized and the implementation is under active development.

## Development

The package targets Python 3.10 and later. Install the development dependencies with:

```bash
pip install -e ".[dev]"
```

Run the test suite with:

```bash
pytest
```

## OpenRouter Showcase

The optional showcase can route requests through OpenRouter's documented chat-completions endpoint. It reads `OPENROUTER_API_KEY` from the process environment at runtime and never writes the key to logs. Copy `.env.example` to `.env`, populate the key locally, and export it before running:

```bash
set -a
source .env
set +a
python scripts/showcase.py --openrouter --output showcase_results
python scripts/dashboard.py --results showcase_results/showcase_logs/results.json --output showcase_results/dashboard.html
```

Do not paste the key into chat, commit `.env`, or put it in GitHub. If it is exposed, revoke it in OpenRouter and create a replacement. A missing key produces `SKIPPED (no API key)` rather than a fabricated result.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
