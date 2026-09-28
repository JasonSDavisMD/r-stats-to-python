"""statsbench: find and use the right Python library call for a statistics task.

Subpackages are deliberately independent so a problem in one cannot break
the other:

- ``statsbench.finder``   -- load and search the task-to-tool catalog
                             (``statsbench/catalog/*.toml``); CLI ``stats``
- ``statsbench.recipes``  -- thin helpers for workflows no single library provides
- ``statsbench.envcheck`` -- verify the interpreter, libraries and catalog

Nothing is imported here on purpose; import from the subpackage you need,
e.g. ``from statsbench.finder import find``.

Why not name the package ``stats``? ``from scipy import stats`` is the
standard idiom, and a top-level ``stats`` package would be shadowed by, or
shadow, that name in every notebook.
"""

__version__ = "0.2.0"
