# Translating Common R Statistical Operations to Python

I have used R extensively for statistical analysis, and I am now working toward the same level of fluency in Python. The statistical concepts do not change, but the functions, object types, defaults, and modeling conventions often do. I created this guide to make that translation explicit.

My goal is not simply to list Python commands. I want to show what each R operation becomes in Python, which library provides the closest equivalent, and where a literal translation would be misleading. I use `=` for assignment in every R example because that is how I write R and because it makes the comparison with Python easier to follow.

The guide emphasizes the Python libraries that most closely reproduce familiar R statistical workflows:

- **pandas** for data frames and data preparation
- **NumPy** for vectors, matrices, and simulation
- **SciPy** for probability distributions and standalone hypothesis tests
- **statsmodels** for R-like formulas, regression inference, diagnostics, and model summaries
- **Matplotlib and seaborn** for statistical graphics
- **scikit-learn** for prediction-oriented workflows and validation

> **Guiding principle:** If the goal is inference like `lm()` plus `summary()`, start with **statsmodels**. If the goal is production prediction, preprocessing pipelines, cross-validation, or machine learning, use **scikit-learn**.

> **Companion workspace:** [`workbench/`](workbench/README.md) is a VS Code workspace built from this guide. It adds a searchable task-to-function catalog (`psl find "R plogis"`), runnable worked examples, and a pinned Python environment for CS 598 PSL.

## Contents

