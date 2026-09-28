# %% [markdown]
# # 07 - Smoothing spline: the penalty lam controls wiggliness
#
# **Given:** noisy samples of a smooth curve.
#
# **Operation requested:** FIT smoothing splines that minimize
# sum (y_i - f(x_i))^2 + lam * integral f''(t)^2 dt for several lam, plus
# one chosen by GCV (R: `smooth.spline`). Then EVALUATE the fitted curves and
# their roughness penalty.
#
# **Library choice:** `scipy.interpolate.make_smoothing_spline` returns a
# `BSpline`, a function you can call, differentiate and integrate.

# %%
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_smoothing_spline

# %%
rng = np.random.default_rng(598)
x = np.sort(rng.uniform(0, 1, 100))       # must be strictly increasing
y = np.sin(2 * np.pi * x) + rng.normal(scale=0.3, size=x.size)
grid = np.linspace(0, 1, 400)

# %% [markdown]
# ## Fit for several lam, and let GCV choose one

# %%
def roughness(spline, a=0.0, b=1.0):
    """integral of f''(t)^2 over [a, b]: the quantity lam multiplies."""
    second = spline.derivative(2)
    t = np.linspace(a, b, 4001)
    return float(np.trapezoid(second(t) ** 2, t))


fits = {lam: make_smoothing_spline(x, y, lam=lam) for lam in [1e-7, 1e-5, 1e-3, 1e-1]}
gcv_fit = make_smoothing_spline(x, y)     # lam=None -> generalized cross-validation
for lam, spline in fits.items():
    rss = float(np.sum((y - spline(x)) ** 2))
    print(f"lam={lam:8.0e}  RSS={rss:7.3f}  roughness={roughness(spline):12.2f}")
print(f"GCV fit      RSS={float(np.sum((y - gcv_fit(x)) ** 2)):7.3f}  roughness={roughness(gcv_fit):12.2f}")

# %% [markdown]
# ## What the output means
# * Small lam: the curve chases the noise (low RSS, huge roughness).
# * Large lam: roughness is heavily penalized and the fit tends to a straight
#   line (f'' = 0), i.e. ordinary least squares on x.
# * GCV balances the two automatically. R's `smooth.spline` scales lambda
#   differently (and is usually driven by `spar`/`df`), so lam values do not
#   transfer between the two.

# %% [markdown]
# ## Validation checks
# 1. As lam increases, RSS increases and roughness decreases (the trade-off).
# 2. A large lam reproduces the least-squares line from `np.polyfit(x, y, 1)`.
#    (Do not push lam to 1e8: the linear system becomes ill-conditioned and
#    floating-point error, not the penalty, dominates the result.)

# %%
rss_values = [float(np.sum((y - s(x)) ** 2)) for s in fits.values()]
rough_values = [roughness(s) for s in fits.values()]
assert all(np.diff(rss_values) > 0) and all(np.diff(rough_values) < 0)
line = np.polyval(np.polyfit(x, y, 1), grid)
assert np.allclose(make_smoothing_spline(x, y, lam=1e4)(grid), line, atol=1e-3)
print("all checks passed")

# %%
fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(x, y, s=10, color="grey")
for lam, spline in fits.items():
    ax.plot(grid, spline(grid), label=f"lam={lam:.0e}")
ax.plot(grid, gcv_fit(grid), "k--", linewidth=2, label="GCV")
ax.legend()
plt.show()
