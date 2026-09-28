# Operation kinds: what is the question actually asking the computer to do?

Every catalog entry has one `kind`. Choosing the kind first usually tells you
the library.

| Kind | Question shape | Typical library | Logistic-regression example |
|---|---|---|---|
| **fit** | "Estimate the coefficients from these data" | statsmodels, scikit-learn | `smf.glm("y ~ x", data=df, family=sm.families.Binomial()).fit()` |
| **evaluate** | "Given these coefficients, what is the probability/class/likelihood?" | NumPy, `scipy.special`, `scipy.stats` | `expit(b0 + b1 * x)`, then `np.where(p > 0.5, 1, 0)` |
| **optimize** | "Numerically find the parameter that minimizes this function" | `scipy.optimize` | `minimize(negative_log_likelihood, x0)` |
| **solve** | "For which x is the probability exactly/at least 0.5?" (exact algebra) | SymPy | `sp.solveset(b0 + b1*x1 >= 0, x1, sp.S.Reals)` |
| **compute** | Reshape, clean, summarize or transform data; no model | pandas, NumPy | `df.groupby("g")["y"].mean()` |
| **visualize** | Draw data or an already-computed result | Matplotlib, seaborn | `ax.contour(xx, yy, log_odds, levels=[0])` |

`psl kinds` prints this list. `psl find "<task>" --kind evaluate` narrows a search.

## The mistakes this prevents

* **Fitting when you should evaluate.** If a question gives you
  coefficients, running `glm()` on some data answers a different question.
  Evaluate the given model with `expit`.
* **Evaluating when you should fit.** Coefficients from another question,
  or made-up values, don't describe *these* data.
* **Optimizing when an exact answer exists.** `brentq` finds x where
  p = 0.7 to about 12 digits. SymPy gives `x = (logit(0.7) - b0) / b1`
  exactly and shows the formula.
* **Confusing a boundary with a region.** The boundary `log_odds = 0` is a
  line (or point). The class-1 region is `log_odds > 0` or `>= 0`, depending
  on the stated tie rule. `solveset` returns open vs closed intervals, so the
  difference is visible.
* **Similar names, different things.** `scipy.special.logit` (a function,
  probability to log-odds), `scipy.special.expit` (its inverse), and
  `statsmodels ... Logit` (a *model* that you fit) are three different objects.

## Under-specified questions

If a question needs a value it doesn't give (e.g. x2 for a new patient), say
so in the **Given** section and state your assumption explicitly. Don't
silently reuse a value from another question. A coefficient of exactly zero is
the one case where a missing feature doesn't matter. `sp.solve(..., x2)`
returns `[]` there, which shows the feature drops out (see example 02).
