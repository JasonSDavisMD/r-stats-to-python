# %% [markdown]
# # 05 - Regression tree: splits, predictions, and cross-validated depth
#
# **Given:** synthetic data with two features where y jumps at x1 = 4 and again at x2 = 6.
#
# **Operation requested:** FIT a regression tree (R: `rpart`), read the split
# rules, EVALUATE predictions for new points, and choose depth by 5-fold CV.
#
# **Library choice:** `sklearn.tree.DecisionTreeRegressor`, `export_text` to
# print the splits, `sklearn.model_selection.cross_val_score` for CV.

# %%
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import KFold, cross_val_score
from sklearn.tree import DecisionTreeRegressor, export_text, plot_tree

# %%
rng = np.random.default_rng(598)
n = 300
X = rng.uniform(0, 10, size=(n, 2))
y = np.where(X[:, 0] <= 4, 1.0, 5.0) + np.where(X[:, 1] > 6, 3.0, 0.0) + rng.normal(scale=0.5, size=n)

# %% [markdown]
# ## Fit and read the splits
# Rule: `feature <= threshold` goes LEFT. Each leaf predicts the **mean of the
# training y** that fall in it.

# %%
tree = DecisionTreeRegressor(max_depth=2, random_state=0).fit(X, y)
print(export_text(tree, feature_names=["x1", "x2"], decimals=3))

new_points = np.array([[2.0, 2.0], [2.0, 8.0], [7.0, 2.0], [7.0, 8.0]])
print("predictions:", tree.predict(new_points).round(3))

# %% [markdown]
# ## Choose depth by cross-validation
# `cross_val_score` refits the tree on each training fold and scores it on the
# held-out fold. sklearn reports *negative* MSE (it always maximizes), so negate it.

# %%
cv = KFold(n_splits=5, shuffle=True, random_state=0)
depths = range(1, 9)
cv_mse = [
    -cross_val_score(DecisionTreeRegressor(max_depth=d, random_state=0), X, y,
                     cv=cv, scoring="neg_mean_squared_error").mean()
    for d in depths
]
for d, m in zip(depths, cv_mse):
    print(f"max_depth={d}  CV MSE={m:.3f}")
best_depth = list(depths)[int(np.argmin(cv_mse))]
print("best depth:", best_depth)

# %% [markdown]
# ## What the output means
# * The first split finds the big jump at x1 ~ 4. The next splits find x2 ~ 6.
# * CV MSE falls sharply up to the depth that captures both jumps (the noise
#   variance here is 0.25), then stays flat or rises as deeper trees fit noise.

# %% [markdown]
# ## Validation checks
# 1. A tree prediction equals the mean training y in that point's leaf (`tree.apply`).
# 2. The root split is on x1 near 4.

# %%
train_leaf = tree.apply(X)
for point, pred in zip(new_points, tree.predict(new_points)):
    leaf = tree.apply(point.reshape(1, -1))[0]
    assert np.isclose(pred, y[train_leaf == leaf].mean())
assert tree.tree_.feature[0] == 0 and abs(tree.tree_.threshold[0] - 4) < 0.3
assert min(cv_mse) < 0.4
print("all checks passed")

# %%
fig, ax = plt.subplots(figsize=(9, 4))
plot_tree(tree, feature_names=["x1", "x2"], filled=True, ax=ax)
plt.show()
