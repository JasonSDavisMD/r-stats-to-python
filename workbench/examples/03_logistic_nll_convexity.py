# %% [markdown]
# # 03 - Negative log-likelihood, three ways, and why it is convex
#
# **Given:** synthetic binary data (x, y) generated from a known logistic model.
#
# **Operation requested:**
# 1. **fit** logistic regression from data (statsmodels GLM, R's `glm(family = binomial)`);
# 2. **evaluate** the negative log-likelihood (NLL) at a *given* coefficient vector;
# 3. **optimize** the NLL numerically and confirm it lands on the GLM answer;
# 4. **check convexity**: the Hessian X^T W X has no negative eigenvalues.
#
# **Library choice:** statsmodels (fit + inference), NumPy/SciPy
# (`log_expit` for a stable NLL, `scipy.optimize.minimize`), `np.linalg.eigvalsh`.

# %%
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.optimize import minimize
from scipy.special import expit, log_expit

# %% [markdown]
# ## Data (seeded, so Restart + Run All reproduces it exactly)

# %%
rng = np.random.default_rng(598)
n = 400
true_beta = np.array([-0.5, 1.2])
x = rng.normal(size=n)
y = rng.binomial(1, expit(true_beta[0] + true_beta[1] * x))
df = pd.DataFrame({"x": x, "y": y})
X = np.column_stack([np.ones(n), x])       # design matrix with intercept column

# %% [markdown]
# ## 1. FIT: the library does the maximum-likelihood estimation

# %%
glm_fit = smf.glm("y ~ x", data=df, family=sm.families.Binomial()).fit()
print(glm_fit.summary().tables[1])
glm_beta = glm_fit.params.to_numpy()

# %% [markdown]
# ## 2. EVALUATE: NLL at a given beta
# For one observation, log p = log_expit(eta) and log(1 - p) = log_expit(-eta).
# `log_expit` avoids log(0) when |eta| is large.

# %%
def negative_log_likelihood(beta, X, y):
    """-(sum y*log p + (1-y)*log(1-p)); beta is GIVEN, nothing is estimated here."""
    eta = X @ beta
    return -np.sum(y * log_expit(eta) + (1 - y) * log_expit(-eta))


def nll_gradient(beta, X, y):
    return X.T @ (expit(X @ beta) - y)


print("NLL at beta = 0      :", negative_log_likelihood(np.zeros(2), X, y))
print("NLL at the GLM answer:", negative_log_likelihood(glm_beta, X, y))

# %% [markdown]
# ## 3. OPTIMIZE: let SciPy search for the minimizer

# %%
result = minimize(negative_log_likelihood, x0=np.zeros(2), args=(X, y),
                  jac=nll_gradient, method="BFGS")
print(result.success, result.x)

# %% [markdown]
# ## 4. Convexity
# Hessian of the NLL = X^T W X with W = diag(p_i (1 - p_i)). For any vector v,
# v^T X^T W X v = sum_i w_i (x_i . v)^2 >= 0, so the Hessian is positive
# semidefinite for **every** beta. That makes the NLL convex: any local
# minimum is the global one, and the starting point does not matter.

# %%
def nll_hessian(beta, X):
    p = expit(X @ beta)
    return X.T @ (X * (p * (1 - p))[:, None])


for beta in [np.zeros(2), glm_beta, np.array([5.0, -7.0])]:
    print(beta.round(3), "eigenvalues:", np.linalg.eigvalsh(nll_hessian(beta, X)).round(4))

# %% [markdown]
# ## What the output means / validation checks
# * The optimizer and the GLM agree. Both compute the same MLE.
# * `glm_fit.llf` (log-likelihood) is exactly `-NLL` at the estimate.
# * Hessian eigenvalues are non-negative at every tested beta.
# * GLM standard errors = sqrt(diag(inverse Hessian at the MLE)).

# %%
assert result.success
assert np.allclose(result.x, glm_beta, atol=1e-4)
assert np.isclose(glm_fit.llf, -negative_log_likelihood(glm_beta, X, y))
for beta in [np.zeros(2), glm_beta, np.array([5.0, -7.0])]:
    assert np.all(np.linalg.eigvalsh(nll_hessian(beta, X)) >= -1e-10)
assert np.allclose(np.sqrt(np.diag(np.linalg.inv(nll_hessian(glm_beta, X)))), glm_fit.bse, rtol=1e-4)
print("all checks passed")
