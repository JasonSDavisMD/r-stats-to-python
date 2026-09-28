# RStudio users: start here

> **Prefer JupyterLab?** It's the recommended interface. See
> [jupyterlab-guide.md](jupyterlab-guide.md) for the RStudio-style JupyterLab
> layout and a private workspace. This page covers VS Code and Positron.

VS Code opens as a plain editor. This page shows how to arrange it into
RStudio's four panes, how to launch it in the browser with no setup, and
when to use **Positron**, Posit's RStudio-style IDE that also runs Python.

## 1. Fastest start: GitHub Codespaces (browser, nothing to install)

1. On the repository page, click **Code -> Codespaces -> Create codespace on main**.
2. Wait for the setup log to finish (a few minutes the first time). The
   container opens **directly in `workbench/`**, installs `uv`, builds `.venv`
   from `uv.lock`, adds the Python and Jupyter extensions, and runs the
   environment check. The configuration is in `.devcontainer/` at the
   repository root.
3. Continue with section 2.

Stop the Codespace when you finish (Code -> Codespaces -> "..." -> Stop) so it
doesn't use up your monthly free allowance. Your files are kept until you
delete the Codespace.

## 2. Build the four-pane layout

```
+--------------------------+--------------------------+
| EDITOR (Source pane)     | INTERACTIVE WINDOW       |
| a .py file with # %%     | = Console + Plots pane   |
| cells; Shift+Enter runs  | output and plots inline  |
+--------------------------+--------------------------+
| VARIABLES                | TERMINAL                 |
| = Environment pane       | stats find "..." here      |
+--------------------------+--------------------------+
```

1. In the Explorer (left sidebar), open `examples/01_logistic_known_coefficients.py`.
2. Click **Run Cell**, the small grey link above the first `# %%`. If asked
   for a kernel, choose **Python Environments -> .venv**. The **Interactive
   Window** opens on the right. That is your console and plots pane.
3. Keep pressing **Shift+Enter** to run cell by cell. To run only part of a
   cell, select lines and press Shift+Enter; the selection runs in the same
   window.
4. Click **Variables** in the Interactive Window toolbar to open the
   Environment pane in the bottom panel. Double-click a DataFrame or array
   to open it in the Data Viewer.
5. Open a **new terminal** (Ctrl+Shift+`) in the same bottom panel and drag
   its tab to the right half. `.venv` is active there: try `stats find "inverse logit"`.

VS Code remembers this layout for the folder.

## 3. RStudio habits, translated

| RStudio | VS Code |
|---|---|
| Ctrl+Enter runs line/selection | **Shift+Enter** (or add the Ctrl+Enter shortcut below) |
| Ctrl+Shift+Enter runs whole script | **Run All** in the Interactive Window toolbar, or "Run Above/Below" links |
| Session -> Restart R | **Restart** button in the Interactive Window toolbar |
| Environment pane | **Variables** view |
| `View(df)` | Double-click `df` in Variables (Data Viewer / Data Wrangler) |
| `?fun`, Help pane | Hover over the name; `help(fun)`; `stats show <id>` |
| Tab completion with argument list | Ctrl+Space; parameter hints appear after `(` (Ctrl+Shift+Space) |
| R Markdown `.Rmd` | Jupyter notebook `.ipynb` (see `templates/exercise.ipynb`) |
| `rm(list = ls())` then rerun | Restart, then Run All: proves no hidden state |

**Optional: Ctrl+Enter exactly like RStudio.** Keyboard shortcuts are
per-user, so the repository can't set this for you. Press Ctrl+Shift+P, choose
**Preferences: Open Keyboard Shortcuts (JSON)**, and add inside the `[ ]`:

```json
{ "key": "ctrl+enter", "command": "jupyter.execSelectionInteractive",
  "when": "editorTextFocus && editorLangId == python" }
```

## 4. Want the RStudio layout by default? Use Positron (desktop)

**Positron** is a free data-science IDE from Posit, the company that makes
RStudio. It is built on the same open-source core as VS Code, but opens with
RStudio-style **Console, Variables, Plots, Help and Data Explorer** panes, and
supports Python as a first-class language.

1. Install it from https://positron.posit.co (Windows, macOS, Linux).
2. Clone the repository and run `uv sync` in `workbench\` (see the README).
3. **File -> Open Folder -> `workbench`**. Select the `.venv` interpreter
   when Positron offers it.
4. Open any example. **Ctrl+Enter** sends the current line or selection to
   the console. Plots and variables appear in their own panes.

Everything in this workbench is ordinary Python, so it works the same in
Positron, VS Code, JupyterLab and Codespaces: `stats` search, examples, templates, tests.

| If you want... | Use |
|---|---|
| Zero install, works from any computer | Codespaces (section 1) |
| The RStudio look on your Windows machine | Positron |
| The same editor as your classmate, R + Python in one place | VS Code (section 2 layout) |
