"""Catalog integrity: every shipped entry is valid, linked, and runnable.

Running each entry's example against the installed library versions catches
API drift (renamed arguments, deprecations) that a text review would miss.
"""

import warnings

import matplotlib.pyplot as plt
import pytest

from conftest import WORKBENCH
from psl.finder import KINDS, load_catalog


def test_catalog_loads_without_problems(catalog):
    assert catalog.problems == []
    assert len(catalog.entries) >= 60


def test_cross_references_resolve(catalog):
    ids = {entry.id for entry in catalog.entries}
    for entry in catalog.entries:
        assert entry.kind in KINDS
        for other in entry.see_also:
            assert other in ids, f"{entry.id}: see_also '{other}' does not exist"
        if entry.recipe:
            assert (WORKBENCH / entry.recipe).is_file(), f"{entry.id}: missing {entry.recipe}"


def _entries():
    return load_catalog(WORKBENCH / "catalog").entries


@pytest.mark.parametrize("entry", _entries(), ids=lambda e: e.id)
def test_entry_example_runs(entry):
    with warnings.catch_warnings():
        warnings.simplefilter("error", FutureWarning)       # deprecated API = failure
        warnings.simplefilter("error", DeprecationWarning)
        exec(compile(entry.example, f"<catalog:{entry.id}>", "exec"), {"__name__": "__main__"})
    plt.close("all")
