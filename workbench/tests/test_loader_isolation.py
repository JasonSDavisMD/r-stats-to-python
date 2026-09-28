"""A broken topic file or entry must not prevent the others from loading."""

from statsbench.finder import load_catalog

GOOD = '''
[[entry]]
id = "good"
title = "A good entry"
kind = "evaluate"
library = "NumPy"
import = "import numpy as np"
call = "np.sum(x)"
example = "print(1)"
docs = "https://numpy.org/"
'''


def test_bad_file_is_skipped_and_reported(tmp_path):
    (tmp_path / "a_good.toml").write_text(GOOD)
    (tmp_path / "b_broken.toml").write_text("[[entry]\nid = ")
    catalog = load_catalog(tmp_path)
    assert [e.id for e in catalog.entries] == ["good"]
    assert any("b_broken.toml" in p for p in catalog.problems)


def test_invalid_entries_are_skipped_individually(tmp_path):
    bad_kind = GOOD.replace('id = "good"', 'id = "bad-kind"').replace("evaluate", "guess")
    missing = '[[entry]]\nid = "no-call"\ntitle = "x"\n'
    duplicate = GOOD
    (tmp_path / "t.toml").write_text(GOOD + bad_kind + missing + duplicate)
    catalog = load_catalog(tmp_path)
    assert [e.id for e in catalog.entries] == ["good"]
    assert len(catalog.problems) == 3
