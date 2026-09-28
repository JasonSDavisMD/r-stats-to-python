"""Run-all reproducibility: each example script and the notebook template run
top-to-bottom in a fresh process/kernel with no hidden state."""

import os
import subprocess
import sys

import nbformat
import pytest
from nbclient import NotebookClient

from conftest import WORKBENCH

EXAMPLES = sorted((WORKBENCH / "examples").glob("*.py"))


@pytest.mark.parametrize("script", EXAMPLES, ids=lambda p: p.name)
def test_example_runs_clean(script):
    env = {**os.environ, "MPLBACKEND": "Agg"}
    result = subprocess.run(
        [sys.executable, "-W", "error::FutureWarning", str(script)],
        cwd=WORKBENCH, env=env, capture_output=True, text=True, timeout=300,
    )
    assert result.returncode == 0, result.stderr[-2000:]


NOTEBOOKS = [
    WORKBENCH / "start-here.ipynb",
    WORKBENCH / "templates" / "exercise.ipynb",
    WORKBENCH / "templates" / "private-workspace" / "notebooks" / "start-here.ipynb",
]


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: str(p.relative_to(WORKBENCH)))
def test_notebook_runs_in_project_kernel(path):
    notebook = nbformat.read(path, as_version=4)
    NotebookClient(notebook, timeout=180, kernel_name="python3",
                   resources={"metadata": {"path": str(path.parent)}}).execute()
