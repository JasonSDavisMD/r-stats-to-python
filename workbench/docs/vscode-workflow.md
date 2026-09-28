# VS Code workflow: the RStudio features, and where they are

New to VS Code after RStudio? Read [rstudio-users-start-here.md](rstudio-users-start-here.md) first. It sets up the four-pane layout this page assumes.

Keyboard shortcuts are the Windows defaults. Mac users: replace Ctrl with Cmd.

## Two ways to write code

| Format | Use it for | Run code |
|---|---|---|
| `.ipynb` notebook | graded write-ups mixing text, code and output | Shift+Enter runs a cell; **Run All** at the top |
| `.py` with `# %%` cells | reusable scripts (all of `examples/`) | Shift+Enter or **Run Cell** above a `# %%` sends it to the **Interactive Window** |

A `# %%` file is plain Python, so Git diffs stay readable. It still gives
inline plots and output in the Interactive Window. `# %% [markdown]` starts a
text cell.

## Discovering a function without leaving the editor

| RStudio habit | VS Code action |
|---|---|
| Type a name, see its arguments | Type `expit(`. Parameter hints appear. Re-open them with **Ctrl+Shift+Space** |
| Autocomplete | **Ctrl+Space** (Pylance also offers auto-imports) |
| `?function` / F1 help | **Hover** over the name for its docstring. In a notebook: `expit?` (docstring) or `expit??` (source) |
| `help(function)` | `help(expit)` in any cell |
| View a function's source | **F12** go to definition; **Alt+F12** peek inline |
| Which library has it? | `stats find "<task>"` in the terminal, or the **stats: find** task |
| Official docs | the `docs:` link in `stats show <id>` (Ctrl+click opens it) |

Hover and hints come from **Pylance**, which reads the installed packages in
`.venv`. That's why selecting the right interpreter matters.

## Seeing your data (RStudio's Environment pane)

* Notebook toolbar or Interactive Window toolbar: **Variables**. It lists
  every variable with its type, shape and value.
* Double-click a DataFrame or array to open the **Data Viewer**, or **Data
  Wrangler** if it's installed. There you can sort, filter and look at
  column summaries.
* The last expression in a cell is displayed automatically, e.g. `df.head()`.

## Assignments are snapshots, not spreadsheet formulas

`probability = expit(b0 + b1 * x)` computes a value **once**, from the values
at that moment. Changing `b1` afterwards doesn't update `probability` until
you re-run that cell. Two habits prevent confusion:

1. Put computations inside functions, e.g. `def probability_of(x, b0, b1)`. A
   function call always recomputes from its current inputs.
2. Before you trust a result, run **Restart** then **Run All** (notebook
   toolbar, or the Interactive Window's restart button). If it still works,
   nothing depends on hidden state from cells run out of order.

## Debugging

* In a notebook cell: open the cell's run-button menu and choose **Debug Cell**.
* In a `.py` file: click left of a line number to set a breakpoint, then
  **F5** ("Python: current file").
* While paused, the **Variables** and **Watch** panes show values, and the
  **Debug Console** evaluates expressions. Step with F10/F11.

## Terminal and interpreter

* **Ctrl+`** opens the integrated terminal with `.venv` already active.
* The status bar (bottom right) shows the selected interpreter. The notebook
  kernel picker is at the top right. Both should show `.venv`.
* `python -m statsbench.envcheck` prints the interpreter path. In a notebook,
  `from statsbench.envcheck import main; main()` should print the same path.

## End-to-end question workflow

1. **Search.** `stats find "probabilities from given coefficients"`. The top
   hit is `logistic-predict-known-params` (kind **evaluate**: nothing to fit).
2. **Locate the call.** `stats show logistic-predict-known-params` gives the
   import, the call, what goes in and comes out, the tie-rule caveat, and the
   recipe `examples/01_logistic_known_coefficients.py`.
3. **Inspect the signature.** Type `expit(` in a cell and read the hints, or
   run `help(expit)`.
4. **Run the example.** Open the recipe file and Shift+Enter through its cells.
5. **Inspect values.** Open **Variables**, double-click `log_odds` or a DataFrame.
6. **Record.** Copy `templates/exercise.ipynb` into `coursework/`. Fill in
   Given / Operation / Library / Code / Meaning / Validation with the
   question's values. Then Restart and Run All.

`examples/00_workflow_tour.py` walks through these steps in code.
