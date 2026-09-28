"""Environment check: ``python -m statsbench.envcheck`` (terminal) or in a notebook.

Answers the setup questions that usually go wrong:

1. Is this interpreter a project virtual environment? The terminal and the
   notebook kernel should be the same one. Compare the printed paths.
2. Does every core library import, and at what version? Which optional
   add-ons (deep learning, Bayesian, ...) are installed?
3. Does the task catalog load cleanly?

Exit code 0 means every REQUIRED check passed. Optional add-ons are only
reported. Each check runs in isolation, so one failure never hides the others.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

CORE = [
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

# extra name -> (label, import name). Mirrors [project.optional-dependencies].
OPTIONAL = {
    "ml": [("xgboost", "xgboost"), ("lightgbm", "lightgbm")],
    "deep": [("torch", "torch")],
    "bayes": [("pymc", "pymc"), ("arviz", "arviz")],
    "stats-extra": [("pingouin", "pingouin"), ("lifelines", "lifelines")],
}


def check_interpreter() -> tuple[bool, str]:
    executable = Path(sys.executable)  # not resolved: show the .venv path editors show
    in_venv = sys.prefix != sys.base_prefix
    detail = f"{executable} (Python {sys.version.split()[0]})"
    if in_venv:
        return True, detail + " -- virtual environment"
    return False, detail + " -- system Python; select the project's .venv interpreter/kernel"


def check_library(label: str, module_name: str) -> tuple[bool, str]:
    try:
        module = importlib.import_module(module_name)
    except Exception as error:  # report any import failure, keep checking others
        return False, f"{label}: import failed ({error.__class__.__name__}: {error})"
    return True, f"{label} {getattr(module, '__version__', '?')}"


def check_catalog() -> tuple[bool, str]:
    try:
        from statsbench.finder import load_catalog

        catalog = load_catalog()
    except Exception as error:
        return False, f"catalog: could not load ({error})"
    if catalog.problems:
        return False, f"catalog: {len(catalog.entries)} entries, problems: {catalog.problems}"
    return True, f"catalog: {len(catalog.entries)} entries"


def optional_status() -> list[str]:
    lines = []
    for extra, modules in OPTIONAL.items():
        found = [check_library(label, name) for label, name in modules]
        if all(ok for ok, _ in found):
            lines.append(f"[ok]   {extra}: " + ", ".join(msg for _, msg in found))
        else:
            lines.append(f"[--]   {extra}: not installed  (uv sync --extra {extra})")
    return lines


def run_checks() -> list[tuple[bool, str]]:
    results = [check_interpreter()]
    results += [check_library(label, name) for label, name in CORE]
    results.append(check_catalog())
    return results


def main() -> int:
    results = run_checks()
    for ok, message in results:
        print(f"[{'ok' if ok else 'FAIL'}] {message}")
    print("\nOptional add-ons:")
    for line in optional_status():
        print(line)
    failures = sum(1 for ok, _ in results if not ok)
    print("\nAll required checks passed." if not failures else f"\n{failures} check(s) failed.")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
