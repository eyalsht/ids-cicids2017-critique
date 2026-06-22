"""Reusable, unit-tested core for the CICIDS2017 critique.

This package factors the notebook's stateless, dataset-independent helpers into a clean,
importable library with separate concerns:

- :mod:`ids_critique.config`   -- constants and the weekday split key.
- :mod:`ids_critique.data`     -- loading/cleaning primitives (whitespace, Inf, duplicates).
- :mod:`ids_critique.features` -- feature engineering (skew, log1p, correlation pruning).
- :mod:`ids_critique.evaluate` -- the IDS metric suite.
- :mod:`ids_critique.critique` -- the flaw deltas that drive the critique narrative.

The notebook remains the primary, self-contained analysis artifact; this package is the
canonical, tested implementation of the same logic.
"""

from ids_critique.config import RANDOM_STATE, WEEKDAY_ORDER

__all__ = ["RANDOM_STATE", "WEEKDAY_ORDER"]
