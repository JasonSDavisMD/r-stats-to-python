"""Shared test setup: single-threaded native libraries, headless plotting, paths."""

import os

# Cap native thread pools BEFORE numpy/sklearn/xgboost/lightgbm/torch load.
# Many small examples run back to back; letting each library start one OpenMP
# thread per core oversubscribes the CPU (seen as multi-minute stalls on busy
# or small CI machines). Set here, it also reaches the example subprocesses.
for _var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_var, "1")

from pathlib import Path  # noqa: E402

import matplotlib  # noqa: E402
import pytest  # noqa: E402

matplotlib.use("Agg")  # no windows during tests (also safe on CI / Windows)

WORKBENCH = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def catalog():
    from statsbench.finder import load_catalog

    return load_catalog()
