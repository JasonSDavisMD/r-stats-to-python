"""Catalog integrity: every shipped entry is valid, linked, and runnable.

Running each entry's example against the installed library versions catches
API drift (renamed arguments, deprecations) that a text review would miss.
Entries for optional add-ons (torch, pymc, ...) are skipped when the add-on
is not installed; CI installs every add-on so they are still exercised.
"""

import tomllib
import warnings

import matplotlib.pyplot as plt
import pytest

from conftest import WORKBENCH
from statsbench.finder import KINDS, load_catalog

EXTRAS = set(tomllib.loads((WORKBENCH / "pyproject.toml").read_text())["project"]["optional-dependencies"])


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


def test_optional_entries_name_a_real_extra(catalog):
    for entry in catalog.entries:
        assert bool(entry.requires) == bool(entry.extra), f"{entry.id}: set both requires and extra"
        if entry.extra:
            assert entry.extra in EXTRAS, f"{entry.id}: extra '{entry.extra}' not in pyproject"


@pytest.mark.parametrize("entry", load_catalog().entries, ids=lambda e: e.id)
def test_entry_example_runs(entry):
    missing = entry.missing_modules()
    if missing:
        pytest.skip(f"optional add-on '{entry.extra}' not installed ({', '.join(missing)})")
    with warnings.catch_warnings():
        warnings.simplefilter("error", FutureWarning)       # deprecated API = failure
        warnings.simplefilter("error", DeprecationWarning)
        exec(compile(entry.example, f"<catalog:{entry.id}>", "exec"), {"__name__": "__main__"})
    plt.close("all")
