# %% [markdown]
# # 06 - LDA and QDA: fit, then reproduce the discriminant by hand
#
# **Given:** two Gaussian classes in 2-D with different covariance matrices.
#
# **Operation requested:** FIT LDA (shared covariance, linear boundary) and QDA
# (class covariances, quadratic boundary). Then EVALUATE the discriminant
# score log pi_k + log N(x; mu_k, Sigma_k) by hand from the fitted parameters,
# and confirm it gives the same classes.
#
# **Library choice:** `sklearn.discriminant_analysis` (R: `MASS::lda`,
# `MASS::qda`), `scipy.stats.multivariate_normal` for the hand calculation,
# `sklearn.inspection.DecisionBoundaryDisplay` for the picture.

# %%
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import multivariate_normal
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.inspection import DecisionBoundaryDisplay

# %%
rng = np.random.default_rng(598)
X0 = rng.multivariate_normal([0, 0], [[1.0, 0.3], [0.3, 0.6]], size=120)
X1 = rng.multivariate_normal([2, 1], [[2.0, -0.8], [-0.8, 1.5]], size=80)
X = np.vstack([X0, X1])
y = np.repeat([0, 1], [120, 80])

lda = LinearDiscriminantAnalysis(store_covariance=True).fit(X, y)
qda = QuadraticDiscriminantAnalysis(store_covariance=True).fit(X, y)
print("priors:", lda.priors_, "\nclass means:\n", lda.means_)
print("LDA boundary: %.3f + %.3f*x1 + %.3f*x2 = 0" % (lda.intercept_[0], *lda.coef_[0]))

# %% [markdown]
# ## EVALUATE the discriminant with the fitted (now known) parameters

# %%
def discriminant_scores(X, means, covariances, priors):
    """delta_k(x) = log prior_k + log N(x; mean_k, cov_k); predict argmax_k."""
    return np.column_stack([
        np.log(prior) + multivariate_normal(mean=mean, cov=cov).logpdf(X)
        for mean, cov, prior in zip(means, covariances, priors)
    ])


lda_scores = discriminant_scores(X, lda.means_, [lda.covariance_] * 2, lda.priors_)
qda_scores = discriminant_scores(X, qda.means_, qda.covariance_, qda.priors_)
print("training error  LDA: %.3f  QDA: %.3f" % (np.mean(lda.predict(X) != y), np.mean(qda.predict(X) != y)))

# %% [markdown]
# ## What the output means
# * LDA uses one pooled covariance, so the quadratic terms cancel between classes
#   and the boundary is the straight line printed above.
# * QDA keeps a covariance per class. The x^T Sigma_k^{-1} x terms no longer
#   cancel, so the boundary is a conic (curved).

# %% [markdown]
# ## Validation checks
# 1. Hand-computed discriminants pick the same class as `.predict` (LDA and QDA).
# 2. For LDA, the difference of discriminants equals `decision_function`, the linear score.

# %%
assert np.array_equal(lda_scores.argmax(axis=1), lda.predict(X))
assert np.array_equal(qda_scores.argmax(axis=1), qda.predict(X))
assert np.allclose(lda_scores[:, 1] - lda_scores[:, 0], lda.decision_function(X))
print("all checks passed")

# %%
fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
for ax, model, name in zip(axes, [lda, qda], ["LDA (linear)", "QDA (quadratic)"]):
    DecisionBoundaryDisplay.from_estimator(model, X, response_method="predict", alpha=0.25, ax=ax)
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap="coolwarm", s=10)
    ax.set(title=name, xlabel="x1")
axes[0].set_ylabel("x2")
plt.show()
