# %% [markdown]
# # 00 - End-to-end workflow tour (do this once, in VS Code)
#
# The question-answering loop this workbench is built for:
#
# 1. **Search** the task:   terminal -> `stats find "inverse logit"`
#    (or Ctrl+Shift+P -> "Tasks: Run Task" -> "stats: find").
# 2. **Locate** the exact function: `stats show expit` prints import, call, example, docs.
# 3. **Inspect** its signature: hover over `expit` below, or put the cursor
#    inside `expit(` and press Ctrl+Shift+Space. Run `help(expit)` in a cell.
# 4. **Run** a minimal example: Shift+Enter on each `# %%` cell.
# 5. **Inspect values**: open the Interactive Window's "Variables" view and
#    double-click `results` to see it in the Data Viewer.
# 6. **Record** the result in your own notebook: copy `templates/exercise.ipynb`
#    into `coursework/` and fill in Given / Operation / Library / Code / Meaning / Check.
#
# The same search is available inside Python, shown next.

# %%
from statsbench.finder import find

for hit in find("R plogis", limit=3):
    print(f"{hit.entry.id:<32} {hit.entry.import_line.splitlines()[0]:<42} {hit.entry.call}")

# %%
import numpy as np
import pandas as pd
from scipy.special import expit

help(expit)            # in a notebook cell, `expit?` shows the same docs

# %%
log_odds = np.linspace(-4, 4, 9)
results = pd.DataFrame({"log_odds": log_odds, "probability": expit(log_odds)})
results            # last expression in a cell is displayed; open it in the Data Viewer

# %%
assert np.isclose(results.loc[results["log_odds"] == 0, "probability"].item(), 0.5)
print("tour complete")
