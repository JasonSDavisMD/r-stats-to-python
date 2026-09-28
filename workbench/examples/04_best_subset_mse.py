# %% [markdown]
# # 04 - Best subset selection with train and test MSE
#
# **Given:** synthetic data with 6 candidate predictors, of which only 3
# (`x1`, `x3`, `x5`) truly affect y. A fixed train/test split.
#
# **Operation requested:** for each model size k, FIT every k-predictor linear
# model on the training rows, keep the best by training RSS (R:
# `leaps::regsubsets`). Then EVALUATE each size's best model on the test rows.
#
# **Library choice:** there is no single sklearn/statsmodels call for exhaustive
# best subset, so `psl.recipes.best_subset` loops over
# `LinearRegression().fit(X[cols], y)`. Test error uses
# `sklearn.metrics.mean_squared_error`. We refit the chosen columns *visibly*.

# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

from psl.recipes.best_subset import best_subset

# %%
rng = np.random.default_rng(598)
n, p = 200, 6
X = pd.DataFrame(rng.normal(size=(n, p)), columns=[f"x{j}" for j in range(1, p + 1)])
y = 1.0 + 2.0 * X["x1"] - 1.5 * X["x3"] + 1.0 * X["x5"] + rng.normal(scale=1.0, size=n)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)

# %% [markdown]
# ## Best model of each size (by TRAINING RSS)

# %%
table = best_subset(X_train, y_train)

test_mse = []
for predictors in table["predictors"]:
    if predictors:
        model = LinearRegression().fit(X_train[list(predictors)], y_train)
        y_hat = model.predict(X_test[list(predictors)])
    else:                                            # size 0: intercept-only model
        y_hat = np.full(len(y_test), y_train.mean())
    test_mse.append(mean_squared_error(y_test, y_hat))
table["test_mse"] = test_mse
print(table.to_string(index=False))

# %% [markdown]
# ## What the output means
# * `train_mse` can only go down as k grows: more predictors never fit training
#   data worse. It cannot be used to choose k.
# * `test_mse` drops until the true predictors are in, then flattens or rises
#   (extra noise predictors add variance). Pick k by test/CV error, Cp, AIC or BIC.

# %%
best_k = int(table.loc[table["test_mse"].idxmin(), "size"])
print("size with lowest test MSE:", best_k, table.loc[best_k, "predictors"])

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(table["size"], table["train_mse"], "o-", label="train MSE")
ax.plot(table["size"], table["test_mse"], "s-", label="test MSE")
ax.set(xlabel="number of predictors k", ylabel="MSE")
ax.legend()
plt.show()

# %% [markdown]
# ## Validation checks
# 1. Training RSS is non-increasing in k.
# 2. The full-size row equals an ordinary LinearRegression on all predictors.
# 3. The size-3 winner is the true set {x1, x3, x5} (strong signal, so expected).

# %%
assert np.all(np.diff(table["rss"]) <= 1e-9)
full = LinearRegression().fit(X_train, y_train)
full_rss = float(np.sum((y_train - full.predict(X_train)) ** 2))
assert np.isclose(table.loc[p, "rss"], full_rss)
assert set(table.loc[3, "predictors"]) == {"x1", "x3", "x5"}
print("all checks passed")
