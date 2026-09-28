#!/usr/bin/env bash
# post-create.sh -- runs once when a Codespace / dev container is created.
# Installs uv, builds workbench/.venv from uv.lock, and runs the environment
# check. It only touches workbench/, and a failure here leaves the container
# usable: rerun this script, or run `uv sync` in workbench/ by hand.
set -euo pipefail

WORKBENCH="$(cd "$(dirname "${BASH_SOURCE[0]}")/../workbench" && pwd)"

if ! command -v uv >/dev/null 2>&1; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi
export PATH="$HOME/.local/bin:$PATH"

cd "$WORKBENCH"
uv sync --frozen                 # exact versions from uv.lock, into ./.venv
uv run python -m psl.envcheck

echo
echo "Workbench ready. Open examples/00_workflow_tour.py and click 'Run Cell'."
echo "Search the toolbox from a NEW terminal (Ctrl+Shift+\`):  psl find \"inverse logit\""
