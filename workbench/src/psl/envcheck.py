"""Environment check: ``python -m psl.envcheck`` (terminal) or in a notebook cell.

Answers the setup questions that usually go wrong on Windows:

1. Is this interpreter the project's ``.venv``? The terminal and the
   notebook kernel must be the same one.
2. Does every course library import, and at what version?
3. Does the task catalog load cleanly?

Exit code 0 means everything passed. Each check runs in isolation, so one
failure is reported and the rest still run.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

LIBRARIES = [
    ("numpy", "numpy"),
    ("scipy", "scipy"),
    ("sympy", "sympy"),
    ("pandas", "pandas"),
    ("statsmodels", "statsmodels"),
    ("scikit-learn", "sklearn"),
    ("matplotlib", "matplotlib"),
    ("seaborn", "seaborn"),
    ("ipykernel", "ipykernel"),
]


def check_interpreter() -> tuple[bool, str]:
    executable = Path(sys.executable)  # not resolved: show the .venv path VS Code shows
    in_venv = sys.prefix != sys.base_prefix
    project_venv = False
    try:
        from psl.finder.catalog import workbench_root

        project_venv = (workbench_root() / ".venv").resolve() == Path(sys.prefix).resolve()
    except FileNotFoundError:
        pass
    detail = f"{executable} (Python {sys.version.split()[0]})"
    if project_venv:
        return True, detail + " -- project .venv"
    if in_venv:
        return False, detail + " -- a virtual env, but NOT this project's .venv"
    return False, detail + " -- system Python; select the .venv interpreter/kernel"


def check_library(label: str, module_name: str) -> tuple[bool, str]:
    try:
        module = importlib.import_module(module_name)
    except Exception as error:  # report any import failure, keep checking others
        return False, f"{label}: import failed ({error.__class__.__name__}: {error})"
    return True, f"{label} {getattr(module, '__version__', '?')}"


def check_catalog() -> tuple[bool, str]:
    try:
        from psl.finder import load_catalog

        catalog = load_catalog()
    except Exception as error:
        return False, f"catalog: could not load ({error})"
    if catalog.problems:
        return False, f"catalog: {len(catalog.entries)} entries, problems: {catalog.problems}"
    return True, f"catalog: {len(catalog.entries)} entries from {catalog.directory}"


def run_checks() -> list[tuple[bool, str]]:
    results = [check_interpreter()]
    results += [check_library(label, name) for label, name in LIBRARIES]
    results.append(check_catalog())
    return results


def main() -> int:
    results = run_checks()
    for ok, message in results:
        print(f"[{'ok' if ok else 'FAIL'}] {message}")
    failures = sum(1 for ok, _ in results if not ok)
    print("\nAll checks passed." if not failures else f"\n{failures} check(s) failed.")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
