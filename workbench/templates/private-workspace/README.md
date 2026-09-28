# my-stats-work (private)

My private notebooks, powered by the public
[statsbench](https://github.com/JasonSDavisMD/r-stats-to-python/tree/main/workbench)
toolkit. **Keep this repository private.** Graded work, notes and data live here,
not in the public toolkit repository.

## Open JupyterLab

1. Go to https://github.com/codespaces and click this repository's codespace.
   If there isn't one yet: on this repository's page, click
   **Code -> Codespaces -> Create codespace on main**.
2. JupyterLab starts by itself. Use the pop-up **Open in Browser**, or the
   **Ports** tab -> row **8888 (JupyterLab)** -> globe icon.
3. Work in `notebooks/`. Search the toolkit in any cell
   (`from statsbench.finder import find; find("wilcox.test")`) or in a JupyterLab
   terminal (`stats find "wilcox.test"`).

## Save to GitHub (do this at the end of every session)

In JupyterLab, press **Ctrl+S** to save the notebook, then open the **Git**
sidebar (the Git icon on the left):
1. Under *Changed*, click **+** next to your files (stage).
2. Type a summary and click **Commit**.
3. Click the **push** button (cloud with an up arrow).

Or in a terminal: `git add -A && git commit -m "Notes" && git push`.

A stopped Codespace keeps your files, but GitHub **deletes Codespaces after a
period of inactivity** (30 days by default). Only pushed work is safe.

## Stop when done

https://github.com/codespaces -> "..." next to the codespace -> **Stop codespace**.
Stopping saves your free monthly hours. Next time, click it to resume, and
JupyterLab comes back automatically.

## Update the toolkit

```bash
uv lock --upgrade-package statsbench && uv sync --group lab
```
Then restart the kernel. Commit the updated `uv.lock`.
