"""Best-subset selection for linear regression (R: ``leaps::regsubsets``).

Neither scikit-learn nor statsmodels ships exhaustive best-subset search,
so this is a thin, transparent loop. For every predictor combination of
size k, the exact underlying call is::

    LinearRegression().fit(X[list(columns)], y)

It keeps the combination with the smallest training RSS for each k. It
returns plain data (a DataFrame of column tuples and scores), not a hidden
model object. You refit the chosen columns yourself, so the library call
stays visible in your notebook.
"""

from __future__ import annotations

from itertools import combinations
from math import comb

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

MAX_MODELS = 2_000_000  # guard: exhaustive search grows as 2**p


def best_subset(
    X: pd.DataFrame,
    y,
    max_size: int | None = None,
    all_models: bool = False,
) -> pd.DataFrame:
    """Search every predictor subset up to ``max_size``; rank by training RSS.

    Parameters
    ----------
    X : DataFrame of candidate predictors (column names are reported back).
    y : 1-D response aligned with X.
    max_size : largest subset size to try (default: all columns).
    all_models : if True return every fitted subset, else the best per size.

    Returns
    -------
    DataFrame with columns ``size``, ``predictors`` (tuple of names),
    ``rss``, ``train_mse`` and ``r2``, sorted by size then RSS.
    Size 0 is the intercept-only model.
    """
    if not isinstance(X, pd.DataFrame):
        raise TypeError("X must be a pandas DataFrame so predictors keep their names")
    y = np.asarray(y, dtype=float).ravel()
    if len(y) != len(X):
        raise ValueError(f"X has {len(X)} rows but y has {len(y)} values")
    p = X.shape[1]
    max_size = p if max_size is None else max_size
    if not 0 <= max_size <= p:
        raise ValueError(f"max_size must be between 0 and {p}")
    n_models = sum(comb(p, k) for k in range(max_size + 1))
    if n_models > MAX_MODELS:
        raise ValueError(
            f"{n_models:,} subsets is too many for exhaustive search; lower "
            "max_size or use sklearn.feature_selection.SequentialFeatureSelector"
        )

    n = len(y)
    total_ss = float(np.sum((y - y.mean()) ** 2))
    rows = []
    for size in range(max_size + 1):
        for columns in combinations(X.columns, size):
            if size == 0:
                residuals = y - y.mean()
            else:
                model = LinearRegression().fit(X[list(columns)], y)
                residuals = y - model.predict(X[list(columns)])
            rss = float(residuals @ residuals)
            rows.append(
                {
                    "size": size,
                    "predictors": tuple(columns),
                    "rss": rss,
                    "train_mse": rss / n,
                    "r2": 1 - rss / total_ss if total_ss > 0 else np.nan,
                }
            )

    table = pd.DataFrame(rows).sort_values(["size", "rss"], kind="stable")
    if not all_models:
        table = table.groupby("size", sort=True).head(1)
    return table.reset_index(drop=True)
