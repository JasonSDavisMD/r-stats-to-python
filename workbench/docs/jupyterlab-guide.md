# Working in JupyterLab with statsbench

JupyterLab in the browser is the recommended way to use statsbench. There are
three places to run it:

| Where | Who it's for | Saved? |
|---|---|---|
| **Your private workspace** (a private GitHub repository + Codespace) | Your own notebooks, coursework, data | Yes: files persist, and you push to your private repository |
| **This public repository's Codespace** | Trying or improving the toolkit itself | Only if you commit to the public repository, so don't put personal work here |
| **Binder** (the "launch binder" badge) | Anyone, instantly, with no account | **No.** Temporary; everything is lost after about 10 idle minutes |

The toolkit stays **public**. Your work stays **private**, in a separate
repository that installs the public toolkit as a dependency. This split is the
standard way to share a tool without sharing your own work.

---

## Part 1: One-time setup of your private workspace (about 10 minutes)

**1. Create the private repository.**
Go to https://github.com/new
* Repository name: `my-stats-work` (any name works)
* Choose **Private**
* Tick **Add a README file** (the repository needs one commit before a Codespace can start)
* Click **Create repository**

**2. Open a temporary Codespace on it.**
On the new repository's page: **Code -> Codespaces -> Create codespace on main**.
VS Code opens in the browser. This first Codespace only copies the template in.

**3. Copy the template in.** In that Codespace's terminal (bottom panel), paste:

```bash
git clone --depth 1 https://github.com/JasonSDavisMD/r-stats-to-python /tmp/statsbench
cp -r /tmp/statsbench/workbench/templates/private-workspace/. .
git add -A
git commit -m "Start from the statsbench private-workspace template"
git push
```

**4. Rebuild so the template's setup takes effect.**
Press **Ctrl+Shift+P** (Cmd+Shift+P on a Mac), type **Rebuild Container**, and
choose **Codespaces: Rebuild Container**. Confirm with **Rebuild**.

The first build takes a few minutes. It installs `uv`, then statsbench (from
this public repository) and JupyterLab, runs the environment check, and starts
JupyterLab. A browser tab opens automatically. If your browser blocks it, use
the **Ports** tab -> row **8888 (JupyterLab)** -> globe icon.

**5. Save the lock file.**
The first build creates `uv.lock`, which records the exact versions you're
using, including which statsbench commit. In JupyterLab, open the **Git**
sidebar and stage, commit and push `uv.lock`
(Part 2, "Save to GitHub"). You only need to do this once, and again after updates.

From now on you only use Part 2.

---

## Part 2: Everyday routine

**Open**
1. Go to https://github.com/codespaces
2. Click your `my-stats-work` codespace. It resumes where you left it, and
   JupyterLab starts by itself.
3. Open JupyterLab: the **Open in Browser** pop-up, or **Ports** tab -> **8888** -> globe icon.
   Tip: bookmark that JupyterLab address. It stays the same for this Codespace.

**Work**
* Notebooks go in `notebooks/`. **File -> New -> Notebook**, choose *Python 3 (ipykernel)*.
* Find the right function: `find("wilcox.test")` in a cell (after
  `from statsbench.finder import find`), or in a JupyterLab terminal:
  `stats find "wilcox.test"`, `stats show mann-whitney`, `stats r lm`.

**Save to GitHub** (end of every session)
1. **Ctrl+S** saves the notebook to the Codespace disk.
2. Click the **Git** icon in the left sidebar.
3. Under **Changed**, hover over each file and click **+** to stage it.
4. Type a short summary and click **Commit**.
5. Click the **push** button (cloud with an up arrow) at the top of the Git panel.

In a terminal, the same thing is `git add -A && git commit -m "notes" && git push`.

**Stop**
At https://github.com/codespaces click **...** next to the codespace -> **Stop codespace**.
Stopping keeps your files and saves your free monthly hours. GitHub deletes a
Codespace after a period of inactivity (30 days by default), so **pushed work
is the only safe copy**.

---

## Part 3: The RStudio-style layout in JupyterLab

