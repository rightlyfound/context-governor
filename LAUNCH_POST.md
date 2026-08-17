# Launch Post Draft

**Context Governor is now open source.**

ACG introduces an auditable way to detect context deficits, request missing repository anchors, and preserve structural continuity before an agent answers. The repository includes a CLI, optional provider connectors, synthetic debugging tasks, a reproducible scorer, and a local showcase dashboard.

Run it locally:

```bash
git clone https://github.com/rightlyfound/context-governor.git
cd context-governor
pip install -e ".[dev]"
pytest
python scripts/showcase.py
python scripts/dashboard.py
```

The showcase reports each provider as measured or `SKIPPED (no API key)`. It does not fabricate comparative results. Contributions are welcome from AI engineers, open-source developers, and benchmark researchers.
