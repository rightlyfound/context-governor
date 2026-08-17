# Circular Import Example

`a.py` imports `value_b` from `b.py`, while `b.py` imports `value_a` from `a.py`. The expected fix is to move shared state into a third module or refactor the dependency direction.
