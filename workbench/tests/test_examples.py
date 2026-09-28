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


def test_template_notebook_runs_in_project_kernel():
    notebook = nbformat.read(WORKBENCH / "templates" / "exercise.ipynb", as_version=4)
    NotebookClient(notebook, timeout=120, kernel_name="python3",
                   resources={"metadata": {"path": str(WORKBENCH)}}).execute()