```
+--------------------------+--------------------------+
| NOTEBOOK (Source pane)   | CONTEXTUAL HELP (Help)   |
| Shift+Enter runs a cell  | follows your cursor      |
+--------------------------+--------------------------+
| CONSOLE (Console pane)   | TERMINAL / VARIABLES     |
| shares notebook memory   | stats find "..."         |
+--------------------------+--------------------------+
```

1. **Help pane:** press **Ctrl+I** (or Launcher -> *Show Contextual Help*), then
   drag its tab to the right half. Click inside any function name to see its docs.
2. **Console:** right-click in the notebook -> **New Console for Notebook**, then
   drag it below the notebook. It uses the same variables as the notebook.
3. **Terminal:** **File -> New -> Terminal**, then drag it to the bottom right.
4. **Environment pane:** click the bug icon in the notebook toolbar (debugger on),
   then the bug icon in the right sidebar. It has a **Variables** section.
   Quicker: run `%whos` in the console.

JupyterLab remembers the layout.

| RStudio | JupyterLab |
|---|---|
| Ctrl+Enter | **Ctrl+Enter** runs the cell and stays; **Shift+Enter** runs it and moves on |
| Tab completion with arguments | **Tab**; **Shift+Tab** inside `f(` shows the signature |
| `?fun` | `fun?` in a cell, or the Contextual Help pane |
| `ls()` | `%whos` |
| Session -> Restart R | **Kernel -> Restart Kernel and Run All Cells...** (reproducibility check) |

**Worked examples as notebooks.** The `examples/*.py` files (public repository)
are notebooks in plain-text form. Right-click one -> **Open With -> Jupytext
Notebook** to open it as a regular notebook. It's still one file, so it stays
easy to review in Git.

---

## Part 4: Optional add-ons (PyTorch, Bayesian, boosting, survival)

The core install covers NumPy, SciPy, SymPy, pandas, statsmodels,
scikit-learn, Matplotlib and seaborn. Heavier libraries are opt-in so the core
stays fast. In your private workspace, edit `pyproject.toml`:

```toml
dependencies = [
    "statsbench[deep,bayes]",   # or: ml, stats-extra, all
]
```

Then run `uv sync --group lab` in a terminal and restart the kernel
(**Kernel -> Restart Kernel**).

| Add-on | Libraries | Typical R counterpart |
|---|---|---|
| `ml` | XGBoost, LightGBM | xgboost, lightgbm |
| `deep` | PyTorch | torch for R, keras |
| `bayes` | PyMC, ArviZ | rstanarm, brms, bayesplot |
| `stats-extra` | pingouin, lifelines | irr/psych (ICC), survival |

`stats show <id>` tells you when an entry needs an add-on, and whether it's installed.

---

## Part 5: Updating the toolkit

When the public toolkit gets new entries, update your private workspace in a
JupyterLab terminal:

```bash
uv lock --upgrade-package statsbench
uv sync --group lab
```

Restart the kernel, then commit the changed `uv.lock`. Until you run this,
your workspace keeps using the exact version recorded in `uv.lock`, so results
don't change underneath you.

---

## Troubleshooting

* **JupyterLab isn't in the Ports tab.** In a terminal, run
  `bash .devcontainer/start-lab.sh`. The log is in `/tmp/jupyterlab.log`.
* **Asked for a token or password.** You're outside a Codespace, or the port was
  made Public. In Codespaces, make sure port 8888 shows **Private**.
* **`ModuleNotFoundError`** in a notebook: the kernel isn't the workspace's
  `.venv`. Use *Python 3 (ipykernel)* from JupyterLab (it runs inside `.venv`),
  then check with `from statsbench.envcheck import main; main()`.
* **Push fails with "configured for Git LFS but 'git-lfs' was not found":** a
  leftover hook from the temporary Codespace in Part 1. Run
  `rm .git/hooks/pre-push`, then push again. (Newer copies of the template
  install Git LFS, so this no longer happens.)
* **Anything else:** `python -m statsbench.envcheck` prints the interpreter,
  library versions, add-ons and catalog status. Include it in a bug report.
