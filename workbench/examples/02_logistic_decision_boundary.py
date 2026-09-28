# %% [markdown]
# # 02 - Two-feature logistic decision boundary (one coefficient is zero)
#
# **Given:** log-odds = b0 + b1*x1 + b2*x2 with supplied coefficients where
# **b2 = 0**. Tie rule: a point *on* the boundary (probability exactly 0.5)
# is classified as **class 1**. Values are illustrative.
#
# **Operation requested:** SOLVE for the boundary (an equation) and for the
# class-1 region (an inequality). This is an exact, symbolic question: nothing
# is fit and nothing is searched numerically.
#
# **Library choice:** SymPy (`sp.solve` for the boundary, `sp.solveset` for the
# region), then NumPy/SciPy to check numerically, then Matplotlib to draw it.
# `stats find "solve classifier decision boundary"`.

# %%
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from scipy.special import expit

# %% [markdown]
# ## Code: symbols are unknowns, not numbers
# `sp.Rational` keeps answers exact (3/2 rather than 1.4999999).

# %%
x1, x2 = sp.symbols("x1 x2", real=True)
b0, b1, b2 = sp.Rational(-3), sp.Rational(2), sp.Rational(0)   # GIVEN

log_odds = b0 + b1 * x1 + b2 * x2
print("log-odds expression:", log_odds)            # x2 has vanished: 2*x1 - 3

boundary_x1 = sp.solve(sp.Eq(log_odds, 0), x1)
boundary_x2 = sp.solve(sp.Eq(log_odds, 0), x2)
print("solve for x1:", boundary_x1)                # [3/2] -> vertical line x1 = 3/2
print("solve for x2:", boundary_x2)                # []   -> x2 cannot move the decision

# Class 1 when probability >= 0.5  <=>  log_odds >= 0 (expit is increasing)
class1_region = sp.solveset(log_odds >= 0, x1, domain=sp.S.Reals)
boundary_only = sp.solveset(sp.Eq(log_odds, 0), x1, domain=sp.S.Reals)
print("class-1 region in x1:", class1_region)      # Interval(3/2, oo): closed at 3/2
print("boundary points     :", boundary_only)      # {3/2}

# %% [markdown]
# ## What the output means
# * The **boundary** is the set where log-odds = 0: the vertical line `x1 = 3/2`
#   for every x2. It is a line, not a region.
# * The **class-1 region** is `x1 >= 3/2` (closed, because ties go to class 1).
#   It contains the boundary, but the two are different sets.
# * `solve(..., x2)` returning `[]` is informative. Because `b2 = 0`, x2 never
#   changes the prediction, so there is no x2-value that "solves" anything.

# %% [markdown]
# ## Validation checks: evaluate numerically at points left of, on, and right of the line

# %%
f_log_odds = sp.lambdify((x1, x2), log_odds, "numpy")
test_points = np.array([[1.0, -5.0], [1.5, 0.0], [1.5, 99.0], [2.0, 3.0]])
numeric_log_odds = f_log_odds(test_points[:, 0], test_points[:, 1])
probability = expit(numeric_log_odds)
predicted_class = np.where(probability >= 0.5, 1, 0)   # GIVEN tie rule: >=
print(np.column_stack([test_points, probability, predicted_class]))

assert boundary_x1 == [sp.Rational(3, 2)] and boundary_x2 == []
assert sp.Rational(3, 2) in class1_region
assert list(predicted_class) == [0, 1, 1, 1]
assert all(
    (sp.Float(px) in class1_region) == bool(c) for px, c in zip(test_points[:, 0], predicted_class)
)
print("all checks passed")

# %% [markdown]
# ## Picture (shows the result; the computation above is the answer)

# %%
xx, yy = np.meshgrid(np.linspace(-1, 4, 300), np.linspace(-3, 3, 300))
zz = f_log_odds(xx, yy) + 0 * yy          # + 0*yy keeps the grid shape when x2 drops out
fig, ax = plt.subplots(figsize=(6, 4))
ax.contourf(xx, yy, (zz >= 0).astype(float), levels=[-0.5, 0.5, 1.5], alpha=0.25)
ax.contour(xx, yy, zz, levels=[0], colors="black")
ax.scatter(test_points[:, 0], np.clip(test_points[:, 1], -3, 3), c=predicted_class, cmap="coolwarm")
ax.set(xlabel="x1", ylabel="x2", title="Class 1 (shaded) where 2*x1 - 3 >= 0")
plt.show()
