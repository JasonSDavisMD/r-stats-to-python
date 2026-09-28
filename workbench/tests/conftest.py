"""Shared test setup: headless plotting and the workbench root path."""

from pathlib import Path

import matplotlib
import pytest

matplotlib.use("Agg")  # no windows during tests (also safe on CI / Windows)

WORKBENCH = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def catalog():
    from statsbench.finder import load_catalog

    return load_catalog()
