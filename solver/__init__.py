"""Top‑level package for the linear system solver.

The original simple interactive ``main`` has been replaced by a
proper command‑line interface located in :mod:`solver.cli`.  Users can
still run ``python -m solver`` and obtain the same behaviour.
"""

from solver.alg import *  # noqa: F401  (exported for convenience)

from solver.cli import main  # re-export the CLI entry point


if __name__ == "__main__":
    main()