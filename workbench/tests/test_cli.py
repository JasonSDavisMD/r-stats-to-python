"""CLI behaviour: exit codes and the key lines a user relies on."""

from psl.finder.cli import main


def test_find_prints_import_and_docs(capsys):
    assert main(["find", "R", "plogis"]) == 0
    out = capsys.readouterr().out
    assert "from scipy.special import expit" in out and "docs: https://" in out


def test_find_without_match_exits_1(capsys):
    assert main(["find", "zzqqxx"]) == 1


def test_show_full_and_code_only(capsys):
    assert main(["show", "expit"]) == 0
    assert "EXAMPLE" in capsys.readouterr().out
    assert main(["show", "expit", "--code"]) == 0
    assert capsys.readouterr().out.lstrip().startswith("import numpy")


def test_show_unknown_suggests(capsys):
    assert main(["show", "expitt"]) == 1
    assert "Did you mean: expit" in capsys.readouterr().out


def test_r_lookup_and_table(capsys):
    assert main(["r", "qlogis"]) == 0
    assert "logit(probability)" in capsys.readouterr().out
    assert main(["r"]) == 0
    assert len(capsys.readouterr().out.splitlines()) > 50


def test_list_and_kinds(capsys):
    assert main(["list", "--topic", "trees"]) == 0
    assert "tree-regressor" in capsys.readouterr().out
    assert main(["kinds"]) == 0
    assert "optimize" in capsys.readouterr().out
