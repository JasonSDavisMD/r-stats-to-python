# PSL Workbench

A Python-first, RStudio-like workspace for **CS 598 Practical Statistical
Learning**, opened in **VS Code on Windows**. You don't need to hunt across
five documentation sites. You search one **task-to-tool catalog** from the
terminal, and each result gives you the library, the exact import and call,
whether the operation *fits*, *evaluates*, *optimizes* or *solves*, a runnable
example, caveats (including R differences) and the official docs link.

```text
> psl find "R plogis"
1. expit  [SciPy | evaluate]  Inverse logit (logistic sigmoid): log-odds -> probability
   from scipy.special import expit
   expit(log_odds)
   R: plogis, boot::inv.logit   recipe: examples/01_logistic_known_coefficients.py
   docs: https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.expit.html
```

This is a workspace, not a new statistics engine. The analysis always uses
NumPy, SciPy, SymPy, pandas, statsmodels and scikit-learn directly. The
workbench adds a curated index, reproducible examples and a consistent setup.

> **Coming from RStudio?** Start with
> **[docs/rstudio-users-start-here.md](docs/rstudio-users-start-here.md)**.
> It covers the four-pane layout, key translations, and Positron.

## 0. Try it in the browser first (GitHub Codespaces, no install)

On the repository page, click **Code -> Codespaces -> Create codespace on main**.
The dev container in `.devcontainer/` opens straight into `workbench/`,
installs `uv`, builds `.venv` from `uv.lock`, adds the Python and Jupyter
extensions, and runs the environment check. Then follow the four-pane
steps in the RStudio guide.

## 1. Windows setup (one time, about 5 minutes)

**Primary path: `uv`.** `uv` installs the pinned Python version and the exact
package versions from `uv.lock` into a project-local `.venv`.

```powershell
# 1. Install uv (PowerShell, no admin needed); then open a NEW terminal
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Get the repository and create the environment
git clone https://github.com/jasonsdavismd/r-stats-to-python.git
cd r-stats-to-python\workbench
uv sync                      # creates .venv with Python 3.12 + locked packages

# 3. Verify
uv run python -m psl.envcheck
```

Then in VS Code:

1. **File -> Open Folder... -> `r-stats-to-python\workbench`**. Open this
   folder itself, not the repository root, so the `.vscode` settings apply.
2. Accept **"Install recommended extensions"**: Python, Pylance, Jupyter,
   Python Environments, and optionally Data Wrangler.
3. **Ctrl+Shift+P -> "Python: Select Interpreter" -> `.venv`**. In a notebook,
   pick the same `.venv` from the kernel picker (top right).
4. Open a **new** terminal (Ctrl+`). It activates `.venv` automatically. Run
   `python -m psl.envcheck`. The first line must say `-- project .venv`.

Run the same check in a notebook cell (`from psl.envcheck import main; main()`)
to confirm the kernel and the terminal use the same interpreter.

**Fallback without uv** (e.g. a locked-down machine), using pinned versions:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.lock.txt
python -m pip install -e . --no-deps
```

If PowerShell refuses to run `activate`, run
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once.

## 2. Searching the toolbox

| Command | What it does |
|---|---|
| `psl find "inverse logit"` | Ranked matches for a task, concept, or R name |
| `psl find "logistic" --kind evaluate` | Only entries of one operation kind |
| `psl show expit` | Full entry: inputs, returns, runnable example, caveats, docs |
| `psl show expit --code` | Just the example code, ready to paste |
| `psl r plogis` / `psl r` | R -> Python lookup / the full R table |
| `psl list --topic trees` | Browse a topic |
| `psl kinds` | fit vs evaluate vs optimize vs solve vs compute vs visualize |

The same search works in three other places:

* **VS Code task:** Ctrl+Shift+P -> *Tasks: Run Task* -> **psl: find**. It
  prompts for the query, so there's nothing to type in a shell.
* **Inside a notebook:** `from psl.finder import find; find("best subset")`.
* **Offline plain-text search:** Ctrl+Shift+F over `catalog/*.toml`. Every
  entry is readable text.

`python -m psl ...` is equivalent to `psl ...` if the script isn't on PATH.

## 3. Layout

```text
workbench/
  catalog/        one TOML file per course topic (the searchable index)
  examples/       runnable "# %%" worked examples, one per seeded topic
  templates/      exercise.ipynb and exercise.py: Given/Operation/Library/Code/Meaning/Check
  coursework/     YOUR notebooks (git-ignored by default; see its README)
  src/psl/
    finder/       catalog loader, search ranking, CLI (independent of recipes)
    recipes/      thin helpers only where no single library call exists
    envcheck.py   interpreter/library/catalog check
  docs/           VS Code workflow, operation kinds, adding a topic
  tests/          catalog validity + every example executed, search, CLI, recipes
  pyproject.toml / uv.lock / requirements.lock.txt   the one pinned environment
```

## 4. Seeded examples

| File | Topic | Operation kinds |
|---|---|---|
| `00_workflow_tour.py` | search -> help -> run -> inspect -> record | all |
| `01_logistic_known_coefficients.py` | probabilities from given coefficients, strict `>` cutoff | evaluate |
| `02_logistic_decision_boundary.py` | boundary with a zero coefficient; ties go to class 1 | solve, evaluate |
| `03_logistic_nll_convexity.py` | GLM fit vs hand NLL + `minimize`; Hessian PSD | fit, evaluate, optimize |
| `04_best_subset_mse.py` | best subset, train vs test MSE | fit, evaluate |
| `05_regression_tree.py` | splits, leaf-mean predictions, CV over depth | fit, evaluate |
| `06_lda_qda.py` | LDA/QDA fit and hand-computed discriminants | fit, evaluate |
| `07_smoothing_spline.py` | penalty `lam`, GCV, roughness | fit, evaluate |

Each example states **Given**, **Operation requested**, **Library choice**,
**Code**, **What the output means** and **Validation check**, then ends in
`assert` checks. All data are synthetic. There are no assignment answers.

## 5. Everyday workflow

See **[docs/vscode-workflow.md](docs/vscode-workflow.md)** for hover,
signature help, go to definition, `?` and `help()`, the Variables pane and
Data Viewer, the debugger, and the end-to-end question workflow.
**[docs/operation-kinds.md](docs/operation-kinds.md)** explains the
fit / evaluate / optimize / solve distinction that the catalog is organized around.

## 6. Adding a topic or function

Add an `[[entry]]` to a `catalog/*.toml` file (or create a new topic file),
then run `pytest tests/test_catalog.py`. Steps and field reference:
**[docs/adding-a-topic.md](docs/adding-a-topic.md)**. You never need to write
a VS Code extension or edit a central program.

## 7. Tests

```powershell
uv run pytest        # about 30 s; or the Testing sidebar / task "psl: run tests"
```

The tests run every catalog example and every example script against the
installed versions, with deprecation warnings treated as failures. When a
library update renames an API, the tests catch it before it confuses you.

## 8. Updating packages

```powershell
uv lock --upgrade    # re-resolve to newest allowed versions
uv sync
uv run pytest        # catalog examples verify the APIs still work
uv export --format requirements-txt --no-dev --no-emit-project -o requirements.lock.txt
```

## Limitations

* The catalog covers the seeded course topics (72 entries). It grows as you add entries.
* Search is lexical (words and names), not semantic. If a phrasing misses,
  try an R name or a shorter query. Add the phrasing as an `aliases` item so
  it hits next time.
* The environment was verified on Linux with the locked versions. The Windows
  steps follow the official uv and VS Code documentation. Report anything that
  differs on your machine.
