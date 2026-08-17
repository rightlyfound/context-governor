# Synthetic Benchmark Repositories

The showcase uses three deterministic defect classes. Each example is intentionally small so contributors can inspect, reproduce, and patch the issue without external services.

- `repo1_circular_import`: two modules import each other.
- `repo2_hidden_env`: startup requires an undocumented environment variable.
- `repo3_type_mismatch`: a function is called with a value of the wrong type.

Each directory contains a README describing the expected fix.
