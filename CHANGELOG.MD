# Changelog

## 0.2.0 (statsbench)

### Changed

- Workbench generalized from a course workspace into **statsbench**, a general statistics toolkit: package `statsbench`, command `stats` (was `psl`)
- Catalog moved into the package (`src/statsbench/catalog/`), so it ships with any install, including private workspaces that install from GitHub

### Added

- About 100 new catalog entries: hypothesis tests, agreement and diagnostic accuracy, advanced regression, time series, unsupervised learning, more ML models, numerics, survival, deep learning (PyTorch), Bayesian (PyMC/ArviZ), boosting (XGBoost/LightGBM)
- Optional add-ons `ml`, `deep`, `bayes`, `stats-extra`, `all`; entries declare `requires`/`extra`, and their tests skip when an add-on is absent
- JupyterLab-first workflow: `lab` dependency group (JupyterLab, Jupytext, Git sidebar); Codespaces start JupyterLab automatically on every resume
- Private-workspace template (`workbench/templates/private-workspace/`) and `docs/jupyterlab-guide.md`
- Binder configuration (`binder/`) and launch badge; `start-here.ipynb`
- Public-repository hygiene: CI on Linux/Windows/macOS, Dependabot, issue forms, PR template, SECURITY.md, CITATION.cff, .gitattributes

## Unreleased (0.1.x)

### Added

- `.devcontainer/`: one-click GitHub Codespaces setup that opens `workbench/` with the locked environment and extensions
- `workbench/docs/rstudio-users-start-here.md`: RStudio-style four-pane layout, key translations, and Positron guidance
- `workbench/`: VS Code Python workbench with a searchable task-to-function catalog (`psl` CLI), seeded PSL examples, exercise templates, pinned `uv` environment, and tests
- Initial R-to-Python statistical translation guide
- Boolean syntax and missing-value comparisons
- NumPy `column_stack()` and pandas `concat()` examples
- Regression, ANOVA, diagnostic, and model-selection examples

### Corrected

- Clarified the required `anova_lm` import
