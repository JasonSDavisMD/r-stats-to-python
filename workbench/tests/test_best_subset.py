"""best_subset recipe: behaviour that is ours, not re-testing LinearRegression."""

import numpy as np
import pandas as pd
import pytest

from psl.recipes.best_subset import best_subset


@pytest.fixture
def data():
    rng = np.random.default_rng(0)
    X = pd.DataFrame(rng.normal(size=(100, 5)), columns=list("abcde"))
    y = 3 * X["b"] - 2 * X["d"] + rng.normal(scale=0.3, size=100)
    return X, y


def test_best_per_size_recovers_true_predictors(data):
    table = best_subset(*data)
    assert list(table["size"]) == [0, 1, 2, 3, 4, 5]
    assert set(table.loc[2, "predictors"]) == {"b", "d"}
    assert table.loc[0, "predictors"] == ()
    assert np.all(np.diff(table["rss"]) <= 1e-9)


def test_all_models_counts_every_subset(data):
    table = best_subset(*data, max_size=2, all_models=True)
    assert len(table) == 1 + 5 + 10


def test_input_validation(data):
    X, y = data
    with pytest.raises(TypeError):
        best_subset(X.to_numpy(), y)
    with pytest.raises(ValueError):
        best_subset(X, y[:-1])
    with pytest.raises(ValueError):
        best_subset(X, y, max_size=9)
