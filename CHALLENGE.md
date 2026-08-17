# Context Density Challenge

The Context Density Challenge evaluates how an agent diagnoses small but realistic repository defects while controlling context and interaction overhead.

## Tasks

The included tasks cover circular imports, undocumented environment-variable dependencies, and a function-signature type mismatch. Participants may run the examples locally and submit a corrected patch.

## Metrics

**Precision** is the percentage similarity between expected and submitted corrected lines, computed with a line-based sequence matcher. **Token Economy** is the number of source lines used as a deterministic local proxy for tokens in offline mode; live adapters should replace this with provider usage metadata. **Round-Trip Efficiency** is the number of user-assistant exchanges required to produce the final patch. These definitions are intentionally explicit so results can be reproduced and audited.

## Run locally

```bash
pip install -e ".[dev]"
pytest
python challenge.py --repo examples/repo3_type_mismatch --model mock
python scripts/showcase.py
python scripts/dashboard.py
```

Live providers are optional. Missing credentials are reported as `SKIPPED (no API key)` rather than treated as failures.
