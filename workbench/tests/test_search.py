"""Search quality: queries from the handoff must surface the right entry first."""

import pytest

from psl.finder import Index


@pytest.fixture(scope="module")
def index(catalog):
    return Index(catalog)


def top_ids(index, query, n=3, **kw):
    return [hit.entry.id for hit in index.search(query, limit=n, **kw)]


@pytest.mark.parametrize(
    "query, expected_first",
    [
        ("inverse logit", "expit"),
        ("R plogis", "expit"),
        ("plogis", "expit"),
        ("qlogis", "logit"),
        ("logit", "logit"),
        ("fit logistic regression with coefficient summary", "glm-binomial"),
        ("glm binomial", "glm-binomial"),
        ("solve classifier decision boundary", "sympy-solveset"),
        ("cross validation for a tree", "cross-val-score"),
        ("best subset", "best-subset"),
        ("tree", "tree-regressor"),
        ("spline", "smoothing-spline"),
        ("MASS::lda", "lda"),
        ("optim", "minimize"),
        ("uniroot", "brentq"),
        ("probabilities from given coefficients", "logistic-predict-known-params"),
    ],
)
def test_expected_first_hit(index, query, expected_first):
    assert top_ids(index, query)[0] == expected_first


def test_expit_and_logit_are_distinguished(index):
    assert top_ids(index, "inverse logit")[:2] == ["expit", "logit"]
    assert top_ids(index, "log odds of a probability")[0] == "logit"


def test_tree_cv_query_also_surfaces_a_tree(index):
    assert "tree-regressor" in top_ids(index, "cross validation for a tree", n=5)


def test_kind_filter(index):
    hits = index.search("logistic", kind="fit", limit=10)
    assert hits and all(hit.entry.kind == "fit" for hit in hits)
    assert "expit" not in [hit.entry.id for hit in hits]


def test_nonsense_and_stopword_queries_return_nothing(index):
    assert index.search("the of and") == []
    assert index.search("zzqqxx") == []
