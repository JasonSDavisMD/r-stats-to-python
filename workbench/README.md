# statsbench

**Find and use the right Python call for a statistics or machine-learning
task.** statsbench is a searchable, tested catalog that maps tasks (and their R
names) to the Python scientific stack: NumPy, SciPy, SymPy, pandas,
statsmodels, scikit-learn, Matplotlib/seaborn. Optional add-ons cover PyTorch,
PyMC/ArviZ, XGBoost/LightGBM, pingouin and lifelines.

[![Launch in Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/JasonSDavisMD/r-stats-to-python/main?urlpath=lab/tree/workbench/start-here.ipynb)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/JasonSDavisMD/r-stats-to-python)

```text
$ stats find "R wilcox.test"
1. mann-whitney  [SciPy | fit]  Mann-Whitney U / Wilcoxon rank-sum test ...
   from scipy import stats
   stats.mannwhitneyu(x, y, alternative="two-sided")
   R: wilcox.test ...
```

Each entry gives:
* the library, the exact import and call, and what goes in and comes out;
* its **operation kind** (fit / evaluate / optimize / solve / compute / visualize);
* R equivalents, and **caveats where Python's defaults differ from R's**;
* a runnable example and the official documentation link.

Every example runs in the test suite against the pinned library versions, so
the catalog can't silently drift out of date.

This is a toolkit, not a new statistics engine: your analysis always calls the
underlying libraries directly.

## Choose how to use it

| I want to... | Do this |
|---|---|
| Try it now, no account, nothing saved | Click **launch binder** above |
| Do my own work in JupyterLab, privately | Follow **[docs/jupyterlab-guide.md](docs/jupyterlab-guide.md)** (private repository + Codespace, about 10 min once) |
| Improve the toolkit itself | Click **Open in GitHub Codespaces** above (JupyterLab starts on port 8888), or clone locally (below) |
| Use it in any existing project | `pip install "statsbench @ git+https://github.com/JasonSDavisMD/r-stats-to-python#subdirectory=workbench"` |

## Searching

| Command (terminal) | In a notebook | What it does |
|---|---|---|
| `stats find "inverse logit"` | `find("inverse logit")` | Ranked matches for a task, concept or R name |
| `stats find "logistic" --kind evaluate` | `find("logistic", kind="evaluate")` | Only one operation kind |
| `stats show expit` | `find("expit")[0].entry.example` | Full entry with runnable example |
| `stats r glm` / `stats r` | | R -> Python lookup / full table |
| `stats list --topic survival` | | Browse a topic |
| `stats kinds` | | What fit / evaluate / optimize / solve mean |

In a notebook, import it first: `from statsbench.finder import find`.
`python -m statsbench ...` is the same as `stats ...`.

## Topics

Core (always installed): arrays and linear algebra, data frames, probability
and distributions, hypothesis tests, agreement and diagnostic accuracy,
regression, GLMs, advanced regression (mixed models, GEE, quantile, robust,
ordinal), classification, model selection, trees, splines, unsupervised
learning, more ML models, time series, survival (statsmodels), numerics
(integration, ODEs, curve fitting, QMC), symbolic maths (SymPy), optimization,
plotting.

Optional add-ons (`uv sync --extra <name>` or `pip install "statsbench[<name>]"`):

| Add-on | Libraries | Topics |
|---|---|---|
| `ml` | XGBoost, LightGBM | gradient boosting |
| `deep` | PyTorch | tensors, autograd, neural networks |
| `bayes` | PyMC, ArviZ | Bayesian models, MCMC, diagnostics |
| `stats-extra` | pingouin, lifelines | ICC and effect sizes; Kaplan-Meier, Cox, AFT |
| `all` | all of the above | |

## Local setup (Windows, macOS, Linux)

`uv` installs the pinned Python version and the exact package versions from `uv.lock`:

```bash
# install uv once: https://docs.astral.sh/uv/getting-started/installation/
#   Windows PowerShell:  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
git clone https://github.com/JasonSDavisMD/r-stats-to-python.git
cd r-stats-to-python/workbench
uv sync --group lab                 # core + JupyterLab  (add --all-extras for every add-on)
uv run python -m statsbench.envcheck
uv run jupyter lab                  # or open the folder in VS Code / Positron
```

**Fallback without uv** (pinned core versions only):

```bash
python -m venv .venv
.venv\Scripts\activate              # macOS/Linux: source .venv/bin/activate
pip install -r requirements.lock.txt
pip install -e . --no-deps
```

## Layout

```text
workbench/
  start-here.ipynb         first notebook (Binder opens this)
  src/statsbench/
    catalog/               one TOML file per topic: the searchable index
    finder/                loader, search ranking, CLI (independent of recipes)
    recipes/               thin helpers only where no single library call exists
    envcheck.py            interpreter / library / add-on / catalog check
  examples/                worked "# %%" examples (open as notebooks via Jupytext)
  templates/
    exercise.ipynb|.py     Given / Operation / Library / Code / Meaning / Check
    private-workspace/     starter for YOUR private repository (see jupyterlab-guide)
  docs/                    JupyterLab guide, VS Code/RStudio guides, operation kinds, contributing entries
  tests/                   catalog validity + every example executed, search, CLI, recipes, notebooks
  pyproject.toml / uv.lock / requirements.lock.txt
```

## Worked examples

| File | Topic | Operation kinds |
|---|---|---|
| `00_workflow_tour.py` | search -> help -> run -> inspect -> record | all |
| `01_logistic_known_coefficients.py` | probabilities from given coefficients, strict `>` cutoff | evaluate |
| `02_logistic_decision_boundary.py` | boundary with a zero coefficient; ties to class 1 | solve, evaluate |
| `03_logistic_nll_convexity.py` | GLM fit vs hand NLL + `minimize`; Hessian PSD | fit, evaluate, optimize |
| `04_best_subset_mse.py` | best subset, train vs test MSE | fit, evaluate |
| `05_regression_tree.py` | splits, leaf-mean predictions, CV over depth | fit, evaluate |
| `06_lda_qda.py` | LDA/QDA fit and hand-computed discriminants | fit, evaluate |
| `07_smoothing_spline.py` | penalty `lam`, GCV, roughness | fit, evaluate |

## More documentation

* [docs/jupyterlab-guide.md](docs/jupyterlab-guide.md): private workspace, daily routine, RStudio-style layout, add-ons
* [docs/operation-kinds.md](docs/operation-kinds.md): fit vs evaluate vs optimize vs solve
* [docs/adding-a-topic.md](docs/adding-a-topic.md): add or correct catalog entries
* [docs/rstudio-users-start-here.md](docs/rstudio-users-start-here.md) and [docs/vscode-workflow.md](docs/vscode-workflow.md): for VS Code or Positron users

## Tests

```bash
uv run pytest              # add --all-extras to the sync to include add-on entries
```

CI runs the core suite on Linux, Windows and macOS, and the add-on suite on
Linux, for every pull request. Dependabot opens weekly update PRs, and the
tests catch any library API change before it reaches the catalog.

## Limitations

* Search is lexical (words and names), not semantic. If a phrasing misses, try
  an R name or fewer words. You can also add the phrasing as an alias
  ([docs/adding-a-topic.md](docs/adding-a-topic.md)).
* Coverage is broad but not exhaustive. Contributions are welcome
  ([CONTRIBUTING](../CONTRIBUTING.MD)).
* Optional add-ons are large. On Linux, PyTorch pulls CUDA libraries (several
  GB), so install only the add-ons you need.
