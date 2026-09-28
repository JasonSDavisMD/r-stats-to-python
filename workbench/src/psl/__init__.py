"""PSL Workbench: a task-to-library finder plus a few course recipes.

Subpackages are deliberately independent so a problem in one cannot break
the other:

- ``psl.finder``  -- load and search the task-to-tool catalog (``catalog/*.toml``)
- ``psl.recipes`` -- thin helpers for workflows no single library provides
- ``psl.envcheck`` -- verify that the terminal/notebook use this project's .venv

Nothing is imported here on purpose; import from the subpackage you need.
"""

__version__ = "0.1.0"