1. [Installation and imports](#1-installation-and-imports)
2. [R-to-Python syntax essentials](#2-r-to-python-syntax-essentials)
3. [Reading and inspecting data](#3-reading-and-inspecting-data)
4. [Selecting, filtering, and modifying data](#4-selecting-filtering-and-modifying-data)
5. [Descriptive statistics and missing values](#5-descriptive-statistics-and-missing-values)
6. [Vectors, matrices, and linear algebra](#6-vectors-matrices-and-linear-algebra)
7. [Random simulation and probability distributions](#7-random-simulation-and-probability-distributions)
8. [Plotting](#8-plotting)
9. [Simple and multiple linear regression](#9-simple-and-multiple-linear-regression)
10. [Regression output and hypothesis tests](#10-regression-output-and-hypothesis-tests)
11. [Prediction and confidence intervals](#11-prediction-and-confidence-intervals)
12. [Categorical predictors, interactions, and polynomials](#12-categorical-predictors-interactions-and-polynomials)
13. [Nested-model comparison and ANOVA](#13-nested-model-comparison-and-anova)
14. [Regression diagnostics](#14-regression-diagnostics)
15. [Model selection with AIC and BIC](#15-model-selection-with-aic-and-bic)
16. [Logistic regression and classification](#16-logistic-regression-and-classification)
17. [Writing functions, loops, and conditionals](#17-writing-functions-loops-and-conditionals)
18. [Compact function crosswalk](#18-compact-function-crosswalk)
19. [Important differences from R](#19-important-differences-from-r)

---

## 1. Installation and imports

### Install packages

In Colab or Jupyter, run this once if the packages are not already available:

```python
%pip install numpy pandas scipy statsmodels matplotlib seaborn scikit-learn patsy
```

### General-purpose imports

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scipy import stats

import statsmodels.api as sm
import statsmodels.formula.api as smf

from statsmodels.stats.anova import anova_lm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import OLSInfluence
from statsmodels.stats.outliers_influence import variance_inflation_factor

from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
```

You do not need every import for every analysis. A smaller notebook should import only what it uses.

### Conventional aliases

| Alias | Library | Primary role |
|---|---|---|
| `np` | NumPy | Arrays, matrices, random values, linear algebra |
| `pd` | pandas | DataFrames and data manipulation |
| `plt` | Matplotlib | Base plotting interface |
| `sns` | seaborn | Higher-level statistical graphics |
| `stats` | SciPy statistics | Distributions and hypothesis tests |
| `sm` | statsmodels API | Matrix-oriented statistical models |
| `smf` | statsmodels formula API | R-like formula models |

---

## 2. R-to-Python syntax essentials

### Assignment and indexing

| R | Python |
|---|---|
| `x = 5` | `x = 5` |
| `x[1]` | `x[0]` |
| `x[1:3]` | `x[0:3]` |
| `df$age` | `df["age"]` or `df.age` |
| `df[, c("x", "y")]` | `df[["x", "y"]]` |
| `df[rows, columns]` | `df.loc[rows, columns]` |
| `x^2` | `x**2` |
| `%*%` | `@` |
| `TRUE`, `FALSE` | `True`, `False` |
| `NULL` | `None` |
| `!condition` | `not condition` for one scalar Boolean; `~condition` elementwise |
| `a && b` | `a and b` for scalar conditions |
| `a || b` | `a or b` for scalar conditions |
| `a & b` | `a & b` for elementwise conditions |
| `a | b` | `a | b` for elementwise conditions |
| `x %in% values` | `x.isin(values)` or `np.isin(x, values)` |

Python uses zero-based indexing. R's first element is `x[1]`; Python's first element is `x[0]`.

### Boolean values: `TRUE`/`FALSE` versus `True`/`False`

R spells its logical constants in uppercase:

**R**

```r
plotit = TRUE
testit = FALSE

if (plotit) {
  print("Make the plot")
}
```

Python capitalizes only the first letter:

**Python**

```python
plotit = True
testit = False

if plotit:
    print("Make the plot")
```

The following Python spellings are incorrect:

```python
# Incorrect Python: TRUE, FALSE, true, and false are not Boolean constants.
```

R calls this data type **logical**; Python calls it **Boolean** or `bool`:

**R**

```r
class(TRUE)
# "logical"
```

**Python**

```python
type(True)
# bool
```

Scalar Boolean operators and elementwise operators are different:

**R**

```r
# Scalar control-flow conditions
if (is_ready && has_data) {
  print("Continue")
}

# Elementwise comparison of vectors
keep = (df$age >= 18) & (df$group == "A")
```

**Python**

```python
# Scalar control-flow conditions
if is_ready and has_data:
    print("Continue")

# Elementwise comparison of pandas Series
keep = (df["age"] >= 18) & (df["group"] == "A")
```

For pandas Series or NumPy arrays, use `&`, `|`, and `~`, with each comparison enclosed in parentheses. Do not use Python's `and`, `or`, or `not` on an entire Series or array; Python cannot reduce a multi-value array to one unambiguous truth value.

Missingness is separate from Boolean truth:

| Concept | R | Python |
|---|---|---|
| Boolean true | `TRUE` | `True` |
| Boolean false | `FALSE` | `False` |
| Missing value | `NA` | `np.nan` or `pd.NA` |
| No object/value | `NULL` | `None` |

### Creating vectors and sequences

```r
x = c(1, 2, 3)
zeros = rep(0, 5)
grid = seq(0, 10, length.out = 50)
```

```python
x = np.array([1, 2, 3])
zeros = np.repeat(0, 5)       # or np.zeros(5)
grid = np.linspace(0, 10, 50)
```

### Accessing model attributes

R frequently uses `$`:

```r
summary(model)$adj.r.squared
```

Python generally uses attributes:

```python
model.rsquared_adj
```

---

## 3. Reading and inspecting data

### CSV files

```r
df = read.csv("data.csv")
```

```python
df = pd.read_csv("data.csv")
```

### Whitespace-separated files without headers

```r
df = read.table(
  "grocery.txt",
  header = FALSE,
  col.names = c("Y", "X1", "X2", "X3")
)
```

```python
df = pd.read_csv(
    "grocery.txt",
    sep=r"\s+",
    header=None,
    names=["Y", "X1", "X2", "X3"],
)
```

For a file in mounted Google Drive:

```python
df = pd.read_csv(
    "/content/drive/MyDrive/grocery.txt",
    sep=r"\s+",
    header=None,
    names=["Y", "X1", "X2", "X3"],
)
```

### Inspecting a DataFrame

| R | Python | Result |
|---|---|---|
| `head(df)` | `df.head()` | First five rows |
| `head(df, 10)` | `df.head(10)` | First ten rows |
| `View(df)` | `display(df)` | Notebook table view |
| `str(df)` | `df.info()` | Types and missingness |
| `summary(df)` | `df.describe(include="all")` | Column summaries |
| `names(df)` | `df.columns` | Column names |
| `colnames(df)` | `df.columns` | Column names |
| `nrow(df)` | `df.shape[0]` | Number of rows |
| `ncol(df)` | `df.shape[1]` | Number of columns |
| `dim(df)` | `df.shape` | `(rows, columns)` |
| `class(df)` | `type(df)` | Object type |

In a notebook, use `display()` to show multiple outputs from one cell:

```python
display(df.head())
display(df.describe())
df.info()
```

---

## 4. Selecting, filtering, and modifying data

### Selecting columns

```r
selected = df[, c("Y", "X1", "X2")]
```

```python
selected = df[["Y", "X1", "X2"]]
```

Select by column position:

```r
selected = df[, c(4, 6, 7, 8)]
```

```python
selected = df.iloc[:, [3, 5, 6, 7]]
```

The Python positions are one lower because indexing starts at zero.

### Renaming columns

```r
colnames(df) = c("ozone", "wind", "humidity", "temp")
```

```python
df.columns = ["ozone", "wind", "humidity", "temp"]
```

Rename selected columns:

```python
df = df.rename(columns={"old_name": "new_name"})
```

### Filtering rows

```r
positive = subset(df, Balance > 0)
```

```python
positive = df.loc[df["Balance"] > 0].copy()
```

Multiple conditions require parentheses:

```python
filtered = df.loc[(df["age"] >= 18) & (df["smoke"] == 1)].copy()
```

### Dropping columns

```r
df = subset(df, select = -c(ID))
```

```python
df = df.drop(columns=["ID"])
```

### Missing observations

```r
clean = na.omit(df)
clean = df[complete.cases(df), ]
```

```python
clean = df.dropna()
```

Select complete cases for particular columns:

```python
clean = df.dropna(subset=["Y", "X1", "X2"])
```

### Creating or replacing columns

```r
df$calories_expected = 4 * df$Carbs + 4 * df$Protein + 9 * df$Fat
```

```python
df["calories_expected"] = (
    4 * df["Carbs"] + 4 * df["Protein"] + 9 * df["Fat"]
)
```

### `ifelse()` and vectorized conditions

```r
x1 = ifelse(df$pclass == "2nd", 1, 0)
```

```python
x1 = np.where(df["pclass"] == "2nd", 1, 0)
```

### Membership

```r
names(coef(model)) %in% not_significant
```

```python
model.params.index.isin(not_significant)
```

---

## 5. Descriptive statistics and missing values

### Common summaries

| R | pandas/NumPy equivalent |
|---|---|
| `mean(x, na.rm=TRUE)` | `x.mean(skipna=True)` |
| `sd(x, na.rm=TRUE)` | `x.std(skipna=True, ddof=1)` |
| `var(x)` | `x.var(ddof=1)` |
| `sum(x)` | `x.sum()` or `np.sum(x)` |
| `min(x)` | `x.min()` or `np.min(x)` |
| `max(x)` | `x.max()` or `np.max(x)` |
| `length(x)` | `len(x)` |
| `summary(x)` | `x.describe()` |
| `cor(df)` | `df.corr(numeric_only=True)` |

For an R-compatible **sample** standard deviation or variance, use `ddof=1`. NumPy's bare `np.std(x)` and `np.var(x)` default to population denominators (`ddof=0`). pandas `Series.std()` and `Series.var()` default to `ddof=1`.

### Counting missing values

```r
sum(is.na(df$sleep_rem))
```

```python
df["sleep_rem"].isna().sum()
```

### Position and label of a maximum

```r
i = which.max(df$sleep_rem)
df$name[i]
```

```python
i = df["sleep_rem"].idxmax()   # index label
name = df.loc[i, "name"]
```

If you specifically need the zero-based integer position:

```python
i_position = df["sleep_rem"].to_numpy().argmax()
```

### Correlation matrix

```r
cor(df)
```

```python
correlations = df.corr(numeric_only=True)
display(correlations)
```

```python
sns.heatmap(correlations, annot=True, cmap="coolwarm", center=0)
plt.show()
```

---

## 6. Vectors, matrices, and linear algebra

### Combining columns

R's `cbind()` combines objects side by side:

**R**

```r
X = cbind(1, x1, x2, x3)
```

There are two common Python translations, depending on the object you want back.

#### NumPy: `np.column_stack()`

Use `np.column_stack()` when you want a numeric NumPy matrix for linear algebra:

**Python**

```python
X = np.column_stack((np.ones(len(x1)), x1, x2, x3))
```

Arguments:

- The outer parentheses call `np.column_stack()`.
- The inner tuple `(np.ones(...), x1, x2, x3)` contains the columns to combine.
- `np.ones(len(x1))` creates the intercept column.
- The result is a two-dimensional NumPy array with one input vector per column.

Example without an intercept:

```python
X = np.column_stack((x1, x2, x3))
```

#### pandas: `pd.concat(..., axis=1)`

Use `pd.concat()` when you want to preserve pandas row indexes and column names:

**Python**

```python
X = pd.concat(
    [df["X1"], df["X2"], df["X3"]],
    axis=1,
)
```

Arguments:

- The list contains the Series or DataFrames to combine.
- `axis=1` means combine them horizontally as columns.
- `axis=0` would stack them vertically as additional rows.
- pandas aligns objects by their index labels, not merely by physical row position.

Add and name an intercept column while keeping a DataFrame:

```python
intercept = pd.Series(1.0, index=df.index, name="Intercept")
X = pd.concat([intercept, df[["X1", "X2", "X3"]]], axis=1)
```

If the objects have unrelated indexes but should be combined strictly by row position, reset their indexes first:

```python
X = pd.concat(
    [series_a.reset_index(drop=True), series_b.reset_index(drop=True)],
    axis=1,
)
```

For DataFrame columns:

**Python**

```python
X = sm.add_constant(df[["X1", "X2", "X3"]])
```

`sm.add_constant()` adds the column of ones needed for an intercept in matrix-oriented statsmodels code.

In short:

| Goal | Python operation |
|---|---|
| Numeric matrix for algebra | `np.column_stack((x1, x2, x3))` |
| DataFrame preserving names/index | `pd.concat([x1, x2, x3], axis=1)` |
| Existing columns from one DataFrame | `df[["X1", "X2", "X3"]]` |
| statsmodels design matrix with intercept | `sm.add_constant(df[["X1", "X2", "X3"]])` |

### Conversion to arrays

```r
y = as.matrix(df$Y)
X = as.matrix(df[, c("X1", "X2")])
```

```python
y = df["Y"].to_numpy()
X = df[["X1", "X2"]].to_numpy()
```

### Transpose and matrix multiplication

```r
t(X)
X %*% beta
```

```python
X.T
X @ beta
```

### Solving the normal equations

R expression:

```r
beta_hat = solve(t(X) %*% X) %*% t(X) %*% y
```

Literal Python translation:

```python
beta_hat = np.linalg.inv(X.T @ X) @ X.T @ y
```

Numerically preferable Python:

```python
beta_hat = np.linalg.lstsq(X, y, rcond=None)[0]
```

Avoid explicitly calculating \((X^TX)^{-1}\) in production code. `lstsq()` is generally more numerically stable and also handles more rank-deficient situations.

### Other matrix operations

| R | Python |
|---|---|
| `t(X)` | `X.T` |
| `solve(A)` | `np.linalg.inv(A)` |
| `solve(A, b)` | `np.linalg.solve(A, b)` |
| `diag(A)` | `np.diag(A)` |
| `sum(diag(A))` | `np.trace(A)` |
| `as.vector(A)` | `np.asarray(A).ravel()` |
| `all.equal(a, b)` | `np.allclose(a, b)` |

### Manual regression quantities

```python
y_hat = X @ beta_hat
residuals = y - y_hat

n = X.shape[0]
p = X.shape[1]                 # includes the intercept column

sse = residuals @ residuals
sst = np.sum((y - y.mean()) ** 2)
r_squared = 1 - sse / sst
residual_standard_error = np.sqrt(sse / (n - p))
```

---

## 7. Random simulation and probability distributions

### Reproducible random values

R uses one global random-number generator:

```r
set.seed(420)
x = rnorm(1000)
```

Modern NumPy uses an explicit generator:

```python
rng = np.random.default_rng(420)
x = rng.normal(loc=0, scale=1, size=1000)
```

Using `default_rng()` is preferred to the older `np.random.seed()` interface.

### Random distributions

| R | NumPy |
|---|---|
| `rnorm(n, mean, sd)` | `rng.normal(loc=mean, scale=sd, size=n)` |
| `runif(n, min, max)` | `rng.uniform(low=min_, high=max_, size=n)` |
| `rexp(n, rate)` | `rng.exponential(scale=1/rate, size=n)` |
| `sample(x, size)` | `rng.choice(x, size=size, replace=False)` |
| `sample(nrow(df), 300)` | `rng.choice(df.index, size=300, replace=False)` |

R parameterizes the exponential distribution by **rate**; NumPy uses **scale**, where `scale = 1 / rate`.

### Density, cumulative probability, and quantiles

| R | SciPy |
|---|---|
| `dnorm(x, mean, sd)` | `stats.norm.pdf(x, loc=mean, scale=sd)` |
| `pnorm(x, mean, sd)` | `stats.norm.cdf(x, loc=mean, scale=sd)` |
| `qnorm(p, mean, sd)` | `stats.norm.ppf(p, loc=mean, scale=sd)` |
| `pt(t, df)` | `stats.t.cdf(t, df=df)` |
| `qt(p, df)` | `stats.t.ppf(p, df=df)` |

Upper-tail probability:

```r
pt(abs(t_value), df, lower.tail = FALSE)
```

```python
stats.t.sf(abs(t_value), df=df)
```

Two-sided p-value:

```python
p_value = 2 * stats.t.sf(abs(t_value), df=df)
```

`sf()` is the survival function, \(1-F(x)\), and is generally preferable to manually calculating `1 - cdf()` in a distribution tail.

---

## 8. Plotting

### Scatterplot

```r
plot(df$x, df$y, pch = 20, col = "darkblue")
```

```python
plt.scatter(df["x"], df["y"], color="darkblue")
plt.xlabel("x")
plt.ylabel("y")
plt.show()
```

Using seaborn:

```python
sns.scatterplot(data=df, x="x", y="y", color="darkblue")
plt.show()
```

### Regression line

```r
plot(y ~ x, data = df)
abline(model, col = "red")
```

```python
sns.regplot(data=df, x="x", y="y", ci=None,
            scatter_kws={"color": "darkblue"},
            line_kws={"color": "red"})
plt.show()
```

Or draw fitted values explicitly:

```python
order = np.argsort(df["x"].to_numpy())
plt.scatter(df["x"], df["y"])
plt.plot(df["x"].to_numpy()[order], model.fittedvalues.to_numpy()[order],
         color="red")
plt.show()
```

### Histogram

```r
hist(x, breaks = 20, col = "darkblue")
```

```python
plt.hist(x, bins=20, color="darkblue", edgecolor="white")
plt.show()
```

### Boxplot by group

```r
boxplot(y ~ group, data = df)
```

```python
sns.boxplot(data=df, x="group", y="y")
plt.show()
```

### Multiple panels

```r
par(mfrow = c(1, 2))
```

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
```

### Horizontal reference line

```r
abline(h = 0, col = "red")
```

```python
plt.axhline(0, color="red")
```

### Normal Q-Q plot

```r
qqnorm(resid(model))
qqline(resid(model), col = "red")
```

```python
sm.qqplot(model.resid, line="45", fit=True)
plt.show()
```

### Pairwise plots

```python
sns.pairplot(df)
plt.show()
```

---

## 9. Simple and multiple linear regression

### R-like formula interface: recommended for inference

```r
model = lm(Y ~ X1 + X2 + X3, data = df)
summary(model)
```

```python
model = smf.ols("Y ~ X1 + X2 + X3", data=df).fit()
print(model.summary())
```

`OLS` means **ordinary least squares**. It selects coefficient estimates that minimize

\[
\sum_{i=1}^n (y_i - \hat y_i)^2.
\]

The parts of the Python expression are:

- `smf`: `statsmodels.formula.api`
- `.ols(...)`: defines an ordinary least-squares model
- `"Y ~ X1 + X2 + X3"`: models `Y` using the three predictors
- `data=df`: finds those variables in `df`
- `.fit()`: estimates the coefficients and inference statistics

### Formula shorthand

| R formula | statsmodels/Patsy formula |
|---|---|
| `Y ~ X1 + X2` | `Y ~ X1 + X2` |
| `Y ~ .` | No universal dot shorthand; construct a formula |
| `Y ~ X1 * X2` | `Y ~ X1 * X2` |
| `Y ~ X1 + X2 + X1:X2` | `Y ~ X1 + X2 + X1:X2` |
| `Y ~ X1^2` | `Y ~ X1 + I(X1**2)` |
| `Y ~ poly(X1, 2)` | `Y ~ X1 + I(X1**2)` for raw powers |
| `Y ~ X1 - 1` | `Y ~ X1 - 1` |

Build an additive formula from all columns except the response:

```python
response = "Y"
predictors = [column for column in df.columns if column != response]
formula = response + " ~ " + " + ".join(predictors)
model = smf.ols(formula, data=df).fit()
```

### Matrix interface

```python
y = df["Y"]
X = sm.add_constant(df[["X1", "X2", "X3"]])
model = sm.OLS(y, X).fit()
print(model.summary())
```

Unlike the formula interface, `sm.OLS()` does **not** automatically add an intercept. Use `sm.add_constant()`.

### scikit-learn interface: recommended for prediction workflows

```python
X = df[["X1", "X2", "X3"]]
y = df["Y"]

sk_model = LinearRegression()
sk_model.fit(X, y)

print(sk_model.intercept_)
print(sk_model.coef_)
print(sk_model.score(X, y))
```

scikit-learn does not produce an R-style inferential summary with standard errors and p-values. Use statsmodels when those quantities matter.

---

## 10. Regression output and hypothesis tests

### Full R-like summary

```python
print(model.summary())
```

The output includes:

- coefficient estimates
- standard errors
- t-statistics
- two-sided p-values
- confidence intervals
- \(R^2\) and adjusted \(R^2\)
- overall F-statistic and its p-value
- residual diagnostics

### Extracting individual quantities

| R | statsmodels |
|---|---|
| `coef(model)` | `model.params` |
| `coef(model)[2]` | `model.params["X1"]` |
| `fitted(model)` | `model.fittedvalues` |
| `resid(model)` | `model.resid` |
| `summary(model)$r.squared` | `model.rsquared` |
| `summary(model)$adj.r.squared` | `model.rsquared_adj` |
| `deviance(model)` for OLS | `model.ssr` |
| `confint(model)` | `model.conf_int()` |
| `AIC(model)` | `model.aic` |
| `BIC(model)` | `model.bic` |

Named access is safer than position-based access:

```python
estimate = model.params["X1"]
standard_error = model.bse["X1"]
t_statistic = model.tvalues["X1"]
p_value = model.pvalues["X1"]
confidence_interval = model.conf_int().loc["X1"]
```

### Testing a coefficient against a nonzero value

For

\[
H_0: \beta_1 = c,
\]

the test statistic is

\[
t = \frac{\hat\beta_1-c}{SE(\hat\beta_1)}.
\]

Manual Python:

```python
c = 3.5
t_value = (model.params["X1"] - c) / model.bse["X1"]
p_value = 2 * stats.t.sf(abs(t_value), df=model.df_resid)
```

Statsmodels can perform the test directly:

```python
test = model.t_test("X1 = 3.5")
print(test)
```

### Testing several restrictions jointly

```python
test = model.f_test("X2 = 0, X3 = 0")
print(test)
```

### One-sample, independent, and paired t-tests

One-sample test:

```r
t.test(x, mu = 0)
```

```python
result = stats.ttest_1samp(x, popmean=0, nan_policy="omit")
print(result.statistic, result.pvalue)
```

Two independent groups with equal variances:

```r
t.test(values ~ groups, data = df, var.equal = TRUE)
```

```python
group_a = df.loc[df["groups"] == "A", "values"]
group_b = df.loc[df["groups"] == "B", "values"]

result = stats.ttest_ind(
    group_a,
    group_b,
    equal_var=True,
    nan_policy="omit",
)
```

Welch's two-sample test, which does not assume equal variances:

```python
result = stats.ttest_ind(
    group_a,
    group_b,
    equal_var=False,
    nan_policy="omit",
)
```

Paired test:

```python
result = stats.ttest_rel(before, after, nan_policy="omit")
```

The sign of a two-sample t-statistic depends on the subtraction order. `ttest_ind(group_a, group_b)` evaluates the difference `mean(group_a) - mean(group_b)`. Reversing the arguments reverses the sign but not the two-sided p-value.

---

## 11. Prediction and confidence intervals

### Point prediction

```r
predict(model, newdata = data.frame(X1 = 2.1, X2 = 7, X3 = 0))
```

```python
new_data = pd.DataFrame({"X1": [2.1], "X2": [7], "X3": [0]})
point_prediction = model.predict(new_data)
```

### Confidence interval for the mean response

```r
predict(model, newdata = new_data, interval = "confidence", level = 0.95)
```

```python
prediction = model.get_prediction(new_data).summary_frame(alpha=0.05)
prediction[["mean", "mean_ci_lower", "mean_ci_upper"]]
```

### Prediction interval for a new observation

```r
predict(model, newdata = new_data, interval = "prediction", level = 0.95)
```

```python
prediction = model.get_prediction(new_data).summary_frame(alpha=0.05)
prediction[["mean", "obs_ci_lower", "obs_ci_upper"]]
```

The prediction interval is wider because it accounts for both uncertainty in the estimated mean and the irreducible variation of a new individual observation.

### Plotting fitted line and intervals

```python
x_grid = np.linspace(df["X1"].min(), df["X1"].max(), 100)
grid = pd.DataFrame({"X1": x_grid})
pred = model.get_prediction(grid).summary_frame(alpha=0.05)

plt.scatter(df["X1"], df["Y"], color="darkblue")
plt.plot(x_grid, pred["mean"], color="red", label="Fitted mean")
plt.fill_between(x_grid, pred["mean_ci_lower"], pred["mean_ci_upper"],
                 alpha=0.25, label="95% confidence interval")
plt.plot(x_grid, pred["obs_ci_lower"], color="purple", linestyle="--")
plt.plot(x_grid, pred["obs_ci_upper"], color="purple", linestyle="--",
         label="95% prediction interval")
plt.legend()
plt.show()
```

---

## 12. Categorical predictors, interactions, and polynomials

### Categorical predictors

R factors are represented by pandas categorical data or explicitly marked with `C()` in a statsmodels formula:

```r
model = lm(y ~ factor(group), data = df)
```

```python
model = smf.ols("y ~ C(group)", data=df).fit()
```

Convert the column itself to categorical data:

```python
df["group"] = df["group"].astype("category")
```

### Choosing a reference level

```r
df$group = relevel(factor(df$group), ref = "control")
```

```python
model = smf.ols(
    'y ~ C(group, Treatment(reference="control"))',
    data=df,
).fit()
```

Inspect or explicitly order category levels:

```r
levels(df$group)
df$group = factor(df$group, levels = c("control", "treatment"))
```

```python
df["group"] = pd.Categorical(
    df["group"],
    categories=["control", "treatment"],
    ordered=True,
)

print(df["group"].cat.categories)
```

### Interactions

Main effects plus interaction:

```r
lm(y ~ x1 * x2, data = df)
```

```python
model = smf.ols("y ~ x1 * x2", data=df).fit()
```

Both expand to:

```text
x1 + x2 + x1:x2
```

Interaction only:

```python
model = smf.ols("y ~ x1 + x2 + x1:x2", data=df).fit()
```

Categorical-by-continuous interaction:

```python
model = smf.ols("y ~ C(group) * x", data=df).fit()
```

### Polynomial terms

Raw quadratic regression:

```r
lm(y ~ x + I(x^2), data = df)
```

```python
model = smf.ols("y ~ x + I(x**2)", data=df).fit()
```

R's `poly(x, 2)` uses orthogonal polynomials by default. `x + I(x**2)` uses raw powers and therefore does not produce the same coefficient values, although it spans the same quadratic model space and gives the same fitted values when implemented consistently.

### Log transformations and back-transformation

```r
model = lm(log(price) ~ log(carat), data = diamonds)
exp(predict(model, newdata = data.frame(carat = 3), interval = "prediction"))
```

```python
model = smf.ols("np.log(price) ~ np.log(carat)", data=diamonds).fit()

new_data = pd.DataFrame({"carat": [3]})
log_interval = model.get_prediction(new_data).summary_frame(alpha=0.05)

back_transformed = np.exp(
    log_interval[["mean", "obs_ci_lower", "obs_ci_upper"]]
)
```

Exponentiating converts results from the log scale back to the original scale, but `exp(mean(log(Y)))` estimates a conditional median/geometric mean rather than automatically producing an unbiased conditional arithmetic mean. A smearing or distribution-specific correction may be needed when the arithmetic mean is the target.

---

## 13. Nested-model comparison and ANOVA

### Comparing nested linear models

**R**

```r
small = lm(Y ~ X1 + X2, data = df)
large = lm(Y ~ X1 + X2 + X3, data = df)
anova(small, large)
```

**Python**

```python
small = smf.ols("Y ~ X1 + X2", data=df).fit()
large = smf.ols("Y ~ X1 + X2 + X3", data=df).fit()

print(anova_lm(small, large))
```

The nested-model F-test evaluates whether the additional terms collectively improve the model:

\[
H_0: \text{all coefficients added to the large model equal zero}.
\]

The models must be fit on the same observations, and the smaller model must be nested within the larger model.

### ANOVA table for one fitted model

**Python**

```python
print(anova_lm(large, typ=1))
```

Types I, II, and III sums of squares answer different questions, especially with unbalanced categorical designs. Do not switch among them without considering the model and hypothesis.

---

## 14. Regression diagnostics

### Residuals versus fitted values

**R**

```r
plot(fitted(model), resid(model))
abline(h = 0)
```

**Python**

```python
plt.scatter(model.fittedvalues, model.resid)
plt.axhline(0, color="red")
plt.xlabel("Fitted values")
plt.ylabel("Residuals")
plt.show()
```

### Q-Q plot

**Python**

```python
sm.qqplot(model.resid, line="45", fit=True)
plt.show()
```

### Shapiro-Wilk normality test

**R**

```r
shapiro.test(resid(model))
```

**Python**

```python
statistic, p_value = stats.shapiro(model.resid)
print({"statistic": statistic, "p_value": p_value})
```

The null hypothesis is that the residuals follow a normal distribution. With large samples, the test can detect small, practically unimportant departures from normality; inspect the Q-Q plot as well.

### Breusch-Pagan test for heteroscedasticity

**R**

```r
library(lmtest)
bptest(model)
```

**Python**

```python
lm_stat, lm_pvalue, f_stat, f_pvalue = het_breuschpagan(
    model.resid,
    model.model.exog,
)

print({
    "LM statistic": lm_stat,
    "LM p-value": lm_pvalue,
    "F statistic": f_stat,
    "F p-value": f_pvalue,
})
```

The null hypothesis is constant residual variance.

### Leverage, hat values, and Cook's distance

**R**

```r
hatvalues(model)
cooks.distance(model)
```

**Python**

```python
influence = OLSInfluence(model)

hat_values = influence.hat_matrix_diag
cooks_distance, cooks_pvalues = influence.cooks_distance
studentized_residuals = influence.resid_studentized_external
```

**Python: influence summary**

```python
display(influence.summary_frame().head())
```

**R: find row positions exceeding a threshold**

```r
which(cooks.distance(model) > 4 / n)
```

**Python**

```python
positions = np.flatnonzero(cooks_distance > 4 / len(df))
```

**R: refit after filtering observations**

```r
new_model = update(model, subset = cooks.distance(model) < 4 / n)
```

**Python**

```python
keep = cooks_distance < 4 / len(df)
filtered_df = df.loc[keep].copy()
new_model = smf.ols(model.model.formula, data=filtered_df).fit()
```

Statsmodels has no direct general equivalent of R's `update()` for every model change. The clearest approach is usually to alter the DataFrame or formula explicitly and refit.

**Python: recover observations used by a formula model**

```python
used_data = model.model.data.frame.loc[model.model.data.row_labels].copy()
```

This is the closest practical analogue to using R's `model.frame(model)` when missing rows may have been excluded during fitting.

### Variance inflation factors

**R**

```r
library(faraway)
vif(model)
```

**Python**

```python
X = model.model.exog
names = model.model.exog_names

vif_table = pd.DataFrame({
    "variable": names,
    "VIF": [variance_inflation_factor(X, i) for i in range(X.shape[1])],
})

display(vif_table)
```

The intercept's VIF is usually not substantively interpreted. Large VIF values indicate that a predictor is strongly linearly associated with other predictors, inflating its coefficient variance.

### Leave-one-out cross-validation RMSE from hat values

**R**

```r
sqrt(mean((resid(model) / (1 - hatvalues(model)))^2))
```

**Python**

```python
influence = OLSInfluence(model)
loocv_residuals = model.resid / (1 - influence.hat_matrix_diag)
loocv_rmse = np.sqrt(np.mean(loocv_residuals**2))
```

### A reusable diagnostic function

**Python**

```python
def regression_diagnostics(model, alpha=0.05, make_plots=True):
    """Return basic OLS diagnostic tests and optionally draw two plots."""
    shapiro_stat, shapiro_p = stats.shapiro(model.resid)
    bp_lm, bp_lm_p, bp_f, bp_f_p = het_breuschpagan(
        model.resid,
        model.model.exog,
    )

    if make_plots:
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))

        axes[0].scatter(model.fittedvalues, model.resid)
        axes[0].axhline(0, color="red")
        axes[0].set_xlabel("Fitted values")
        axes[0].set_ylabel("Residuals")

        stats.probplot(model.resid, dist="norm", plot=axes[1])
        axes[1].set_title("Normal Q-Q plot")

        plt.tight_layout()
        plt.show()

    return {
        "Shapiro-Wilk p-value": shapiro_p,
        "Shapiro decision": "Reject" if shapiro_p < alpha else "Fail to reject",
        "Breusch-Pagan p-value": bp_lm_p,
        "Breusch-Pagan decision": "Reject" if bp_lm_p < alpha else "Fail to reject",
    }
```

Function arguments:

- `model`: a fitted statsmodels OLS result
- `alpha`: significance level used for both diagnostic-test decisions
- `make_plots`: `True` displays the residual and Q-Q plots; `False` skips them

Returned value: a Python dictionary containing both p-values and the corresponding reject/fail-to-reject decisions.

---

## 15. Model selection with AIC and BIC

### Reading AIC and BIC

**R**

```r
AIC(model)
BIC(model)
```

**Python**

```python
print(model.aic)
print(model.bic)
```

For models fit to the same response and observations, lower values are preferred. AIC and BIC use different penalties; BIC generally penalizes additional parameters more strongly as sample size grows.

### Important difference: no built-in `step()` equivalent

**R: backward selection with `step()`**

```r
step(full_model, direction = "backward")
step(full_model, direction = "backward", k = log(n))
```

Statsmodels does not provide an exact built-in clone of R's `step()`.

**Python: custom backward-selection function**

The following helper repeatedly removes the one predictor whose removal most improves AIC or BIC:

```python
def backward_selection(data, response, predictors, criterion="aic"):
    """Backward selection for additive OLS models using AIC or BIC."""
    remaining = list(predictors)

    def fit(columns):
        right_side = " + ".join(columns) if columns else "1"
        return smf.ols(f"{response} ~ {right_side}", data=data).fit()

    current_model = fit(remaining)
    current_score = getattr(current_model, criterion)

    while remaining:
        candidates = []

        for removed in remaining:
            candidate_columns = [x for x in remaining if x != removed]
            candidate_model = fit(candidate_columns)
            candidate_score = getattr(candidate_model, criterion)
            candidates.append(
                (candidate_score, removed, candidate_columns, candidate_model)
            )

        best_score, removed, best_columns, best_model = min(
            candidates,
            key=lambda item: item[0],
        )

        if best_score >= current_score:
            break

        remaining = best_columns
        current_model = best_model
        current_score = best_score

    return current_model, remaining
```

Function arguments:

- `data`: pandas DataFrame containing the response and predictors
- `response`: response-column name supplied as a string
- `predictors`: list of predictor-column names
- `criterion`: either `"aic"` or `"bic"`

Returned values:

- `current_model`: final fitted statsmodels model
- `remaining`: predictor names retained in that model

**Python: function usage**

```python
predictors = [column for column in df.columns if column != "Y"]

aic_model, aic_terms = backward_selection(
    df, response="Y", predictors=predictors, criterion="aic"
)

bic_model, bic_terms = backward_selection(
    df, response="Y", predictors=predictors, criterion="bic"
)
```

This helper is appropriate for simple additive numeric terms. Hierarchical interactions, categorical terms that expand into several columns, polynomial blocks, and missing-data changes require term-aware selection rather than removing individual design-matrix columns blindly.

Model selection is exploratory and can make ordinary post-selection p-values and confidence intervals appear more certain than they are. Use validation and subject-matter reasoning, not criterion minimization alone.

---

## 16. Logistic regression and classification

### Binomial generalized linear model

**R**

```r
model = glm(
  survived ~ x1 + x2 + x3 + x4 + x3:x4,
  data = train,
  family = "binomial"
)
summary(model)
```

**Python: statsmodels GLM**

```python
model = smf.glm(
    "survived ~ x1 + x2 + x3 + x4 + x3:x4",
    data=train,
    family=sm.families.Binomial(),
).fit()

print(model.summary())
```

Arguments:

- The first argument is the model formula.
- `data=train` tells statsmodels where to find the formula variables.
- `family=sm.families.Binomial()` specifies a binomial response with the default logit link.
- `.fit()` estimates the coefficients.

**Python: alternative statsmodels Logit interface**

```python
model = smf.logit(
    "survived ~ x1 + x2 + x3 + x4 + x3:x4",
    data=train,
).fit()
```

### Predicted probabilities and classes

**R**

```r
probability = predict(model, newdata = test, type = "response")
predicted = ifelse(probability > 0.5, 1, 0)
```

**Python**

```python
probability = model.predict(test)
predicted = np.where(probability > 0.5, 1, 0)
```

Here, `model.predict(test)` returns fitted probabilities. `np.where(condition, value_if_true, value_if_false)` converts each probability into a class using the chosen threshold of `0.5`.

### Accuracy and confusion matrix

**R**

```r
accuracy = mean(predicted == test$survived)
confusion = table(actual = test$survived, predicted = predicted)
```

**Python**

```python
actual = test["survived"].astype(int)

accuracy = accuracy_score(actual, predicted)
matrix = confusion_matrix(actual, predicted, labels=[0, 1])

tn, fp, fn, tp = matrix.ravel()

print({
    "accuracy": accuracy,
    "true_negative": tn,
    "false_positive": fp,
    "false_negative": fn,
    "true_positive": tp,
})
```

Arguments and output order:

- `accuracy_score(actual, predicted)` calculates the proportion classified correctly.
- `labels=[0, 1]` fixes the class order in the confusion matrix.
- With that order, `matrix.ravel()` returns `tn, fp, fn, tp`.
- If the label order changes, that unpacking interpretation also changes.

### Deviance

**R**

```r
deviance(model)
```

**Python: statsmodels GLM result**

```python
model.deviance
```

For `smf.logit()`, useful quantities include `model.llf`, `model.llnull`, and `model.llr_pvalue`; the result object differs somewhat from a GLM result.

---

## 17. Writing functions, loops, and conditionals

### Function definition

**R**

```r
sum_of_squares = function(x) {
  sum(x^2)
}
```

**Python**

```python
def sum_of_squares(x):
    return np.sum(np.asarray(x) ** 2)
```

Python uses indentation rather than braces to define the function body.

### Default arguments

**R**

```r
diagnostics = function(model, alpha = 0.05, plotit = TRUE) {
  # body
}
```

**Python**

```python
def diagnostics(model, alpha=0.05, plotit=True):
    # body
    pass
```

### Conditionals

**R**

```r
if (p_value < alpha) {
  decision = "Reject"
} else {
  decision = "Fail to reject"
}
```

**Python**

```python
if p_value < alpha:
    decision = "Reject"
else:
    decision = "Fail to reject"
```

**Python: compact scalar conditional**

```python
decision = "Reject" if p_value < alpha else "Fail to reject"
```

### Loops

**R**

```r
results = numeric(2500)
for (i in 1:2500) {
  results[i] = calculation
}
```

**Python**

```python
results = np.empty(2500)

for i in range(2500):
    results[i] = calculation
```

### Simulating a simple linear regression dataset

**R**

```r
sim_slr = function(x, beta0, beta1, sigma) {
  epsilon = rnorm(length(x), mean = 0, sd = sigma)
  y = beta0 + beta1 * x + epsilon
  data.frame(predictor = x, response = y)
}

set.seed(420)
x = runif(25, min = 0, max = 10)
simulated = sim_slr(x, beta0 = 5, beta1 = -3, sigma = sqrt(10.24))
model = lm(response ~ predictor, data = simulated)
```

**Python**

```python
def simulate_slr(x, beta0, beta1, sigma, rng):
    x = np.asarray(x)
    epsilon = rng.normal(loc=0, scale=sigma, size=len(x))
    y = beta0 + beta1 * x + epsilon
    return pd.DataFrame({"predictor": x, "response": y})


rng = np.random.default_rng(420)
x = rng.uniform(0, 10, size=25)
simulated = simulate_slr(x, beta0=5, beta1=-3, sigma=np.sqrt(10.24), rng=rng)
model = smf.ols("response ~ predictor", data=simulated).fit()
```

Python function arguments:

- `x`: predictor values
- `beta0`: true intercept
- `beta1`: true slope
- `sigma`: error standard deviation
- `rng`: NumPy random-number generator, passed explicitly for reproducibility

### Lists and dictionaries

**R: named list**

```r
list(decision = decision, p_value = p_value)
```

**Python: dictionary**

```python
{"decision": decision, "p_value": p_value}
```

---

## 18. Compact function crosswalk

| R operation | Python equivalent |
|---|---|
| `library(pkg)` | `import package` or `from package import item` |
| `install.packages("pkg")` | `%pip install package` |
| `read.csv()` | `pd.read_csv()` |
| `data.frame()` | `pd.DataFrame()` |
| `c()` | `np.array([...])` or a Python list |
| `cbind()` to make a NumPy matrix | `np.column_stack((x1, x2, x3))` |
| `cbind()` to preserve pandas labels | `pd.concat([x1, x2, x3], axis=1)` |
| `rep()` | `np.repeat()`, `np.tile()`, or `np.full()` |
| `seq()` | `np.arange()` or `np.linspace()` |
| `numeric(n)` | `np.zeros(n)` |
| `character(n)` | `np.full(n, "", dtype=object)` |
| `as.numeric()` | `pd.to_numeric()` or `.astype(float)` |
| `as.factor()` | `.astype("category")` |
| `as.matrix()` | `.to_numpy()` |
| `as.vector()` | `np.asarray(x).ravel()` |
| `head()` | `.head()` |
| `str()` | `.info()` for DataFrames; `type()` otherwise |
| `summary(df)` | `df.describe(include="all")` |
| `summary(model)` | `model.summary()` |
| `names(df)` | `df.columns` |
| `rownames(df)` | `df.index` |
| `colnames(df)` | `df.columns` |
| `subset()` | `.loc[...]`, `.drop()`, or column selection |
| `complete.cases()` | `.notna().all(axis=1)` |
| `na.omit()` | `.dropna()` |
| `is.na()` | `.isna()` or `pd.isna()` |
| `which()` | `np.flatnonzero(condition)` |
| `which.max()` | `.idxmax()` or `np.argmax()` |
| `ifelse()` | `np.where()` |
| `TRUE`, `FALSE` | `True`, `False` |
| `&&`, `||`, `!` for scalar logic | `and`, `or`, `not` |
| `&`, `|`, `!` for vector logic | `&`, `|`, `~` |
| `mean()` | `np.mean()` or `.mean()` |
| `sd()` | `np.std(..., ddof=1)` or `.std()` |
| `var()` | `np.var(..., ddof=1)` or `.var()` |
| `cor()` | `.corr()` or `np.corrcoef()` |
| `set.seed()` | `np.random.default_rng(seed)` |
| `rnorm()` | `rng.normal()` |
| `runif()` | `rng.uniform()` |
| `rexp()` | `rng.exponential()` |
| `dnorm()` | `stats.norm.pdf()` |
| `pnorm()` | `stats.norm.cdf()` |
| `qnorm()` | `stats.norm.ppf()` |
| `pt()` | `stats.t.cdf()` or `stats.t.sf()` |
| `qt()` | `stats.t.ppf()` |
| `t.test()` | `stats.ttest_1samp()`, `ttest_ind()`, or `ttest_rel()` |
| `lm()` | `smf.ols(...).fit()` |
| `glm(..., family="binomial")` | `smf.glm(..., family=sm.families.Binomial()).fit()` |
| `coef()` | `.params` |
| `resid()` | `.resid` |
| `fitted()` | `.fittedvalues` |
| `predict()` | `.predict()` |
| `confint()` | `.conf_int()` |
| `anova()` | `anova_lm()` |
| `deviance()` | `.deviance` for GLM; `.ssr` for OLS |
| `hatvalues()` | `OLSInfluence(model).hat_matrix_diag` |
| `cooks.distance()` | `OLSInfluence(model).cooks_distance` |
| `vif()` | `variance_inflation_factor()` |
| `bptest()` | `het_breuschpagan()` |
| `shapiro.test()` | `stats.shapiro()` |
| `qqnorm()` + `qqline()` | `sm.qqplot(..., line="45", fit=True)` |
| `plot()` | `plt.plot()`, `plt.scatter()`, or seaborn |
| `hist()` | `plt.hist()` |
| `boxplot()` | `sns.boxplot()` |
| `abline(h=0)` | `plt.axhline(0)` |
| `lines()` | `plt.plot()` |
| `par(mfrow=...)` | `plt.subplots()` |
| `step()` | Custom selection routine; no exact built-in clone |

---

## 19. Important differences from R

1. **Indexing starts at zero.** Python's `x[0]` is R's `x[1]`.

2. **A pandas Series is one-dimensional.** Use `df[["X1"]]` when an API requires a two-dimensional predictor matrix, and `df["Y"]` when it expects a one-dimensional response.

3. **Statsmodels has two interfaces.** Formula models such as `smf.ols()` include an intercept automatically. Matrix models such as `sm.OLS()` require `sm.add_constant()`.

4. **`df.describe()` is not a regression summary.** It summarizes raw variables. `model.summary()` summarizes a fitted statsmodels model.

5. **scikit-learn and statsmodels serve different priorities.** scikit-learn emphasizes prediction and validation; statsmodels emphasizes inference and familiar statistical output.

6. **R and NumPy may use different defaults.** Check degrees of freedom for variance and standard deviation, and check distribution parameterizations such as exponential rate versus scale.

7. **Formula syntax is similar but not identical.** Patsy, which powers statsmodels formulas, supports many R-like expressions but not every base R shortcut.

8. **Categorical variables need deliberate handling.** Use pandas categorical data or `C(variable)` in a statsmodels formula, and specify the desired reference category.

9. **Use stable linear algebra.** Prefer `np.linalg.lstsq()` to explicitly computing the inverse in the normal equation.

10. **A translation should preserve the statistical question, not merely the spelling of the code.** Verify the fitted sample, intercept convention, contrast coding, missing-value handling, and test definition before comparing numerical results across languages.

---

---

## Contributions

Corrections, additions, and clearer translations are welcome.

You can contribute by:

1. Opening an Issue to report an error or suggest an addition.
2. Forking this repository.
3. Creating a branch for your change.
4. Submitting a pull request with a brief explanation of the statistical or programming rationale.

When possible, please verify that examples run in a current Python environment and identify any important differences in defaults between R and Python.

## Suggested workflow for an R user

**Python**

```python
# 1. Read and inspect the data
df = pd.read_csv("data.csv")
display(df.head())
df.info()
display(df.describe())

# 2. Visualize the relationships
sns.pairplot(df)
plt.show()

# 3. Fit an inferential model with an R-like formula
model = smf.ols("Y ~ X1 + X2 + X3", data=df).fit()

# 4. Review coefficients, R-squared, and hypothesis tests
print(model.summary())

# 5. Inspect assumptions and influence
results = regression_diagnostics(model)
print(results)

# 6. Generate predictions with uncertainty
new_data = pd.DataFrame({"X1": [1.0], "X2": [2.0], "X3": [0]})
display(model.get_prediction(new_data).summary_frame(alpha=0.05))
```

This sequence is the closest Python analogue to the familiar R workflow of reading a data frame, exploring it, fitting `lm()`, calling `summary()`, checking diagnostics, and using `predict()`.
