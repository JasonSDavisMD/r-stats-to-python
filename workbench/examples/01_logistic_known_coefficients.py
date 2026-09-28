# %% [markdown]
# # 01 - Logistic probabilities from KNOWN coefficients
#
# **Given:** a logistic model's coefficients are supplied (intercept `b0`, slope `b1`)
# and a few feature values `x`. Values here are illustrative, not from any assignment.
#
# **Operation requested:** EVALUATE the model: turn each x into a probability,
# then into a class with a 50% cutoff and a strict `>` rule.
#
# **Library choice:** nothing is estimated, so there is nothing to *fit*.
# NumPy computes the log-odds `b0 + b1*x`, and `scipy.special.expit` maps
# log-odds to probability (R: `plogis`).
# `stats find "R plogis"` -> `expit`;  `stats show logistic-predict-known-params`.
#
# Run cells with Shift+Enter (Interactive Window) or "Run Cell" above each `# %%`.

# %%
import numpy as np
from scipy.special import expit, logit

# %% [markdown]
# ## Code
# Assignments are *snapshots*: if you change `b1` later you must re-run the
# cells that use it. Unlike a spreadsheet, nothing updates by itself.
# Restart + Run All reproduces everything.

# %%
b0 = -1.5            # GIVEN intercept
b1 = 0.8             # GIVEN slope
threshold = 0.5      # GIVEN cutoff; rule: class 1 iff probability > threshold (strict)

x = np.array([0.0, 1.0, 1.875, 3.0, 5.0])   # 1.875 sits exactly on the boundary

log_odds = b0 + b1 * x
probability = expit(log_odds)
predicted_class = np.where(probability > threshold, 1, 0)

for xi, lo, p, c in zip(x, log_odds, probability, predicted_class):
    print(f"x={xi:6.3f}  log_odds={lo:+.3f}  probability={p:.4f}  class={c}")

# %% [markdown]
# ## What the output means
# * `probability` is P(Y = 1 | x) under the given model.
# * At `x = 1.875` the log-odds is 0 and the probability is exactly 0.5. The
#   strict rule `>` puts that point in class **0**. With `>=` it would be class 1.
# * The boundary in x is where log-odds = 0, i.e. `x = -b0 / b1`. Because
#   `expit` is increasing, `probability > 0.5` is the same as `log_odds > 0`.

# %%
boundary_x = -b0 / b1
inclusive_class = np.where(probability >= threshold, 1, 0)
print("boundary x:", boundary_x)
print("strict  > :", predicted_class)
print("incl.  >= :", inclusive_class)

# %% [markdown]
# ## Validation checks
# 1. `expit` equals the textbook formula `1 / (1 + exp(-z))`.
# 2. `logit` really inverts `expit` (round trip).
# 3. The probability cutoff and the log-odds cutoff give identical classes.
#    `logit(threshold)` converts one into the other.

# %%
assert np.allclose(probability, 1 / (1 + np.exp(-log_odds)))
assert np.allclose(logit(probability), log_odds)
assert np.array_equal(predicted_class, np.where(log_odds > logit(threshold), 1, 0))
assert np.isclose(expit(b0 + b1 * boundary_x), 0.5)
assert predicted_class[x == 1.875][0] == 0 and inclusive_class[x == 1.875][0] == 1
print("all checks passed")
